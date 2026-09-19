#!/usr/bin/env python3
"""Gera as fichas de ligação — uma por município, imprimíveis.

O roteiro está em `06-roteiro-qualificacao.md`; aqui ficam os números que a pessoa
precisa ter na mão enquanto fala. Uma folha por município, quebra de página entre
elas, pensado para sair na impressora e ir para a mesa.

Ordem: índice declarado de três fatores (ver §4 do roteiro). A RCL ficou de fora
de propósito — foi medida e não discrimina, porque o contrato é 0,16% dela na
mediana do segmento B.

Uso:  .venv/bin/python dossie-dispensa/gerar_fichas.py [--segmento B] [--n 40] [--todos]
Saída: dossie-dispensa/fichas-qualificacao.html
"""
import html, json, os, sys
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
D = os.path.join(RAIZ, 'painel', 'dados')

SEG = 'B'
N = 40
for i, a in enumerate(sys.argv):
    if a == '--segmento' and i + 1 < len(sys.argv):
        SEG = sys.argv[i + 1]
    if a == '--n' and i + 1 < len(sys.argv):
        N = int(sys.argv[i + 1])
if '--todos' in sys.argv:
    N = 10**6

mun = [f['properties'] for f in json.load(open(os.path.join(D, 'municipios.json'), encoding='utf-8'))['features']]
cne = json.load(open(os.path.join(D, 'cnefe.json'), encoding='utf-8'))['municipios']
# TCE-PI: tem o fiscal dos 72 que o SICONFI não tem, e o elemento 3.3.90.39
_tce = os.path.join(D, 'tce.json')
tce = json.load(open(_tce, encoding='utf-8'))['municipios'] if os.path.exists(_tce) else {}
alvo = [x for x in mun if SEG in ('*', x.get('segmento') or '')] if SEG != '*' else mun

# quintis de volume, para o terceiro fator do índice
vols = sorted(cne[x['cd']]['end'] for x in alvo if cne.get(x['cd']))
def quintil(v):
    if not vols or v is None:
        return 0
    for q in range(4, 0, -1):
        if v >= vols[int(len(vols) * q / 5) - 1]:
            return q
    return 0

def indice(x):
    c = cne.get(x['cd']) or {}
    return (3 * (1 if x['rreo'][2] else 0)
            + 2 * (0 if x.get('tenant_fox') else 1)
            + 1 * quintil(c.get('end')) / 4)

alvo.sort(key=lambda x: (-indice(x), -(cne.get(x['cd'], {}).get('end') or 0)))
# O peso 3 da entrega do RREO joga os 72 sem demonstrativo para o fim da fila, e
# com N=40 eles nunca apareceriam. Mas são justamente os de maior necessidade —
# o roteiro §5 diz isso. Vão numa seção própria, com o volume como critério.
vivos = [x for x in alvo if x['rreo'][2]][:N]
cegos = sorted((x for x in alvo if not x['rreo'][2]),
               key=lambda x: -(cne.get(x['cd'], {}).get('end') or 0))[:max(10, N // 4)]

N_ = lambda v: '—' if v is None else f'{v:,.0f}'.replace(',', '.')
RS = lambda v: '—' if v is None else ('R$ ' + (f'{v/1e6:,.2f} mi' if v >= 1e6 else f'{v:,.0f}')).replace(',', '.')
e = html.escape

EXFISC = '2025'


def ficha(x):
    c = cne.get(x['cd']) or {}
    r = x['rreo']
    sinal = ' '.join('✓' if a else '✗' for a in r)
    fox = ('<b>host da Foxinline detectado</b> — confirme na porta 2'
           if x.get('tenant_fox') else 'nenhum host detectado — <i>evidência fraca para ausência</i>')
    sem_fiscal = not x['rreo'][2]
    # IPTU ou ITBI reportado como zero (ou quase) NÃO é dado faltando — é dado, e é
    # o argumento mais forte que existe: quem arrecada R$ 0 de imposto sobre imóvel
    # não tem cadastro. Sem esta nota o interlocutor lê como erro da planilha.
    T = tce.get(x['cd']) or {}
    # SICONFI e TCE são duas prestações de contas do MESMO município a órgãos
    # diferentes. Nenhuma é autoritativa a priori: quando divergem, mostra as
    # duas. Escolher em silêncio seria inventar hierarquia que não existe.
    iptu = x.get('iptu') if x.get('iptu') is not None else T.get('iptu')
    itbi = x.get('itbi') if x.get('itbi') is not None else T.get('itbi')
    origem_fiscal = 'SICONFI/RREO' if x.get('iptu') is not None else 'TCE-PI'
    diverge = ''
    if x.get('iptu') is not None and T.get('iptu') is not None and x['iptu'] > 0:
        r = T['iptu'] / x['iptu']
        if not (0.9 <= r <= 1.1):
            diverge = (f'<div class="aviso"><b>As duas fontes divergem.</b> IPTU 2025: '
                       f'SICONFI {RS(x["iptu"])} · TCE-PI {RS(T["iptu"])} ({r:.2f}×). '
                       f'São prestações do mesmo município a órgãos diferentes — '
                       f'<b>pergunte qual está certa</b>, é boa abertura de conversa.</div>')
    pj = T.get('terceiros_pj') or {}
    emp = pj.get('empenhada')
    zerado = ''
    if iptu is not None and itbi is not None and (iptu < 1000 or itbi < 1000):
        quais = ' e '.join(n for n, v in (('IPTU', iptu), ('ITBI', itbi)) if v < 1000)
        zerado = (f'<div class="forte">O município <b>declarou {quais} praticamente zerado em '
                  f'2025</b> — e isso é declaração a {origem_fiscal}, não ausência de dado. '
                  f'É o argumento mais direto da conversa: <b>não se cobra sobre imóvel que '
                  f'não está cadastrado.</b></div>')
    return f"""
<section class="ficha">
 <header>
  <div><h2>{e(x['name'])}</h2>
   <div class="sub">IBGE {x['cd']} · {e(x.get('rgint') or '')} · segmento {e(x.get('segmento') or '—')}</div></div>
  <div class="vol"><div class="l">imóveis a inscrever</div><div class="v">{N_(c.get('end'))}</div>
   <div class="l">CNEFE · Censo 2022</div></div>
 </header>

 <div class="linha"><b>Porta 1</b> — a obrigação é conhecida? <i>art. 266 da LC 214/2025 · prazo 31/12/2026</i></div>
 <div class="linha"><b>Porta 2</b> — já existe fornecedor? {fox}</div>
 <div class="linha destaque"><b>Porta 3 — a dotação.</b> Há saldo não empenhado em
  <b>3.3.90.39</b> (serviços de terceiros, PJ)? Se não, cabe suplementação por decreto?
  Quantos dias leva a dispensa, incluindo o aviso do art. 75 §3º?</div>
 <div class="linha"><b>Porta 4</b> — quem assina a dispensa?</div>

 <table>
  <tr><td class="k">População / domicílios</td><td>{N_(x.get('pop'))} · {N_(x.get('dom'))}</td>
      <td class="k">Domicílios em casa</td><td>{N_(c.get('casa'))}</td></tr>
  <tr><td class="k">IPTU 2025</td><td>{RS(iptu)}</td>
      <td class="k">ITBI 2025</td><td>{RS(itbi)}</td></tr>
  <tr><td class="k">RCL 2025</td><td>{RS(x.get('rcl'))}</td>
      <td class="k">Contrato / RCL</td><td>{'—' if not x.get('rcl') else f"{100*65492.11/x['rcl']:.3f}".replace('.', ',') + '%'}</td></tr>
  <tr><td class="k">RREO 23 · 24 · 25</td><td>{sinal}</td>
      <td class="k">CIB transmitido</td><td>{N_(x.get('cib_ativo') or 0)}</td></tr>
  <tr><td class="k">Fonte fiscal</td><td>{origem_fiscal}</td>
      <td class="k">Dívida ativa de IPTU</td><td>{RS(T.get('iptu_divida'))}</td></tr>
 </table>
 {'' if emp is None else f'''<div class="ancora"><b>Âncora da porta 3.</b> Em {EXFISC} este
  município <b>empenhou {RS(emp)}</b> no elemento <i>Outros Serviços de Terceiros – Pessoa
  Jurídica</i> (3.3.90.39). Um contrato no limite de dispensa é <b>{100*65492.11/emp:.2f}%</b>
  disso.<br><span class="miudo">É o tamanho do elemento, não o saldo livre — o TCE publica
  empenhada, liquidada e paga, não a dotação autorizada. O saldo continua sendo a pergunta.</span></div>'''}
 {diverge}

 {zerado}
 {f'<div class="aviso"><b>Não entregou o RREO 2025 ao SICONFI</b> — os números acima vêm da '
  f'prestação de contas ao <b>TCE-PI</b>. Isso é argumento, não lacuna: ele deve ao Tesouro '
  f'Nacional um demonstrativo que já entregou ao Tribunal. A ausência é o mesmo sintoma que o '
  f'produto resolve.</div>' if sem_fiscal else ''}

 <div class="anota"><b>Anotar:</b> com quem falei · há saldo? · precisa suplementar? ·
  prazo da dispensa · quem assina · próximo passo e data</div>
</section>"""

css = """
:root{--navy:#0B2545;--teal:#12B0A0;--tinta:#0B2545;--fraca:#5B6B7A;--linha:#E2E6EA;--papel:#F4F6F8}
*{box-sizing:border-box}
body{margin:0;background:var(--papel);color:var(--tinta);
 font-family:Inter,-apple-system,'Segoe UI',sans-serif;font-size:13px;line-height:1.5}
.capa{max-width:780px;margin:0 auto;padding:36px 28px}
h1{font-size:23px;letter-spacing:-.02em;margin:0 0 4px}
.capa .sub{color:var(--fraca);font-size:12.5px;margin-bottom:18px}
.capa p{margin:0 0 10px}
.ficha{max-width:780px;margin:0 auto 22px;background:#fff;border:1px solid var(--linha);
 border-radius:12px;padding:20px 22px;page-break-inside:avoid;page-break-after:always}
.ficha header{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;
 border-bottom:2px solid var(--navy);padding-bottom:10px;margin-bottom:12px}
h2{font-size:20px;margin:0;letter-spacing:-.02em}
.sub{color:var(--fraca);font-size:11.5px;margin-top:3px}
.vol{text-align:right;flex:none}
.vol .v{font:600 26px 'IBM Plex Mono',monospace;color:var(--navy);font-variant-numeric:tabular-nums}
.vol .l{font-size:9.5px;color:var(--fraca);text-transform:uppercase;letter-spacing:.09em}
.linha{padding:6px 0;border-bottom:1px solid var(--linha)}
.linha.destaque{background:#F2FBF9;border-left:3px solid var(--teal);padding:9px 11px;margin:5px 0;border-bottom:none}
table{width:100%;border-collapse:collapse;margin:12px 0 10px}
td{padding:5px 6px;border-bottom:1px solid var(--linha);font-variant-numeric:tabular-nums}
td.k{color:var(--fraca);font-size:11px;width:24%}
.aviso{background:#FDF3E7;border-left:3px solid #8F5A02;padding:9px 11px;font-size:12px;margin-bottom:10px}
.forte{background:#FBEDEA;border-left:3px solid #C03A24;padding:9px 11px;font-size:12px;margin-bottom:10px}
.ancora{background:#EEF6FC;border-left:3px solid #12689F;padding:9px 11px;font-size:12px;margin-bottom:10px}
.miudo{color:var(--fraca);font-size:11px}
.anota{border:1px dashed var(--linha);border-radius:8px;padding:22px 11px 30px;font-size:11px;color:var(--fraca)}
@media print{body{background:#fff}.ficha{border:none;margin:0;padding:0 0 12px}.capa{page-break-after:always}}
"""

saida = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Fichas de qualificação · Vertical Data</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<div class="capa">
 <h1>Fichas de qualificação</h1>
 <div class="sub">segmento {e(SEG)} · duas filas · gerado em {date.today().isoformat()}</div>
 <p>O roteiro completo está em <b>dossie-dispensa/06-roteiro-qualificacao.md</b>. Cada ficha
  traz as quatro portas e os números para respondê-las.</p>
 <p><b>A porta que importa é a 3.</b> Está medido que o preço não é obstáculo — um contrato no
  limite de dispensa de 2026 (R$ 65.492,11) é 0,16% da RCL mediana do segmento B. O que não se
  sabe, e nenhuma base aberta responde, é se ainda há <b>dotação não empenhada</b>.</p>
 <p><b>Ordem:</b> índice declarado de três fatores — entregou RREO 2025 (peso 3), sem incumbente
  detectado (peso 2), quintil de volume (peso 1). A RCL ficou fora de propósito: foi medida e não
  discrimina. <b>O índice não prevê dotação</b> — ordena quem atender primeiro, não quem compra.</p>
 <p><b>Novo nesta versão:</b> os municípios sem RREO 2025 deixaram de vir em branco — o
  <b>TCE-PI</b> publica a prestação de contas deles, e a ficha diz qual fonte está usando.
  Onde as duas existem e divergem mais de 10%, as duas aparecem.</p>
 <p style="color:var(--fraca)">Fontes: IBGE Censo 2022 e CNEFE · SICONFI/RREO 2023–2025 ·
  TCE-PI, Portal da Cidadania, exercício 2025 · RFB/Sinter set/2026 · Certificate Transparency.</p>
</div>
<div class="capa"><h1>Fila 1 — gestão viva</h1>
 <div class="sub">{len(vivos)} municípios que entregaram o RREO 2025</div>
 <p>Têm demonstrativo em dia, logo têm contabilidade funcionando — é o sinal mais forte de
  que existe quem execute um contrato. São os de <b>menor atrito</b>, não os de maior
  necessidade.</p></div>
{''.join(ficha(x) for x in vivos)}
<div class="capa"><h1>Fila 2 — o ponto cego</h1>
 <div class="sub">{len(cegos)} dos 72 que não entregaram o RREO 2025, por volume de imóveis</div>
 <p>Estes vêm <b>sem número fiscal</b>: sem RREO 2025 não há IPTU, ITBI nem RCL nesta base.
  E é exatamente por isso que estão aqui — <b>não entregar demonstrativo é o mesmo sintoma
  que o produto resolve</b>. São os de maior necessidade e os que menos consigo qualificar
  antes de ligar.</p>
 <p>Com eles a ligação começa pela porta 1, sem número na mão, e a primeira pergunta útil é
  outra: <b>quem responde pela contabilidade hoje?</b></p></div>
{''.join(ficha(x) for x in cegos)}
</body></html>"""

cam = os.path.join(AQUI, 'fichas-qualificacao.html')
with open(cam, 'w', encoding='utf-8') as fh:
    fh.write(saida)
print(f'ok: {cam} · {os.path.getsize(cam)//1024} KB · {len(vivos)+len(cegos)} fichas')
print(f'  fila 1 (gestão viva): {len(vivos)} · começa por {", ".join(x["name"] for x in vivos[:4])}')
print(f'  fila 2 (ponto cego):  {len(cegos)} · começa por {", ".join(x["name"] for x in cegos[:4])}')
