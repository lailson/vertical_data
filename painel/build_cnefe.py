#!/usr/bin/env python3
"""Agrega o CNEFE 2022 — o cadastro de endereços do Censo — por município e bairro.

Por que esta base importa aqui: ela traz, para todo município do país, **os
endereços que o Censo enumerou, com coordenada**, e com os campos que a remessa
ao CADURB exige (tipo e nome de logradouro, CEP, número, setor/quadra/face).
Não substitui o cadastro imobiliário do município — não tem inscrição, titular
nem geometria de lote — mas mede a distância até ele antes da primeira reunião.

Recorte urbano: o CNEFE referencia **setores de coleta**, e os agregados do Censo
usam **setores de divulgação**; juntar pelos códigos perde 10,4% dos endereços do
Piauí. Por isso o corte por bairro é feito por **geometria** (ponto em polígono
sobre a malha oficial de bairros), que é exato. Como bairro é recorte urbano, a
contagem por bairro já é a contagem urbana; o que cai fora fica declarado como
"fora da malha de bairros", não classificado.

Entrada: dados/bruto/cnefe/22_PI.zip  ·  painel/dados/bairros/*.json
Saída:   painel/dados/cnefe.json
Uso:     .venv/bin/python painel/build_cnefe.py [--uf 22]
"""
import csv, io, json, os, sys, zipfile
from collections import defaultdict
from datetime import date

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DADOS = os.path.join(AQUI, 'dados')

UF = '22'
for i, a in enumerate(sys.argv):
    if a == '--uf' and i + 1 < len(sys.argv):
        UF = sys.argv[i + 1]

# COD_ESPECIE do dicionário do CNEFE (Censo 2022)
ESPECIE = {
    '1': 'domicilio_particular',
    '2': 'domicilio_coletivo',
    '3': 'estab_agropecuario',
    '4': 'estab_ensino',
    '5': 'estab_saude',
    '6': 'estab_outros',
    '7': 'em_construcao',
    '8': 'estab_religioso',
}
# COD_TIPO_ESPECIE — a edificação do domicílio
TIPO = {'101': 'casa', '102': 'casa_vila_condominio', '103': 'apartamento', '104': 'outros'}


# ------------------------------------------------------- ponto em polígono
def aneis_do(geo):
    """Anéis externos do polígono, como arrays Nx2. Ignora buracos: um endereço
    num vazio interno do bairro segue sendo endereço daquele bairro."""
    t = geo['type']
    if t == 'Polygon':
        return [np.asarray(geo['coordinates'][0], dtype=float)]
    return [np.asarray(po[0], dtype=float) for po in geo['coordinates']]


def dentro(anel, px, py):
    """Regra par-ímpar, vetorizada por aresta. px/py já filtrados pela bbox."""
    x, y = anel[:, 0], anel[:, 1]
    x1, y1 = np.roll(x, -1), np.roll(y, -1)
    res = np.zeros(px.shape, dtype=bool)
    # em blocos de arestas, para não estourar memória em bairro com muito vértice
    for ini in range(0, len(x), 256):
        fim = min(ini + 256, len(x))
        yi = y[ini:fim, None]; yj = y1[ini:fim, None]
        xi = x[ini:fim, None]; xj = x1[ini:fim, None]
        cruza = (yi > py) != (yj > py)
        with np.errstate(divide='ignore', invalid='ignore'):
            corte = (xj - xi) * (py - yi) / (yj - yi) + xi
        res ^= np.logical_and(cruza, px < corte).sum(axis=0) % 2 == 1
    return res


# ------------------------------------------------------------------ leitura
print('· lendo CNEFE…')
import glob
_cam = glob.glob(os.path.join(RAIZ, 'dados', 'bruto', 'cnefe', f'{UF}_*.zip'))
if not _cam:
    raise SystemExit(f'não achei o CNEFE da UF {UF} em dados/bruto/cnefe/ — ver dados/baixar.py')
zc = zipfile.ZipFile(_cam[0])
nome = zc.namelist()[0]

mun = defaultdict(lambda: {'total': 0, 'especie': defaultdict(int), 'tipo': defaultdict(int),
                           'cep': set()})
# pontos só dos municípios que têm malha de bairros
com_bairro = {f[:-5] for f in os.listdir(os.path.join(DADOS, 'bairros')) if f.endswith('.json')}
pontos = defaultdict(lambda: {'x': [], 'y': [], 'esp': []})

with zc.open(nome) as f:
    txt = io.TextIOWrapper(f, encoding='latin-1', newline='')
    r = csv.reader(txt, delimiter=';')
    h = next(r)
    # o cabeçalho vem truncado em alguns arquivos do IBGE ('COD_TIPO_ESPECI')
    col_tipo = next(c for c in h if c.startswith('COD_TIPO_ESPECI'))
    iM, iE, iT = h.index('COD_MUNICIPIO'), h.index('COD_ESPECIE'), h.index(col_tipo)
    iLat, iLon, iCep = h.index('LATITUDE'), h.index('LONGITUDE'), h.index('CEP')
    for row in r:
        if not row:
            continue
        cd = row[iM].strip()
        m = mun[cd]
        m['total'] += 1
        m['especie'][row[iE].strip()] += 1
        if row[iT].strip():
            m['tipo'][row[iT].strip()] += 1
        # prefixos de CEP observados: é com esta lista que a regra R3 do validador
        # confere "CEP do município". Intervalo não serve — em Parnaíba, 64203 e
        # 64214 estão dentro da faixa e não pertencem ao município.
        cep = row[iCep].strip()
        if len(cep) == 8 and cep.isdigit():
            m['cep'].add(cep[:5])
        if cd in com_bairro:
            p = pontos[cd]
            p['x'].append(row[iLon]); p['y'].append(row[iLat]); p['esp'].append(row[iE].strip())

print(f'  {sum(m["total"] for m in mun.values()):,} endereços · {len(mun)} municípios'.replace(',', '.'))

# --------------------------------------------------- atribuição a bairros
print('· cruzando com a malha de bairros…')
bairros = {}
resumo_mun_bairro = {}
for cd in sorted(pontos, key=lambda c: -len(pontos[c]['x'])):
    p = pontos[cd]
    px = np.asarray(p['x'], dtype=float)
    py = np.asarray(p['y'], dtype=float)
    esp = np.asarray(p['esp'])
    dom = esp == '1'
    restante = np.ones(px.shape, dtype=bool)

    pac = json.load(open(os.path.join(DADOS, 'bairros', f'{cd}.json'), encoding='utf-8'))
    for ft in pac['features']:
        cdb = ft['properties']['cd']
        achou = np.zeros(px.shape, dtype=bool)
        for anel in aneis_do(ft['geometry']):
            x0, y0 = anel[:, 0].min(), anel[:, 1].min()
            x1, y1 = anel[:, 0].max(), anel[:, 1].max()
            cand = restante & (px >= x0) & (px <= x1) & (py >= y0) & (py <= y1)
            if not cand.any():
                continue
            idx = np.flatnonzero(cand)
            achou[idx] |= dentro(anel, px[idx], py[idx])
        restante &= ~achou
        # acumula: se a malha partir um bairro em mais de uma feature, atribuir
        # descartaria a contagem da anterior e subcontaria em silêncio
        acc = bairros.setdefault(cdb, {'end': 0, 'dom': 0})
        acc['end'] += int(achou.sum())
        acc['dom'] += int((achou & dom).sum())
    fora = int(restante.sum())
    resumo_mun_bairro[cd] = {'na_malha': int(len(px) - fora), 'fora_da_malha': fora}
    print(f'  {cd}: {len(px):>7} endereços · {len(px)-fora:>7} em bairro · {fora:>7} fora')

# ------------------------------------------------------------------ saída
saida = {'uf': UF, 'fonte': 'IBGE · CNEFE Censo 2022', 'consulta': date.today().isoformat(),
         'especies': ESPECIE, 'tipos': TIPO, 'municipios': {}, 'bairros': bairros}
for cd, m in mun.items():
    saida['municipios'][cd] = {
        'end': m['total'],
        'dom': m['especie'].get('1', 0),
        'dom_col': m['especie'].get('2', 0),
        'agro': m['especie'].get('3', 0),
        'estab': sum(m['especie'].get(k, 0) for k in ('4', '5', '6', '8')),
        'obra': m['especie'].get('7', 0),
        'casa': m['tipo'].get('101', 0) + m['tipo'].get('102', 0),
        'apto': m['tipo'].get('103', 0),
        'cep': sorted(m['cep']),
        **(resumo_mun_bairro.get(cd) or {}),
    }

os.makedirs(DADOS, exist_ok=True)
cam = os.path.join(DADOS, 'cnefe.json')
with open(cam, 'w', encoding='utf-8') as fh:
    json.dump(saida, fh, ensure_ascii=False, separators=(',', ':'))
print(f"\nok: {cam} · {os.path.getsize(cam)//1024} KB · "
      f"{len(saida['municipios'])} municípios · {len(bairros)} bairros")
