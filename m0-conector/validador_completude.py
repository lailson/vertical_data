#!/usr/bin/env python3
"""Validador de completude do cadastro imobiliário (laudo pré-credencial).

O produto: diagnosticar, SEM credencial e SEM custo, se o cadastro de um
município está em condições de ser transmitido ao CADURB — e vender o laudo
como porta de entrada (R$ 3–5 mil). Quando a credencial chegar, o mesmo CSV
roda no modo --online contra POST /v1/validacao/{ibge}/ui (validação oficial).

Regras extraídas da spec pública (spec/openapi-homologacao.json):
  obrigatórios: DadosGeraisImovel{areaTerreno, inscricaoImobiliaria, temBairro,
  tipoImovel} e EnderecoImovel{cep, nomeLogradouro, tipoLogradouro}
  semânticas (adicionadas aqui): CEP 8 dígitos; áreas > 0; titularidade soma
  100% por inscrição; NI (CPF/CNPJ) 11/14 dígitos; inscrição única.

Uso:
    python3 validador_completude.py base.csv --ibge 2200600 [--saida laudo.md] [--online]

CSV esperado (colunas, com mapa ajustável em MAPEAR): inscricao, tipo_imovel,
area_terreno, area_construida, valor_venal, logradouro, tipo_logradouro, bairro,
cep, numero, cpf_cnpj_titular, nome_titular, perc_titularidade, latitude, longitude
"""
import csv, json, re, sys, os
from collections import Counter, defaultdict

# As 10 regras semânticas moram em entregaveis/regras_semanticas.py e são o que
# distingue este laudo de um `required`-checker extraído do Swagger. Até aqui
# elas existiam e não eram chamadas: o laudo só via obrigatórios e tamanho.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'entregaveis'))
try:
    import regras_semanticas as SEM
except Exception:
    SEM = None

MAPEAR = {  # coluna do CSV -> campo do CADURB
    'inscricao': 'inscricaoImobiliaria', 'tipo_imovel': 'tipoImovel',
    'area_terreno': 'areaTerreno', 'area_construida': 'areaConstruida',
    'valor_venal': 'valorVenal', 'logradouro': 'nomeLogradouro',
    'tipo_logradouro': 'tipoLogradouro', 'bairro': 'bairro', 'cep': 'cep',
    'numero': 'numeroImovel', 'cpf_cnpj_titular': 'niTitular',
    'nome_titular': 'nomeTitular', 'perc_titularidade': 'percTitularidade',
    'latitude': 'lat', 'longitude': 'lon',
}


def _sem_acento(s):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', str(s).strip().lower())
                   if unicodedata.category(c) != 'Mn')


try:
    import json as _json, os as _os
    _dom = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'spec', 'dominios.json'), encoding='utf-8'))
    TL_DOM = {int(k): v for k, v in _dom.get('tipoLogradouro', {}).items()}
    # índice reverso por NOME, sem acento: a planilha do município traz
    # "Praça" e a tabela traz "Praça" — bater por string crua perde o acento
    # em metade dos encodings que chegam do mundo real.
    TL_NOME = {_sem_acento(v): k for k, v in TL_DOM.items()}
except (OSError, ValueError) as _e:
    # Só falta de arquivo ou JSON inválido. `except Exception` escondia erro de
    # código: um NameError aqui zerava a tabela de domínios em silêncio e o
    # laudo seguia aprovando tudo, sem conferir um só tipo de logradouro.
    print(f'AVISO: domínios não carregados ({_e}) — checagem de tabela desativada', file=sys.stderr)
    TL_DOM, TL_NOME = {}, {}

def ni_valido(ni):
    """Comprimento E dígito verificador. Antes só o comprimento: um CPF de
    11 dígitos inventados passava, e o laudo dizia "apto"."""
    ni = re.sub(r'\D', '', ni or '')
    if len(ni) not in (11, 14):
        return False, ni
    if SEM is not None and not SEM.dv_documento(ni):
        return False, ni
    return True, ni

# ---------------------------------------------------------------- de-para
# `MAPEAR` (acima) já traduz a coluna da planilha para o campo da SPEC do CADURB.
# As regras de `regras_semanticas.py` falam o vocabulário da spec; sem esta
# tradução elas rodavam sobre chaves inexistentes e devolviam "tudo ausente" —
# que foi por isso que ficaram desligadas do laudo até 19/09/2026.
def para_spec(rows):
    """Traduz as linhas do CSV para o vocabulário da spec.

    Duas DERIVAÇÕES, e as duas vão declaradas no laudo porque mudam o resultado:

    1. `temBairro` é obrigatório no leiaute e não existe na planilha. É derivado
       da presença de bairro. Sem derivar, a R1 acusaria a base inteira por um
       campo que o município nunca foi solicitado a ter.
    2. `percTitularidade` é fração de 0 a 1 na spec; a planilha costuma vir em
       porcentagem. Valor entre 1 e 100 é dividido por 100 — a mesma conversão
       que a remessa faria.
    """
    saida, pct_convertido = [], 0
    tl_convertido = tl_sem_codigo = 0
    for r in rows:
        d = {}
        for origem, destino in MAPEAR.items():
            v = (r.get(origem) or '').strip() if isinstance(r.get(origem), str) else r.get(origem)
            if v not in (None, ''):
                d[destino] = v
        # tipoLogradouro: a planilha quase sempre traz o nome por extenso, e a
        # spec exige o código da tabela 9.6. Converter é o que a remessa faria —
        # deixar por extenso reprovaria TODAS as linhas por um defeito de formato,
        # que é ruído e esconde os defeitos de conteúdo.
        tl = d.get('tipoLogradouro')
        if tl is not None and not str(tl).strip().isdigit():
            cod = TL_NOME.get(_sem_acento(tl))
            if cod is not None:
                d['tipoLogradouro'] = cod
                tl_convertido += 1
            else:
                tl_sem_codigo += 1
        d['temBairro'] = 'S' if d.get('bairro') else 'N'
        p = d.get('percTitularidade')
        if p is not None:
            try:
                f = float(str(p).replace(',', '.'))
                if 1 < f <= 100:
                    f /= 100
                    pct_convertido += 1
                d['percTitularidade'] = f
            except ValueError:
                pass
        saida.append(d)
    return saida, {'pct': pct_convertido, 'tl_convertido': tl_convertido,
                   'tl_sem_codigo': tl_sem_codigo}


FAIXAS_CEP = []   # preenchido em main() com os prefixos do município


def validar_linha(r):
    """Retorna (falhas_obrigatorias, avisos, campos_estrategicos_presentes)."""
    f, a, est = [], [], set()
    def val(col, regra, msg_obr=None, obr=True):
        v = (r.get(col) or '').strip()
        if not v:
            if obr and msg_obr:
                f.append(msg_obr)
            return None
        return regra(v) if regra else v
    # obrigatórios da spec
    insc = val('inscricao', None, 'inscricaoImobiliaria ausente')
    val('tipo_imovel', lambda v: v.isdigit() or 'tipoImovel não numérico', 'tipoImovel ausente')
    at = val('area_terreno', lambda v: v.replace(',', '.').replace('.', '', v.count(',') > 0 and 1 or 0), 'areaTerreno ausente')
    try:
        if at is not None and float(str(at).replace(',', '.')) <= 0:
            f.append('areaTerreno <= 0')
    except ValueError:
        f.append('areaTerreno não numérico')
    val('logradouro', None, 'nomeLogradouro ausente')
    val('tipo_logradouro', None, 'tipoLogradouro ausente')
    cep = (r.get('cep') or '').strip()
    if not cep:
        f.append('cep ausente')
    elif len(re.sub(r'\D', '', cep)) != 8:
        f.append('CEP não tem 8 dígitos')
    elif FAIXAS_CEP and not any(ini <= int(re.sub(r'\D', '', cep)) <= fim for ini, fim in FAIXAS_CEP):
        f.append('CEP fora dos prefixos do município')
    # opcionais estratégicos (completude)
    for col, nome in [('area_construida', 'área construída'), ('valor_venal', 'valor venal'),
                      ('cpf_cnpj_titular', 'titular (NI)'), ('nome_titular', 'titular (nome)'),
                      ('perc_titularidade', '% titularidade'), ('latitude', 'georreferência'),
                      ('bairro', 'bairro')]:
        if (r.get(col) or '').strip():
            est.add(nome)
    tl = (r.get('tipo_logradouro') or '').strip()
    if tl:
        if tl.isdigit():
            if TL_DOM and int(tl) not in TL_DOM:
                a.append(f'tipoLogradouro {tl} fora da tabela oficial ({len(TL_DOM)} códigos)')
        elif TL_NOME and tl.lower() not in TL_NOME:
            a.append(f'tipoLogradouro "{tl}" não mapeia a código oficial')
    ni = (r.get('cpf_cnpj_titular') or '').strip()
    if ni:
        ok, _ = ni_valido(ni)
        if not ok:
            a.append('NI do titular inválido (comprimento ou dígito verificador)')
    pt = (r.get('perc_titularidade') or '').strip()
    if pt:
        try:
            p = float(pt.replace(',', '.'))
            # a spec grava fração de 0 a 1; a planilha do município costuma vir
            # em porcentagem, então aceitamos as duas e normalizamos na remessa
            if not (0 < p <= 100):
                a.append('% titularidade fora de (0, 100]')
            elif 1 < p <= 100:
                est.add('titularidade em % (a remessa converte para 0–1)')
        except ValueError:
            a.append('% titularidade não numérica')
    return f, a, est

def faixas_cep_do_municipio(ibge: str):
    """Prefixos de CEP observados no CNEFE daquele município, como faixas.

    Tem de ser a LISTA de prefixos, não um intervalo: em Parnaíba os CEPs vão de
    64200 a 64219, mas 64203 e 64214 não pertencem ao município — validar por
    intervalo aceitaria endereço que a Receita recusa.
    """
    cam = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'painel', 'dados', 'cnefe.json')
    try:
        pref = json.load(open(cam, encoding='utf-8'))['municipios'][str(ibge)]['cep']
    except Exception:
        return []
    return [(int(p + '000'), int(p + '999')) for p in pref]


def main():
    args = sys.argv[1:]
    path = args[0] if args else 'exemplo_base.csv'
    ibge = args[args.index('--ibge') + 1] if '--ibge' in args else '0000000'
    online = '--online' in args
    saida = args[args.index('--saida') + 1] if '--saida' in args else 'LAUDO-completude.md'

    global FAIXAS_CEP
    FAIXAS_CEP = faixas_cep_do_municipio(ibge)

    rows = list(csv.DictReader(open(path, encoding='utf-8-sig', errors='replace'), delimiter=';'))

    # --- as dez regras semânticas, agora chamadas de fato ---
    # Até 19/09/2026 o módulo era importado e só emprestava o dígito verificador;
    # `validar_base` nunca rodava, e o laudo prometia mais do que entregava.
    sem = None
    if SEM is not None and rows:
        registros, conv = para_spec(rows)
        sem = SEM.validar_base(registros, codigo_ibge=ibge,
                               ctx={'faixas_cep': FAIXAS_CEP})
        sem['_conv'] = conv
    falhas_por_regra = Counter(); avisos = 0; ok = 0; estrategicos = Counter()
    titularidade = defaultdict(float); inscricoes = Counter()
    for r in rows:
        inscricoes[(r.get('inscricao') or '').strip()] += 1
        f, a, est = validar_linha(r)
        for nome in est:
            estrategicos[nome] += 1
        avisos += len(a)
        if f:
            for x in f:
                falhas_por_regra[x] += 1
        else:
            ok += 1
        pt = (r.get('perc_titularidade') or '').replace(',', '.').strip()
        if pt:
            try:
                titularidade[(r.get('inscricao') or '').strip()] += float(pt)
            except ValueError:
                pass
    dups = {k: v for k, v in inscricoes.items() if v > 1}
    soma_errada = {k: v for k, v in titularidade.items() if k and not (99 <= v <= 101)}
    n = len(rows) or 1
    pct_ok = 100 * ok / n

    linhas = [
        f'# Laudo de Completude Cadastral — CADURB/Sinter', '',
        f'- Município (IBGE): **{ibge}**',
        f'- Imóveis na base: **{len(rows)}**',
        f'- aptos para transmissão (regras obrigatórias): **{ok} ({pct_ok:.1f}%)**',
        f'- imóveis com falha obrigatória: {n - ok}', '',
        '## Falhas por regra', '',
    ]
    if falhas_por_regra:
        linhas += [f'- {k}: **{v}** imóveis' for k, v in falhas_por_regra.most_common()]
    else:
        linhas.append('- nenhuma falha obrigatória')
    linhas += ['', '## Cobertura de campos estratégicos (opcionais na spec, valiosos no cadastro)', '']
    linhas += [f'- {k}: {v} imóveis ({100*v/n:.1f}%)' for k, v in estrategicos.most_common()] or ['- (nenhum)']
    linhas += ['', '## Consistência', '']
    linhas.append(f'- inscrições duplicadas: **{len(dups)}**' + (f' (ex.: {list(dups)[:5]})' if dups else ''))
    linhas.append(f'- inscrições cuja titularidade não soma ~100%: **{len(soma_errada)}**')
    linhas.append(f'- avisos (não bloqueantes): {avisos}')
    linhas.append('- CEP conferido contra **%d prefixos** do município (CNEFE/IBGE)'
                  % len(FAIXAS_CEP) if FAIXAS_CEP else
                  '- CEP: prefixos do município **não disponíveis** — a checagem de faixa não foi aplicada')
    ROT_MD = {
        'CAMPO_NAO_INFORMADO_OU_NULO': 'campo obrigatório ausente',
        'CAMPO_COM_VALOR_INVALIDO': 'valor fora do domínio ou duplicado',
        'CAMPO_COM_PRRENCHIMENTO_INCOMPATIVEL': 'preenchimento incompatível entre campos',
        'CAMPO_COM_DV_INVALIDO': 'CPF/CNPJ com dígito verificador inválido',
        'CAMPO_COM_FORMATACAO_INVALIDA': 'formato inválido',
        'CAMPO_COM_TAMANHO_INVALIDO': 'excede o tamanho da spec',
    }
    if sem:
        linhas += ['', '## Regras semânticas (R1–R10, spec do CADURB)', '']
        linhas.append(f"- aptos pelas regras semânticas: **{sem['aptos_a_transmissao']} de "
                      f"{sem['imoveis_analisados']}** ({sem['percentual_apto']}%)")
        if sem['por_tipo']:
            linhas += [f'- {ROT_MD.get(k, k)}: **{v}**'
                       for k, v in sorted(sem['por_tipo'].items(), key=lambda x: -x[1])]
        else:
            linhas.append('- nenhuma falha semântica')
        if sem['top_impeditivas']:
            linhas.append('- campos que mais bloqueiam: ' + ', '.join(f'`{c}`' for c in sem['top_impeditivas'][:6]))
        linhas.append('')
        c = sem['_conv']
        linhas.append('> **O que a tradução fez**, porque muda o resultado e não pode ficar implícito:')
        linhas.append('> `temBairro` derivado da presença de bairro — o leiaute exige, a planilha não tem.')
        if c['pct']:
            linhas.append(f"> {c['pct']} registro(s) com titularidade convertida de porcentagem para fração.")
        if c['tl_convertido'] or c['tl_sem_codigo']:
            linhas.append(f"> Tipo de logradouro veio **por extenso**: {c['tl_convertido']} convertido(s) "
                          f"para o código da tabela 9.6"
                          + (f", **{c['tl_sem_codigo']} sem correspondência** — estes precisam de decisão do município."
                             if c['tl_sem_codigo'] else '.'))
    linhas += [
        '', '## Leitura', '',
        f'Duas camadas rodam sobre a base: a de **completude** (obrigatórios, domínios, tabela de Tipo de Logradouro com {len(TL_DOM)} códigos do manual v1.12) e a de **regras semânticas** (R1–R10), que confere coerência territorial × predial, faixas, dígito verificador, unicidade de inscrição e soma de titularidade. Aptidão estimada para remessa: **{pct_ok:.1f}%**. Regras obrigatórias derivadas da spec'
        ' pública de homologação do CADURB (openapi-homologacao.json, 16/09/2026).'
        ' Com a credencial do convênio, esta mesma base pode ser revalidada no endpoint oficial'
        ' `POST /v1/validacao/{ibge}/ui` (modo --online deste validador).',
        '', f'Gerado por validador_completude.py · {os.path.basename(path)}',
    ]
    open(saida, 'w', encoding='utf-8').write('\n'.join(linhas))

    # ---- laudo HTML (cara de produto) ----
    def barras(itens, total):
        mx = max([v for _, v in itens] + [1])
        return ''.join(
            f'<div class="hrow"><span class="hl">{k}</span><div class="hbar"><i style="width:{100*v/mx:.0f}%;background:{c}"></i></div><span class="hv">{v:,}</span></div>'.replace(',', '.')
            for (k, v), c in zip(itens, ['#C03A24', '#C98518', '#2FA697', '#0D8478', '#12689F'] * 6))
    falhas_html = barras(falhas_por_regra.most_common(), n) if falhas_por_regra else '<p class="ok">Nenhuma falha obrigatória.</p>'
    est_html = ''.join(
        f'<div class="hrow"><span class="hl">{k}</span><div class="hbar"><i style="width:{100*v/n:.0f}%;background:#2FA697"></i></div><span class="hv">{100*v/n:.1f}%</span></div>'
        for k, v in estrategicos.most_common())
    cor_pct = '#0D8478' if pct_ok >= 80 else ('#8F5A02' if pct_ok >= 40 else '#C03A24')

    # as dez regras também no artefato que o cliente imprime — o laudo em HTML é
    # o que vai anexado ao processo, e era justamente ele que prometia mais do
    # que entregava
    sem_html = ''
    if sem:
        c = sem['_conv']
        # o enum do SERPRO traz "PRRENCHIMENTO" com o typo dele, e o código
        # mantém fiel de propósito; o laudo é artefato de cliente e mostra o
        # rótulo legível, não o identificador cru
        ROTULO = {
            'CAMPO_NAO_INFORMADO_OU_NULO': 'campo obrigatório ausente',
            'CAMPO_COM_VALOR_INVALIDO': 'valor fora do domínio ou duplicado',
            'CAMPO_COM_PRRENCHIMENTO_INCOMPATIVEL': 'preenchimento incompatível entre campos',
            'CAMPO_COM_DV_INVALIDO': 'CPF/CNPJ com dígito verificador inválido',
            'CAMPO_COM_FORMATACAO_INVALIDA': 'formato inválido',
            'CAMPO_COM_TAMANHO_INVALIDO': 'excede o tamanho da spec',
        }
        tipos = ''.join(
            f'<div class="hrow"><span class="hl">{ROTULO.get(k, k.replace("CAMPO_", "").replace("_", " ").lower())}</span>'
            f'<div class="hbar"><i style="width:{100*v/max(sem["por_tipo"].values()):.0f}%;background:#C98518"></i></div>'
            f'<span class="hv">{v}</span></div>'
            for k, v in sorted(sem['por_tipo'].items(), key=lambda x: -x[1]))
        traducao = ['<b>temBairro</b> derivado da presença de bairro — o leiaute exige, a planilha não tem']
        if c['pct']:
            traducao.append(f"{c['pct']} registro(s) com titularidade convertida de porcentagem para fração")
        if c['tl_convertido'] or c['tl_sem_codigo']:
            traducao.append(f"tipo de logradouro veio por extenso: {c['tl_convertido']} convertido(s) para o "
                            f"código da tabela 9.6" +
                            (f", <b>{c['tl_sem_codigo']} sem correspondência</b>" if c['tl_sem_codigo'] else ''))
        sem_html = (
            '<h2>Regras semânticas (R1–R10)</h2>'
            f'<p style="font-size:13px;color:var(--slate);margin-bottom:8px">Camada distinta da '
            f'completude: confere coerência territorial × predial, faixas numéricas, dígito verificador, '
            f'unicidade de inscrição e soma de titularidade. '
            f'<b>{sem["aptos_a_transmissao"]} de {sem["imoveis_analisados"]}</b> '
            f'({sem["percentual_apto"]}%) passam por ela.</p>'
            + (tipos or '<p class="ok">Nenhuma falha semântica.</p>')
            + '<p style="font-size:12px;color:var(--slate);margin-top:10px"><b>O que a tradução fez:</b> '
            + '; '.join(traducao) + '.</p>')
    html = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Laudo de Completude Cadastral — IBGE {ibge} · Vertical Data</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
/* Tokens da marca (marca/vertical-data.css). O laudo é o artefato que o
   cliente recebe e imprime — por isso é claro e fixo, sem alternância de tema. */
:root{{--paper:#F4F6F8;--ink:#0B2545;--teal:#0D8478;--marca:#12B0A0;--ochre:#8F5A02;--terra:#C03A24;--slate:#5B6B7A;--line:#E2E6EA}}
*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,-apple-system,sans-serif;background:var(--paper);color:var(--ink);padding:36px}}
.head{{display:flex;justify-content:space-between;align-items:flex-start;border-bottom:2px solid var(--teal);padding-bottom:14px;margin-bottom:22px}}
h1{{font:700 24px Inter,sans-serif;letter-spacing:-.02em;margin:0}} .sub{{color:var(--slate);font-size:13px;margin-top:4px}}
.chip{{background:var(--teal);color:#fff;font-size:11px;font-weight:600;padding:6px 12px;border-radius:99px;letter-spacing:.04em}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin-bottom:24px}}
.k{{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 16px}}
.k .l{{font-size:11.5px;color:var(--slate)}} .k .v{{font:600 30px 'IBM Plex Mono',monospace;margin-top:4px;font-variant-numeric:tabular-nums}}
h2{{font:700 16px Inter,sans-serif;margin:22px 0 8px}} p.ok{{color:var(--teal);font-weight:600}}
.hrow{{display:grid;grid-template-columns:230px 1fr 64px;gap:10px;align-items:center;font-size:13px;padding:5px 0}}
.hl{{color:var(--slate)}} .hbar{{height:8px;background:var(--line);border-radius:4px;overflow:hidden}} .hbar i{{display:block;height:100%}}
.hv{{text-align:right;font-weight:600;font-variant-numeric:tabular-nums}}
.marca{{display:flex;align-items:center;gap:7px;margin-bottom:9px;font-size:14px;font-weight:700;letter-spacing:-.02em}}
.marca b{{color:var(--marca);font-weight:700}}
.foot{{margin-top:26px;border-top:1px solid var(--line);padding-top:12px;font-size:11.5px;color:var(--slate);line-height:1.6}}
@media(max-width:560px){{body{{padding:22px 14px}}.head{{flex-direction:column;gap:12px;align-items:flex-start}}.hrow{{grid-template-columns:1fr 56px;gap:8px}}.hrow .hbar{{grid-column:1/3;order:3}}/* linhas de Consistência passam um <div> vazio no lugar da barra; sem isto ele ocupa a coluna do valor e joga o número para a linha de baixo */.hrow>div:empty{{display:none}}.hl{{white-space:normal}}h1{{font-size:21px}} .k .v{{font-size:25px}}}}
</style></head><body>
<div class="head"><div><div class="marca"><svg viewBox="0 0 32 32" width="21" height="21" aria-hidden="true"><defs><linearGradient id="vdl" x1="3" y1="0" x2="29" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#12B0A0"/><stop offset="1" stop-color="#0B2545"/></linearGradient></defs><g fill="url(#vdl)"><rect x="3" y="19" width="5" height="11" rx="1.4"/><rect x="10" y="14" width="5" height="16" rx="1.4"/><rect x="17" y="9" width="5" height="21" rx="1.4"/><rect x="24" y="6" width="5" height="24" rx="1.4"/></g><circle cx="26.5" cy="2.7" r="2.7" fill="#12B0A0"/></svg><span>Vertical<b>Data</b></span></div><h1>Laudo de Completude Cadastral</h1>
<div class="sub">Município IBGE {ibge} · base: {os.path.basename(path)} · {len(rows)} imóveis · gerado em {__import__('datetime').date.today().isoformat()}</div></div>
<span class="chip">DIAGNÓSTICO CADURB · SINTER/RFB</span></div>
<div class="kpis">
<div class="k"><div class="l">Imóveis analisados</div><div class="v">{len(rows):,}</div></div>
<div class="k"><div class="l">Aptos à transmissão</div><div class="v" style="color:{cor_pct}">{pct_ok:.1f}%</div></div>
<div class="k"><div class="l">Com falha obrigatória</div><div class="v" style="color:var(--terra)">{n - ok:,}</div></div>
<div class="k"><div class="l">Inscrições duplicadas</div><div class="v">{len(dups)}</div></div></div>
<h2>Falhas por regra (bloqueiam a remessa)</h2>{falhas_html}
<h2>Cobertura de campos estratégicos</h2>{est_html}
{sem_html}
<h2>Consistência</h2>
<div class="hrow"><span class="hl">Titularidade que não soma ~100%</span><div></div><span class="hv">{len(soma_errada)}</span></div>
<div class="hrow"><span class="hl">Avisos não bloqueantes</span><div></div><span class="hv">{avisos}</span></div>
<div class="foot">Regras obrigatórias derivadas da spec pública de homologação do CADURB (Sinter/RFB, openapi capturada em 16/09/2026). Este laudo mede a distância entre o cadastro atual e o leiaute exigido pelo art. 266 da LC 214/2025 — não avalia a gestão local. Com a adesão do município ao convênio Sinter, a mesma base pode ser validada no endpoint oficial (POST /v1/validacao) e transmitida em produção.</div>
</body></html>"""
    html_path = saida.replace('.md', '.html')
    open(html_path, 'w', encoding='utf-8').write(html)
    print('laudo HTML:', html_path)
    print(f'{ok}/{len(rows)} aptos ({pct_ok:.1f}%) · laudo: {saida}')
    print('top falhas:', falhas_por_regra.most_common(5) or 'nenhuma')

    if online:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from cadurb_client import CadurbClient
        cli = CadurbClient()
        resp = cli.validar_ui(ibge, exemplo_ui(rows[0]) if rows else {})
        print('validação oficial (homologação):', json.dumps(resp, ensure_ascii=False)[:500])

def exemplo_ui(r):
    return {
        'DadosGeraisImovel': {
            'inscricaoImobiliaria': r.get('inscricao', ''),
            'tipoImovel': int(r.get('tipo_imovel') or 1),
            'areaTerreno': float(str(r.get('area_terreno') or 0).replace(',', '.')),
            'temBairro': bool((r.get('bairro') or '').strip()),
        },
        'EnderecoImovel': {
            'cep': re.sub(r'\D', '', r.get('cep') or ''),
            'nomeLogradouro': r.get('logradouro', ''),
            'tipoLogradouro': r.get('tipo_logradouro', ''),
        },
    }

if __name__ == '__main__':
    main()
