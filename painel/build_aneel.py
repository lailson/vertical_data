#!/usr/bin/env python3
"""Agrega a micro e minigeração distribuída da ANEEL por município do Piauí.

O que esta base é: **cada empreendimento** de geração distribuída conectado no
país, com fonte, potência, classe de consumo, porte e **data de conexão**.
4,6 milhões de linhas nacionais, 90 mil no Piauí. Licença ODbL — uso comercial
permitido, com atribuição.

O que ela **não** é:

- **Não desce de município.** O `CodCEP` existe, mas vem mascarado nos três
  últimos dígitos (`64066***`): sobra o prefixo de 5, que é o mesmo recorte que
  já se usa para validar CEP. Serve de pista grossa dentro de cidade grande,
  nunca de atribuição de bairro. Qualquer número por bairro aqui é modelagem.
- **Não está em dia.** A atualização é diária, mas a conexão mais recente fica
  ~3 meses atrás do dia da carga. Atualização frequente e dado atual são coisas
  diferentes, e a tela tem de dizer qual das duas ela tem.

Dado pessoal: o arquivo traz `NumCPFCNPJ` e `NomTitularEmpreendimento` de cada
titular. **Nenhum dos dois sai daqui.** A leitura seleciona coluna a coluna, e
o agregado é por município — não há como reidentificar a partir da saída.

Entrada: dados/bruto/aneel/*.parquet  ·  painel/dados/municipios.json
Saída:   painel/dados/aneel.json
Uso:     .venv/bin/python painel/build_aneel.py [--uf 22]
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

EMP = os.path.join(BRUTO, 'gd_empreendimentos.parquet')
FOT = os.path.join(BRUTO, 'gd_fotovoltaica_tecnica.parquet')
for p in (EMP, FOT):
    if not os.path.exists(p):
        raise SystemExit(f'falta {p} — rode `python3 dados/baixar.py`')

c = duckdb.connect()
# A junção com o técnico traz DatConexao, que é o que interessa: no Piauí ela
# casa 90.528/90.528 e coincide com a data cadastral do arquivo principal.
BASE = f"""
  FROM read_parquet('{EMP}') e
  LEFT JOIN read_parquet('{FOT}') f ON e.CodEmpreendimento = f.CodGeracaoDistribuida
  WHERE e.CodUFibge = {int(UF)}
"""

print('· lendo ANEEL…')
vintage, ref, n_uf = c.execute(f"""
  SELECT max(e.DatGeracaoConjuntoDados), max(e.AnmPeriodoReferencia), count(*) {BASE}""").fetchone()
conexao_max = c.execute(f"SELECT max(f.DatConexao) {BASE}").fetchone()[0]
print(f'  {n_uf:,} empreendimentos · carga {vintage} · conexão mais recente {conexao_max}'.replace(',', '.'))

# ---------------------------------------------------------------- por município
linhas = c.execute(f"""
  SELECT e.CodMunicipioIbge cd, any_value(e.NomMunicipio) nome,
         count(*) n, round(sum(e.MdaPotenciaInstaladaKW), 2) kw,
         sum(CASE WHEN e.DscPorte ILIKE 'micro%' THEN 1 ELSE 0 END) micro,
         sum(CASE WHEN e.DscFonteGeracao ILIKE '%solar%' THEN 1 ELSE 0 END) solar,
         -- residencial (RE) + baixa renda (REBR): é o numerador que combina com
         -- um denominador de domicílios. Comércio, rural e indústria não moram
         -- em domicílio, e somá-los inflava a penetração em 1 a 2 pontos.
         sum(CASE WHEN e.CodClasseConsumo IN ('RE','REBR') THEN 1 ELSE 0 END) res,
         round(sum(CASE WHEN e.DscFonteGeracao ILIKE '%solar%'
                        THEN e.MdaPotenciaInstaladaKW ELSE 0 END), 2) kw_solar,
         min(f.DatConexao) c0, max(f.DatConexao) c1
  {BASE} GROUP BY 1 ORDER BY 3 DESC""").fetchall()

classes = c.execute(f"""
  SELECT e.CodMunicipioIbge cd, e.DscClasseConsumo classe, count(*) n
  {BASE} GROUP BY 1, 2""").fetchall()
serie = c.execute(f"""
  SELECT e.CodMunicipioIbge cd, year(f.DatConexao) ano, count(*) n,
         round(sum(e.MdaPotenciaInstaladaKW), 2) kw
  {BASE} AND f.DatConexao IS NOT NULL GROUP BY 1, 2 ORDER BY 1, 2""").fetchall()

por_classe, por_ano = {}, {}
for cd, cl, n in classes:
    por_classe.setdefault(str(cd), {})[(cl or 'sem classe').strip()] = n
for cd, ano, n, kw in serie:
    if ano and ano > 2009:
        por_ano.setdefault(str(cd), {})[str(ano)] = [n, kw]

# Série nacional, para comparação. Sem ela o Piauí sozinho é ambíguo: uma queda
# pode ser o mercado inteiro encolhendo ou só este estado perdendo participação —
# e são conclusões comerciais opostas.
br = c.execute(f"""
  SELECT year(f.DatConexao) ano, count(*) n
  FROM read_parquet('{EMP}') e
  LEFT JOIN read_parquet('{FOT}') f ON e.CodEmpreendimento = f.CodGeracaoDistribuida
  WHERE f.DatConexao IS NOT NULL AND year(f.DatConexao) BETWEEN 2010 AND 2100
  GROUP BY 1 ORDER BY 1""").fetchall()

# domicílios do Censo: transforma contagem em penetração, que é o número que decide
mun = {f['properties']['cd']: f['properties']
       for f in json.load(open(os.path.join(DADOS, 'municipios.json'), encoding='utf-8'))['features']}

saida = {
    'fonte': 'ANEEL · Relação de empreendimentos de micro e minigeração distribuída',
    'url': 'https://dadosabertos.aneel.gov.br/dataset/relacao-de-empreendimentos-de-geracao-distribuida',
    'licenca': 'ODbL — Open Data Commons Open Database License',
    'baixado_em': date.today().isoformat(),
    'vintage': str(vintage),
    'periodo_referencia': ref,
    # a diferença entre estes dois é a defasagem real da base
    'conexao_mais_recente': str(conexao_max),
    'nota_defasagem': ('atualização diária, mas a conexão mais recente fica meses atrás '
                       'da data de carga — frequência de atualização não é atualidade do dado'),
    'nota_penetracao': ('penetração = conexões RESIDENCIAIS (classes RE e REBR) ÷ domicílios '
                        'do Censo 2022. Usar todas as classes sobre o mesmo denominador '
                        'inflava o número em 1 a 2 pontos, porque comércio, rural e indústria '
                        'não moram em domicílio'),
    'nota_granularidade': ('município é o menor recorte: o CEP vem mascarado nos 3 últimos '
                           'dígitos. Número por bairro seria modelagem, não medição'),
    'nota_lacuna': ('a ANEEL suspendeu a atualização entre 23/09 e 13/11/2025 na migração '
                    'SISGD → MMGD; o vale de 2025 na série reflete isso'),
    'uf': UF, 'municipios': {},
    'br_ano': {str(ano): n for ano, n in br},
}
for cd, nome, n, kw, micro, solar, res, kw_solar, c0, c1 in linhas:
    k = str(cd)
    p = mun.get(k) or {}
    dom = p.get('dom')
    saida['municipios'][k] = {
        'nome': nome, 'n': n, 'kw': kw, 'micro': micro,
        'solar': solar, 'kw_solar': kw_solar, 'res': res,
        'primeira': str(c0) if c0 else None, 'ultima': str(c1) if c1 else None,
        # penetração só existe onde há denominador; sem domicílio fica nulo, não zero.
        # Numerador é só residencial, para casar com o denominador de domicílios.
        'pen': round(100 * res / dom, 3) if dom else None,
        'pen_todas': round(100 * n / dom, 3) if dom else None,
        'classe': por_classe.get(k, {}),
        'ano': por_ano.get(k, {}),
    }

sem_gd = [cd for cd in mun if cd not in saida['municipios']]
saida['municipios_sem_registro'] = sorted(sem_gd)
saida['uf_total'] = {
    'n': sum(x['n'] for x in saida['municipios'].values()),
    'kw': round(sum(x['kw'] for x in saida['municipios'].values()), 2),
    'municipios_com': len(saida['municipios']),
    'municipios_sem': len(sem_gd),
}

cam = os.path.join(DADOS, 'aneel.json')
with open(cam, 'w', encoding='utf-8') as fh:
    json.dump(saida, fh, ensure_ascii=False, separators=(',', ':'))
t = saida['uf_total']
print(f"\nok: {cam} · {os.path.getsize(cam)//1024} KB")
print(f"  {t['n']:,} conexões · {t['kw']/1000:,.1f} MW".replace(',', '.'))
print(f"  {t['municipios_com']} municípios com registro · {t['municipios_sem']} sem")
