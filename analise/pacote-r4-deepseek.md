# Rodada 4 — FINAL. Eixo técnico. Fatos novos que corrigem suas rodadas anteriores.

Três correções ao que você respondeu antes:

1. **Você errou no Achado 3 da Rodada 1 (e eu te induzi ao erro):** disse que a granularidade pública
   para em município/setor e que "prometer bairro é vender ficção". **FALSO.** O Censo 2022 publica
   `Agregados_por_Bairro` — 17.576 bairros no Brasil, 123 em Teresina (Anexo 2, correção 1).
2. **Existe dado público de PAVIMENTAÇÃO e ILUMINAÇÃO por bairro** (Censo 2022, entorno urbanístico
   por face de quadra: V05406, V05412, V05409 sobre V05400). Extraí para os 123 bairros de Teresina
   (Anexo 2, correção 4; Anexo 3 seção 9).
3. **Existe base pública de valor venal + preço de transação por imóvel, georreferenciada**
   (ITBI Fortaleza e São Paulo) — serve de base de treino para avaliação em massa (Anexo 5).

E dois contextos novos: o mercado-alvo é **Piauí** (mediana de IPTU R$ 2.214/ano, 194 de 224
municípios abaixo de R$ 100 mil — Anexo 1); e o protótipo tem dados fictícios que **contradizem a
realidade** de forma detectável (diz que Mocambinho tem 36% de pavimentação; o real é 99,6% —
Anexo 3, seção 4).

Responda no máximo 6 achados, só o que muda:

1. Com bairro, pavimentação, iluminação e favelas-com-geometria disponíveis em dado aberto, **qual é
   agora o escopo técnico da v1** e em quanto tempo ela fica de pé? Refaça seu plano do Anexo 7.
2. O protótipo deve ser repopulado com dado real, reescrito do zero, ou descartado? Justifique
   tecnicamente e diga o que fazer com cada uma das 11 telas (Anexo 3).
3. **Metodologia do índice de vulnerabilidade (`iv`)**: proponha uma fórmula concreta, com as
   variáveis do Censo por bairro que existem hoje, pesos e como torná-la auditável/publicável.
   Esse é o item de maior risco contratual (Anexo 3, seção 3).
4. Renda só existe por setor censitário, e o painel é por bairro. Qual o método correto de agregar
   setor→bairro, e qual erro isso introduz? Como declarar isso honestamente.
5. Com a base ITBI de Fortaleza como treino e o alvo sendo municípios do Piauí (mercado muito
   diferente), **transferir modelo entre municípios é defensável?** Se não, o que fazer no PI, onde
   os municípios não publicam ITBI?
6. Arquitetura final: o que construir, em que ordem, e o que é reutilizável entre municípios.

# ANEXO 1 — RECORTE PIAUÍ (dimensionamento real do mercado-alvo)

# Recorte Piauí — o dimensionamento que corrige os dois pareceres

O go-to-market definido pelo cliente é **Piauí primeiro, depois Ceará e Maranhão**. Ambos os
pareceres (Anexos E e F) foram escritos sobre um mercado genérico de 5.570 municípios. Medi o
mercado real do PI com dado público. **Os números mudam o modelo comercial.**

## 1. Arrecadação de IPTU nos 224 municípios do Piauí (SICONFI, 2025, 12 meses móveis)

Consultei os **224 municípios**, obtive retorno para **224**.

| Posição | Município | IPTU 2025 | População | R$/hab |
|---|---|---|---|---|
| 1 | **Teresina** | R$ 166.321.115 | 868.523 | 191,50 |
| 2 | Picos | R$ 7.062.110 | 82.028 | 86,09 |
| 3 | Parnaíba | R$ 4.161.751 | 163.087 | 25,52 |
| 4 | São Raimundo Nonato | R$ 1.675.238 | 39.036 | 42,92 |
| 5 | Piripiri | R$ 1.533.757 | 65.762 | 23,32 |
| 6 | Floriano | R$ 1.208.395 | 62.593 | 19,31 |
| 7 | Oeiras | R$ 1.099.628 | 38.192 | 28,79 |
| 8 | Campo Maior | R$ 1.043.286 | 45.252 | 23,06 |
| 9 | Bom Jesus | R$ 1.022.221 | 28.857 | 35,42 |

### A distribuição é o achado

| Métrica | Valor |
|---|---|
| **Mediana de IPTU no PI** | **R$ 2.214,26 por ano** |
| Municípios com IPTU < R$ 100 mil/ano | **194 de 224** |
| Municípios com IPTU < R$ 500 mil/ano | **212 de 224** |
| Municípios com IPTU > R$ 1 mi/ano | **9 de 224** |

A mediana não está em milhares: o município mediano do Piauí arrecada **dois mil duzentos reais por
ano** de IPTU. Teresina sozinha responde por mais que todos os outros 223 somados.

## 2. Consequência 1 — o fee de eficiência sobre IPTU NÃO funciona no Piauí

O parecer de negócio (Anexo F, Achado 4; Anexo G, Achado 6) propõe remuneração de **10–15% sobre o
incremento de IPTU acima do baseline SICONFI**, com exemplo de município com IPTU₀ = R$ 20 mi.

**No Piauí, esse município praticamente não existe.** Só Teresina e Picos passariam perto. Num
município com IPTU de R$ 2 mil/ano, 15% de um incremento de 100% são **R$ 300**. O modelo de
eficiência é matematicamente inaplicável a 212 dos 224 municípios do estado.

**Correção:** no beachhead PI, a remuneração tem de ser **preço fixo**. O fee de eficiência fica
reservado a Teresina, Picos, Parnaíba e às capitais de CE e MA (Fortaleza, São Luís) — onde a base
existe.

## 3. Consequência 2 — "aumentar a arrecadação do IPTU" é o argumento errado no interior do PI

A proposta original tem como objetivo declarado aumentar a arrecadação de IPTU. No interior do
Piauí **não há IPTU a aumentar** — e há uma razão política que nenhum modelo resolve: prefeito de
município pequeno **não vai instituir cobrança efetiva de IPTU sobre eleitor de baixa renda**. Vender
recuperação fiscal ali é vender um problema, não uma solução.

**O argumento que funciona no PI é outro: conformidade legal obrigatória.** O CIB vence em
**01/01/2027** para os 224 municípios, independentemente de quanto cada um arrecada. É dever legal,
não oportunidade de receita.

## 4. Consequência 3 — mas a capacidade de pagamento EXISTE, e isso salva a tese

Consultei a Receita Corrente Líquida dos mesmos municípios (152 com retorno):

| Métrica | RCL 2025 |
|---|---|
| **Mediana** | **R$ 45.747.394** |
| p25 / p75 | R$ 35.427.582 / R$ 69.241.799 |

| Ticket | % da RCL mediana |
|---|---|
| R$ 8.000 (adesão SINTER) | 0,017% |
| R$ 15.000 | 0,033% |
| R$ 50.000 (diagnóstico) | 0,109% |
| R$ 58.800 | 0,129% |
| R$ 36.000/ano (P2 anual) | 0,079% |

**O município piauiense mediano tem R$ 45,7 milhões de receita corrente e arrecada R$ 2,2 mil de
IPTU.** O dinheiro vem de FPM, Fundeb e transferências — não de tributo próprio. Um contrato de
R$ 50 mil é **um milésimo** da receita dele.

**Ou seja: os tickets propostos pelo parecer de negócio são pagáveis no Piauí. O que não se sustenta
é a *justificativa* baseada em retorno de IPTU.** O ordenador de despesa precisa comprar
**cumprimento de prazo legal**, e a fonte é orçamento corrente ou PROFISCO III — nunca a promessa de
receita futura de IPTU.

## 5. Consequência 4 — o alerta do parecer sobre o beachhead

O parecer de negócio (Anexo G, Achado 5) recomenda explicitamente **começar fora do Piauí**, porque o
PI é o quintal da Foxinline (~236 tenants, Anexo D). O cliente decidiu o contrário, e há razões
legítimas para isso: relação comercial existente, proximidade, conhecimento do território e o canal
da REURB.

**A decisão é do cliente e é defensável — mas o custo dela precisa estar explícito:** disputar o PI é
disputar onde o incumbente já está instalado, com o argumento fiscal enfraquecido pela ausência de
IPTU. As duas compensações reais são: (a) o canal da REURB, que a Foxinline **não** tem do lado do
serviço de campo do cliente; e (b) o fato de que estar instalado com o sistema de REURB **não**
significa estar instalado com conformidade CIB — que é produto novo para todo mundo.

## 6. Mercado endereçável, por segmento, no beachhead

| Segmento | Nº municípios (PI) | Produto | Ticket |
|---|---|---|---|
| **A — tese fiscal completa** | ~9 (Teresina, Picos, Parnaíba, S. R. Nonato, Piripiri, Floriano, Oeiras, Campo Maior, Bom Jesus) | diagnóstico + PGV + eficiência | alto; fee de eficiência viável |
| **B — conformidade CIB pura** | ~215 | adesão SINTER + remessa CADURB, padronizado e automatizado | baixo (R$ 8–25 mil), volume |
| **C — expansão** | CE (184) + MA (217) | mesmo playbook | após validar B |

O segmento B só fecha conta se for **produto automatizado e replicável**, não serviço sob medida —
com 215 municípios a R$ 15 mil e margem alta, o negócio existe; com 215 projetos artesanais, não.

# ANEXO 2 — ACHADOS DA ANÁLISE PARALELA + CORREÇÕES FACTUAIS

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

# ANEXO 3 — AUDITORIA DO PROTÓTIPO HTML

# Auditoria do protótipo `painel-gestao-municipal (1).html`

43.163 bytes, sendo 18.721 de JavaScript. Auditado campo a campo e confrontado com dado real.

## 1. Estrutura

11 telas: Painel principal, Mapa territorial, Ranking de bairros, Saneamento, Pavimentação,
Educação, Perfis socioeconômicos, Simulador de investimento, Séries históricas, Status CERURB,
Relatórios exportáveis.

Funções existentes — **todas de apresentação**: `buildMiniMap`, `renderBigMap`, `buildRankMini`,
`colorFor`, `colorForInverse`, `fmtPct`, `prioTag`, `goToPage`, `runSimulation`, `xFor`, `yFor`.
**Nenhuma função de cálculo de indicador.**

## 2. O modelo de dados: 18 registros, 17 campos

```
{nome, iv, saneamento, pavimentacao, evasao, escolas, distEscola, matriculas,
 familias, renda, moradores, idosos, criancas, posse, pendentes, analise, regularizados}
```

| Campo | Domínio no protótipo |
|---|---|
| `iv` (índice de vulnerabilidade) | 9 a 88 — **sem fórmula em lugar nenhum** |
| `saneamento` | 24% a 96% |
| `pavimentacao` | 31% a 96% |
| `evasao` | 1,9% a 14,2% |
| `renda` | "até 1 SM", "1–2 SM", "2–3 SM", "3+ SM" |
| `posse` | Posseiro, Proprietário, Proprietário informal, Cessão |
| `idosos`, `criancas` | booleanos (!) |
| `familias` | 40 a 212 |
| `pendentes` / `analise` / `regularizados` | 0–64 / 1–60 / 39–90 |

## 3. Problema 1 — o indicador central não tem metodologia

O `iv` ordena o ranking, colore o mapa, define as faixas de prioridade (alta/média/baixa) e alimenta
o simulador de investimento. **Ele é um número digitado à mão.** Não há pesos, não há fontes, não há
reprodutibilidade.

Num produto que ordena prioridade de investimento público, isso é passivo contratual: basta um
vereador cujo bairro ficou em último, ou o controle interno, perguntar "como calcularam" — e não há
resposta. **Definir a metodologia do índice é item de escopo, não detalhe de implementação.**

## 4. Problema 2 — os dados fictícios contradizem a realidade, e isso é detectável na hora

Os 18 nomes **são bairros reais de Teresina**. Cruzei com a base do IBGE: **13 casam diretamente**,
2 por variante de grafia (Renascença, Horto) e **3 não são bairros oficiais** (Vila Irmã Dulce,
Vila Nova do Alto da Ressurreição, Parque Piauí) — são vilas/comunidades dentro de bairros.

Confrontando o protótipo com o dado real do Censo 2022 (entorno urbanístico por face de quadra):

| Bairro | Pavimentação no protótipo | **Pavimentação real** | Erro |
|---|---|---|---|
| Mocambinho | 36% | **99,6%** | protótipo diz que é o 2º pior; é dos melhores |
| Santa Luzia | 41% | **78,6%** | subestimado |
| Todos os Santos | — | 62,1% | — |
| Centro | — | 100,0% | — |

E os bairros **realmente** carentes de pavimentação em Teresina — Chapadinha (36,7%), Tabajaras
(36,8%), Brasilar (44,8%), Morros (46,0%), Verdecap (46,9%) — **não aparecem no protótipo.**

**Risco imediato:** qualquer gestor de Teresina que olhe esse painel reconhece que Mocambinho não é
bairro sem pavimentação. O protótipo, apresentado como está, destrói credibilidade na primeira
reunião. Ele precisa ou ser rotulado explicitamente como maquete visual, ou ser repopulado com dado
real antes de qualquer apresentação.

## 5. Problema 3 — a divisão territorial não corresponde a nenhuma base oficial

Teresina tem **123 bairros** (IBGE, Censo 2022). O protótipo usa 18, misturando bairros oficiais com
comunidades. Isso impede junção com qualquer fonte e precisa ser decidido antes de construir:
o recorte é bairro oficial (123), comunidade/núcleo informal, ou setor censitário?

## 6. Problema 4 — campos com tipo inadequado

`idosos: true/false` e `criancas: true/false` tratam presença de idosos e crianças como booleano por
bairro. Não existe bairro sem crianças. O dado correto é **proporção** (o Censo dá por bairro), e o
uso pretendido provavelmente era "concentração acima da média" — o que é outra coisa e precisa de
definição.

## 7. O que o protótipo acerta e deve ser preservado

- **A arquitetura de navegação** (11 telas) é adequada e cobre o módulo 4 da proposta.
- **A escolha de indicadores** é pertinente: saneamento, pavimentação, educação, perfil
  socioeconômico, posse e status de regularização são de fato os eixos certos.
- **O simulador de investimento e os relatórios exportáveis** são diferenciais reais frente a um
  dashboard passivo — mas o simulador precisa de modelo por trás, não de regra ad hoc.
- Como **peça comercial e especificação visual**, cumpre a função.

## 8. Veredito técnico

**O protótipo é uma maquete de interface de boa qualidade, com dados inventados que não sobrevivem
ao confronto com a realidade.** Não serve como base de código (HTML estático, array hardcoded, sem
camada de dados), mas serve como especificação de produto.

**Ação recomendada, em ordem:**
1. Repopular com dado real do IBGE por bairro — **é factível hoje**, os dados existem e foram
   baixados nesta análise (pavimentação, iluminação, bueiro, domicílios, demografia por bairro).
2. Definir e publicar a metodologia do `iv` (pesos, fontes, fórmula).
3. Substituir a grade de células por geometria real (malha de bairros do IBGE + PostGIS).
4. Adotar os 123 bairros oficiais, com camada separada para comunidades/núcleos informais.
5. Adicionar a métrica ausente e mais importante: **arrecadação** (SICONFI, já validado).
6. Até que 1–4 estejam feitos, marcar toda tela com "dados ilustrativos" de forma inequívoca.

## 9. Mapa de cada indicador do protótipo para sua fonte real

| Indicador do painel | Fonte real | Granularidade | Status |
|---|---|---|---|
| Pavimentação | **Censo 2022 — entorno, V05406/V05400** | **bairro** | ✅ pronto |
| Iluminação pública | **Censo 2022 — entorno, V05412** | **bairro** | ✅ pronto |
| Drenagem (bueiro) | Censo 2022 — entorno, V05409 | bairro | ✅ pronto (não está no protótipo) |
| Saneamento (água/esgoto) | Censo 2022 — características do domicílio | bairro | ✅ pronto |
| Densidade, moradores/domicílio | Censo 2022 — demografia/básico | bairro | ✅ pronto |
| Idosos e crianças (proporção) | Censo 2022 — demografia | bairro | ✅ pronto |
| **Renda** | Censo 2022 — Rendimento do Responsável | **só setor censitário** | ⚠️ agregar setor→bairro |
| Escolas, matrículas, distância | INEP Censo Escolar (escola geolocalizada) | ponto → bairro | ✅ pronto |
| Evasão / rendimento escolar | INEP (distorção idade-série, IDEB) | escola | ✅ pronto |
| Energia solar / GD | ANEEL (diário) | município | ⚠️ não desce a bairro |
| **Arrecadação (ausente)** | SICONFI / TCE-PI | município | ✅ validado |
| Núcleos informais / favelas | **Censo 2022 — Favelas e Comunidades Urbanas (vetorial)** | **polígono** | ✅ pronto |
| Status CERURB (regularizados/pendentes) | CERURB | imóvel | ❌ depende de acordo |
| Tipo de posse | CERURB ou coleta própria | imóvel | ❌ depende de acordo |
| Valor venal / PGV | cadastro da Fazenda municipal | imóvel | ❌ via contrato |

**Dos 15 indicadores, 11 são obteníveis hoje com dado aberto.** Só 4 dependem de acordo — e são
exatamente os do núcleo fundiário e fiscal.

# ANEXO 4 — REFORMA TRIBUTÁRIA (CIB/SINTER/art.256) E SUA RESSALVA

# Adendo 2 — a reforma tributária transforma a PGV em obrigação anual recorrente

Fonte: **Nota Técnica CTAT nº 05/2025 da CNM** ("Orientações aos Municípios sobre Sinter e CIB",
texto extraído do PDF oficial), **LC 214/2025**, **IN RFB 2.275/2025**, página oficial do CIB na
Receita Federal.

## 1. O CIB é obrigação legal com prazo, não recomendação

**LC 214/2025, art. 265:** todos os bens imóveis urbanos e rurais **deverão ser inscritos no CIB**.
O CIB **deve constar obrigatoriamente de todos os documentos relativos a obra de construção civil
expedidos pelo Município** (§2º).

**Art. 266 — prazos de inscrição:**
- **12 meses** → órgãos federais, serviços notariais e registrais, **capitais e DF** incluem o CIB
  em seus sistemas → **a partir de 01/01/2026**.
- **24 meses** → órgãos estaduais e **os demais Municípios** → **a partir de 01/01/2027**.

Formato do CIB: alfanumérico, 7 caracteres + dígito verificador (`ABC1234-5`).

## 2. O achado central: o art. 256 torna a avaliação de imóveis uma obrigação ANUAL

**LC 214/2025, art. 256** — os entes devem **divulgar e disponibilizar no SINTER o VALOR DE
REFERÊNCIA** dos imóveis, **estimado para TODOS os bens imóveis que integram o CIB** e
**ATUALIZADO ANUALMENTE**. Esse valor de referência **será utilizado no cálculo do IBS** nas
operações com bens imóveis.

A metodologia prevista no art. 256 considera: preços praticados no mercado imobiliário; informações
enviadas pelas administrações tributárias de Municípios, DF, Estados e União; informações dos
serviços registrais e notariais; e **localização, tipologia, destinação, data, padrão e área de
construção** do imóvel.

### Por que isso reposiciona o projeto inteiro

1. **A PGV deixa de ser módulo opcional e vira obrigação recorrente.** Na proposta original, a
   Planta Genérica de Valores era o módulo 3, vendável como melhoria de justiça fiscal. Com o
   art. 256, avaliar todos os imóveis e atualizar **todo ano** passa a ser dever legal ligado à
   arrecadação do IBS. "Atualizado anualmente" é a definição de assinatura recorrente.
2. **A metodologia do art. 256 é literalmente um problema de modelo estatístico** — estimar valor
   de mercado a partir de localização, tipologia, padrão e área construída, calibrado por preços
   observados. É **avaliação em massa (CAMA / mass appraisal)**. Aqui, e só aqui, machine learning
   deixa de ser enfeite de proposta e vira o método tecnicamente indicado — com a ressalva de que
   exige cadastro robusto e amostra de transações (ITBI, cartórios) para calibrar.
3. **Muda o comprador dentro da prefeitura**: sai o planejamento urbano (compra por vontade) e entra
   a Secretaria de Fazenda/Finanças (compra por prazo legal e por receita).
4. **Muda o argumento**: não é "painel bonito", é "sem isso o município perde base de cálculo do IBS
   e fica inadimplente com a LC 214".

## 3. Existe especificação técnica pública para a integração

A RFB publicou o **Roteiro Técnico de Integração ao SINTER** — especificamente o *"Roteiro
Operacional para envio de Remessa com Informações Georreferenciadas e Alfanuméricas das Unidades
Imobiliárias das Prefeituras ao Módulo Cadastro Urbano — CADURB do SINTER"* (RFB, 2023), disponível
no sítio do ENAT. O módulo aceita **envio alfanumérico puro ou alfanumérico + georreferenciado**.

Ou seja: **o formato de saída do produto já está especificado por norma federal.** Isso é raro e é
bom — elimina ambiguidade de requisito e cria um critério de aceite objetivo ("a remessa foi aceita
pelo CADURB").

## 4. Existe dinheiro carimbado para o município pagar por isso

A NT da CNM (seção 6.4, "Municípios que necessitam de recursos financeiros para implantação")
aponta o **PROFISCO III — Programa de Apoio à Gestão dos Fiscos do Brasil**, do **Ministério da
Fazenda em parceria com o BID**, linha de crédito disponível para **municípios**, desenhada em
grande parte para apoiar a operacionalização da Reforma Tributária.

**Consequência:** a objeção "a prefeitura não tem orçamento" tem resposta pronta e oficial. Ajudar o
município a acessar o PROFISCO III é, em si, parte da venda.

## 5. O caminho de adesão é burocrático e conhecido — e isso é oportunidade de serviço

A NT descreve **16 passos** de adesão: Termo de Adesão ao Convênio SINTER assinado com certificado
digital ICP-Brasil → processo digital no e-CAC da RFB → "Celebração de Acordos Nacionais" → "Aderir
ao Convênio Sinter de 15/12/2022" → juntada de documentos → **publicação do Termo no DOU** → só
então o município pode enviar suas bases conforme o Roteiro Técnico. Normativo de referência:
**Portaria ASCIF nº 6, de 15/12/2022**.

Nenhuma prefeitura pequena tem equipe para conduzir isso. **A condução da adesão é um produto de
entrada barato, de ciclo curto, que cria o relacionamento e a dependência técnica antes da venda
grande.**

---

## 6. RESSALVA IMPORTANTE — uma ambiguidade que precisa ser confirmada antes de virar tese de venda

A leitura da seção 2 acima ("a PGV vira obrigação anual do município") **é a interpretação otimista,
e ela tem um contraponto sério que não pode ser ignorado.**

O art. 256 da LC 214/2025 diz que o valor de referência é apurado **"pelas administrações
tributárias"** — no plural e sem especificar qual ente —, considerando preços de mercado,
informações enviadas pelas administrações tributárias **dos Municípios, do DF, dos Estados e da
União**, e informações **dos serviços registrais e notariais**.

E a **IN RFB nº 2.275, de 15/08/2025**, obriga os **serviços notariais e de registro a compartilhar
as informações das operações imobiliárias via SINTER**.

**O contraponto:** se a RFB passa a receber de cartório o preço de todas as transações imobiliárias
do país, ela tem, centralizadamente, a melhor amostra de calibração que existe — e pode apurar o
valor de referência **ela mesma**, sem que cada município precise contratar avaliação em massa.
Nesse cenário, a obrigação municipal é **enviar dados cadastrais**, não **produzir avaliação**, e a
tese de "PGV anual como assinatura recorrente" enfraquece bastante.

### Como isso muda o que se pode afirmar

- **Não afirmar, ainda, que o município é obrigado a contratar avaliação em massa anual.** Isso
  precisa ser confirmado na IN e no Roteiro Técnico antes de entrar em qualquer proposta.
- **O que se pode afirmar com segurança**, independentemente de quem apura:
  1. O município é obrigado a **inscrever todos os imóveis no CIB** e a **enviar seus dados
     cadastrais** ao SINTER (art. 265/266) — isso não é ambíguo.
  2. Se a RFB publicar um valor de referência **acima do valor venal da PGV municipal**, a defasagem
     fica **visível e auditável** — pelo TCE, pelo Ministério Público e pela imprensa. A pressão
     política e jurídica para o município atualizar a PGV vira consequência quase automática.
     **O efeito é indireto, mas é forte, e talvez mais forte que a obrigação direta:** o município
     não vai poder mais alegar que não sabia da defasagem.
  3. A PGV continua sendo competência municipal para fins de **IPTU e ITBI**, independentemente do
     IBS.

**Conclusão prática:** a recorrência do negócio provavelmente existe, mas por um mecanismo diferente
do que a seção 2 sugere — não por obrigação direta de avaliar, e sim por **exposição da defasagem**.
Isso é uma tese de venda melhor (o município reage a um número publicado pela Receita), mas é uma
tese diferente, e o time precisa saber qual das duas está usando.

**Item obrigatório de due diligence antes de qualquer proposta:** ler a íntegra da IN RFB 2.275/2025
e obter o Roteiro Técnico do CADURB. Registro relevante: **o Roteiro Técnico NÃO é público** — a
tentativa de baixá-lo do sítio do ENAT retorna conteúdo restrito, e a NT da CNM confirma que ele é
"enviado aos Gestores (do Convênio e de TI) indicados no requerimento", isto é, **só após a adesão
do município ao convênio**. Isso reforça o valor de entrar pelo serviço de condução da adesão: é o
que dá acesso à especificação.

# ANEXO 5 — PROVA DE CONCEITO E DEFASAGEM FISCAL

# Prova de conceito — executada em 2026-09-15, com dados reais

Não é estimativa nem promessa: são chamadas reais, feitas agora, a APIs públicas, sem credencial,
sem contrato e sem contato com nenhuma prefeitura ou fornecedor.

## Série de arrecadação de IPTU — Teresina (IBGE 2211001)
Fonte: SICONFI / Tesouro Nacional, `apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo`,
RREO Anexo 03, 6º bimestre, soma dos 12 meses móveis.

| Exercício | IPTU (12 meses móveis) | Variação |
|---|---|---|
| 2021 | R$ 111.185.334,24 | — |
| 2022 | R$ 113.795.928,55 | +2,3% |
| 2023 | R$ 141.352.685,04 | +24,2% |
| 2024 | R$ 139.369.320,66 | −1,4% |
| 2025 | R$ 166.321.115,49 | +19,3% |

## O que isso prova, concretamente

1. **A métrica que falta no protótipo é a mais fácil de obter.** O painel atual não tem nenhuma
   métrica de arrecadação — que é o objetivo declarado da proposta ("aumentar a arrecadação do
   IPTU"). Ela estava a uma chamada HTTP de distância, para **qualquer um dos 5.570 municípios**.
2. **Dá para dimensionar a oferta antes da primeira reunião.** Aplicando os ganhos documentados de
   recadastramento + PGV à base real de Teresina de 2025 (R$ 166,3 mi):
   - cenário conservador **+23%** (caso Amparo/SP) → **+R$ 38,3 mi/ano**
   - cenário intermediário **+86,6%** (caso Santana de Parnaíba/SP) → **+R$ 144,0 mi/ano**

   *Ressalva honesta e obrigatória:* esses percentuais vêm de municípios com cadastro muito
   defasado; Teresina é capital e já cresceu 19,3% em 2025, então o ganho marginal tende a ser
   bem menor. O número serve para **dimensionar a conversa**, não para ir numa proposta como
   promessa. Em município pequeno com cadastro dos anos 90, o potencial é comparativamente maior.
3. **O mesmo pipeline roda para qualquer município**, trocando um código IBGE — o que é a definição
   de produto replicável, e não de consultoria sob medida.

## Demais endpoints validados na mesma sessão
| Chamada | Status |
|---|---|
| `servicodados.ibge.gov.br/api/v1/localidades/municipios/2211001` | 200, JSON completo |
| `servicodados.ibge.gov.br/api/v3/malhas/municipios/2211001?formato=application/vnd.geo+json` | 200, GeoJSON |
| SICONFI RREO Anexo 02 (receitas detalhadas) | 200, 1.065 itens |
| ANEEL CKAN `package_show` (geração distribuída) | 200, CSV + **Parquet** + dicionário |
| IBGE SIDRA v3 `/agregados` | **timeout** — instável; usar como fonte secundária, nunca crítica |

---

## Auditoria do protótipo HTML entregue

Análise do arquivo `painel-gestao-municipal (1).html` (43.163 bytes, 18.721 deles de JavaScript):

- Os dados são um **array literal hardcoded de 18 bairros** fictícios de Teresina
  (`const bairros = [{nome:"Vila Irmã Dulce", iv:88, saneamento:24, ...}]`).
- As funções existentes são todas de apresentação: `buildMiniMap`, `renderBigMap`, `colorFor`,
  `colorForInverse`, `fmtPct`, `prioTag`, `goToPage`, `runSimulation`.
- **Não há nenhuma função que calcule o `iv`** — o "índice de vulnerabilidade", que é o indicador
  central de todo o painel e ordena o ranking, é um **número digitado à mão**, sem fórmula, sem
  pesos, sem fonte.

**Duas consequências:**
1. Como artefato técnico, o protótipo é uma **maquete de interface**, não um protótipo funcional.
   Serve como especificação visual e como peça comercial; não serve como base de código.
2. Como risco, o `iv` sem metodologia é **passivo contratual**. Um índice que ordena prioridade de
   investimento público precisa de metodologia publicável e defensável (pesos declarados, fontes
   declaradas, reprodutibilidade) — senão, no primeiro questionamento do controle interno, do TCE
   ou de um vereador cujo bairro ficou em último, o produto inteiro perde credibilidade.
   **Definir a metodologia do índice é item de escopo, não detalhe.**

---

## Fonte extra validada: MUNIC/IBGE como motor de qualificação comercial

Baixei e inspecionei as bases da **Pesquisa de Informações Básicas Municipais (MUNIC)** direto do
FTP do IBGE (`ftp.ibge.gov.br/Perfil_Municipios/`), edições disponíveis de 2001 a 2024.

- **MUNIC 2023** (`Base_MUNIC_2023.xlsx`, 23 MB): temática — assistência social, segurança, primeira
  infância, mulheres. **Não** traz cadastro imobiliário.
- **MUNIC 2021** (`Base_MUNIC_2021_20240425.xlsx`, 19 MB): traz a aba *"Legislação e instrumentos de
  planejamento"*, com as variáveis: **legislação sobre regularização fundiária**, plano diretor
  (existência e se está em elaboração), lei de perímetro urbano, legislação sobre parcelamento do
  solo, zoneamento/uso e ocupação do solo, outorga onerosa, e *cadastro pré-existente
  municipal/estadual/federal*.

**Uso comercial direto:** cruzar essas variáveis dá uma **lista nacional de municípios qualificados**
— os que têm legislação de regularização fundiária (logo, demanda de REURB) mas não têm plano
diretor nem cadastro estruturado (logo, não têm como cumprir o CIB até 01/01/2027). Isso é
prospecção baseada em dado público, feita antes de qualquer contato comercial, para os 5.570
municípios. O bloco específico de *cadastro imobiliário e Planta Genérica de Valores* aparece em
edições mais antigas da MUNIC (2015) — útil como proxy de defasagem, com a ressalva da idade do dado.

---

## Dados de energia (pergunta específica: fotovoltaica, geração distribuída)

Dataset ANEEL *"Relação de empreendimentos de Mini e Micro Geração Distribuída"*, via API CKAN:

| Recurso | Tamanho |
|---|---|
| `empreendimento-geracao-distribuida.parquet` | 105,6 MB |
| `empreendimento-gd-informacoes-tecnicas-fotovoltaica.parquet` | 109,8 MB |
| `...-termeletrica.csv` / `-hidreletrica.csv` / `-eolica.csv` | 8–48 KB |

Esquema verificado no CSV pequeno: `DatGeracaoConjuntoDados`, **`CodGeracaoDistribuida`** (chave, ex.
`GD.AL.000.842.763`), `MdaPotenciaInstalada`, `DatConexao`, e campos técnicos por fonte. O dataset
principal traz ainda **município, UF, titular, classe de produção, subgrupo, distribuidora e
quantidade de UCs que recebem créditos**.

**`DatGeracaoConjuntoDados` = 2026-09-15** — ou seja, o conjunto é regenerado **diariamente**.

**Viabilidade:** alta e imediata, sem negociação. Dá para produzir por município a série de adesão à
geração distribuída, potência instalada acumulada, e perfil (residencial × comercial × rural).
**Limite honesto:** a granularidade é **município**, não bairro nem lote — só desce a endereço se
cruzado com cadastro próprio. Não use isso para prometer mapa de telhado solar por quadra.

**Nota de ambiente:** esta máquina não tem `pandas`, `pyarrow`, `duckdb`, `geopandas` nem `openpyxl`
instalados. Processar os Parquet de ~100 MB exige montar o ambiente analítico primeiro — é item de
setup do projeto, não obstáculo.

# Prova quantitativa: a defasagem que o SINTER vai expor — medida hoje, com dado público

Executado em 2026-09-15. **79.985 transações imobiliárias reais analisadas.** Nenhuma negociação,
nenhuma credencial, nenhum contrato.

## A fonte

**Portal de Dados Abertos de Fortaleza** — dataset *"Imposto sobre Transmissão de Bens Imóveis
(ITBI)"*, via API CKAN: *"Relação de transações imobiliárias com recolhimento de ITBI, contendo a
geolocalização e características dos imóveis e informações sobre as operações."*

O esquema é, quase literalmente, a lista de atributos que o **art. 256 da LC 214/2025** manda
considerar na apuração do valor de referência:

| Campo | Papel na avaliação em massa |
|---|---|
| `XSIRGAS2000`, `YSIRGAS2000` | **localização** (coordenada projetada, SIRGAS 2000) |
| `AREA_TERRENO`, `AREA_EDIFICADA`, `FRACAO_IDEAL` | **área** |
| `DATA_CONSTRUCAO`, `NUMERO_PAVIMENTOS`, `QTD_FRENTES` | idade e forma |
| `TIPO_USO_IMOVEL`, `PADRAO_CONSTRUCAO`, `TIPO_TERRENO` | **tipologia, destinação, padrão** |
| `NOME_ZONEAMENTO`, `BAIRRO`, `CEP` | contexto urbano |
| `DATA_DA_TRANSACAO_ITBI` | **data** |
| **`VL_BASE_CALCULO`** | **o alvo: preço praticado no mercado** |
| **`VL_VENAL`**, `VL_LANCAMENTO_IPTU` | o que a prefeitura usa hoje |

Ou seja: **existe base de treino pública, georreferenciada e com variável-resposta** para construir e
validar um modelo de avaliação em massa — sem precisar de contrato com nenhuma prefeitura.

## O resultado

Razão entre **valor venal** (o que a prefeitura usa) e **valor de transação** (o que o mercado pagou):

| Estatística | Valor |
|---|---|
| Mediana | **30,8%** |
| Média | 32,8% |
| p10 / p90 | 1,3% / 54,0% |

**O valor venal em Fortaleza corresponde à mediana de ~31% do preço de mercado observado —
uma defasagem mediana de ~69%.**

Dispersão por bairro (apenas bairros com ≥40 transações):

| Extremo | Bairro | Venal / mercado | n |
|---|---|---|---|
| Maior defasagem | Guajeru | 0,6% | 475 |
| | Barroso | 0,9% | 1.020 |
| | Carlito Pamplona | 1,3% | 1.091 |
| | Antônio Bezerra | 1,5% | 871 |
| Menor defasagem | Mucuripe | 43,0% | 1.199 |
| | Vicente Pinzon | 42,8% | 914 |
| (anomalia) | Parque Manibura | 106,3% | 623 |

## Ressalvas metodológicas — obrigatórias antes de usar este número

1. **A cauda inferior é suspeita de qualidade de dado, não de defasagem real.** Razões de 0,6% a 2%
   provavelmente indicam registros onde o `VL_VENAL` está zerado, desatualizado ou refere-se apenas
   ao terreno, não ao conjunto terreno+edificação. **Não usar o p10 em material comercial.** A
   mediana (30,8%) é a estatística robusta e é a que deve ser citada.
2. **Parque Manibura a 106%** indica o problema inverso (venal acima do declarado) e reforça que há
   ruído nos dois sentidos.
3. **O ITBI é subdeclarado.** O preço declarado tende a ser menor que o preço real, o que significa
   que a defasagem verdadeira é **ainda maior** que a medida — a estimativa é conservadora.
4. Defasagem de valor venal **não converte linearmente em aumento de IPTU**: há alíquotas,
   isenções, limites legais de majoração e o princípio da anterioridade. É indicador de *base de
   cálculo desatualizada*, não uma promessa de receita.
5. A análise cobre a amostra lida (~25 MB do CSV, 88.696 linhas); a base completa é maior.

## Por que isso é a peça central do argumento

A ressalva do documento `02-adendo-reforma-tributaria.md` (seção 6) dizia que talvez não seja o
município quem apura o valor de referência — pode ser a Receita Federal, com os dados de cartório
que a **IN RFB 2.275/2025** passou a exigir.

**Este resultado mostra que, para o negócio, tanto faz quem apura.** Quando o valor de referência de
mercado for publicado no SINTER ao lado do valor venal municipal, a diferença fica visível,
auditável e atribuível — para o TCE, o Ministério Público, a imprensa e a oposição na Câmara. Em
Fortaleza, essa diferença é da ordem de **3 vezes**.

O produto não é "um painel". É: **"medimos sua defasagem antes que a Receita Federal a publique, e
entregamos o plano para fechá-la."** Isso é vendável hoje, com dado público, para qualquer município
que publique ITBI — e é vendável com mais urgência ainda para os que não publicam, porque eles não
fazem ideia do tamanho do próprio buraco.

## Replicabilidade
São Paulo publica transações com ITBI desde 2019; Fortaleza publica com geolocalização. O mesmo
pipeline roda em qualquer município com portal de dados abertos, e o resultado é um número em reais
específico daquele município — obtido **antes da primeira reunião comercial**.

# ANEXO 6 — CERURB: STACK, APIs E ESCALA DO CONCORRENTE

# Adendo — achados que corrigem a Rodada 1

Obtidos por reconhecimento passivo (Certificate Transparency via crt.sh, DNS, HTTP HEAD em
superfície pública, sem autenticação) e por teste direto das APIs públicas.

## A. CORREÇÃO GRAVE: o CERURB TEM camada de API. Ela só não é pública.

Certificate Transparency de `*.foxinline.com` revelou **307 nomes únicos**, entre eles **subdomínios
de API dedicados**:

| Host | DNS | HTTP na raiz | Leitura |
|---|---|---|---|
| `api-exportacao.foxinline.com` | 54.161.19.184 (AWS) | **404** | serviço vivo, rota raiz inexistente |
| `api-cerurbjus-integracao.foxinline.com` | 54.161.19.184 | **502** | serviço registrado, backend fora agora |
| `api-cerurb-relatorioprocesso.foxinline.com` | 54.161.19.184 | **502** | idem |
| `api-mapa.foxinline.com` | 54.161.19.184 | 404 | vivo |
| `api-autenticacao.foxinline.com` | 54.161.19.184 | 404 | vivo |
| `apimapacerurbproprod.foxinline.com` | 54.161.19.184 | 404 | vivo, sufixo "prod" |
| `api-memorial`, `api-spi`, `api-secrel` | mesmo IP | — | demais microserviços |

**Consequência direta:** a conclusão "não há API, logo scraping ou CSV" está ERRADA.
Existe **`api-exportacao`** e existe **`api-...-integracao`**. O pedido à Foxinline deixa de ser
"nos manda um CSV toda semana" e passa a ser **"emita credencial e contrato de uso da API de
exportação já existente"**. Isso é um pedido tecnicamente trivial para eles — o que desloca a
negociação de capacidade técnica para **vontade comercial**. O gargalo é político, não técnico.

## B. CORREÇÃO GRAVE: a Foxinline não é frágil. É incumbente regional.

Dos 307 nomes: **~33 cartórios/ofícios** (1º e 2º ofícios de Teresina, Parnaíba, Luís Correia,
Piracuruca, Corrente, Simplício Mendes, Cocal, União, Altos, Crato, Russas, Barras, Petrolândia,
Serra Talhada, Surubim, Tacaratu, Ibimirim…) e **~236 tenants** que são municípios em **PI, CE, PE,
PA e MA** (Amarante, Campo Maior, Canto do Buriti, Batalha, Beloardim/PE, Bonito/PA, Breves/PA,
Itapipoca/CE, Buriticupu/MA, Assaré/CE…).

A arquitetura do CERURB Pro é **multi-tenant por subdomínio, um por município**
(`barroduro.cerurb`, `saojoaosoter.cerurb`, `santafilomena.cerurb`, `itapipoca.cerurb`,
`cerurb.valefreire`, `cerurb.prourb`, `cerurb.codice`, `cerurb.mapatech`, `sigma.cerurb`).

`cerurbpro.foxinline.com` está **vivo (HTTP 200)**, JSF+PrimeFaces, atrás de **Cloudflare**.
Só a instância `pi-cerurb.foxinline.com` perdeu o registro A — é uma instância, não a empresa.

**Consequência:** a tese do parecer de negócio ("fornecedora pequena, infra fora do ar, pode sumir")
cai. O risco real não é a Foxinline quebrar — é a Foxinline **ser forte o bastante para não precisar
cooperar**, e ter distribuição em 5 estados para lançar o painel dela primeiro. Também significa
que, se houver acordo, o alcance é imediato: ~236 municípios já instrumentados.

## C. A cartografia é subproduto legal obrigatório da REURB
Lei 13.465/2017, **art. 35**: o projeto de regularização exige levantamento **planialtimétrico e
cadastral georreferenciado**, com **ART/RRT**, demonstrando unidades, construções, sistema viário e
áreas públicas. **Art. 40, III**: o CRF traz a **listagem de ocupantes com qualificação e direitos
reais**. Ou seja: o município que faz REURB é obrigado a gerar a base cartográfica, e o custo já está
dentro do contrato de REURB. O módulo de aerolevantamento deixa de ser pré-requisito caro.

## D. O mercado tem incumbentes, incluindo um com o produto exato
- **Geopixel**: +100 municípios, e vende um **"Observatório Municipal de Informações"** — que é
  precisamente o "painel de integração de dados" proposto aqui.
- Também: Geosite CTM, GeoOne, SQLINK, Terracore, Eixo Soluções, CTM Geo.

## E. O ROI é documentado e é o argumento de venda
Recadastramento + PGV: **São Pedro do Iguaçu (PR)** R$ 172,34 mil → R$ 829,91 mil (**+380%**, sem
mudar alíquota); **Santana de Parnaíba (SP)** **+86,6%**; **Amparo (SP)** **+23%** no ano seguinte.

## F. Fontes públicas TESTADAS por mim agora (não é promessa, é resultado)
| Teste | Resultado |
|---|---|
| `servicodados.ibge.gov.br/api/v1/localidades/municipios/2211001` | **200**, JSON completo de Teresina |
| `api/v3/malhas/municipios/2211001?formato=application/vnd.geo+json` | **200**, GeoJSON (5.551 bytes) |
| SICONFI `apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo` RREO-Anexo 03, Teresina 2024 | **200**, 426 itens, **14 linhas de IPTU com valor mensal** (ex.: R$ 46.869.298,89 num mês; R$ 27,2 mi noutro) |
| SICONFI RREO-Anexo 02 | **200**, 1.065 itens |
| ANEEL CKAN `package_show` geração distribuída | **200**, recursos em **CSV e PARQUET** + dicionário de dados |
| IBGE SIDRA v3 agregados | **timeout** — instável, não confiar como dependência dura |

**Consequência:** dá para construir hoje, sem nenhuma negociação, um painel com geometria real,
indicadores censitários por setor, e **a série de arrecadação de IPTU do município** — que é
exatamente o número que interessa ao prefeito e que o protótipo atual não tem.

# ANEXO 7 — SEU PARECER DA RODADA 3

**Achado 1 (Q1)**  
Diagnóstico: O art. 256 da LC 214/2025 (Anexo A) torna a avaliação em massa anual uma obrigação legal, mas isso **não muda** o escopo da v1 — ML/chat continuam fora porque v1 entrega diagnóstico CIB e baseline fiscal, não PGV.  
Consequência: O método defensável perante TCE é regressão hedônica linear/espacial (CAMA) com coeficientes declarados, diagnóstico de resíduos e validação fora da amostra; GBM fica só como benchmark. Exigível: contribuição por atributo, pesos publicados, mapa de erros e análise de colinearidade.

**Achado 2 (Q2)**  
Diagnóstico: Dados mínimos para calibração: preço de transação (ITBI/escritura), área construída, padrão, tipologia, destinação, data e localização georreferenciada; fontes primárias são ITBI municipal e cartório, com portais de anúncio como suplemento e CERURB como cadastro tipológico.  
Consequência: Com amostra insuficiente (< ~30 por estrato zona×tipologia), usar modelo hierárquico bayesiano com empréstimo de informação entre estratos ou abordagem de custo/renda calibrada, declarando incerteza e não emitindo valor pontual para estrato sem dado.

**Achado 3 (Q3)**  
Diagnóstico: O Roteiro Técnico do CADURB (Anexo A) normatiza a saída e o art. 256 exige valor de referência anual, tornando obsoleto o modelo `setor_censitario`/`imovel_fazenda` do Anexo E, achado 2.  
Consequência: Modelo alvo: `municipio(codigo_ibge)`, `unidade_imobiliaria(cib, setor_id, tipologia, destinacao, padrao, data_construcao, area_construida, geom, valor_referencia, data_referencia)`, `lote_remessa_cadurb(protocolo, status_validacao, data_envio)` e `log_erro_validacao`; toda carga passa a ser desenhada para gerar remessa alfanumérica+georreferenciada validável.

**Achado 4 (Q4)**  
Diagnóstico: O plano v1 (60–90 dias) exige fases: Setup (repo/PostGIS/APIs), Ingestão pública (IBGE malhas/Censo, SICONFI IPTU), Ingestão do cadastro da Fazenda (sanitização/geocodificação), Compatibilização setor×imóvel, Cálculo de gap CIB e Baseline fiscal.  
Consequência: Entregáveis e aceites: scripts versionados (aceite: carga sem erro e checksum), cadastro sanitizado com chave setor (aceite: 100% mapeado ou flag), tabela de cobertura/gap (aceite: domicílios IBGE × imóveis lançados), relatório de potencial com incerteza declarada (aceite: ±30–50% explícito). O prazo quebra se o cadastro não tiver setor/endereço georreferenciável, se a entrega da Fazenda atrasar além da semana 3 ou se >20% exigir geocodificação manual.

**Achado 5 (Q5)**  
Diagnóstico: Ativos reutilizáveis desde o dia 1: dimensão `municipio`, ETL parametrizado por código IBGE, fetcher SICONFI, metodologia de gap CIB e schema CADURB.  
Consequência: Descartável no primeiro cliente: nomes hardcoded de bairros, layout visual do dashboard, regras locais de limpeza de endereço e qualquer acoplamento ao CERURB — manter fora do núcleo.

**Achado 6 (Q6)**  
Diagnóstico: Riscos técnicos novos: homologação CADURB exige certificado digital e-CAC e pode ter schema/validação alterados; art. 256 trata valor de referência de mercado, não valor venal de IPTU; ITBI subdeclarado viésa o modelo para baixo; remessa georreferenciada exige acurácia posicional que cadastros antigos não têm; atualização anual gera drift e exige monitoramento contínuo; scraping de portais de anúncio para calibração pode violar termos/LGPD.  
Consequência: Incluir desde já: ambiente de homologação com certificado municipal, validação de schema versionado, separação explícita entre valor de referência e valor venal, auditoria de subdeclaração por escritura e fonte lícita para dados de anúncio; sem isso a remessa é rejeitada e o modelo não se sustenta.
