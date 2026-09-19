#!/usr/bin/env python3
"""Gera a amostra de dez linhas anexa à carta à Equatorial.

Amostra não entrega ativo: vai sem coordenada e sem titular. O que ela mostra é o
formato e a qualidade do recorte — bairro, CEP, CNAE e carga —, o suficiente para
alguém do outro lado decidir se quer ver o resto.
"""
import csv, os, sys
import duckdb

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
BRUTO = os.path.join(RAIZ, 'dados', 'bruto', 'aneel')
N = 10
for i, a in enumerate(sys.argv):
    if a == '--n' and i + 1 < len(sys.argv):
        N = int(sys.argv[i + 1])

c = duckdb.connect()
TIPOS = "types={'MUN':'VARCHAR','CEP':'VARCHAR','BRR':'VARCHAR','CEG_GD':'VARCHAR'}"
linhas = c.execute(f"""
  SELECT MUN, BRR, CEP, CNAE, round(TRY_CAST(CAR_INST AS DOUBLE), 1) carga, 'MT' nivel
  FROM read_csv('{os.path.join(BRUTO, 'bdgd_ucmt_pj.csv')}', delim=';', header=true,
                ignore_errors=true, sample_size=-1, {TIPOS})
  WHERE MUN LIKE '22%' AND (CEG_GD IS NULL OR CEG_GD = '')
    AND BRR IS NOT NULL AND TRY_CAST(CAR_INST AS DOUBLE) > 0
  ORDER BY carga DESC LIMIT {N}""").fetchall()

import json
mun = {f['properties']['cd']: f['properties']['name']
       for f in json.load(open(os.path.join(RAIZ, 'painel', 'dados', 'municipios.json'),
                               encoding='utf-8'))['features']}
cam = os.path.join(AQUI, 'amostra-bdgd-equatorial.csv')
with open(cam, 'w', encoding='utf-8-sig', newline='') as fh:
    w = csv.writer(fh, delimiter=';')
    w.writerow(['municipio', 'cod_ibge', 'bairro', 'cep', 'cnae', 'carga_instalada_kw', 'nivel_tensao'])
    for m, brr, cep, cnae, carga, niv in linhas:
        w.writerow([mun.get(m, m), m, brr, cep, cnae, f'{carga:.1f}'.replace('.', ','), niv])
print(f'ok: {cam} · {len(linhas)} linhas')
print('  sem coordenada e sem titular, de propósito')
for r in linhas[:3]:
    print(f'   {mun.get(r[0], r[0])[:16]:18} {str(r[1])[:18]:20} {r[2]} · {r[4]} kW')
