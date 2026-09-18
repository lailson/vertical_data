#!/usr/bin/env python3
"""Extrai as tarifas homologadas vigentes das distribuidoras que servem o Piauí.

Por que isto importa: **sem tarifa não se calcula payback, e payback é o que
decide adoção de geração distribuída**. É a variável causal que falta a qualquer
modelo que só olhe renda e irradiação.

O que o arquivo da ANEEL traz, e que não é óbvio: a tarifa aparece **duas vezes**
por subgrupo — uma com `DscDetalhe = 'Não se aplica'` (consumo comum) e outra com
`DscDetalhe = 'SCEE'`, o Sistema de Compensação de Energia Elétrica, que é o
regime de quem tem geração própria. Na Equatorial PI a diferença está quase toda
no TE. **Somar as duas dá um número que não existe** — foi o primeiro erro ao ler
este arquivo.

O que este script NÃO faz: calcular payback. A Lei 14.300/2022 tem cronograma de
transição do Fio B até 2029, e a regra muda conforme a data de conexão. Publicar
uma conta de retorno sem essa transição seria inventar precisão.

Entrada: dados/bruto/aneel/tarifas.csv
Saída:   painel/dados/tarifas.json
Uso:     .venv/bin/python painel/build_tarifas.py
"""
import json, os
from datetime import date

import duckdb

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DADOS = os.path.join(AQUI, 'dados')
CSV = os.path.join(RAIZ, 'dados', 'bruto', 'aneel', 'tarifas.csv')
if not os.path.exists(CSV):
    raise SystemExit(f'falta {CSV} — rode `python3 dados/baixar.py`')

# quem de fato serve o Piauí, medido na base de geração distribuída
AGENTES = ('EQUATORIAL PI',)

c = duckdb.connect()
c.execute(f"""CREATE VIEW tar AS SELECT * FROM read_csv('{CSV}', delim=';', header=true,
          ignore_errors=true, sample_size=-1)""")

num = "CAST(replace(%s, ',', '.') AS DOUBLE)"
linhas = c.execute(f"""
  SELECT SigAgente, DscSubGrupo, DscModalidadeTarifaria, DscClasse, DscSubClasse,
         DscDetalhe, NomPostoTarifario, DscUnidadeTerciaria,
         {num % 'VlrTUSD'} tusd, {num % 'VlrTE'} te,
         DatInicioVigencia, DatFimVigencia, DscREH
  FROM tar
  WHERE SigAgente IN {AGENTES if len(AGENTES) > 1 else "('" + AGENTES[0] + "')"}
    AND DscBaseTarifaria = 'Tarifa de Aplicação'
    AND current_date BETWEEN DatInicioVigencia AND DatFimVigencia
  ORDER BY DscSubGrupo, DscClasse, DscSubClasse, DscDetalhe, NomPostoTarifario""").fetchall()
if not linhas:
    raise SystemExit('nenhuma tarifa vigente encontrada — conferir SigAgente e vigência')

vintage = c.execute("SELECT max(DatGeracaoConjuntoDados) FROM tar").fetchone()[0]

itens = []
for (ag, sg, mod, cl, sub, det, posto, un, tusd, te, ini, fim, reh) in linhas:
    itens.append({
        'agente': ag, 'subgrupo': sg, 'modalidade': mod, 'classe': cl, 'subclasse': sub,
        # 'SCEE' = regime de compensação (quem tem geração própria); 'Não se aplica' = consumo comum
        'detalhe': det, 'posto': posto, 'unidade': un,
        'tusd': tusd, 'te': te,
        'total': round((tusd or 0) + (te or 0), 2),
        'vigencia': [str(ini), str(fim)], 'reh': reh,
    })


def achar(**kw):
    for x in itens:
        if all(x.get(k) == v for k, v in kw.items()):
            return x
    return None


# o par que interessa à conversa de geração: consumo comum × regime de compensação
res = achar(subgrupo='B1', modalidade='Convencional', classe='Residencial',
            subclasse='Residencial', detalhe='Não se aplica', posto='Não se aplica')
res_scee = achar(subgrupo='B1', modalidade='Convencional', classe='Residencial',
                 subclasse='Residencial', detalhe='SCEE', posto='Não se aplica')

saida = {
    'fonte': 'ANEEL · Tarifas de aplicação das distribuidoras de energia elétrica',
    'url': 'https://dadosabertos.aneel.gov.br/dataset/tarifas-distribuidoras-energia-eletrica',
    'licenca': 'ODbL — Open Data Commons Open Database License',
    'baixado_em': date.today().isoformat(),
    'vintage': str(vintage),
    'nota_scee': ('a mesma tarifa aparece com DscDetalhe "Não se aplica" (consumo comum) e '
                  '"SCEE" (regime de compensação, de quem tem geração). São alternativas, '
                  'não parcelas: somar as duas produz um valor que não existe'),
    'nota_payback': ('payback NÃO é calculado aqui: a Lei 14.300/2022 tem cronograma de '
                     'transição do Fio B até 2029 e a regra varia com a data de conexão'),
    'agentes': list(AGENTES),
    'residencial_b1': res, 'residencial_b1_scee': res_scee,
    'itens': itens,
}
cam = os.path.join(DADOS, 'tarifas.json')
with open(cam, 'w', encoding='utf-8') as fh:
    json.dump(saida, fh, ensure_ascii=False, separators=(',', ':'))
print(f'ok: {cam} · {os.path.getsize(cam)//1024} KB · {len(itens)} tarifas vigentes')
if res:
    print(f"  B1 residencial convencional: TUSD {res['tusd']} + TE {res['te']} = "
          f"R$ {res['total']}/{res['unidade']}  (vigência {res['vigencia'][0]} a {res['vigencia'][1]})")
if res_scee:
    print(f"  mesma, regime SCEE:          TUSD {res_scee['tusd']} + TE {res_scee['te']} = "
          f"R$ {res_scee['total']}/{res_scee['unidade']}")
