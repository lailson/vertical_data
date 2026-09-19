#!/usr/bin/env python3
"""Coleta receitas e despesas municipais da API do Portal da Cidadania do TCE-PI.

**Por que existe.** 72 dos 224 municípios não entregaram o RREO 2025 ao SICONFI e
por isso ficam sem IPTU, ITBI e RCL no painel — justamente os que mais precisam do
produto. O TCE recebe prestação de contas por obrigação própria, e **tem o dado
desses municípios**. Verificado em Alagoinha do Piauí, que no SICONFI é nulo e
aqui tem IPTU de R$ 19.333,08.

**E o que não estava previsto:** `/despesas/.../porElemento` traz *Outros Serviços
de Terceiros – Pessoa Jurídica* — o elemento 3.3.90.39, que é o que o roteiro de
qualificação pergunta na porta 3. Não dá o saldo livre (a API expõe empenhada,
liquidada e paga, não a dotação autorizada), mas dá **o tamanho do elemento**, o
que muda a conversa de "vocês têm saldo?" para "vocês empenham X aqui; proponho
1% disso".

API sem chave, sem limite documentado. A coleta é educada: 0,3 s entre chamadas,
três tentativas com espera crescente, e cache em disco para poder retomar.

Uso:  python3 dados/baixar_tce.py [--exercicio 2025] [--refazer]
Saída: dados/bruto/tce/<exercicio>/<idUnidadeGestora>.json
"""
import json, os, sys, time, urllib.error, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://sistemas.tce.pi.gov.br/api/portaldacidadania'
EX = '2025'
for i, a in enumerate(sys.argv):
    if a == '--exercicio' and i + 1 < len(sys.argv):
        EX = sys.argv[i + 1]
REFAZER = '--refazer' in sys.argv
DEST = os.path.join(AQUI, 'bruto', 'tce', EX)
os.makedirs(DEST, exist_ok=True)


def get(path, tentativas=3):
    for i in range(tentativas):
        try:
            req = urllib.request.Request(BASE + path, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            if i == tentativas - 1:
                print(f'    falhou {path}: {e}')
                return None
            time.sleep(2 ** i)
    return None


def receitas(uid):
    """Pagina até esgotar. O tamanho da página é 10 e não é configurável — as
    tentativas de limit/size/porPagina foram todas ignoradas pelo servidor."""
    total = (get(f'/receitas/{uid}/{EX}/quantidadeTotal') or {}).get('numeroTotalRegistros')
    if not total:
        return None
    linhas, pg = [], 1
    while len(linhas) < total and pg <= (total // 10) + 3:
        d = get(f'/receitas/{uid}/{EX}?pagina={pg}')
        if not d:
            break
        linhas += d
        pg += 1
        time.sleep(0.3)
    # a paginação pode repetir a última página; deduplica por conteúdo
    vistos, unicas = set(), []
    for x in linhas:
        k = json.dumps(x, sort_keys=True, ensure_ascii=False)
        if k not in vistos:
            vistos.add(k)
            unicas.append(x)
    return {'total_declarado': total, 'linhas': unicas}


prefs = get('/prefeituras')
if not prefs:
    raise SystemExit('não consegui listar /prefeituras')
print(f'{len(prefs)} prefeituras · exercício {EX}')

novos = pulados = falhas = 0
for i, p in enumerate(prefs, 1):
    cam = os.path.join(DEST, f"{p['id']}.json")
    if os.path.exists(cam) and not REFAZER:
        pulados += 1
        continue
    rec = receitas(p['id'])
    time.sleep(0.3)
    des = get(f"/despesas/{p['id']}/{EX}/porElemento")
    time.sleep(0.3)
    if rec is None and des is None:
        falhas += 1
        print(f"  [{i:>3}/{len(prefs)}] {p['nome'][:26]:28} sem dado")
        continue
    with open(cam, 'w', encoding='utf-8') as fh:
        json.dump({'prefeitura': p, 'exercicio': EX, 'receitas': rec,
                   'despesas_por_elemento': des}, fh, ensure_ascii=False)
    novos += 1
    if i % 20 == 0 or i == len(prefs):
        print(f"  [{i:>3}/{len(prefs)}] {p['nome'][:26]:28} · novos {novos} · pulados {pulados} · falhas {falhas}")

print(f'\nok: {DEST} · {novos} novos · {pulados} já existentes · {falhas} sem dado')
