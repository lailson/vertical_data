#!/usr/bin/env python3
"""Cliente CADURB (Sinter/RFB) — gerado a partir da spec pública de homologação.

Spec: spec/openapi-homologacao.json (capturada em 16/09/2026 de
https://hom-sinter2-cadurb.np.estaleiro.serpro.gov.br/api/v3/api-docs)

Credenciais: o token OAuth (client_credentials) é fornecido pelo time do CADURB
após a adesão gratuita ao convênio — sinter.df.cocad@rfb.gov.br.
Sem credenciais, o cliente funciona em modo --dry-run (monta e imprime a chamada).

Uso:
    export CADURB_CLIENT_ID=... CADURB_CLIENT_SECRET=...
    python3 cadurb_client.py validar ui.json --ibge 2200600
    python3 cadurb_client.py inserir-batch base.ndjson --ibge 2200600
    python3 cadurb_client.py consultar 0001234 --ibge 2200600
"""
import json, os, sys, urllib.request, urllib.parse

HOMOLOG = 'https://hom-sinter2-cadurb.np.estaleiro.serpro.gov.br/api'
# URL de produção: seção 12.5 do Manual Operacional (ENAT, v1.12) — preencher quando credenciar
PROD = os.environ.get('CADURB_PROD_URL', '')

class CadurbClient:
    def __init__(self, base=None, dry=False):
        self.base = base or os.environ.get('CADURB_BASE') or HOMOLOG
        self.client_id = os.environ.get('CADURB_CLIENT_ID', '')
        self.secret = os.environ.get('CADURB_CLIENT_SECRET', '')
        self.dry = dry
        self._token = None

    def token(self):
        if self._token:
            return self._token
        url = self.base + '/v1/keycloak/oidc/token'
        data = urllib.parse.urlencode({
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.secret,
        }).encode()
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=60) as r:
            self._token = json.load(r)['access_token']
        return self._token

    def call(self, method, path, body=None, ndjson=False, params=None):
        url = self.base + path + ('?' + urllib.parse.urlencode(params) if params else '')
        headers = {'Accept': 'application/json'}
        if self.dry:
            print(f'[dry-run] {method} {url}')
            if body is not None:
                print(json.dumps(body, ensure_ascii=False, indent=1)[:2000])
            return {'dry_run': True}
        headers['Authorization'] = 'Bearer ' + self.token()
        data = None
        if body is not None:
            if ndjson:
                data = ('\n'.join(json.dumps(b, ensure_ascii=False) for b in body)).encode()
                headers['Content-Type'] = 'application/x-ndjson'
            else:
                data = json.dumps(body, ensure_ascii=False).encode()
                headers['Content-Type'] = 'application/json'
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)

    # --- endpoints da spec ---
    def validar_ui(self, ibge, ui):
        """POST /v1/validacao/{codigoIbge}/ui — valida sem gravar (a porta do laudo)."""
        return self.call('POST', f'/v1/validacao/{ibge}/ui', ui)

    def inserir_ui(self, ibge, ui):
        return self.call('POST', f'/v1/{ibge}/ui', ui)

    def inserir_batch(self, ibge, uis):
        return self.call('POST', f'/v1/{ibge}/uis', uis, ndjson=True)

    def consultar_por_inscricao(self, ibge, inscricao):
        return self.call('GET', f'/v1/{ibge}/ui/{inscricao}')

    def consultar_cib(self, cib):
        return self.call('GET', f'/v1/ui/{cib}')

    def listar_uis(self, ibge, **params):
        return self.call('GET', f'/v1/{ibge}/uis', params=params)

    def consulta_processamento(self, ibge, id_req):
        return self.call('GET', f'/v1/{ibge}/consulta/{id_req}')

    def consulta_arquivo(self, ibge, id_arquivo):
        return self.call('GET', f'/v1/{ibge}/arquivo/{id_arquivo}/consulta')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    a = sys.argv[1:]
    cmd = a[0]
    ibge = None
    if '--ibge' in a:
        ibge = a[a.index('--ibge') + 1]
    cli = CadurbClient(dry='--dry-run' in a or not (os.environ.get('CADURB_CLIENT_ID') and os.environ.get('CADURB_CLIENT_SECRET')))
    if cmd == 'validar' and len(a) > 1:
        ui = json.load(open(a[1], encoding='utf-8'))
        print(json.dumps(cli.validar_ui(ibge, ui), ensure_ascii=False, indent=2))
    elif cmd == 'inserir-batch' and len(a) > 1:
        uis = [json.loads(l) for l in open(a[1], encoding='utf-8') if l.strip()]
        print(json.dumps(cli.inserir_batch(ibge, uis), ensure_ascii=False, indent=2)[:4000])
    elif cmd == 'consultar' and len(a) > 1:
        v = a[1]
        r = cli.consultar_por_inscricao(ibge, v) if ibge else cli.consultar_cib(v)
        print(json.dumps(r, ensure_ascii=False, indent=2)[:4000])
    elif cmd == 'listar' and ibge:
        print(json.dumps(cli.listar_uis(ibge), ensure_ascii=False, indent=2)[:4000])
    else:
        print(__doc__)
