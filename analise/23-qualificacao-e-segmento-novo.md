# Tabela de qualificação dos 224 municípios do PI + um segmento não identificado antes

Arquivo: **`dados/qualificacao-pi.csv`** — 224 municípios, 16 colunas:
`nome · ibge · pop · bairros · tenant_fox · segmento · iptu · itbi · iss · rcl ·
itbi_sobre_iptu · itbi_per_capita · sinal_rreo · rreo2025 · rreo2024 · rreo2023`

## 1. Panorama do estado

| Métrica | Valor |
|---|---|
| Segmento **A** (IPTU ≥ R$ 1 mi) | **9** |
| Segmento **fronteira** (R$ 100 mil–1 mi) | **21** |
| Segmento **B** (IPTU < R$ 100 mil) | **194** |
| Com divisão de bairros no Censo | **25** |
| **Tenants municipais Foxinline** | **63** (28% do estado) |
| **Nunca entregaram RREO em 3 exercícios** | **49** |
| Entregaram antes e falharam em 2025 | **23** |
| ITBI total do PI 2025 | R$ 86.485.792 |
| IPTU total do PI 2025 | R$ 193.996.424 |

**49 municípios que não entregam demonstrativo fiscal obrigatório há três anos** é o pool de leads
de maior sinal do Segmento B — muito maior do que os 5 que apareciam na amostra dos 25 com bairros.

E **63 tenants Foxinline** (contra os 6 entre os municípios com bairros) mostra que a penetração dela
é concentrada exatamente nos municípios pequenos — que são o alvo do Segmento B. Isso endurece a
disputa e torna o e-SIC à SEAD (lista PROUrbe) ainda mais importante, porque a contagem real é maior.

## 2. O segmento que nenhuma rodada identificou: ITBI alto com IPTU nulo

Sete municípios com **ITBI acima de R$ 200 mil e IPTU abaixo de R$ 50 mil**:

| Município | ITBI 2025 | IPTU 2025 | ITBI/IPTU | Pop. | Tenant |
|---|---|---|---|---|---|
| **Santa Filomena** | R$ 2.866.396 | **R$ 780** | **3.675×** | 6.084 | — |
| **Monte Alegre do Piauí** | R$ 853.282 | R$ 1.115 | **765×** | 10.683 | — |
| Alvorada do Gurguéia | R$ 570.643 | R$ 27.928 | 20× | 5.327 | — |
| Sebastião Leal | R$ 454.375 | R$ 30.016 | 15× | 4.427 | SIM |
| Currais | R$ 380.556 | R$ 3.077 | 124× | 4.832 | — |
| Redenção do Gurguéia | R$ 323.007 | R$ 8.473 | 38× | 8.393 | SIM |
| Barreiras do Piauí | R$ 211.084 | R$ 200 | 1.055× | 3.271 | — |

**Santa Filomena arrecada R$ 780 de IPTU no ano inteiro e R$ 2,87 milhões de ITBI.**

**Todos os sete são do sul do Piauí** — a região dos Gerais / Uruçuí, fronteira agrícola do MATOPIBA.
O perfil é inequívoco: municípios pequenos, sem cidade relevante, com **receita tributária própria
quase inteiramente dependente de transmissão de imóveis**.

### Por que isso é potencialmente o melhor alvo do estado
Para eles, o argumento do plano funciona na sua forma mais forte: **travar registro é travar
praticamente toda a receita tributária própria do município.** Não é "além do IPTU" — é *em vez do*
IPTU. Nenhum outro segmento tem essa concentração.

### ⚠️ A ressalva que precisa ser resolvida ANTES de virar alvo
Esse ITBI vem, com alta probabilidade, de **transação de terra rural** (fazendas de soja), não de
imóvel urbano. E isso importa porque:

- **O CIB de imóvel rural é alimentado pelo INCRA via SNCR**, não pelo município.
- O módulo **CADURB é o cadastro URBANO** — é o que o município transmite.
- Logo, **"seu CIB trava seu ITBI" pode não se aplicar a eles** — o CIB que trava aquela transação
  não é o que eles enviariam.

**Chegar em Santa Filomena falando de cadastro imobiliário urbano quando a receita vem de terra
rural é o tipo de erro que encerra a reunião no primeiro minuto** — e, pior, em um circuito pequeno,
circula.

**Verificação necessária, e é barata:** confirmar a composição do ITBI desses municípios (urbano ×
rural). Fontes: o próprio município via e-SIC, ou o cartório de registro de imóveis da comarca. Se
for majoritariamente rural, o segmento **sai da lista de alvos de conformidade CADURB** — mas pode
virar outra coisa: apoio ao cadastro rural, que é mercado diferente e com outro interlocutor.

**Enquanto não verificado, tratar como hipótese, não como alvo.**

## 3. Correção de um bug próprio nesta tabela
A primeira versão contou **18 municípios com bairros**; o correto é **25**. Causa: o DBF do shapefile
do IBGE está em **UTF-8**, e eu o li como latin-1 — "Parnaíba" virou "ParnaÃ­ba" e falhou no
cruzamento por nome. Corrigido e reprocessado.

**Lição para o pipeline:** os arquivos do IBGE **não têm encoding uniforme** — os CSVs de agregados
são latin-1, o DBF da malha é UTF-8. Testar encoding por arquivo, nunca assumir.

## 4. Verificação do Sinter — NÃO foi possível pelos caminhos públicos
Tentado hoje:
- `/sinter/dados-abertos` → redireciona para o portal geral de dados abertos da RFB, sem dataset do Sinter
- `/sinter/estatisticas` → **redireciona para um relatório Looker Studio que é um Google Analytics da
  RFB, com "Erro do sistema" e dados de abril/2023**. Não é o painel do Sinter.
- Busca pelo arquivo `inscricoes_ativas_*.csv` → não localizado

**Conclusão: os números "apenas Teresina no PI" e "188 no Brasil" não são verificáveis por fonte
pública aberta neste momento.** O e-SIC à RFB (texto já pronto) é a via — e isso **eleva sua
prioridade**, porque hoje esses dois números são o coração do "por que agora" e não têm lastro
conferível.

**Até a resposta chegar, usar as formulações seguras:** *"o cadastro transmitido conhecido no PI é o
de Teresina"* e *"menos de 4% dos 5.570 municípios até [mês/2026]"*.
