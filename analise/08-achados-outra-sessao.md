# Achados incorporados da análise paralela (outra sessão) + correções desta

## Contexto institucional local (Piauí / Teresina) — da outra sessão
- **ETURB** opera a REURB em Teresina (LC municipal 5.444/2019; programa "Teresina é REURB+",
  1.600 títulos em 2026). O **CERURBJus é do TJ-PI**, não é base municipal.
- **SEMDUH** (habitação, prepara Cadastro Municipal de Habitação), **SEMPLAN** (planejamento),
  **SEMFIN** (fisco), **SEMOP** (iluminação), **ADH-PI** (habitação estadual, sucessora da COHAB).
- **CEHURB não existe no Piauí** — é a companhia habitacional do Espírito Santo.
- **Contrato TJ-PI nº 156/2023** com a Foxinline: R$ 1,19 mi, prorrogável até 10 anos.
  - **Cláusula de sigilo: veda repasse das informações a outras empresas.**
  - **Cláusula 4.1.1: o TJ pode autorizar uso por outros órgãos** — é a porta formal.
  - **Cláusula 3.4 (o que o CERURB coleta):** núcleos/quadras/lotes/edificações, cadastro
    socioeconômico **com renda familiar e programas sociais**, características do imóvel, documentos
    digitalizados, **shapefiles/polígonos georreferenciados e memoriais descritivos**.
- **TR da SEAD-PI (PROUrbe, R$ 400 mil 1ª etapa):** a "API" do CERURB é a **CERURB-WEB interna**,
  sincronizada com o **CERURB-MOBILE**; integrações existentes com **PJe, cartórios, Receita Federal
  e OAB**. Tudo privado.
- **Programa Regularizar (TJ-PI, Provimentos 89 e 96/2023):** 79 mil famílias no estado; Guaribas,
  N. Sra. de Nazaré e Floresta do Piauí 100% regularizados; Teresina, Tanque do Piauí, Juazeiro do
  Piauí e Coivaras em tramitação. Adesão por formulário APPM/TJ-PI.
- **Lei Municipal 6.383/2026 (jul/2026): Teresina institui CTM + SIG + IDE na SEMPLAN.**
  Janela e ameaça ao mesmo tempo — a prefeitura tem agenda de dados, e pode internalizar ou licitar.
- **TCE-PI auditou o IPTU de Teresina; a PMT suspendeu a cobrança do IPTU 2026 para imóveis
  edificados.** Tema politicamente quente — muda o discurso de "justiça fiscal".
- **TCE-PI tem API documentada**: `sistemas.tce.pi.gov.br/api/portaldacidadania/docs/`
- **e-SIC Teresina** operante (Decreto 14.605/2014); LAI 15 dias + 10 de prorrogação.
  **Não existe portal de dados abertos municipal** (`dadosabertos.teresina.pi.gov.br` fora do ar).
- **SEMPLAN "Mapas de Teresina"**: shapefile completo, bairros 2013 (KMZ), perímetro urbano 2022,
  zoneamento, mapa de esgoto 2016, posteamento 2016 — download direto, maior ativo local.
- **DataJud/CNJ + Consulta Pública PJe**: métricas processuais de REURB, públicas.
- **APIs descontinuadas** (não gastar engenharia): `api.opendata.inep.gov.br`, `api.datasus.gov.br`,
  `imunizacao.esusab.ufsc.br`, `apis.tesouro.net`, app série histórica do SNIS, ENEM por Escola
  pós-2015, `atlasbrasil.ipea.gov.br`.
- **Foxinline vende "Central CERURB" para gestores municipais** — é concorrente direta no dashboard.
- Contatos: `notario@foxinline.com`, `contato@foxinline.com`, +55 86 98837-4045;
  fiscal do contrato TJ-PI: `yara.mota@tjpi.jus.br`.

## Correções factuais estabelecidas nesta rodada (verificadas empiricamente)

1. **Existe agregado por BAIRRO no Censo 2022** — corrige afirmação anterior desta análise.
   17.576 bairros no Brasil; **123 em Teresina**. Arquivos por bairro: básico, alfabetização,
   características do domicílio (1,2,3), cor/raça, demografia, óbitos, parentesco,
   indígenas e quilombolas.
2. **Renda NÃO existe por bairro** — corrige a outra análise. O rendimento está em
   `Agregados_por_Setores_Censitarios_Rendimento_do_Responsavel/`, **só por setor censitário**.
   Solução: agregar setor→bairro (o setor é mais fino), declarando o método.
3. **Existe valor venal público por imóvel** — corrige a outra análise ("nenhuma base pública tem").
   Fortaleza publica ITBI com `VL_VENAL`, `VL_BASE_CALCULO`, `VL_LANCAMENTO_IPTU`, coordenadas
   SIRGAS 2000, área, padrão, tipologia e zoneamento. São Paulo publica desde 2019.
   Medido: **valor venal = 30,8% do preço de mercado (mediana, n=79.985)**.
4. **NOVO — Características urbanísticas do entorno, por face de quadra, agregadas por bairro.**
   Nenhuma das duas análises tinha. 11 temas, entre eles **VIA PAVIMENTADA (V05406)**,
   **ILUMINAÇÃO PÚBLICA (V05412)** e **BUEIRO (V05409)**, sobre `FACES NO SETOR (V05400)`.
   **Elimina 2 das 5 negociações institucionais da matriz de fontes do cliente.**
   Extraído para os 123 bairros de Teresina: pavimentação de **36,7% (Chapadinha)** a **100%**;
   iluminação de **57,9% (Tabajaras)** a 100%.
5. **NOVO — `Favelas_e_comunidades_urbanas_Resultados_do_universo/` com `arquivos_vetoriais/`.**
   O IBGE delimitou e caracterizou favelas e comunidades urbanas no Censo 2022, **com geometria**.
   É, conceitualmente, o universo dos **núcleos urbanos informais** da REURB — permite dimensionar
   o mercado de regularização por município, com mapa, antes de qualquer contato comercial.
6. **Dimensionamento do beachhead (SICONFI, 224 municípios do PI):** mediana de IPTU
   **R$ 2.214/ano**; 194 de 224 abaixo de R$ 100 mil; só 9 acima de R$ 1 mi;
   **RCL mediana R$ 45,7 mi**. Fee de eficiência sobre IPTU é inaplicável fora de Teresina/Picos/
   Parnaíba; capacidade de pagamento existe, mas a justificativa não pode ser retorno de IPTU.
