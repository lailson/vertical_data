# Rodada 2 — CONVERGÊNCIA. Eixo negócio/risco/estratégia.

Você deu o parecer de negócio da Rodada 1 (Anexo 4). O reconhecimento posterior (Anexo 2) **derruba
a premissa central do seu Achado 1**: a Foxinline NÃO é frágil — tem ~236 tenants municipais em PI,
CE, PE, PA e MA, ~33 cartórios, arquitetura multi-tenant e microserviços de API (`api-exportacao`,
`api-cerurbjus-integracao`) vivos. E existe um concorrente (Geopixel, +100 municípios) que já vende
exatamente o "Observatório Municipal de Informações" proposto.

Responda APENAS o que muda de decisão, em no máximo 6 achados:

1. Revise seu Achado 1: se a Foxinline é forte e tem API interna, a jogada é **competir com ela,
   integrar com ela, ou fazer PARCERIA/revenda em cima dos ~236 municípios que ela já instrumentou?**
   Qual das três, e por quê? Quantifique o trade-off.
2. Com a Geopixel já vendendo o produto proposto para +100 municípios, **qual é o diferencial
   defensável que sobra?** Se não houver, diga.
3. A cartografia é subproduto legal obrigatório da REURB (Anexo 2, item C). Isso muda a economia da
   proposta e a estrutura de preço? Como capturar esse valor sem pagar por ele?
4. Com o ROI documentado de +23% a +380% de IPTU (Anexo 2, item E) e com a arrecadação real do
   município disponível via API pública (Anexo 2, item F), **desenhe o modelo comercial**: é possível
   pagamento atrelado a resultado? Quais os riscos jurídicos disso numa contratação pública?
5. Mantendo ou revisando seu Achado 5 (v1 = diagnóstico de conformidade CIB): qual é o preço de
   tabela dessa primeira entrega, e o que justifica esse preço para o ordenador de despesa?
6. Veredito final: ENTRAR, ENTRAR COM CONDIÇÕES ou NÃO ENTRAR — com as condições explícitas e os
   gatilhos de abandono.

Seja adversarial, quantifique. Cite "Anexo N, item/achado X".

# ANEXO 1 — DOSSIÊ ORIGINAL

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

# ANEXO 2 — ADENDO CORRETIVO

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

# ANEXO 3 — PARECER TÉCNICO DA RODADA 1 (DeepSeek)

**Achado 1 — Integração CERURB em tempo real é ilusão (seção 2).**  
Não existe REST; o tráfego é JSF/PrimeFaces com `ViewState` e respostas XML/HTML. Scraping autenticado é frágil e quebra a cada mudança de tela ou versão.  
**Consequência:** integração em tempo real não pode ser requisito da v1; o único caminho realista é exportação periódica de arquivo via `DataExporter`/CSV, formalizada em contrato com a Foxinline/prefeitura.

**Achado 2 — Coleta própria não é uma feature, é outro produto (seção 5).**  
Exige app de campo offline-first, sincronização, georreferenciamento, validação, LGPD, curadoria e equipe treinada. Não é um formulário web.  
**Consequência:** se o projeto não tiver orçamento e dono dedicados para o módulo de coleta, ele falha e contamina CTM/PGV; a decisão real é se a v1 é campo ou painel, não os dois.

**Achado 3 — A granularidade “bairro” prometida não existe nas fontes públicas (seção 4).**  
As bases abertas confiáveis param em município ou setor censitário; setor censitário ≠ bairro. Bairro só existe com geometria da prefeitura ou rateio rotulado como estimativa.  
**Consequência:** contratualmente a v1 deve entregar setor/município e estimativas claramente marcadas; prometer bairro sem dado georreferenciado da prefeitura é vender ficção.

**Achado 4 — ML/preditivo/chat conversacional na v1 é teatro estatístico (seção 1).**  
Com N≈1.800 imóveis, um município e sem série histórica, não há base para modelo preditivo defensável; chat sobre dados pequenos vira RAG de baixa qualidade.  
**Consequência:** remover preditivo e chat da v1; manter descritivo, ranking e simulador rule-based. ML só entra após cadastro robusto e série temporal.

**Achado 5 — Stack mínimo é PostGIS + ETL + BI, não o protótipo HTML (seções 3 e 4).**  
A entrega honesta começa ingerindo IBGE, SICONFI, INEP, ANEEL etc., publicando mapa por setor e indicadores municipais; CTM/PGV exigem cadastro por imóvel e não se resolvem com dashboard.  
**Consequência:** adotar PostGIS + pipeline de ingestão + ferramenta de visualização; descartar o HTML estático como base técnica e não prometer PGV sem cadastro/avaliação imobiliária.

**Achado 6 — Ativo indefensável sem contrato de titularidade e LGPD (seções 2 e 5).**  
A Foxinline é concorrente potencial e os dados cadastrais são pessoais; o município é controlador, vocês seriam operadores. Sem contrato, qualquer coleta ou integração pode ser bloqueada.  
**Consequência:** não investir antes de garantir contrato com titularidade/uso compartilhado e base legal LGPD; caso contrário, o software nasce refém e sem ativo de dados.

# ANEXO 4 — PARECER DE NEGÓCIO DA RODADA 1 (GLM)

# Parecer R1 — eixo Negócio, Risco e Estratégia de Entrada (dossiê CERURB)

Consultor: GLM. Data: 2026-09-15. Eixo: negócio/risco. Regra da rodada respeitada: 6 achados, adversarial, sem resumo final.

---

## Achado 1 — O risco Foxinline é de mercado, não de integração (seção 2)

**Diagnóstico:** A Foxinline concentra três papéis incompatíveis — fornecedora do dado, único canal de acesso (sem API, exportação como via realista) e concorrente adjacente com ecossistema fim-a-fim — e, como fornecedora pequena com infraestrutura pública fora do ar hoje, pode bloquear, atrasar ou simplesmente descontinuar o acesso sem qualquer obrigação contratual para com quem depende dela.

**Consequência:** Toda receita que depender do dado CERURB carrega risco de interrupção de 100% e sem remédio, e o módulo de coleta (seção 5) será replicado como módulo do CERURB Pro em 1–2 ciclos de venda — a única neutralização é estrutural: CERURB expressamente fora do escopo contratual da v1, dado CERURB tratado como bônus se exportado, e zero dia-homem de engenharia em integração/scraping que não se pague no primeiro trimestre.

## Achado 2 — A janela CIB/SINTER reescreve produto, comprador e preço — e a proposta ignora (seções 1 e 3)

**Diagnóstico:** A proposta vende "painel de gestão" ao comprador errado (planejamento urbano, compra por vontade) quando a obrigação CIB de jan/2027 para os ~5.540 municípios fora das capitais cria um comprador novo (Fazenda/Controloria, comprando por prazo federal) para um produto diferente — cadastro imobiliário conformante e integrável ao SINTER — que o documento de 4 módulos (seção 1) não menciona uma única vez.

**Consequência:** Reposicionar como "conformidade CIB" encurta o ciclo de venda de 12–18 para 3–9 meses, sustenta licenciamento recorrente por município em vez de projeto único e dá ~15 meses para acumular referências antes de o mercado de sistemas de IPTU despertar — e o custo de entrar sem essa tese é competir em estética de dashboard contra BI gratuito e gratuito de brinde pelos incumbentes.

## Achado 3 — Propriedade do dado é o único ativo defensável, e as armadilhas são LGPD + 14.133 (seções 2 e 5)

**Diagnóstico:** O cadastro a ser originado (seção 5) é dado pessoal em volume (CPF, renda, família, geolocalização — seção 2) com o município como controlador, e na Lei 14.133 a contratação direta por dispensa cobre serviços comuns só até ~R$ 59 mil — acima disso o caminho é pregão com dotação orçamentária, e cláusulas omissas deixam tanto a base quanto a propriedade intelectual do software migrarem para o contrato administrativo.

**Consequência:** O contrato exige quatro cláusulas inegociáveis — (i) empresa como operadora LGPD com termo próprio, multa de até 2% do faturamento limitada a R$ 50 mi por infração se omitido; (ii) base exportável pelo município em formato aberto a qualquer momento; (iii) PI do software e dos modelos retida pela empresa, com licença de uso ao município; e (iv) vedação de repasse da nossa base a terceiros concorrentes, inclusive à Foxinline — porque sem (iv) a prefeitura pode presentear o CERURB com o cadastro que nós financiaramos, e o diferencial evapora no ato da assinatura.

## Achado 4 — Como posto, o modelo de receita é projeto único disfarçado (seções 1 e 4)

**Diagnóstico:** Dos 4 módulos da proposta (seção 1), o item mais caro não é software (aerolevantamento na casa de centenas de milhares de reais por município médio — seção 4), o que converte qualquer contrato "completo" em projeto de engenharia com margem desconhecida, enquanto ML/preditivo/chat na v1 (seção 1) só infla custo fixo sem gerar uma linha de receita adicional.

**Consequência:** Entrar pela estrutura de licenciamento — software como SaaS por município (implantação + anuidade), coleta de campo e aerolevantamento como serviço repassado a parceiro especializado fora do nosso balanço, e a posição de originador do dado (seção 5) monetizada como upgrades de conformidade e PGV — porque na forma atual cada contrato reinicia o CAC do zero e a empresa vira consultoria que termina; régua objetiva: se no primeiro contrato a receita recorrente for menor que 30% do valor total, o modelo nasceu errado.

## Achado 5 — Menor escopo que fecha contrato: diagnóstico de conformidade CIB sobre dado aberto (seções 1, 3 e 4)

**Diagnóstico:** O protótipo promete granularidade por bairro que só existe via cadastro próprio (seção 4) e não tem uma tela de imóvel nem métrica de arrecadação (seção 1), então o menor contrato honesto e imediatamente pagável é: um município, diagnóstico de aderência ao CIB/SINTER (seção 3), cruzamento do cadastro imobiliário existente da Fazenda com setor censitário do IBGE e IPTU do SICONFI, e entrega de um índice de conformidade com plano de fechamento de lacunas.

**Consequência:** Esse escopo sai em 60–90 dias com custo marginal baixo (fontes gratuitas — seção 4), entrega ao prefeito um número de campanha (potencial de IPTU não arrecadado em R$) e deixa ao time uma referência replicável para os ~5.540 municípios da janela — qualquer coisa maior que isso (cartografia, PGV, ML, chat) é dívida com juros antes da primeira receita.

## Achado 6 — Sinais de não entrar, com critério de saída (seções 2, 3, 4 e 5)

**Diagnóstico:** Não entrar se dois destes sinais coexistirem: o cliente-parceiro condicionar o projeto à integração com CERURB (seção 2); a prefeitura não emitir os ofícios de acesso às secretarias antes da assinatura (seção 4 — todo dado fino depende disso); não houver dotação orçamentária identificada na 14.133; o pagamento depender de aerolevantamento entregue por terceiros (seção 4); ou a REURB do parceiro tratar o painel como brinde sem orçamento próprio (seção 5).

**Consequência:** O cenário mediano com esses sinais não é "projeto difícil", é um piloto gratuito de 6 meses que queima a equipe dentro da janela de ~15 meses (seção 3) sem gerar contrato replicável — logo o critério de saída deve ser fixado agora: sem contrato assinado com dotação e acordo de operação de dados em até 45 dias de esforço comercial, abortar e realocar para o mercado CIB, cujo custo de oportunidade é todo o resto do país e não este município.
