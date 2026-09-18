# Rodada 3 — FECHAMENTO. Eixo técnico. Fato novo + pedido de plano.

O Anexo A traz fato que você não tinha: **LC 214/2025, art. 256** obriga o município a publicar no
SINTER o **valor de referência de TODOS os imóveis do CIB, atualizado ANUALMENTE**, para cálculo do
IBS, com metodologia que considera preços de mercado, dados registrais/notariais e localização,
tipologia, destinação, padrão e área de construção. Existe **Roteiro Técnico da RFB** especificando a
remessa ao módulo CADURB (alfanumérico ou alfanumérico+georreferenciado).

Responda no máximo 6 achados:

1. Você disse (Anexo E, achado 2) que ML/chat ficam fora da v1. O art. 256 exige **avaliação em
   massa (mass appraisal)** anual. Isso muda sua posição? Qual método é defensável perante um TCE:
   regressão hedônica, GBM, ou outro — e por quê? O que é exigível em termos de explicabilidade?
2. Quais dados são MÍNIMOS para calibrar avaliação em massa, e de onde vêm (ITBI municipal, cartório,
   portais de anúncio, CERURB)? O que fazer quando não há amostra de transações suficiente?
3. Como o Roteiro Técnico do CADURB muda o modelo de dados que você propôs (Anexo E, achado 2)?
   O formato de saída agora está normatizado — redesenhe o modelo de dados com isso como alvo.
4. **PLANO DE EXECUÇÃO da v1** (diagnóstico CIB + baseline fiscal, 60-90 dias): liste as fases, os
   entregáveis por fase, os critérios de aceite objetivos e os pontos onde o prazo realmente quebra.
5. O que deve ser construído como ativo reutilizável (multi-município) desde o dia 1, e o que pode
   ser descartável no primeiro cliente.
6. Riscos técnicos que ainda não foram nomeados em nenhuma rodada.

Adversarial, concreto. Cite "Anexo N".

# ANEXO A — ADENDO 2: REFORMA TRIBUTÁRIA (NOVO, não visto nas rodadas anteriores)

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

# ANEXO B — PROVA DE CONCEITO COM DADO REAL (NOVO)

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

# ANEXO C — DOSSIÊ

# Dossiê CERURB — contexto consolidado para análise de viabilidade
Data: 2026-09-15. Consolidado por Claude Code a partir de material do cliente + pesquisa própria.

## 1. A oportunidade

Escritório (Capybara Labs / parceiro) avalia **entrar em um projeto que vai começar**: construir uma
**plataforma de gestão territorial municipal** apoiada em dados de regularização fundiária (REURB).
A proposta original ao município tem 4 módulos:

1. **Base Cartográfica Digital** — aerolevantamento com drone, ortofotos, quadras/lotes, logradouros georreferenciados.
2. **Cadastro Técnico Multifinalitário (CTM)** — cadastro por imóvel, auditoria, base única entre secretarias.
3. **Planta Genérica de Valores (PGV)** — avaliação de imóveis, valor venal, mapa de R$/m², justiça fiscal.
4. **Plataforma Web de Gestão Territorial** — dashboards, indicadores, relatórios.

Objetivo declarado pelo município na proposta: **aumentar a arrecadação de IPTU** e fortalecer o
planejamento urbano.

Existe um **protótipo HTML** já feito (painel-gestao-municipal.html, 43KB, dados fictícios de Teresina,
18 bairros). Cobre bem só o módulo 4. Suas telas: Painel principal, Mapa territorial (grade de células
coloridas, não geometria real — o próprio rodapé admite "representação ilustrativa, a versão final usará
PostGIS"), Ranking de bairros, Saneamento, Pavimentação, Educação, Perfis socioeconômicos, Simulador de
investimento, Séries históricas, Status CERURB, Relatórios exportáveis (PDF).
Não há: nenhuma tela de imóvel individual, nenhum módulo de valor venal/PGV, nenhuma métrica de
arrecadação, nenhuma camada cartográfica real.

Ambição declarada para a v1: análise de dados + dashboard + **machine learning / modelos preditivos /
impacto futuro** + **chat conversacional**.

## 2. Achado técnico central: o CERURB não tem API — e a stack explica por quê

O CERURB é produto da **Foxinline Technologies** (Fox Inline Serviços de TI Ltda, CNPJ 29.139.662/0001-29,
fundada 24/11/2017, Parnaíba-PI). Duas linhas de produto:
- **CERURB Pro** — municípios e governo estadual.
- **CERURB Jus** — Tribunal de Justiça do Piauí (cerurbjus.tjpi.jus.br).

### Reconhecimento técnico feito (superfície pública, sem autenticação)

- `cerurb.tech` → **domínio parqueado na GoDaddy**, sem produto. Não é o site da aplicação.
- `foxinline.com` → NS no Cloudflare, **sem registro A**. O host `pi-cerurb.foxinline.com/login.xhtml`
  (instância Piauí do CERURB Pro, indexada no Google) **não resolve hoje**. Ou seja: a infraestrutura
  pública do fornecedor está, no mínimo, instável/fora do ar.
- `cerurbjus.tjpi.jus.br` → responde HTTP 200. Análise dos headers e do HTML:
  - `Set-Cookie: JSESSIONID=...; HttpOnly` → sessão de servlet container Java.
  - `via: 1.1 Caddy` → proxy reverso Caddy.
  - IP 18.232.12.44 → **AWS us-east-1**.
  - Contexto da aplicação: **`/cerurb-usucapi`**.
  - Recursos: `jakarta.faces.resource/...` + `PrimeFaces.settings{...}` versão **15.0.13**, tema
    `primefaces-saga-blue`, `viewId:'/login.xhtml'`, tratamento de `jakarta.faces.application.ViewExpiredException`.

**Conclusão: a stack é Jakarta Faces (JSF) + PrimeFaces 15, Java, server-side rendering, stateful.**

Sondagem de camada REST documentada (12 caminhos padrão: `/api`, `/api/v1`, `/rest`, `/swagger-ui.html`,
`/swagger-ui/index.html`, `/openapi.json`, `/v3/api-docs`, `/q/openapi`, `/actuator`, `/health`, no
contexto e na raiz): **todos 404**. Não há API REST exposta nem documentação de API.

### Por que isso é decisivo (e não é um detalhe)

Em JSF/PrimeFaces o navegador **não consome JSON**. O que trafega são POSTs
`application/x-www-form-urlencoded` carregando `jakarta.faces.ViewState`, e a resposta é um
`<partial-response>` **XML com fragmentos de HTML**. Portanto:

- A ideia de "abrir o DevTools, achar o endpoint e reusar" **não se aplica**: não existe endpoint JSON
  por baixo para descobrir.
- Scraping com Playwright é tecnicamente possível, mas: exige login real, navegação pela UI, e o
  ViewState é invalidado a cada troca de view (`ViewExpiredException` está configurado). É frágil a
  qualquer mudança de layout, lento, e quebra em atualização de versão do PrimeFaces.
- **Contrapartida favorável:** PrimeFaces tem `DataExporter` nativo (CSV/XLS/PDF). Se as telas de
  relatório do CERURB Pro têm botão de exportar — e o cliente relata que "antes era possível baixar os
  dados" — o caminho realista é **exportação periódica de arquivo**, não integração em tempo real.

### Riscos não-técnicos associados
- Dependência de um **fornecedor terceiro, pequeno e concorrente potencial** (a Foxinline também vende
  "ecossistema fim-a-fim"; um painel de gestão é adjacência natural do produto dela).
- Titularidade dos dados: definida no contrato **prefeitura × Foxinline**, não no nosso.
- Sob LGPD, dado de cadastro fundiário é dado pessoal (nome, CPF, renda, composição familiar,
  geolocalização da residência). Compartilhamento com terceiro exige base legal, minimização e
  formalização. O município é controlador; nós seríamos operador.

## 3. Janela regulatória — o argumento comercial mais forte, e não está na proposta

- **Lei 13.465/2017** criou a REURB e o CRF (Certidão de Regularização Fundiária).
- **Portaria MCid 3.242/2022** atualizou a Portaria 511/2009 e fixa as diretrizes de criação,
  instituição e atualização do **CTM** nos municípios brasileiros.
- **SINTER** (Decreto 8.764/2016, gerido pela Receita Federal) integra dados de cartórios, prefeituras
  e Incra num banco de dados espacial.
- **CIB — Cadastro Imobiliário Brasileiro ("CPF do imóvel")**: obrigatório desde **janeiro/2026** para
  cartórios, órgãos federais, capitais e DF; **estende-se a estados e a TODOS os demais municípios em
  janeiro/2027**.

**Implicação:** todo município do país tem, em ~15 meses, uma obrigação federal de ter cadastro
imobiliário integrável ao SINTER/CIB. Isso converte um "painel bonito de gestão" em **infraestrutura de
conformidade obrigatória** — muda o argumento de venda, o comprador dentro da prefeitura e a urgência.

## 4. Inventário de fontes de dados (status real de acessibilidade)

### Já acessível, sem negociação (dado aberto)
| Fonte | Conteúdo | Granularidade | Acesso |
|---|---|---|---|
| **IBGE Censo 2022 — Agregados por Setores Censitários** | população, sexo, idade, cor/raça, alfabetização; domicílios: abastecimento de água, destino de lixo, esgotamento sanitário | **setor censitário** (abaixo de bairro) | download direto (ZIP) |
| **IBGE Malhas Territoriais / Malha de Setores 2022** | geometria dos setores | setor censitário | API Malhas 2.0 / download |
| **IBGE SIDRA (API Agregados 3.0)** | séries estatísticas | município e acima | API pública sem auth |
| **INEP Censo Escolar** | escolas, matrículas, infraestrutura, rendimento | **escola (com geolocalização)** | microdados abertos |
| **SNIS / SINISA** | água, esgoto, resíduos, drenagem; série desde 1995 | **município** (não bairro) | CSV; SNIS encerrou coleta em 2023, SINISA sucede desde 2024 |
| **ANEEL dados abertos** | micro/minigeração distribuída: titular, fonte, potência instalada, data de conexão, município; dados técnicos de inversores | **município / unidade consumidora** | portal CKAN + ArcGIS API |
| **SICONFI** | receita/despesa municipal, RREO, RGF, DCA, Matriz de Saldos Contábeis — **inclui arrecadação de IPTU** | município | API pública |
| **CECAD 2.0 / VIS DATA (CadÚnico)** | perfil socioeconômico das famílias cadastradas, equipamentos públicos georreferenciados | agregado público; **identificado só via SolicitaCad/SAGICAD com autorização** | tabulador web |
| **DataSUS / CNES** | estabelecimentos de saúde, produção ambulatorial | município/estabelecimento | download/API |
| **Base dos Dados (BigQuery)** | grande parte do acima já tratado e padronizado, com chaves de município compatíveis | vários | BigQuery, 1 TB/mês grátis |

### Exige negociação institucional (ofício da prefeitura)
Pavimentação (Sec. Obras — malha viária georreferenciada), saneamento por bairro (concessionária),
iluminação pública (Sec. Serviços Urbanos / distribuidora), cadastro imobiliário e IPTU por imóvel
(Sec. Fazenda), educação municipal fina (SEMEDUC).

### Gargalo estrutural a registrar
Quase todo dado público federal para no **município**. O painel promete **bairro**. A única base pública
que desce abaixo do município é o **setor censitário do IBGE** — e setor censitário ≠ bairro, exige
compatibilização espacial. Dado por bairro só existe se: (a) vier do cadastro de campo próprio,
(b) vier da prefeitura georreferenciado, ou (c) for resultado de rateio/estimativa — que precisa ser
rotulado como estimativa, não como medição.

### Custo de referência do módulo cartográfico
Aerolevantamento com drone: ~R$ 50–120/hectare; loteamento urbano de 50 ha ≈ R$ 10 mil. Escala cai com
área. Para área urbana de município médio (p.ex. 3.000 ha) a ordem de grandeza é de centenas de milhares
de reais — é o item mais caro da proposta e não é software.

## 5. A tese alternativa do cliente (e é a mais importante da conversa)

Citação do material: *"no ato da coleta a gente alimenta essa base e isso nos dá total independência para
avançar nas possibilidades. Acho que a melhor saída seria essa. Se puder avançar dessa forma já penso no
módulo de coleta para apresentar a vcs."*

Ou seja: em vez de brigar para extrair dados do CERURB, **construir o próprio módulo de coleta de campo**,
que roda junto com a REURB e captura o que o CERURB não captura — **família, saúde, educação, fiscal
(tributos) e avaliação do imóvel** — sendo o imóvel apenas uma parte. Adicionalmente: municípios que
contratarem a REURB **podem repassar a base cartográfica** (georreferenciamento da área).

Isso desloca o projeto de "integrador refém de uma fonte fechada" para "**originador do dado**".

## 6. Perguntas que a análise precisa responder

1. Integração com o CERURB: qual a estratégia realista, e ela deve ser sequer um requisito de v1?
2. Coleta própria vs. integração: qual é a decisão correta, e qual o custo/prazo de cada caminho?
3. O painel prometido é entregável com as fontes que existem hoje, ou promete granularidade inexistente?
4. ML/preditivo/chat conversacional na v1: viável ou é passivo técnico disfarçado de diferencial?
5. Qual o desenho de contrato/propriedade de dados que torna o negócio defensável?
6. Qual o menor escopo que fecha contrato, prova valor e não cria dívida impagável?

---

## 7. Achados adicionais da pesquisa (incorporados após a Rodada 1 ser disparada)

### 7.1 A base cartográfica não é um custo a criar — é subproduto legal obrigatório da REURB
**Lei 13.465/2017, art. 35:** o projeto de regularização fundiária deve conter, no mínimo,
*levantamento planialtimétrico e cadastral, com georreferenciamento*, subscrito por profissional
competente com **ART/RRT**, demonstrando unidades, construções, sistema viário, áreas públicas e
demais elementos caracterizadores do núcleo urbano informal. O **CRF** (art. 40, III) inclui a
**listagem de ocupantes com qualificação e direitos reais**.

Consequência: **todo município que executa REURB é legalmente obrigado a produzir cartografia
georreferenciada com responsabilidade técnica.** A intuição do cliente ("o município pode repassar a
base cartográfica") é mais forte do que ele mesmo colocou — o dado existe por imposição legal, e o
custo já está pago dentro do contrato de REURB. O módulo 1 da proposta (aerolevantamento) deixa de
ser um investimento inicial obrigatório de centenas de milhares de reais e vira um **complemento**
para áreas não cobertas pela REURB.

### 7.2 O mercado NÃO está vazio — a concorrência é estabelecida
- **Geopixel** — CTM, PGV, regularização fundiária, "Observatório Municipal de Informações" (que é
  exatamente o painel de integração de dados proposto). Declara **mais de 100 municípios atendidos**.
- **Geosite CTM**, **GeoOne**, **SQLINK** (geotecnologia + engenharia de dados + integração com
  sistemas oficiais), **Terracore**, **Eixo Soluções em Gestão Pública** (CTM + PGV), **CTM Geo**.
- Portanto: entrar como "mais um CTM/PGV genérico" é entrar num mercado com incumbentes que têm
  escala, referências e relacionamento com prefeituras. **O diferencial precisa ser outra coisa.**

### 7.3 O ROI do IPTU é documentado e alto — é o que financia o contrato
Casos reais de recadastramento + atualização de PGV:
- **São Pedro do Iguaçu (PR)**: IPTU global de R$ 172,34 mil → R$ 829,91 mil (**~380%**), *sem
  alteração de alíquota*.
- **Santana de Parnaíba (SP)**: **+86,6%** de arrecadação; participação do IPTU na receita total
  saiu de 14,37% (1993) para 26,94% (1996).
- **Amparo (SP)**: **+23%** no lançamento já no ano seguinte ao início da revisão (2022).

Consequência comercial: o projeto pode ser vendido com **pagamento atrelado a resultado de
arrecadação**, e não como despesa de TI. Isso resolve a objeção orçamentária da prefeitura e é o
argumento que a proposta atual já tem ("aumentar arrecadação") mas não sustenta com número.

### 7.4 Dado geoespacial de Teresina existe fora do CERURB
SEMPLAN/PMT publica mapas interativos e a malha de bairros (shapefile disponível por terceiros,
revisão de 2017, base Lei municipal 4.423/2013); PRODATER é a empresa de processamento de dados do
município. O "mapa territorial" do protótipo pode virar geometria real **sem depender da Foxinline**.

# ANEXO D — ADENDO CORRETIVO

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

# ANEXO E — PARECER TÉCNICO R2

1. **Diagnóstico:** A correção do Anexo 2, item A derruba o Anexo 3, Achado 1 — com `api-exportacao` vivo, a via primária é pedir credencial e contrato de uso da API de exportação existente, o que é tecnicamente trivial para a Foxinline e desloca o problema para vontade comercial, não capacidade técnica. **Consequência:** Recomendo tentar primeiro a API de exportação; em seguida, exportação CSV via `DataExporter`/tela do CERURB Pro como fallback contratual; scraping com Playwright só tem lugar como último recurso pontual para lacunas não cobertas por API/exportação, nunca como dependência de v1 — a fragilidade de ViewState persiste.

2. **Diagnóstico:** O Anexo 4, Achado 5 afirma que o diagnóstico de conformidade CIB sobre IBGE + SICONFI + cadastro da Fazenda sai em 60–90 dias; isso é tecnicamente construível **apenas se** o cadastro da Fazenda for entregue como base tabular legível e com chave geográfica (setor), e se SIDRA for evitada (Anexo 2, item F). **Consequência:** Entra: ingestão de malha de setores IBGE (GeoJSON) e agregados do Censo 2022 (ZIP), arrecadação IPTU via SICONFI RREO Anexo 03, cadastro da Fazenda sanitizado, compatibilização setor×imóvel, e relatório de gaps. Não entra: cartografia própria, PGV, CERURB, ML/chat, coleta de campo. Componentes: Python + PostgreSQL/PostGIS + cron/Dagster + BI (Metabase). Modelo de dados: `municipio`, `setor_censitario(geom)`, `imovel_fazenda(sanitizado, setor_id)`, `iptu_siconfi(ano, mes, valor)`, `indicador_gap(cobertura, conformidade)`. Sem chave geográfica, o prazo estoura.

3. **Diagnóstico:** Anexo 2, item F mostra IBGE localidades/malhas, SICONFI e ANEEL funcionando, mas SIDRA instável; portanto a ingestão mínima deve usar cache local, retry/backoff e PostGIS para geometrias, evitando dependência de SIDRA em runtime. **Consequência:** Arquitetura: scripts Python com `requests`; IBGE extraído via API de localidades/malhas e agregados via ZIP, nunca SIDRA; SICONFI via API REST; ANEEL via CKAN/Parquet; carga em PostGIS. **Não usar Base dos Dados/BigQuery** para: (a) geometria vetorial de setores (custo de byte e join espacial local mais rápido), (b) cadastro imobiliário da Fazenda com dados pessoais (LGPD e soberania do dado), (c) dados que exigem baixa latência/ownership — Base dos Dados serve para dados públicos tabulares, não para o ativo central.

4. **Diagnóstico:** O "potencial de IPTU não arrecadado" não é subtração direta; exige comparar domicílios IBGE por setor com imóveis lançados no cadastro da Fazenda, ajustando por isenções, inadimplência e uso, e expressar em faixa — SICONFI (Anexo 2, item F) só dá arrecadação total, não número de lançamentos. **Consequência:** Metodologia defensável: (1) contar domicílios IBGE por setor e imóveis tributáveis por setor (cadastro da Fazenda compatibilizado); (2) calcular déficit de cobertura; (3) estimar valor médio de IPTU por imóvel (SICONFI / total de lançamentos); (4) potencial = déficit × valor médio, com cenários. Declarar margem de erro mínima de ±30–50% dependendo da qualidade do cadastro; se não houver setor confiável, a margem sobe para ±50% e o valor é ordem de grandeza, não promessa de receita.

5. **Diagnóstico:** O Anexo 3, Achado 2 alertou que coleta própria vira outro produto, mas o Anexo 2, item C mostra que a cartografia georreferenciada já é obrigação legal da REURB — então o menor recorte é um formulário de campo acoplado ao fluxo já existente, não um sistema paralelo. **Consequência:** Recorte mínimo: PWA/formulário offline-first com 10–15 campos essenciais (imóvel, ocupantes, uso, valor estimado), preenchido no ato do levantamento planialtimétrico, armazenado em PostGIS com controles LGPD. Isso gera um ativo defensável ("base georreferenciada de imóveis visitados") sem virar outro produto, pois é parte do contrato de REURB. Não entra: saúde, educação, fiscal completo, avaliação imobiliária complexa, ML.

6. **Diagnóstico:** Ainda discordo tecnicamente do Anexo 4, Achado 5, que trata o diagnóstico CIB sobre dado aberto como trivial em 60–90 dias, ignorando que o cadastro da Fazenda não é aberto, frequentemente vem sujo e exige geocodificação prévia; e discordo do Anexo 4, Achado 3, que confunde "formato aberto" com ativo defensável — sem schema versionado, dicionário de dados e chaves geográficas, a exportação é inútil. **Consequência:** O contrato deve especificar o schema mínimo do cadastro da Fazenda (com setor censitário ou endereço georreferenciável) e prever um marco de validação de qualidade antes do prazo de 60–90 dias; caso contrário, o diagnóstico vira dívida técnica e pode atrasar a janela CIB de 15 meses.

# ANEXO F — PARECER DE NEGÓCIO R2

# Parecer R2 — CONVERGÊNCIA. Eixo negócio/risco/estratégia de entrada

Consultor: GLM. Data: 2026-09-15. Rodada 2 do dossiê CERURB: responde apenas o que **muda de decisão** frente ao Parecer R1 (Anexo 4), a partir do adendo corretivo (Anexo 2) e do dossiê original (Anexo 1). Regra da rodada: 6 achados, adversarial, quantificado, citação por "Anexo N, item/achado X".

---

## Achado 1 — Foxinline forte inverte o risco: a jogada é integrar sob mandato do município e competir na lacuna; parceria só como licenciador OEM (corrige Anexo 4, Achado 1)

**Diagnóstico:** A premissa central do meu Achado 1 cai: a Foxinline tem ~236 tenants municipais em 5 estados, ~33 cartórios, arquitetura multi-tenant viva e microserviços de API operantes (Anexo 2, itens A e B). O risco não é ela quebrar — é ela ter escala suficiente para **não precisar cooperar** e para lançar o painel dela primeiro na própria base instalada. As três jogadas têm trade-off assimétrico:

- **Competir de frente:** contra 336 clientes combinados de incumbentes (Foxinline 236 + Geopixel 100+, Anexos 2, itens B e D), com ciclo de venda municipal de 3–9 meses (Anexo 4, Achado 2), uma equipe pequena fecha 5–10 contratos/ano — 25–50 anos para igualar a pegada deles. Competir no produto genérico de CTM/observatório é oceano vermelho com CAC insustentável.
- **Integrar:** a `api-exportacao` existe e o pedido vira "emita credencial e contrato de uso" — tecnicamente trivial para eles (Anexo 2, item A), o que desloca o gargalo de capacidade para **vontade comercial**. Espontaneamente, não vem: somos concorrente adjacente. A via real é o município — controlador LGPD do dado (Anexo 1, seção 2) — impor cláusula de acesso à API no contrato dele com a Foxinline. É um movimento político **por município**; escala só onde já operamos.
- **Parceria/revenda em cima dos 236:** alcance imediato, mas o cliente é dela; ser revenda do dado dela é ser feature com prazo de validade — o módulo é copiado em 1–2 ciclos de venda (Anexo 4, Achado 1). Só vale no formato inverso: **OEM**, ela revendendo nosso módulo de conformidade/fiscal, com PI licenciada por nós.

**Consequência:** Decisão dupla + uma opção com prazo fatal: (i) integrar **apenas** onde o município mandatar o acesso por contrato, com zero dia-homem de engenharia antes da credencial assinada — o risco de interrupção do meu Achado 1 (Anexo 4) sobrevive só onde não houver cláusula; (ii) competir na lacuna que nem Foxinline nem Geopixel ocupam hoje — conformidade CIB com prazo federal (jan/2027, Anexo 1, seção 3) e recuperação fiscal medida contra baseline público; (iii) sondar a Foxinline para OEM por 30 dias, não um a mais: se recusarem ou propuserem o espelho (nós integrados na plataforma deles, sem PI nossa), arquivar — o custo de oportunidade de perseguir é o da janela inteira. Quantificado: integrar por mandato custa semanas de engenharia após a credencial e não cria dependência; competir de frente custa R$ 1–2 mi e 24–36 meses para chegar a 10–20 municípios num mercado onde os incumbentes já somam 336; OEM aceito captura, mesmo a 10% de adesão, 23 municípios × ~R$ 750/mês × 12 ≈ R$ 207 mil/ano recorrentes com CAC ~zero — upside grande, probabilidade baixa, por isso é opção e não plano.

## Achado 2 — No "Observatório Municipal" puro, NÃO sobra diferencial defensável; o defensável são três posições que a Geopixel não ocupa (responde à pergunta 2 com "não há" no eixo proposto)

**Diagnóstico:** A Geopixel vende exatamente o produto proposto — "Observatório Municipal de Informações" — com +100 municípios de referência e CAC amortizado (Anexo 2, item D; Anexo 1, seção 7.2). Sendo adversarial e honesto: no eixo "painel de integração de dados", **nosso diferencial é zero**. O mercado nacional (~5.570 municípios) está longe de saturado — 336 clientes combinados ≈ 6% —, mas o território provável do go-to-market (PI e entorno) é exatamente o quintal da Foxinline (Anexo 2, item B). O que resta de defensável não é feature de dashboard, é posição contratual ou regulatória: (1) o **canal de originação da REURB** — a cartografia e a listagem de ocupantes nascem dentro do contrato do nosso cliente, por imposição legal (art. 35 e art. 40, III, Lei 13.465/2017; Anexo 2, item C), posição que nenhum incumbente de software tem; (2) **produto de prazo** — conformidade CIB/SINTER antes de jan/2027 (Anexo 1, seção 3); (3) **preço por resultado com baseline público auditável** (Anexo 2, itens E e F), que consultoria de software não consegue imitar sem mudar o próprio modelo de receita.

**Consequência:** Reposicionar a proposta para fora do eixo observatório: se o material seguir prometendo "painel", a resposta natural do comprador é "a Geopixel já tem — me mostre o preço dela". O pitch passa a ser **conformidade com prazo + potencial fiscal em R$ + cartografia já paga por lei**, e o painel desce ao papel de camada de entrega. Se o cliente-parceiro insistir no observatório como identidade do produto, esse é um sinal de desalinhamento de tese, não de wording.

## Achado 3 — A cartografia obrigatória da REURB destrói a estrutura de preço original: o item mais caro do dossiê sai do nosso balanço (Anexos 1, seção 4 e seção 7.1; Anexo 2, item C)

**Diagnóstico:** O aerolevantamento era o item mais caro e o único não-software (R$ 50–120/ha; centenas de milhares de reais por município médio — Anexo 1, seção 4) e era o que convertia o contrato em projeto de engenharia com margem desconhecida (Anexo 4, Achado 4). Se todo projeto de REURB exige levantamento planialtimétrico e cadastral georreferenciado com ART/RRT e listagem de ocupantes (art. 35 e art. 40, III; Anexo 2, item C), então **para área REURB o custo já está pago dentro do contrato do parceiro** — R$ 150–360 mil num município de 3.000 ha que nem nós nem a prefeitura voltamos a desembolsar. A captura sem pagar é contratual, não técnica: cláusula de entrega no contrato de REURB (município × parceiro) exigindo a base em **formato aberto** (SHP/GeoPackage/GeoJSON) com acurácia posicional declarada e dicionário de atributos — como o conteúdo já é obrigatório por lei, formatos e critérios de aceitação são acréscimo de custo marginal zero. Dois riscos a precificar: base entregue inutilizável (contratante ruim) — por isso o **QC de aceitação** vira serviço nosso, vendido; e a listagem de ocupantes é dado pessoal — operação LGPD formalizada (Anexo 1, seção 2).

**Consequência:** Reestruturar o preço em três linhas: software/analytics (nosso), QC + ingestão da base REURB (nosso, barato, alta margem), aerolevantamento complementar para área fora da REURB (pass-through de parceiro especializado, fora do balanço — mantém Anexo 4, Achado 4). Gatilho imediato: se o contrato de REURB do cliente já estiver assinado **sem** cláusula de entrega em formato aberto, renegociar antes de qualquer construção — sem ela, a "cartografia de graça" vira refexo da boa vontade do contratante e o custo de centenas de milhares volta para alguém.

## Achado 4 — Modelo comercial: fixo + SaaS + eficiência sobre incremento de IPTU, com baseline SICONFI e teto; os riscos jurídicos existem e têm mitigação contratual (Anexos 2, itens E e F; Anexo 1, seção 7.3)

**Diagnóstico:** Pagamento atrelado a resultado é possível **porque a métrica virou pública**: o SICONFI entrega o IPTU mensal realizado do município via API testada (14 linhas mensais, Anexo 2, item F) — fonte que nenhuma das partes controla, condição necessária para o fee sobreviver à contestação. Modelo proposto: implantação fixa R$ 60–80 mil + SaaS R$ 1,5–3 mil/mês + **eficiência de 10–15% sobre o incremento de IPTU acima do baseline**, teto de 2–3× a implantação por ano, medição em 24 meses, baseline = média SICONFI dos 3 exercícios anteriores **excluindo efeito de alteração de alíquota** (os casos documentados de +23% a +380% são sem mudança de alíquota — Anexo 2, item E; incremento vindo de PGV/recadastro é nosso mérito, de alíquota é mérito do prefeito). Exemplo: município com IPTU₀ = R$ 20 mi/ano e ganho conservador de +10% = R$ 2 mi/ano → fee de R$ 200–300 mil/ano, 3–5× o fixo — daí o teto. Riscos jurídicos na contratação pública (14.133): (i) fee variável não cabe em pregão de preço aberto — o veículo é o **contrato de eficiência (art. 119)** via diálogo competitivo (art. 28, I), ou contratação em duas fases: diagnóstico por dispensa e eficiência depois, com baseline já medido; (ii) a dotação precisa cobrir o **teto** — o TCE pergunta de onde sai o pagamento; (iii) contestação causal ("a arrecadação subiu por outros motivos") — mitigada por baseline público, exclusão de alíquota e teto; (iv) os Tribunais de Contas são hostis a percentual aberto sobre receita — teto + fonte pública de medição são o que torna defensável; (v) risco moral inverso: alíquota alta em ano eleitoral — a exclusão contratual protege as duas partes.

**Consequência:** O contrato muda de "despesa de TI" para "captação de receita com custo líquido zero" — resposta à objeção orçamentária que a proposta promete mas não sustenta com número (Anexo 1, seção 7.3). Condição de entrada inegociável: nenhum contrato de eficiência sem as três cláusulas (baseline SICONFI, exclusão de alíquota, teto) — sem elas, o fee vira litígio de anos com o TCE e a "receita" vira passivo.

## Achado 5 — Preço de tabela da v1 (mantido o escopo do meu Achado 5, Anexo 4): R$ 49,5–58,8 mil, calibrado no teto da dispensa, com payback menor que 2 semanas de incremento

**Diagnóstico:** O escopo permanece — diagnóstico de conformidade CIB/SINTER num município, 60–90 dias, sobre dado público (SICONFI e IBGE por setor censitário — Anexos 1, seção 4; 2, item F) mais o cadastro da Fazenda via ofício. Preço de tabela: **R$ 49,5 mil** (até ~50 mil imóveis) a **R$ 58,8 mil** (acima), calibrado para caber na dispensa por valor (~R$ 59 mil — Anexo 4, Achado 3), que contrata em semanas em vez de pregão em semestres. A justificativa ao ordenador de despesa, nesta ordem: (1) **obrigação com prazo federal** — CIB obrigatório em jan/2027 (Anexo 1, seção 3); o diagnóstico mede a distância até lá; (2) **o deliverable é dinheiro**: potencial de IPTU não arrecadado em R$, ancorado nos casos de +23% a +380% (Anexo 2, item E) — num município de IPTU R$ 20 mi, um ganho conservador de +10% vale R$ 2 mi/ano e o diagnóstico custa menos de 3% disso; (3) **baseline 100% de fonte pública auditável** (Anexo 2, item F) — o município não está comprando estimativa do fornecedor; (4) entrega um plano por prioridade, não relatório morto. Custo interno (150–250 h seniores + ferramenta reutilizável) em 30–50% do preço — a margem financia o SaaS até o fee de eficiência ligar.

**Consequência:** Esse é o menor contrato que fecha dinheiro vivo dentro da janela, sem aerolevantamento, sem CERURB no caminho crítico e sem ML/chat (mantém Anexos 3 e 4, achados 4). E cada diagnóstico vendido produz o **baseline que alimenta o contrato de eficiência do Achado 4** — a v1 é o gargalho de vendas do modelo inteiro: se não vender em 45 dias de esforço comercial, o problema é de mercado, não de produto.

## Achado 6 — Veredito: ENTRAR COM CONDIÇÕES

**Condições (explícitas e verificáveis):**
1. Escopo v1 = diagnóstico CIB do Achado 5: R$ 49,5–58,8 mil, por dispensa, dotação identificada, 60–90 dias.
2. CERURB fora do caminho crítico: integração só com credencial emitida **e** cláusula de acesso no contrato município × Foxinline (Anexo 2, item A); zero engenharia antes disso.
3. Cláusula de entrega da cartografia REURB em formato aberto no contrato do parceiro (Achado 3) — renegociar antes de construir.
4. As quatro cláusulas inegociáveis do meu Achado 3 (Anexo 4): operação LGPD formalizada, base exportável pelo município, PI retida por nós, vedação de repasse a concorrentes — inclui a Foxinline.
5. Sonda OEM com a Foxinline: 30 dias de prazo fatal, aceite só como licenciador (Achado 1).
6. Receita recorrente ≥ 30% do primeiro contrato (régua do Anexo 4, Achado 4) e nenhum contrato de eficiência sem baseline/alíquota/teto (Achado 4).

**Gatilhos de abandono:** (i) sem diagnóstico assinado com dotação em 45 dias de esforço comercial (mantém Anexo 4, Achado 6) — abortar e realocar para o mercado CIB; (ii) cliente ou município condicionar o projeto a dado CERURB; (iii) contrato de REURB sem cláusula de cartografia e parceiro recusar renegociação; (iv) painel tratado como brinde sem orçamento próprio (Anexo 1, seção 5); (v) **Foxinline ou Geopixel anunciar módulo de conformidade CIB com integração SINTER antes da nossa primeira assinatura** — nesse caso a tese de prazo commoditiza, o projeto regride ao "dashboard genérico" do Achado 2, que é o cenário sem diferencial — e a resposta correta passa a ser não entrar.
