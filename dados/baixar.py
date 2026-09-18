#!/usr/bin/env python3
"""Ingestão idempotente das bases públicas do projeto (set/2026).

Origem: `dados/baixar.py` da sessão ZCode (URLs testadas em 15-16/09/2026),
estendido aqui com os **agregados por município** — que são o que permite o
"modo sem bairro" dos 199 municípios do PI sem divisão de bairros no Censo —
e com a **malha municipal do PI**, base do mapa estadual de alvos.

Baixa para dados/bruto/ e PULA arquivos já existentes e não-vazios.

Uso:
    python3 dados/baixar.py             # essencial (~480 MB, com CNEFE e ANEEL)
    python3 dados/baixar.py --completo  # + INEP (537 MB) e as bases por setor
    python3 dados/baixar.py --atualizar # força rebaixar as fontes que mudam sozinhas
"""
import os, sys, urllib.request, time

AQUI = os.path.dirname(os.path.abspath(__file__))
FTP = 'https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022'
GEO = ('https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/'
       'malhas_de_setores_censitarios__divisoes_intramunicipais/censo_2022')
GEOMUN = ('https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/'
          'malhas_municipais/municipio_2023/UFs/PI')
AGREG = FTP + '/Agregados_por_Setores_Censitarios'
ENTORNO = FTP + '/Agregados_por_Setores_Censitarios_Caracteristicas_urbanisticas_do_entorno_dos_domicilios'
RENDA = FTP + '/Agregados_por_Setores_Censitarios_Rendimento_do_Responsavel'
FAVELAS = FTP + '/Favelas_e_comunidades_urbanas_Resultados_do_universo/arquivos_vetoriais'
SINTER = ('https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/'
          'programas-e-atividades/sinter/municipios')
CNEFE = ('https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/'
         'Censo_Demografico_2022/Arquivos_CNEFE')
# ANEEL — dados abertos, licença ODbL (uso comercial permitido, com atribuição).
# Os identificadores de recurso saem da API CKAN e são estáveis:
#   /api/3/action/package_show?id=relacao-de-empreendimentos-de-geracao-distribuida
ANEEL = ('https://dadosabertos.aneel.gov.br/dataset/5e0fafd2-21b9-4d5b-b622-40438d40aba2'
         '/resource/%s/download/%s')
ANEEL_TAR = ('https://dadosabertos.aneel.gov.br/dataset/5a583f3e-1646-4f67-bf0f-69db4203e89e'
             '/resource/%s/download/%s')
ANEEL_BDGD = ('https://dadosabertos.aneel.gov.br/dataset/4459e483-451f-4444-8022-bd8b5eac05c5'
              '/resource/%s/download/%s')

B = AGREG + '/Agregados_por_Bairro_csv'
M = AGREG + '/Agregados_por_Municipio_csv'

ESSENCIAIS = {
    # --- agregados por BAIRRO (Brasil; filtrar CD_BAIRRO por prefixo do município) ---
    'ibge/bairros_basico_BR.zip': B + '/Agregados_por_bairros_basico_BR_20260520.zip',
    'ibge/bairros_domicilio1_BR.zip': B + '/Agregados_por_bairros_caracteristicas_domicilio1_BR.zip',
    'ibge/bairros_domicilio2_BR.zip': B + '/Agregados_por_bairros_caracteristicas_domicilio2_BR_20250417.zip',
    'ibge/bairros_demografia_BR.zip': B + '/Agregados_por_bairros_demografia_BR.zip',
    'ibge/bairros_entorno_domicilios_BR.zip': ENTORNO + '/Agregados_por_Bairro_csv/Agregados_por_bairros_entorno_domic%c3%adlios_BR.zip',
    'ibge/bairros_renda_responsavel_BR.zip': RENDA + '/Agregados_por_bairros_renda_responsavel_BR_20260508_csv.zip',

    # --- agregados por MUNICÍPIO (cobre os 224 do PI; base do modo "sem bairro") ---
    'ibge/municipios_basico_BR.zip': M + '/Agregados_por_municipios_basico_BR_20260520.zip',
    'ibge/municipios_domicilio1_BR.zip': M + '/Agregados_por_municipios_caracteristicas_domicilio1_BR.zip',
    'ibge/municipios_domicilio2_BR.zip': M + '/Agregados_por_municipios_caracteristicas_domicilio2_BR_20250417.zip',
    'ibge/municipios_demografia_BR.zip': M + '/Agregados_por_municipios_demografia_BR.zip',
    'ibge/municipios_entorno_domicilios_BR.zip': ENTORNO + '/Agregados_por_Municipio_csv/Agregados_por_municipios_entorno_domic%c3%adlios_BR.zip',
    'ibge/municipios_renda_responsavel_BR.zip': RENDA + '/Agregados_por_municipios_renda_responsavel_BR_20260508_csv.zip',

    # --- dicionários ---
    'ibge/dicionario_agregados.xlsx': AGREG + '/dicionario_de_dados_agregados_por_setores_censitarios_20260520.xlsx',
    'ibge/dicionario_renda.xlsx': RENDA + '/dicionario_de_dados_renda_responsavel_20260508.xlsx',
    'ibge/dicionarios_entorno.zip': ENTORNO + '/dicionarios_de_dados_entorno.zip',

    # --- geometrias ---
    'ibge/PI_bairros_CD2022.zip': GEO + '/bairros/shp/UF/PI_bairros_CD2022.zip',
    'ibge/PI_Municipios_2023.zip': GEOMUN + '/PI_Municipios_2023.zip',
    'ibge/poligonos_FCUs_shp.zip': FAVELAS + '/poligonos_FCUs_shp.zip',

    # --- CNEFE: os endereços que o Censo enumerou, com coordenada ---
    # É o volume que a remessa ao CADURB tem de cobrir. 34 MB compactados,
    # 289 MB abertos; agregado por painel/build_cnefe.py.
    'cnefe/22_PI.zip': CNEFE + '/CSV/UF/22_PI.zip',
    'cnefe/dicionario_cnefe.xls': CNEFE + '/CSV/Dicionario_CNEFE_Censo_2022.xls',

    # --- ANEEL: micro e minigeração distribuída, atualizada DIARIAMENTE ---
    # Cada empreendimento com fonte, potência, data de conexão e município.
    # Desce a MUNICÍPIO e só: bairro é modelagem, não medição.
    'aneel/gd_empreendimentos.parquet': ANEEL % (
        'cd29f6eb-e08d-4db7-b6fb-ed6e3b682d27', 'empreendimento-geracao-distribuida.parquet'),
    'aneel/gd_fotovoltaica_tecnica.parquet': ANEEL % (
        '703c4cb8-b7e2-4f27-a9bb-7e55324a88a4',
        'empreendimento-gd-informacoes-tecnicas-fotovoltaica.parquet'),

    # Tarifas homologadas. Sem tarifa não se calcula payback, e payback é o que
    # decide adoção de geração — é a variável causal que falta ao modelo.
    'aneel/tarifas.csv': ANEEL_TAR % (
        'fcf2906c-7c32-4b9b-a637-054e7a5234f4',
        'tarifas-homologadas-distribuidoras-energia-eletrica.csv'),

    # BDGD — unidades consumidoras de ALTA e MÉDIA tensão (pessoa jurídica).
    # É o mercado de minigeração: comércio e indústria. A tabela de BAIXA tensão
    # (ucbt_pj.zip) tem 1,2 GB e fica fora até haver uso que a justifique.
    'aneel/bdgd_ucat_pj.csv': ANEEL_BDGD % (
        '4318d38a-0bcd-421d-afb1-fb88b0c92a87', 'ucat_pj.csv'),
    'aneel/bdgd_ucmt_pj.csv': ANEEL_BDGD % (
        'f6671cba-f269-42ef-8eb3-62cb3bfa0b98', 'ucmt_pj.csv'),

    # --- RFB/Sinter (nomes mudam por mês — ajustar se 404) ---
    'sinter/adesoes.xls': SINTER + '/adesoes_setembro_2026_2.xls',
    'sinter/inscricoes.csv': SINTER + '/inscricoes_ativas_setembro_2026_2.csv',
}

EXTRAS = {
    # INEP Censo Escolar 2025 — só depois do conector e da verificação fiscal (PLANO §12.5)
    'inep/microdados_censo_escolar_2025.zip': 'https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_2025_.zip',
    # Malha e agregados por SETOR. Nenhum script depende deles: servem para
    # reproduzir a medição que descartou a junção por código de setor — o CNEFE
    # referencia setor de COLETA e estes usam setor de DIVULGAÇÃO, e o encaixe
    # perde 10,4% dos endereços do Piauí (ver docs/metodologia-iv.md §7.2).
    'ibge/PI_setores_CD2022.zip': GEO + '/setores/shp/UF/PI_setores_CD2022.zip',
    'ibge/setores_basico_BR.zip': AGREG + '/Agregados_por_Setor_csv/Agregados_por_setores_basico_BR_20260520.zip',
}


# Fontes que mudam sozinhas: pular por "já existe" congelaria o painel numa
# vintage antiga sem avisar ninguém. Estas revalidam por idade.
REVALIDAR_DIAS = {
    'aneel/gd_empreendimentos.parquet': 1,
    'aneel/gd_fotovoltaica_tecnica.parquet': 1,
    'aneel/tarifas.csv': 7,     # homologações são episódicas; uma semana basta
    'aneel/bdgd_ucat_pj.csv': 30,
    'aneel/bdgd_ucmt_pj.csv': 30,
}


def baixar(rel, url):
    dest = os.path.join(AQUI, 'bruto', rel)
    if os.path.exists(dest) and os.path.getsize(dest) > 1024:
        limite = REVALIDAR_DIAS.get(rel)
        if limite is None:
            print(f'[ok] {rel} (já existe)')
            return
        idade = (time.time() - os.path.getmtime(dest)) / 86400
        if idade < limite and '--atualizar' not in sys.argv:
            print(f'[ok] {rel} (baixado há {idade*24:.0f}h, revalida em {limite}d)')
            return
        print(f'[revalidando] {rel} — {idade:.1f} dia(s) de idade')
        # Idade vencida não quer dizer arquivo novo. Com If-Modified-Since o
        # servidor responde 304 quando nada mudou, e os ~216 MB dos parquets
        # deixam de ser rebaixados todo dia só porque o relógio virou.
        desde = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(os.path.getmtime(dest)))
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0',
                                                       'If-Modified-Since': desde})
            with urllib.request.urlopen(req, timeout=600) as r:
                if r.status == 304:
                    os.utime(dest, None)
                    print(f'[ok] {rel} (304 — não mudou na origem)')
                    return
                dados = r.read()
            with open(dest + '.part', 'wb') as f:
                f.write(dados)
            os.rename(dest + '.part', dest)
            print(f'[novo] {rel} ({os.path.getsize(dest)//1024} KB)')
            return
        except urllib.error.HTTPError as e:
            if e.code == 304:
                os.utime(dest, None)
                print(f'[ok] {rel} (304 — não mudou na origem)')
                return
            print(f'  condicional falhou ({e.code}); baixando inteiro')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    print(f'[baixando] {rel} …')
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=600) as r, open(dest + '.part', 'wb') as f:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
    os.rename(dest + '.part', dest)
    print(f'[novo] {rel} ({os.path.getsize(dest)//1024} KB)')


if __name__ == '__main__':
    itens = dict(ESSENCIAIS)
    if '--completo' in sys.argv:
        itens.update(EXTRAS)
    falhas = []
    for rel, url in itens.items():
        try:
            baixar(rel, url)
        except Exception as e:
            print(f'[FALHA] {rel}: {e}')
            falhas.append(rel)
        time.sleep(0.5)
    if falhas:
        print('\nPendências:', ', '.join(falhas))
        sys.exit(1)
    print('\nConcluído.')
