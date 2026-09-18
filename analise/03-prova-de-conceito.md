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
