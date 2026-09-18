#!/usr/bin/env python3
"""Agrega as unidades consumidoras de média e alta tensão do BDGD, por município.

**O que esta base acrescenta e nenhuma outra tem.** A base tabular de geração
distribuída da ANEEL para em município, e o CEP dela vem mascarado. Aqui não:
cada unidade consumidora traz **bairro por nome, CEP completo, coordenada com 8
casas decimais, CNAE, carga instalada e consumo mês a mês** — e o campo `CEG_GD`,
que diz se aquela unidade **já tem geração própria**.

**O que ela não cobre.** É só **pessoa jurídica** em média e alta tensão: no Piauí
são ~4,2 mil unidades, contra 90.528 conexões de geração no estado, quase todas
residenciais. A tabela de baixa tensão (`ucbt_pj.zip`) tem 1,2 GB e também é só
PJ — residência de pessoa física não é publicada, por privacidade.

Ou seja: isto é o mercado de **minigeração** — comércio e indústria. É uma lista
de quem tem carga e ainda não gera, com endereço. Não é o mercado residencial.

Entrada: dados/bruto/aneel/bdgd_uc{at,mt}_pj.csv
Saída:   painel/dados/bdgd.json
Uso:     .venv/bin/python painel/build_bdgd.py [--uf 22]
"""
import json, os, sys
from datetime import date

import duckdb

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DADOS = os.path.join(AQUI, 'dados')
BRUTO = os.path.join(RAIZ, 'dados', 'bruto', 'aneel')

UF = '22'
for i, a in enumerate(sys.argv):
    if a == '--uf' and i + 1 < len(sys.argv):
        UF = sys.argv[i + 1]

ARQS = {'AT': 'bdgd_ucat_pj.csv', 'MT': 'bdgd_ucmt_pj.csv'}
for a in ARQS.values():
    if not os.path.exists(os.path.join(BRUTO, a)):
        raise SystemExit(f'falta {a} em {BRUTO} — rode `python3 dados/baixar.py`')

c = duckdb.connect()
# MUN, CEP e BRR têm de ser texto: o DuckDB inferiria número e comeria o zero à
# esquerda do código do município e o traço do CEP.
TIPOS = "types={'MUN':'VARCHAR','CEP':'VARCHAR','BRR':'VARCHAR','CEG_GD':'VARCHAR'}"
for nivel, arq in ARQS.items():
    # TABLE, não VIEW. Sobre uma view, um agregado com DISTINCT faz o DuckDB
    # reexecutar o plano filho — o CSV de 160 MB é varrido DUAS vezes, e com
    # `ignore_errors` cada varredura descarta um conjunto de linhas malformadas
    # ligeiramente diferente. O resultado eram agregados de leituras distintas
    # no mesmo SELECT, com dois municípios perdendo ~8% das unidades.
    c.execute(f"""CREATE TABLE uc_{nivel} AS SELECT *, '{nivel}' AS nivel
      FROM read_csv('{os.path.join(BRUTO, arq)}', delim=';', header=true,
                    ignore_errors=true, sample_size=-1, {TIPOS})""")

# energia mensal: ENE_01..ENE_12 na média tensão, ENE_P/ENE_F na alta.
# Onde a coluna não existir, a soma fica nula — ausência não vira zero.
def soma_energia(nivel):
    cols = {r[0] for r in c.execute(f"DESCRIBE SELECT * FROM uc_{nivel}").fetchall()}
    alvo = [x for x in cols if x.startswith('ENE_') and x[-2:].isdigit()]
    if not alvo:
        return 'NULL'
    # COALESCE(...,0) em todas as parcelas faria uma UC sem NENHUMA leitura somar
    # zero, que é o oposto de "ausência não é zero". Só soma quem tem ao menos uma.
    soma = ' + '.join(f'COALESCE(TRY_CAST({x} AS DOUBLE), 0)' for x in alvo)
    tem = ' OR '.join(f'TRY_CAST({x} AS DOUBLE) IS NOT NULL' for x in alvo)
    return f'(CASE WHEN {tem} THEN ({soma}) ELSE NULL END)'


partes = []
for nivel in ARQS:
    partes.append(f"""SELECT MUN, BRR, CEP, CNAE, CEG_GD, nivel,
        TRY_CAST(CAR_INST AS DOUBLE) carga,
        {soma_energia(nivel)} AS energia_ano,
        TRY_CAST(POINT_X AS DOUBLE) lon, TRY_CAST(POINT_Y AS DOUBLE) lat
      FROM uc_{nivel} WHERE MUN LIKE '{UF}%'""")
c.execute('CREATE TABLE uc AS ' + ' UNION ALL '.join(partes))

tot = c.execute('SELECT count(*) FROM uc').fetchone()[0]
print(f'· {tot} unidades consumidoras PJ de média/alta tensão na UF {UF}')

linhas = c.execute("""
  SELECT MUN cd, count(*) n,
         sum(CASE WHEN nivel='AT' THEN 1 ELSE 0 END) at_,
         round(sum(carga), 1) carga,
         round(sum(energia_ano), 1) energia,
         sum(CASE WHEN CEG_GD IS NOT NULL AND CEG_GD <> '' THEN 1 ELSE 0 END) com_gd,
         count(DISTINCT BRR) bairros
  FROM uc GROUP BY 1 ORDER BY 2 DESC""").fetchall()

# bairros com mais carga e sem geração: é a lista de quem visitar
alvos = c.execute("""
  SELECT MUN cd, BRR bairro, count(*) n, round(sum(carga),1) carga
  FROM uc WHERE (CEG_GD IS NULL OR CEG_GD = '') AND BRR IS NOT NULL
  GROUP BY 1,2 HAVING count(*) >= 3 ORDER BY carga DESC""").fetchall()
por_mun = {}
for cd, bairro, n, carga in alvos:
    por_mun.setdefault(cd, [])
    if len(por_mun[cd]) < 8:
        por_mun[cd].append({'bairro': bairro, 'n': n, 'carga': carga})

# Com a leitura materializada em tabela, ler e agrupar passam a ver exatamente as
# mesmas linhas. A conferência fica — se algum dia divergir, é sinal de problema
# real, não do plano de consulta.
agrupado = sum(r[1] for r in linhas)
if agrupado != tot:
    raise SystemExit(f'ERRO: lidas {tot}, agrupadas {agrupado}. Com a leitura '
                     'materializada isto não deveria acontecer — investigar antes de publicar.')

saida = {
    'fonte': 'ANEEL · BDGD — unidades consumidoras PJ de média e alta tensão',
    'linhas_lidas': tot, 'linhas_agrupadas': agrupado,
    'url': 'https://dadosabertos.aneel.gov.br/dataset/base-de-dados-geografica-da-distribuidora-bdgd',
    'licenca': 'ODbL — Open Data Commons Open Database License',
    'baixado_em': date.today().isoformat(),
    'nota_cobertura': ('somente pessoa jurídica em média e alta tensão. Não cobre o mercado '
                       'residencial, que é a maior parte das conexões de geração do estado'),
    'nota_geografia': ('aqui o CEP é completo e a coordenada tem 8 casas — ao contrário da base '
                       'tabular de geração distribuída, cujo CEP vem mascarado'),
    'uf': UF, 'municipios': {}, 'alvos_por_bairro': por_mun,
}
for cd, n, at_, carga, energia, com_gd, nb in linhas:
    saida['municipios'][cd] = {
        'uc': n, 'uc_at': at_, 'carga_kw': carga, 'energia_mwh_ano': energia,
        'com_gd': com_gd, 'sem_gd': n - com_gd, 'bairros': nb,
    }

cam = os.path.join(DADOS, 'bdgd.json')
with open(cam, 'w', encoding='utf-8') as fh:
    json.dump(saida, fh, ensure_ascii=False, separators=(',', ':'))
s = sum(v['uc'] for v in saida['municipios'].values())
g = sum(v['com_gd'] for v in saida['municipios'].values())
print(f'ok: {cam} · {os.path.getsize(cam)//1024} KB')
print(f'  {s} unidades em {len(saida["municipios"])} municípios · {g} já com geração · {s-g} sem')
