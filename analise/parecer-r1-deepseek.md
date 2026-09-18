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
