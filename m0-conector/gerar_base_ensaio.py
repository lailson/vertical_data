#!/usr/bin/env python3
"""Monta uma base de ENSAIO a partir do CNEFE, para exercitar o validador em escala.

**Por que existe.** O `analise/25` §5.5 registra o único item que a venda não
resolve: *"hoje a primeira execução real aconteceria no cliente"*. Não há cadastro
municipal em mãos — mas há **endereço real**, em volume, com CEP, tipo e nome de
logradouro exatamente como o IBGE os enumerou. Isso exercita a metade do validador
que mais depende do mundo real: endereço, CEP, tabela 9.6 e desempenho.

**O que esta base NÃO é.** Não é cadastro imobiliário. O CNEFE não tem inscrição,
valor venal, área nem titular — os campos que o município traz e que ninguém pode
simular honestamente. Então as regras de titularidade, dígito verificador e
coerência territorial × predial **continuam sem ensaio com dado real**, e isso
segue declarado como risco.

O que ela remove do risco: falha de volume, de encoding, de tipo de logradouro
fora da tabela e de CEP que não casa com o município.

Uso:  .venv/bin/python m0-conector/gerar_base_ensaio.py --ibge 2203909 [--n 0]
Saída: m0-conector/ensaio-<ibge>.csv
"""
import csv, glob, io, os, sys, zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
IBGE, N = '2203909', 0
for i, a in enumerate(sys.argv):
    if a == '--ibge' and i + 1 < len(sys.argv):
        IBGE = sys.argv[i + 1]
    if a == '--n' and i + 1 < len(sys.argv):
        N = int(sys.argv[i + 1])

z = glob.glob(os.path.join(RAIZ, 'dados', 'bruto', 'cnefe', '22_*.zip'))
if not z:
    raise SystemExit('falta o CNEFE — rode `python3 dados/baixar.py`')
saida = os.path.join(AQUI, f'ensaio-{IBGE}.csv')
COLS = ['inscricao', 'tipo_imovel', 'area_terreno', 'area_construida', 'valor_venal',
        'logradouro', 'tipo_logradouro', 'bairro', 'cep', 'numero',
        'cpf_cnpj_titular', 'nome_titular', 'perc_titularidade', 'latitude', 'longitude']

zc = zipfile.ZipFile(z[0])
nome = zc.namelist()[0]
n = 0
with zc.open(nome) as fh, open(saida, 'w', encoding='utf-8-sig', newline='') as out:
    r = csv.reader(io.TextIOWrapper(fh, encoding='latin-1', newline=''), delimiter=';')
    h = next(r)
    iM, iCep = h.index('COD_MUNICIPIO'), h.index('CEP')
    iTipo, iNome = h.index('NOM_TIPO_SEGLOGR'), h.index('NOM_SEGLOGR')
    iNum, iLoc = h.index('NUM_ENDERECO'), h.index('DSC_LOCALIDADE')
    iLat, iLon = h.index('LATITUDE'), h.index('LONGITUDE')
    iEsp = h.index('COD_ESPECIE')
    w = csv.writer(out, delimiter=';')
    w.writerow(COLS)
    for row in r:
        if not row or row[iM].strip() != IBGE:
            continue
        n += 1
        w.writerow([
            f'{IBGE}.{n:07d}',          # inscrição sintética e ÚNICA, para não falsear a R9
            '',                          # tipo do imóvel: o CNEFE não sabe. Fica VAZIO de propósito
            '', '', '',                  # área e valor venal: idem
            row[iNome].strip(), row[iTipo].strip(), row[iLoc].strip(),
            row[iCep].strip(), row[iNum].strip(),
            '', '', '',                  # titular e titularidade: o CNEFE não tem
            row[iLat].strip(), row[iLon].strip(),
        ])
        if N and n >= N:
            break
print(f'ok: {saida} · {n:,} endereços do CNEFE'.replace(',', '.'))
print('  campos vazios de propósito: tipo_imovel, áreas, valor venal, titular, titularidade')
print('  (o CNEFE não os tem — simular seria inventar o cadastro que o município deve trazer)')
