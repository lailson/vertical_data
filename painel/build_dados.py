#!/usr/bin/env python3
"""ETL do Painel CERURB — estadual (224 municípios) + territorial (25 com bairros).

Fusão de dois pipelines:
  * sessão ZCode — `painel/build_dados.py`: métricas v2 por bairro de Teresina
    (denominador de entorno sem "não declarado", renda mediana V06006, n >= 50
    domicílios). Documentado em `docs/metodologia-iv.md`.
  * esta sessão — `dados/qualificacao-pi.csv`: os 224 municípios do PI com IPTU,
    ITBI, ISS, RCL, tenant Foxinline, sinal RREO e segmento A/fronteira/B.

O que este script acrescenta aos dois:
  1. **Generalização por município** — o recorte deixa de ser o prefixo fixo
     '2211001' e passa a ser toda a UF; sai um arquivo de bairros por município
     (25 no PI), não só Teresina.
  2. **Modo "sem bairro"** — os mesmos seis indicadores calculados a partir dos
     *agregados por município* do Censo 2022, de forma que os 199 municípios sem
     divisão de bairros deixem de ser buracos no mapa.
  3. **Universo do entorno separado do universo do domicílio** — V05000 é
     "domicílio em setor ESCOLHIDO para aplicação do entorno" e não o total de
     domicílios; o corte n >= 50 dos indicadores de entorno passa a usar V05000
     (`n_ok_ent`), enquanto `n_ok` continua sobre V00001. No PI isso separa 8
     bairros que passam num corte e falham no outro (Rudiador: 95 domicílios,
     3 no universo do entorno) e 18 sem qualquer registro de entorno.
  4. **Simplificação de geometria** (Douglas-Peucker puro) para o mapa estadual.

Entradas:  dados/bruto/ (ver dados/baixar.py)  ·  dados/qualificacao-pi.csv
Saídas:    painel/dados/*.json
Uso:       .venv/bin/python painel/build_dados.py [--uf 22]
"""
import csv, io, json, os, sys, tempfile, zipfile
from datetime import date

import shapefile  # pyshp

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
BRUTO = os.path.join(RAIZ, 'dados', 'bruto')
SAIDA = os.path.join(AQUI, 'dados')

UF = '22'
for i, a in enumerate(sys.argv):
    if a == '--uf' and i + 1 < len(sys.argv):
        UF = sys.argv[i + 1]

# Pilotos e alvos nomeados no PLANO (analise/PLANO.md §4 e §13.6).
PILOTOS = {
    '2204550': ('piloto', 'REURB 100% regularizada — cadastro georreferenciado pronto'),   # Guaribas
    '2206753': ('piloto', 'REURB 100% regularizada — cadastro georreferenciado pronto'),   # N. Sra. de Nazaré
    '2205516': ('piloto', 'REURB em tramitação'),                                          # Juazeiro do Piauí
    '2202737': ('piloto', 'REURB em tramitação'),                                          # Coivaras
}
ALVOS_ITBI = {
    '2201903': 'ITBI R$ 61/hab — 2º maior per capita do estado',   # Bom Jesus
    '2203909': 'ITBI 1,8× o IPTU',                                 # Floriano
    '2202901': 'ITBI 1,6× o IPTU',                                 # Corrente
}
VITRINE = {'2211001': 'vitrine e conta A de 2027 — não é piloto (Lei mun. 6.383/2026, IPTU suspenso)'}


# ---------------------------------------------------------------- utilidades
def num(v):
    v = (v or '').strip().strip('"')
    if v in ('', 'X', '-'):
        return None
    if ',' in v:
        v = v.replace('.', '').replace(',', '.')
    try:
        return float(v)
    except ValueError:
        return None


def carregar(zipname, keycol=0):
    """Lê o primeiro CSV do zip do IBGE. Atenção: CSV é latin-1, DBF é UTF-8."""
    with zipfile.ZipFile(os.path.join(BRUTO, 'ibge', zipname)) as z:
        nome = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
        texto = z.read(nome).decode('latin-1')
    rows = list(csv.reader(io.StringIO(texto), delimiter=';'))
    hdr = [h.strip('"') for h in rows[0]]
    return hdr, {r[keycol].strip('"'): r for r in rows[1:] if r}


def g(dic, hdr, cd, var):
    r = dic.get(cd)
    if not r or var not in hdr:
        return None
    i = hdr.index(var)
    return num(r[i]) if i < len(r) else None


def pct_sim_nao(dic, hdr, cd, v_sim, v_nao):
    """% = SIM/(SIM+NÃO) — exclui 'não declarado' (docs/metodologia-iv.md §2.1)."""
    s, n = g(dic, hdr, cd, v_sim), g(dic, hdr, cd, v_nao)
    if s is None or n is None or (s + n) == 0:
        return None
    return round(100 * s / (s + n), 1)


def indicadores(cd, D1, H1, D2, H2, DE, HE, DD, HD, DR, HR, DB=None, HB=None):
    """Bloco de indicadores idêntico para bairro e para município."""
    dom, mor = g(D1, H1, cd, 'V00001'), g(D1, H1, cd, 'V00005')
    b = {'dom': dom, 'mor': mor, 'n_ok': 1 if (dom or 0) >= 50 else 0}
    # V0001 do arquivo básico = "Total de pessoas": a população do Censo.
    # V00005 é outra coisa — moradores em domicílios particulares permanentes
    # ocupados — e fica como número secundário.
    if DB is not None:
        pop = g(DB, HB, cd, 'v0001')
        b['pop'] = int(pop) if pop is not None else None
        area = g(DB, HB, cd, 'AREA_KM2')
        b['area_km2'] = round(area, 3) if area is not None else None
    if dom:
        a, e = g(D2, H2, cd, 'V00111'), g(D2, H2, cd, 'V00309')
        b['agua'] = round(100 * a / dom, 1) if a is not None else None
        b['esgoto'] = round(100 * e / dom, 1) if e is not None else None
        b['mor_por_dom'] = round(mor / dom, 2) if mor else None
    n_ent = g(DE, HE, cd, 'V05000')
    b['n_ent'] = n_ent
    b['n_ok_ent'] = 1 if (n_ent or 0) >= 50 else 0
    b['pav'] = pct_sim_nao(DE, HE, cd, 'V05006', 'V05007')
    b['ilum'] = pct_sim_nao(DE, HE, cd, 'V05012', 'V05013')
    b['calcada'] = pct_sim_nao(DE, HE, cd, 'V05021', 'V05022')
    b['rampa'] = pct_sim_nao(DE, HE, cd, 'V05027', 'V05028')
    b['bueiro'] = pct_sim_nao(DE, HE, cd, 'V05009', 'V05010')
    b['onibus'] = pct_sim_nao(DE, HE, cd, 'V05015', 'V05016')
    sem = g(DE, HE, cd, 'V05030')
    b['arbor_sem'] = round(100 * sem / n_ent, 1) if (n_ent and sem is not None) else None
    mt = g(DD, HD, cd, 'V01006')
    if mt:
        # 'X' (valor suprimido) vira None em num(); somá-lo como zero publicaria
        # "0% de idosos" onde o IBGE apenas não divulgou a faixa.
        faixas_i = [g(DD, HD, cd, v) for v in ('V01040', 'V01041')]
        faixas_c = [g(DD, HD, cd, v) for v in ('V01031', 'V01032', 'V01033')]
        if all(x is not None for x in faixas_i):
            b['idosos_pct'] = round(100 * sum(faixas_i) / mt, 1)
        if all(x is not None for x in faixas_c):
            b['criancas_pct'] = round(100 * sum(faixas_c) / mt, 1)
    media, mediana = g(DR, HR, cd, 'V06004'), g(DR, HR, cd, 'V06006')
    b['renda'] = round(media) if media is not None else None          # média — secundária
    b['renda_med'] = round(mediana) if mediana is not None else None  # mediana — principal
    return b


# ------------------------------------------------- simplificação de geometria
def dp(pts, tol):
    """Douglas-Peucker (distância perpendicular em graus). Puro Python."""
    if len(pts) < 3:
        return pts
    x0, y0 = pts[0]
    x1, y1 = pts[-1]
    dx, dy = x1 - x0, y1 - y0
    den = dx * dx + dy * dy
    imax, dmax = 0, -1.0
    for i in range(1, len(pts) - 1):
        px, py = pts[i]
        if den == 0:
            d = ((px - x0) ** 2 + (py - y0) ** 2) ** .5
        else:
            t = ((px - x0) * dx + (py - y0) * dy) / den
            t = max(0.0, min(1.0, t))
            d = ((px - (x0 + t * dx)) ** 2 + (py - (y0 + t * dy)) ** 2) ** .5
        if d > dmax:
            imax, dmax = i, d
    if dmax <= tol:
        return [pts[0], pts[-1]]
    return dp(pts[:imax + 1], tol)[:-1] + dp(pts[imax:], tol)


def anel(pts, tol, casas):
    p = [(round(x, casas), round(y, casas)) for x, y in pts]
    sim = dp(p, tol) if tol else p
    if len(sim) < 4:                      # anel degenerado: mantém o original
        sim = p
    if sim[0] != sim[-1]:
        sim.append(sim[0])
    return [[x, y] for x, y in sim]


def simplificar(geo, tol, casas=5):
    sys.setrecursionlimit(20000)
    t = geo['type']
    if t == 'Polygon':
        return {'type': 'Polygon', 'coordinates': [anel(r, tol, casas) for r in geo['coordinates']]}
    if t == 'MultiPolygon':
        return {'type': 'MultiPolygon',
                'coordinates': [[anel(r, tol, casas) for r in po] for po in geo['coordinates']]}
    return geo


def ler_shp(zipname, shp_hint=None):
    """Extrai o shapefile num diretório temporário e o remove ao fim."""
    with zipfile.ZipFile(os.path.join(BRUTO, 'ibge', zipname)) as z:
        nomes = [n for n in z.namelist() if n.endswith('.shp')]
        alvo = [n for n in nomes if shp_hint in n][0] if shp_hint else nomes[0]
        with tempfile.TemporaryDirectory() as tmp:
            z.extractall(tmp)
            r = shapefile.Reader(os.path.join(tmp, alvo), encoding='utf-8', encodingErrors='replace')
            campos = [f[0] for f in r.fields[1:]]
            for sr in r.iterShapeRecords():
                geo = getattr(sr.shape, '__geo_interface__', None)
                geo = geo() if callable(geo) else geo
                yield dict(zip(campos, sr.record)), geo
            r.close()


def escrever(caminho, obj):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, ensure_ascii=False, separators=(',', ':'))
    return os.path.getsize(caminho)


# ------------------------------------------------------------------ pipeline
print('· agregados por bairro…')
HBB, DBB = carregar('bairros_basico_BR.zip')
HB1, DB1 = carregar('bairros_domicilio1_BR.zip')
HB2, DB2 = carregar('bairros_domicilio2_BR.zip')
HBE, DBE = carregar('bairros_entorno_domicilios_BR.zip')
HBD, DBD = carregar('bairros_demografia_BR.zip')
HBR, DBR = carregar('bairros_renda_responsavel_BR.zip')

print('· agregados por município…')
HMB, DMB = carregar('municipios_basico_BR.zip')
HM1, DM1 = carregar('municipios_domicilio1_BR.zip')
HM2, DM2 = carregar('municipios_domicilio2_BR.zip')
HME, DME = carregar('municipios_entorno_domicilios_BR.zip')
HMD, DMD = carregar('municipios_demografia_BR.zip')
HMR, DMR = carregar('municipios_renda_responsavel_BR.zip')

print('· qualificação comercial (dados/qualificacao-pi.csv)…')
QUAL = {}
with open(os.path.join(RAIZ, 'dados', 'qualificacao-pi.csv'), encoding='utf-8') as fh:
    for r in csv.DictReader(fh):
        QUAL[r['ibge']] = r

print('· CIB ativo (RFB/Sinter)…')
CIB = {}
cam = os.path.join(BRUTO, 'sinter', 'inscricoes.csv')
if os.path.exists(cam):
    with open(cam, encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh, delimiter=';'):
            CIB[r['ibge']] = int(r['Ativa'])

# ---- bairros, por município
print('· bairros + geometria…')
por_mun, nomes_mun = {}, {}
for rec, geo in ler_shp('PI_bairros_CD2022.zip'):
    cd = str(rec['CD_BAIRRO']).strip()
    cdm = str(rec['CD_MUN']).strip()
    if not cd.startswith(UF):
        continue
    nomes_mun[cdm] = rec['NM_MUN']
    p = indicadores(cd, DB1, HB1, DB2, HB2, DBE, HBE, DBD, HBD, DBR, HBR, DBB, HBB)
    p['name'] = (DB1.get(cd, [None, rec['NM_BAIRRO']])[1] or rec['NM_BAIRRO']).strip('"')
    p['cd'] = cd
    p['cd_mun'] = cdm
    por_mun.setdefault(cdm, []).append({'type': 'Feature', 'properties': p,
                                        'geometry': simplificar(geo, 0.00004)})

# ---- FCU (favelas e comunidades urbanas) por município
print('· FCU…')
fcu_por_mun = {}
for rec, geo in ler_shp('poligonos_FCUs_shp.zip'):
    if str(rec['cd_uf']).strip() != UF:
        continue
    cdm = str(rec['cd_mun']).strip()
    fcu_por_mun.setdefault(cdm, []).append(
        {'type': 'Feature',
         'properties': {'cd': str(rec['cd_fcu']).strip(), 'name': rec['nm_fcu']},
         'geometry': simplificar(geo, 0.00003)})

# ---- municípios: indicadores + qualificação + geometria simplificada
print('· municípios + geometria…')
feats_mun = []
for rec, geo in ler_shp('PI_Municipios_2023.zip'):
    cdm = str(rec['CD_MUN']).strip()
    if not cdm.startswith(UF):
        continue
    p = indicadores(cdm, DM1, HM1, DM2, HM2, DME, HME, DMD, HMD, DMR, HMR, DMB, HMB)
    q = QUAL.get(cdm, {})
    p.update({
        'cd': cdm,
        'name': rec['NM_MUN'],
        'rgint': rec.get('NM_RGINT'),
        'area_km2': round(float(rec['AREA_KM2']), 1) if rec.get('AREA_KM2') else None,
        # a estimativa anual do CSV fica como coluna de rastreio, não como o número
        'pop_csv': int(num(q['pop'])) if num(q.get('pop')) is not None else None,
        'bairros': len(por_mun.get(cdm, [])),
        'fcus': len(fcu_por_mun.get(cdm, [])),
        'tenant_fox': 1 if q.get('tenant_fox') == 'SIM' else 0,
        'segmento': q.get('segmento') or None,
        'iptu': num(q.get('iptu')),
        'itbi': num(q.get('itbi')),
        'iss': num(q.get('iss')),
        'rcl': num(q.get('rcl')),
        'itbi_iptu': num(q.get('itbi_sobre_iptu')),
        'itbi_hab_csv': num(q.get('itbi_per_capita')),
        'sinal_rreo': q.get('sinal_rreo') or None,
        # município ausente do CSV de qualificação não tem entrega ZERO: não tem dado.
        'rreo': ([int(q.get('rreo2023') or 0), int(q.get('rreo2024') or 0), int(q.get('rreo2025') or 0)]
                 if q else None),
        'cib_ativo': CIB.get(cdm, 0),
    })
    itbi, pop = p.get('itbi'), p.get('pop')
    p['itbi_hab'] = round(itbi / pop, 2) if (itbi is not None and pop) else None
    # rótulo comercial
    if cdm in PILOTOS:
        p['papel'], p['papel_nota'] = PILOTOS[cdm]
    elif cdm in VITRINE:
        p['papel'], p['papel_nota'] = 'vitrine', VITRINE[cdm]
    elif cdm in ALVOS_ITBI:
        p['papel'], p['papel_nota'] = 'alvo_itbi', ALVOS_ITBI[cdm]
    else:
        p['papel'], p['papel_nota'] = None, None
    # hipótese "ITBI alto com IPTU nulo" (analise/23) — marcada como hipótese, não alvo
    if (p['itbi'] or 0) > 200_000 and (p['iptu'] or 0) < 50_000:
        p['hipotese_itbi_rural'] = 1
    feats_mun.append({'type': 'Feature', 'properties': p, 'geometry': simplificar(geo, 0.0025, 4)})

feats_mun.sort(key=lambda f: f['properties']['name'])

# ------------------------------------------------------------------- escrita
os.makedirs(SAIDA, exist_ok=True)
tam = escrever(os.path.join(SAIDA, 'municipios.json'),
               {'type': 'FeatureCollection', 'features': feats_mun})
print(f'  municipios.json · {len(feats_mun)} municípios · {tam//1024} KB')

idx = []
for cdm, feats in sorted(por_mun.items(), key=lambda kv: -len(kv[1])):
    feats.sort(key=lambda f: f['properties']['name'])
    pac = {'type': 'FeatureCollection',
           'features': feats,
           'fcus': {'type': 'FeatureCollection', 'features': fcu_por_mun.get(cdm, [])}}
    t = escrever(os.path.join(SAIDA, 'bairros', f'{cdm}.json'), pac)
    idx.append({'cd': cdm, 'name': nomes_mun[cdm], 'bairros': len(feats),
                'fcus': len(fcu_por_mun.get(cdm, [])), 'kb': t // 1024})
    print(f'  bairros/{cdm}.json · {nomes_mun[cdm]}: {len(feats)} bairros, '
          f'{len(fcu_por_mun.get(cdm, []))} FCU · {t//1024} KB')

meta = {
    'gerado_em': date.today().isoformat(),
    'uf': UF,
    'municipios': len(feats_mun),
    'com_bairros': len(idx),
    'sem_bairros': len(feats_mun) - len(idx),
    'bairros_total': sum(i['bairros'] for i in idx),
    'fcu_total': sum(i['fcus'] for i in idx),
    'indice': idx,
    'fontes': [
        {'k': 'Censo 2022 — agregados por bairro e por município', 'v': 'IBGE, ftp.ibge.gov.br', 'd': '17/09/2026'},
        {'k': 'Malha de bairros CD2022 e malha municipal 2023', 'v': 'IBGE, geoftp.ibge.gov.br', 'd': '17/09/2026'},
        {'k': 'Favelas e comunidades urbanas (FCU)', 'v': 'IBGE, Censo 2022', 'd': '17/09/2026'},
        {'k': 'IPTU · ITBI · ISS · RCL 2025', 'v': 'Portal SICONFI (classificação RREO) — docs/metodo-fiscal-itbi-iptu.md', 'd': '16/09/2026'},
        {'k': 'Inscrições CIB ativas', 'v': 'RFB/Sinter, inscricoes_ativas_setembro_2026', 'd': '17/09/2026'},
        {'k': 'Endereços com coordenada (CNEFE)', 'v': 'IBGE, Cadastro Nacional de Endereços para Fins Estatísticos — Censo 2022', 'd': '17/09/2026'},
        {'k': 'Tenants Foxinline', 'v': 'Certificate Transparency (crt.sh) — evidência forte para presença, fraca para ausência', 'd': '16/09/2026'},
    ],
}
escrever(os.path.join(SAIDA, 'meta.json'), meta)
print(f"\nok · {meta['municipios']} municípios ({meta['com_bairros']} com bairros, "
      f"{meta['sem_bairros']} em modo sem-bairro) · {meta['bairros_total']} bairros · "
      f"{meta['fcu_total']} FCU")
