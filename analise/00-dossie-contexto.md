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
