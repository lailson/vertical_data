#!/usr/bin/env python3
"""Agrega receitas e despesas municipais do TCE-PI, por município.

**O que esta fonte resolve.** 72 dos 224 municípios não entregaram o RREO 2025 ao
SICONFI e ficam sem IPTU, ITBI e RCL no painel — justamente os que mais precisam
do produto e os que menos se consegue qualificar antes de ligar. O TCE recebe
prestação de contas por obrigação própria e **tem o dado deles**.

**Duas decisões de método, e a primeira muda o número.**

1. **IPTU e ITBI entram só pelo PRINCIPAL.** A API separa cada imposto em três
   lançamentos — principal, dívida ativa, multas e juros. Somar os três infla o
   valor contra o SICONFI, que no demonstrativo traz o imposto do exercício. A
   dívida ativa fica em campo próprio, porque **também é informação comercial**:
   município com dívida ativa alta e IPTU baixo tem cadastro velho, não ausência
   de contribuinte.
2. **O elemento de serviços de terceiros PJ é `empenhada`, não saldo.** A API
   expõe empenhada, liquidada e paga; **não expõe a dotação autorizada**. Então
   isto mede o *tamanho* do elemento, nunca o saldo livre — que continua sendo
   pergunta de telefone (roteiro, porta 3).

Entrada: dados/bruto/tce/<exercicio>/*.json  (ver dados/baixar_tce.py)
Saída:   painel/dados/tce.json
Uso:     .venv/bin/python painel/build_tce.py [--exercicio 2025]
"""
import glob, json, os, re, sys
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
EX = '2025'
for i, a in enumerate(sys.argv):
    if a == '--exercicio' and i + 1 < len(sys.argv):
        EX = sys.argv[i + 1]
D = os.path.join(RAIZ, 'dados', 'bruto', 'tce', EX)
arqs = sorted(glob.glob(os.path.join(D, '*.json')))
if not arqs:
    raise SystemExit(f'nada em {D} — rode `python3 dados/baixar_tce.py --exercicio {EX}`')


def norm(s):
    return re.sub(r'\s+', ' ', (s or '').replace('"', '').strip()).upper()


PRINCIPAL, DIVIDA = 'PRINCIPAL', ('DÍVIDA ATIVA', 'DIVIDA ATIVA', 'MULTAS E JUROS')
# o nome do ITBI é longo e truncado de formas diferentes; a âncora é "INTER VIVOS"
def classifica(det):
    n = norm(det)
    if 'PROPRIEDADE PREDIAL E TERRITORIAL URBANA' in n:
        imposto = 'iptu'
    elif 'INTER VIVOS' in n:
        imposto = 'itbi'
    else:
        return None, None
    if n.endswith(PRINCIPAL) or f'- {PRINCIPAL}' in n:
        return imposto, 'principal'
    if any(d in n for d in DIVIDA):
        return imposto, 'divida'
    return imposto, 'outro'


# "Cota-Parte do Imposto Sobre a Propriedade Territorial Rural" é TRANSFERÊNCIA
# da União, não imposto próprio — entra em "Transferência Corrente" e a âncora
# acima não a pega, mas a conferência abaixo garante.
def e_transferencia(x):
    return 'TRANSFER' in norm(x.get('origem'))


saida = {
    'fonte': 'TCE-PI · API do Portal da Cidadania',
    'url': 'https://sistemas.tce.pi.gov.br/api/portaldacidadania/docs/',
    'baixado_em': date.today().isoformat(),
    'exercicio': EX,
    'nota_principal': ('IPTU e ITBI são o lançamento PRINCIPAL. Dívida ativa e multas '
                       'ficam em campo próprio — somá-los infla o valor contra o SICONFI'),
    'nota_elemento': ('servicos_terceiros_pj é o valor EMPENHADO no elemento, não o saldo '
                      'livre: a API não expõe a dotação autorizada'),
    'municipios': {},
}
sem_iptu = sem_elemento = 0
for f in arqs:
    d = json.load(open(f, encoding='utf-8'))
    p = d['prefeitura']
    cd = p['codIBGE']
    linhas = (d.get('receitas') or {}).get('linhas') or []
    v = {'iptu': 0.0, 'itbi': 0.0, 'iptu_divida': 0.0, 'itbi_divida': 0.0}
    achou = {'iptu': False, 'itbi': False}
    total = 0.0
    for x in linhas:
        a = x.get('arrecadada') or 0
        total += a
        if e_transferencia(x):
            continue
        imp, tipo = classifica(x.get('detalhamento'))
        if not imp:
            continue
        achou[imp] = True
        if tipo == 'principal':
            v[imp] += a
        elif tipo == 'divida':
            v[imp + '_divida'] += a
    el = d.get('despesas_por_elemento') or []
    pj = next((e for e in el if 'PESSOA JUR' in norm(e.get('elemento'))), None)
    if pj is None:
        sem_elemento += 1
    if not achou['iptu']:
        sem_iptu += 1
    saida['municipios'][cd] = {
        'nome': p['nome'], 'id_tce': p['id'],
        # ausência de lançamento é diferente de valor zero declarado
        'iptu': round(v['iptu'], 2) if achou['iptu'] else None,
        'itbi': round(v['itbi'], 2) if achou['itbi'] else None,
        'iptu_divida': round(v['iptu_divida'], 2) if achou['iptu'] else None,
        'itbi_divida': round(v['itbi_divida'], 2) if achou['itbi'] else None,
        'receita_total': round(total, 2),
        'terceiros_pj': None if pj is None else {
            'empenhada': pj.get('empenhada'), 'liquidada': pj.get('liquidada'), 'paga': pj.get('paga')},
        'linhas_receita': len(linhas),
    }

cam = os.path.join(AQUI, 'dados', 'tce.json')
with open(cam, 'w', encoding='utf-8') as fh:
    json.dump(saida, fh, ensure_ascii=False, separators=(',', ':'))
n = len(saida['municipios'])
print(f'ok: {cam} · {os.path.getsize(cam)//1024} KB · {n} municípios')
print(f'  sem lançamento de IPTU: {sem_iptu} · sem elemento de terceiros PJ: {sem_elemento}')
