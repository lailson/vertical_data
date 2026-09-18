# Comparação — esta análise × análise da outra sessão

Data: 2026-09-15. Comparação feita com verificação empírica de cada ponto divergente.

## 1. Onde a OUTRA análise está certa e ESTA estava ERRADA

### 1.1 Granularidade por bairro — erro material meu, verificado e corrigido

Afirmei repetidamente (dossiê seção 4; adendo; e alimentei o parecer técnico com isso, que virou o
Achado 3 da Rodada 1 do DeepSeek) que **"a granularidade pública para em município ou setor
censitário; bairro só existe via cadastro próprio ou prefeitura; prometer bairro é vender ficção"**.

**Isso está errado.** Verificação direta no FTP do IBGE:
`ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/` contém
`Agregados_por_Bairro_csv/` e `Agregados_por_Bairro_xlsx/`, além de Distrito, SubDistrito, Município
e Setor.

Baixei e validei: `Agregados_por_bairros_basico_BR.csv` tem **17.576 bairros no Brasil**, com
`CD_BAIRRO, NM_BAIRRO, CD_MUN, NM_MUN, CD_DIST, CD_SUBDIST, CD_NU, CD_AGLOM`, e **224 registros para
Teresina**. O arquivo `caracteristicas_domicilio2` tem **408 colunas** por bairro.

Arquivos disponíveis por bairro: básico, alfabetização, características do domicílio (1, 2 e 3),
cor ou raça, demografia, domicílios e pessoas indígenas, domicílios e pessoas quilombolas, óbitos,
parentesco.

**Consequência:** o painel por bairro é construível hoje, com dado aberto, sem negociação. A
ressalva que eu impus ("rotular tudo como estimativa") cai para a maior parte dos indicadores.

### 1.2 Contexto institucional local — ela tem, eu não tinha
- **ETURB** é quem opera a REURB em Teresina (LC municipal 5.444/2019), não o CERURB. O CERURBJus é
  ferramenta do **Judiciário** (TJ-PI). Distinção que muda quem é o interlocutor.
- **Contrato TJ-PI 156/2023** com a Foxinline (R$ 1,19 mi, prorrogável até 10 anos), com **cláusula
  de sigilo vedando repasse de informações a outras empresas** e **cláusula 4.1.1** permitindo ao TJ
  autorizar uso por outros órgãos — a porta formal.
- **Termo de Referência da SEAD-PI**: a "API" do CERURB é a CERURB-WEB **interna**, sincronizada com
  o CERURB-MOBILE; integrações existentes com PJe, cartórios, Receita Federal e OAB.
- **Cláusula 3.4 do contrato**: o CERURB coleta núcleos/quadras/lotes/edificações, cadastro
  socioeconômico **com renda familiar e programas sociais**, documentos digitalizados, **shapefiles
  e memoriais descritivos**. Confirma que o dado é rico — e contratualmente fechado.
- **Lei Municipal 6.383/2026 (jul/2026)**: Teresina **já instituiu CTM + SIG + IDE na SEMPLAN**.
- **TCE-PI auditou o IPTU de Teresina; a PMT suspendeu a cobrança do IPTU 2026 para imóveis
  edificados.** Contexto político direto sobre o argumento fiscal.
- **TCE-PI tem API pública documentada** (`sistemas.tce.pi.gov.br/api/portaldacidadania/docs/`).
- **CEHURB não existe no PI** — é a companhia habitacional do Espírito Santo. No PI: ADH-PI
  (estadual), SEMDUH e ETURB (Teresina).
- **e-SIC de Teresina** operante, com prazo LAI de 15+10 dias; **não existe portal de dados abertos
  municipal** (`dadosabertos.teresina.pi.gov.br` fora do ar).
- Lista de **APIs descontinuadas** (INEP, DataSUS antiga, Atlas Brasil antigo, app SNIS) — evita
  desperdício de engenharia.
- **DataJud/CNJ** como fonte de métricas processuais de REURB.

### 1.3 Teresina tem 123 bairros oficiais; o protótipo tem 18
Catch correto. O protótipo não corresponde à divisão territorial de nenhuma base oficial.

## 2. Onde ESTA análise tem o que a outra NÃO tem

### 2.1 A reforma tributária — ausente por completo na outra análise
A outra análise **não menciona uma única vez**: LC 214/2025, CIB, SINTER, art. 256, art. 265/266,
IN RFB 2.275/2025, Portaria ASCIF 6/2022, Roteiro Técnico CADURB, NT CNM 05/2025, PROFISCO III.

Isso é a lacuna mais séria dela, porque é o que transforma o projeto de "dashboard opcional" em
**obrigação legal com prazo (01/01/2027), formato de saída normatizado, e financiamento carimbado**.
Sem esse eixo, o plano dela ("Fase 1: dashboard sobre bases públicas") é um produto sem prazo, sem
comprador obrigado e sem recorrência — exatamente a commodity que a Geopixel já vende.

### 2.2 Dimensionamento econômico do mercado — ela não tem nenhum número
Medi os **224 municípios do PI** via SICONFI:
- **Mediana de IPTU: R$ 2.214/ano.** 194 de 224 abaixo de R$ 100 mil. Só 9 acima de R$ 1 mi.
- **RCL mediana: R$ 45,7 mi** → um contrato de R$ 50 mil é 0,11% da receita.

Isso define o que é vendável e a que preço. A outra análise não tem preço, ticket, LTV, veículo de
contratação nem dimensionamento de mercado — o plano dela termina em "Fase 3", sem modelo de negócio.

### 2.3 Escala real da Foxinline
Mapeei por Certificate Transparency: **307 subdomínios**, ~**236 tenants municipais** em PI, CE, PE,
PA e MA, ~33 cartórios, arquitetura multi-tenant. A outra análise lista ~6 clientes documentados.
A diferença muda a avaliação de risco competitivo: não é uma startup local, é incumbente regional.

Também encontrei os microserviços **`api-exportacao`**, `api-cerurbjus-integracao`,
`api-cerurb-relatorioprocesso`, `api-mapa`, `api-autenticacao` — vivos no mesmo IP AWS. A conclusão
dela ("não existe API") está certa quanto a *API pública*; a minha é mais precisa: **a camada existe
e não é pública**, o que muda o pedido de "nos mande CSV" para "emita credencial".

### 2.4 Concorrência nacional — ausente na outra análise
**Geopixel** (+100 municípios) vende o **"Observatório Municipal de Informações"**, que é
literalmente o produto da Fase 1 dela. Também: Geosite CTM, GeoOne, SQLINK, Terracore, Eixo.
Um plano que propõe como fase 1 um produto que um incumbente já vende para 100 municípios precisa
dizer isso.

### 2.5 Prova quantitativa da defasagem fiscal
79.985 transações reais (ITBI Fortaleza): **valor venal = 31% do preço de mercado**, defasagem
mediana de ~69%.

### 2.6 Modelo comercial e jurídico
Veículo de contratação (dispensa até ~R$ 59 mil; contrato de eficiência art. 119 da Lei 14.133),
preço, LTV (R$ 145–200 mil/município), necessidade de **ART de avaliador** para o valor de
referência, aceite objetivo (**remessa aceita pelo CADURB**), método defensável perante TCE
(regressão hedônica espacial com coeficientes declarados, não caixa-preta).

## 3. Onde a OUTRA análise erra

### 3.1 "Nenhuma base pública tem valor venal por imóvel" — incorreto
**Fortaleza** publica ITBI em dados abertos com `VL_VENAL`, `VL_BASE_CALCULO` (preço da transação),
`VL_LANCAMENTO_IPTU`, coordenadas SIRGAS 2000, área do terreno, área edificada, padrão de
construção, tipologia, zoneamento e data. **São Paulo** publica desde 2019. Isso é base de treino
pronta para avaliação em massa — e ela concluiu o oposto ("manter PGV como módulo condicionado"),
provavelmente por ter limitado a busca ao Piauí.

### 3.2 "Censo 2022 divulga agregados por bairro e setor, incluindo renda" — impreciso
Verificado: **não existe arquivo de renda nos agregados por bairro.** O rendimento está em pasta
separada e **apenas por setor censitário**
(`Agregados_por_Setores_Censitarios_Rendimento_do_Responsavel/`). Como o setor é mais fino que o
bairro, o resultado é alcançável agregando setor→bairro — mas o caminho descrito está errado, e
renda é o indicador central do painel de vulnerabilidade.

### 3.3 O plano não tem preço, prazo contratual, nem critério de aceite
"Fase 1 — imediato", "Fase 2 — o diferencial", "Fase 3 — ML/chat" não é plano executável: não há
esforço estimado, ticket, marco de aceite nem quem paga.

## 4. O que NENHUMA das duas análises tinha — e é o achado mais prático

### As características urbanísticas do entorno, por face de quadra, agregadas por bairro

`ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios_Caracteristicas_urbanisticas_do_entorno_dos_domicilios/`
— disponível por **Bairro, Distrito, SubDistrito, Município e Setor**, com dicionário de dados.

Temas medidos **por face de quadra** (11):

| Tema | Resolve |
|---|---|
| **VIA PAVIMENTADA** (sim/não) | **"Pavimentação por bairro"** |
| **ILUMINAÇÃO PÚBLICA** (sim/não) | **"Iluminação pública por bairro"** |
| **BUEIRO** (sim/não) | drenagem urbana |
| CALÇADA / OBSTÁCULO NA CALÇADA / RAMPA PARA CADEIRANTE | acessibilidade |
| CIRCULAÇÃO DA VIA (caminhão/ônibus, carro, pedestre, aquavia) | hierarquia viária, acesso |
| PONTO DE ÔNIBUS | mobilidade |
| ARBORIZAÇÃO (0, 1–2, 3–4, 5+ árvores) | ambiental / ilha de calor |
| VIA SINALIZADA PARA BICICLETA | mobilidade ativa |

**Impacto direto na matriz de fontes do cliente:** a
`matriz-responsabilidade-fontes-dados.md` classifica **pavimentação** (item 3) como dependente da
Secretaria de Obras — "prioridade média-alta", exigindo malha viária georreferenciada — e
**iluminação pública** (item 5) como dependente da Secretaria de Serviços Urbanos ou da
concessionária, "prioridade baixa-média, segunda fase".

**Os dois estão disponíveis como dado aberto, por bairro, hoje, sem nenhum ofício.**
Isso elimina 2 das 5 negociações institucionais da matriz e antecipa indicadores que estavam
previstos para a "segunda fase".

### E também: `Favelas_e_comunidades_urbanas_Resultados_do_universo/` (com `arquivos_vetoriais/`)
O IBGE delimitou e caracterizou favelas e comunidades urbanas no Censo 2022, **com geometria
vetorial**. Esse é, conceitualmente, o universo dos **núcleos urbanos informais** da REURB. É a
camada que permite dimensionar o mercado de regularização por município, com geometria, antes de
qualquer contato.

## 5. Síntese

As duas análises são **complementares, não concorrentes**, e cada uma tem um erro material que a
outra corrige:

| Eixo | Melhor fonte |
|---|---|
| Contexto institucional local (TJ-PI, ETURB, SEMPLAN, contratos, e-SIC) | **outra análise** |
| Granularidade por bairro | **outra análise** (eu errei) |
| Prova documental do contrato e da vedação de repasse | **outra análise** |
| Reforma tributária, CIB/SINTER, prazo, financiamento | **esta análise** |
| Dimensionamento de mercado e modelo comercial | **esta análise** |
| Escala e arquitetura do concorrente | **esta análise** |
| Concorrência nacional | **esta análise** |
| Prova quantitativa da defasagem fiscal | **esta análise** |
| Entorno urbanístico por bairro; favelas com geometria | **nenhuma das duas — novo** |

**Convergência central (as duas chegaram ao mesmo lugar por caminhos diferentes):** não construir o
produto sobre extração de dados do CERURB; começar por dado público; e ter coleta própria como
independência estratégica. Essa conclusão está agora duplamente confirmada, por duas investigações
independentes — o que aumenta bastante a confiança nela.

**Divergência a resolver:** o que é a Fase 1. A outra análise diz "dashboard sobre bases públicas".
Esta diz "conformidade CIB com prazo legal". A diferença importa: dashboard é commodity que a
Geopixel já vende para 100+ municípios e que o município compra por vontade; conformidade é
obrigação com data marcada, formato normatizado e dinheiro carimbado. **A recomendação é usar o
dashboard como a *entrega visível* e a conformidade como a *razão de compra*.**
