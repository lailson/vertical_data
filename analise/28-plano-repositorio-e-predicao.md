# Plano — repositório de dados, cruzamento e predição

**Data:** 2026-09-18 · **Status:** plano, aguardando execução
**Substitui parcialmente:** `analise/27-plano-modo-demonstracao.md`

---

## 0. O que muda em relação ao plano 27

**O município inventado sai.** Serra do Meio, o regime de "maquete" e toda a §4 do plano
27 estão cancelados. O caminho passa a ser o oposto: **completar o dado que falta e
prever a partir do que existe** — sem ficção em lugar nenhum.

O que sobrevive do plano 27: o simulador (§6), o modelo de risco (§11.3), a regra de
consulta fechada do chat (§11.5) e todos os achados da revisão da rodada 9. O que cai:
tudo que dependia de inventar território.

**Consequência boa:** sem ficção, a regra *"nenhuma tela com dado fictício em bairro
nomeado"* deixa de precisar de guarda, faixa, validade e rota separada. Some um sistema
inteiro de contenção, porque some o que ele continha.

---

## 1. Por que isto é maior do que parece — e por que resolve o problema do negócio

O projeto tem uma fraqueza comercial conhecida e registrada desde a rodada 3: **é um
produto de prazo.** Vende conformidade com o art. 266 até 31/12/2026, entrega a remessa
aceita, e acaba. Venda única, com data de validade.

Um repositório que cruza bases públicas e prevê **não é desvio do negócio — é a resposta
à maior fraqueza dele.** Transforma uma venda de prazo em assinatura: o município que
contratou a conformidade continua pagando por um painel que responde perguntas que ele
não consegue responder sozinho.

E há um ativo que já está no repositório e quase ninguém monta: **1.891.421 endereços do
CNEFE com coordenada e tipo de edificação**. Isso é o denominador de metade das perguntas
interessantes sobre território — inclusive as de energia.

---

## 2. Arquitetura: de arquivos para repositório

Hoje são JSON servidos estáticos. Funciona para 224 municípios e 20 campos; não funciona
para dezenas de bases com histórico.

```
dados/bruto/          ← como hoje: download idempotente, nunca versionado
dados/repo/*.parquet  ← camada canônica, uma tabela por base × versão
dados/repo/vd.duckdb  ← o repositório: views, junções, linhagem
painel/dados/*.json   ← continua existindo: o recorte que o painel abre sem internet
```

**Por que DuckDB + Parquet e não um banco servidor:** o painel abre por `file://` numa
prefeitura sem wifi, e isso é propriedade do produto, não acaso. DuckDB é um arquivo,
lê Parquet direto, fala SQL, e tem **DuckDB-WASM** — o mesmo repositório pode ser
consultado *dentro do navegador*, sem servidor. A propriedade "roda sem internet"
sobrevive ao repositório crescer.

**Proveniência é coluna, não comentário.** Toda tabela carrega `fonte`, `url`,
`baixado_em`, `vigencia`, `licenca`, `sha256`. Um número sem essas seis coisas não entra.
É o que já vale hoje em prosa; passa a ser esquema.

---

## 3. O problema difícil, e ele não é o volume

É **compatibilizar geografias**. Este projeto já pagou por subestimá-lo: juntar CNEFE com
agregados do Censo pelo código de setor perdeu **10,4% dos endereços do Piauí**, porque o
CNEFE referencia *setor de coleta* e os agregados usam *setor de divulgação*. A solução
foi geométrica — ponto em polígono — e é ela que precisa virar infraestrutura.

| base | granularidade real | junta por |
|---|---|---|
| Censo 2022 agregados | bairro / setor de divulgação | código IBGE |
| CNEFE | **endereço com coordenada** | geometria |
| ANEEL GD | **município — e só** | código IBGE |
| SNIS / SINISA | município, autodeclarado | código IBGE |
| LABREN irradiação | **grade ~10 km + sede municipal** | geometria |
| SIGEL (subestação, LT) | **geometria** | geometria |
| SICONFI / RREO | município | código IBGE |

**Regra que evita a próxima perda de 10,4%:** junção por código só entre bases da mesma
autoridade e da mesma vintage. Tudo mais entra por **geometria**, com uma grade comum
(H3 ou o próprio setor censitário) como chave de cruzamento. E **toda junção declara
quantas linhas não casaram** — não casar é resultado, não é erro a esconder.

---

## 4. As bases — o que entra, o que traz, o que custa

Verificado na fonte em 18/09/2026, não de memória:

| base | traz | granularidade | custo / ressalva |
|---|---|---|---|
| **ANEEL — MMGD** ([portal](https://dadosabertos.aneel.gov.br/dataset/relacao-de-empreendimentos-de-geracao-distribuida)) | cada empreendimento de micro/minigeração: fonte, potência em kW, **data de conexão**, classe, distribuidora | **município** (a camada de pontos do SIGEL dá coordenada — §4-bis) | CSV e **Parquet**, atualização **diária**. ⚠️ houve **interrupção de 23/09 a 13/11/2025** na migração SISGD → MMGD: buraco na série que precisa aparecer no gráfico, não ser interpolado |
| **LABREN / INPE — Atlas Solar** ([portal](https://labren.ccst.inpe.br/atlas_2017.html)) | irradiação global horizontal, direta normal, plano inclinado, difusa | grade + **sedes municipais** | CSV e SHP. ⚠️ **licença restringe reprodução para fim comercial sem autorização do INPE** — usar como *insumo* citando a fonte é permitido; republicar a base, não. Isto precisa de decisão antes de virar produto pago |
| **SNIS / SINISA** ([resultados](https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/sinisa/resultados-sinisa/resultados-sinisa-2025)) | água, esgoto, resíduos, drenagem, gestão — **série desde 1995** | município, **autodeclarado pelo prestador** | O SNIS encerrou em 2023; o **SINISA** assumiu em 2024. Em 2024, **3.396 de 5.570** municípios têm todos os componentes — ausência é a regra, não a exceção |
| **ANEEL — SIGEL / SIGET** ([portal](https://dadosabertos-aneel.opendata.arcgis.com/)) | subestações, linhas de transmissão, usinas | **geometria** | SHP/GeoJSON/KML. É o que torna possível falar de usina em solo |
| **CNEFE 2022** (já no repositório) | 1,89 mi de endereços no PI, coordenada, **tipo de edificação** | **endereço** | já baixado e agregado |
| **Censo 2022** (já no repositório) | renda, domicílios, entorno | bairro / município | já baixado |
| **SICONFI / RREO** (já no repositório) | IPTU, ITBI, RCL, 2023–2025 | município | já baixado |

### 4-bis. Revisão de 18/09 — o que faltava, e o que mudou

**Entra por cima de tudo: BDGD** (`base-de-dados-geografica-da-distribuidora-bdgd`, ODbL).
É a rede de **distribuição** georreferenciada — transformador, alimentador, unidade
consumidora. Telhado não se conecta a linha de transmissão, conecta-se ao transformador da
esquina: para geração distribuída ela vale mais que o SIGEL de transmissão.

**Entra junto: tarifas homologadas** (`tarifas-distribuidoras-energia-eletrica`,
atualizada diariamente). **Sem tarifa não há payback, e payback é o que decide adoção.**
É a variável que faz o modelo sair do descritivo — prever com causa, não com correlação.

**Também no catálogo:** `siga-…` (usinas, versão diária) e `atendimento-mmgd`.

**Correção sobre granularidade.** O plano dizia "município e só". Vale para a base
tabular. O SIGEL publica camada de **pontos** de GD com lat/lon — 71.558 no Piauí. Mas
arredondadas em **duas casas (~1,1 km)**, com ~0,9% grosseiramente fora do município
declarado e **79% de cobertura** contra a tabular. Dá **superfície de densidade**, não
contagem por bairro. Detalhe em `analise/29-analise-fontes-propostas.md`.

**Projeção.** Nada de UTM 23S para o estado: a zona vai de −48° a −42° e o Piauí vai a
−40,58°, cruzando para a zona 24. SIRGAS 2000 geográfico (EPSG:4674) com cálculo
geodésico, e projeção equivalente em área quando o cálculo exigir.

Candidatas para depois, na ordem em que provavelmente pagam: **INEP** (Censo Escolar,
já mapeado), **CNES/DATASUS** (saúde), **MapBiomas** (uso do solo, para aptidão de
usina), **RAIS/CAGED** (emprego), **CNPJ da Receita** (estabelecimentos).

---

## 5. Energia: são dois produtos, e confundi-los estraga os dois

### 5.1 Geração distribuída em telhado — mercado endereçável

**A pergunta:** quantos telhados neste município comportam geração, quantos já têm, e
onde estão os que faltam.

O ativo que torna isso possível e que quase ninguém tem montado: o **CNEFE dá tipo de
edificação por endereço, com coordenada**. Casa e apartamento não são o mesmo mercado —
apartamento não tem telhado próprio. O denominador sai daí, não de uma estimativa.

```
potencial = domicílios com telhado próprio (CNEFE, tipo 101/102)
          × irradiação no plano inclinado (LABREN, sede do município)
          × fator de aproveitamento declarado
          − o que já existe (ANEEL MMGD)
```

**Onde isso é honesto e onde não é:** o numerador de adoção (ANEEL) é **município e só**.
Descer a bairro é **modelagem, não medição**, e a tela tem de dizer isso no próprio
número — é a mesma regra que já governa o painel.

### 5.2 Usina em solo — aptidão locacional

**A pergunta:** onde cabe uma usina, e por que ali.

Não é aprendizado de máquina. É **álgebra de mapas com pesos declarados**, o mesmo método
que o projeto já usa no índice de vulnerabilidade e defende perante o TCE:

| critério | fonte | por quê |
|---|---|---|
| irradiação | LABREN | o recurso |
| distância a subestação e a linha de transmissão | SIGEL | conexão é o custo que mata projeto |
| declividade | relevo IBGE / SRTM | acima de ~10% encarece demais |
| uso e cobertura do solo | MapBiomas | não se propõe usina sobre floresta |
| restrição legal | unidades de conservação, terra indígena, quilombola | exclusão dura, não peso |

Saída: mapa de aptidão em classes, **com os pesos na tela e editáveis**. Pesos escondidos
viram exatamente o "índice sintético com pesos arbitrários" que a rodada 4 derrubou.

---

## 6. Predição: o que tem rótulo de verdade

Aqui está a diferença entre este plano e a promessa genérica de "ML e predição".

### 6.1 O que tem rótulo real, datado e abundante

**Adoção de geração distribuída.** A base da ANEEL registra cada conexão **com data**.
Isso é um desfecho observado, datado, nacional e atualizado diariamente — não um proxy,
não 224 linhas.

- **Alvo:** novas conexões de GD por município por trimestre (contagem e kW).
- **Preditoras:** irradiação (LABREN), renda mediana e domicílios por tipo (Censo +
  CNEFE), penetração já existente, porte, distribuidora, tarifa.
- **Treino nacional, aplicação no Piauí.** São 5.570 municípios; treinar só nos 224
  desperdiça o que dá poder estatístico. Este é o ponto metodológico que separa um modelo
  útil de um enfeite.
- **Método:** começa em regressão com coeficientes legíveis; *gradient boosting* entra
  **como referência de comparação** — se ele ganhar muito, é sinal de não-linearidade que
  vale investigar, não licença para apresentar caixa-preta.
- **Validação que não mente:** o corte é **temporal**, não aleatório. Treina até T,
  prevê T+1. Validação aleatória num processo com difusão espacial e temporal infla o
  resultado e é o erro clássico deste tipo de dado.

**O alvo é censurado à direita, e isso precisa de regra — não de aviso.** Medido na série
trimestral do Piauí:

| | |
|---|---|
| último trimestre presente | **2026T2**, e a base fecha em **30/06/2026** |
| 2026T3 em diante | **ausente**, não zero |
| outubro/2025 | **300** conexões contra ~1.100 nos meses vizinhos — resíduo da migração SISGD → MMGD |

Um modelo treinado sobre isso aprende colapso. **Regra: só entram trimestres fechados
pela defasagem, e outubro/2025 entra marcado como observação degradada** — nem descartado
em silêncio, nem tratado como medição boa.

**E a queda de 2025 não é artefato.** O Piauí caiu de 22.177 para 15.721 conexões (−29%)
enquanto o Brasil ficou estável (909.303 → 906.480). A suspensão do sistema explica cerca
de um mês, não o ano. **É perda de participação do estado** — 2,44% para 1,73% —, e isso é
um fato comercial, não um defeito de dado. A tela de energia foi corrigida: ela afirmava a
causa errada.

### 6.2 O que ganhou base agora e estava congelado

**Série histórica.** Estava congelada porque *"o Censo tem uma medição"* — verdade, e
continua verdade. Mas **o SNIS tem série anual de água e esgoto desde 1995**. Não é a
mesma medição do Censo (SNIS é autodeclarado pelo prestador; o Censo pergunta ao
domicílio) e **não podem ser emendadas numa linha só** — mas é, sim, uma segunda fonte
longitudinal e independente.

O descongelamento é parcial e com regra: **duas séries, dois traços, duas legendas.**
Nunca uma linha que atravessa as duas definições.

**Custo unitário do simulador.** O SINISA traz investimento e atendimento por município e
por ano. Isso dá **ordem de grandeza publicável e citável** para custo por ligação — que
era exatamente o que faltava para o simulador deixar de ser "multiplicador de chute com
cara de engenharia". O campo continua editável; passa a ter referência com fonte.

### 6.3 O que continua sem base — e a lista não encolheu por otimismo

| | por quê |
|---|---|
| prever valor venal / PGV | barreira **legal**: exige ART de avaliador (CREA). Modelo não assina ART |
| prever cobertura do Censo no tempo | continua com uma medição só; o SNIS mede outra coisa |
| GD por bairro como medição | a ANEEL não desce de município. Modelado, sim; medido, não |
| "IA que descobre padrões" | com o que há, o que existe para descobrir já está no ranking e no agrupamento, ambos declarados |

---

## 7. Visualização e recomendação

O painel hoje responde *"como está"*. O repositório permite responder *"o que fazer"* —
e é aí que a recomendação tem de ser mais disciplinada, não menos.

**Recomendação é uma frase com três partes obrigatórias:** a ação, o número que a
sustenta com fonte, e a premissa que, se falsa, derruba a recomendação. Sem a terceira,
é palpite com tipografia boa.

> Priorizar GD em **Barras**: **17.827** domicílios em casa (CNEFE, tipo 101/102) contra
> **634** conexões de geração distribuída (ANEEL) — **3,56%**, a menor penetração entre os
> municípios de porte do estado, contra 13,20% em Teresina.
> *Premissa: tarifa do grupo B mantida; se a distribuidora reclassificar, a conta muda.*

Todos os números acima são medidos, não ilustrativos — a versão anterior deste plano
trazia um exemplo com valores inventados, o que é exatamente o que a regra da casa proíbe.
No estado inteiro são **1.246.467** domicílios em casa sem geração.

Camadas novas de tela, em ordem de valor:
1. **mapa de aptidão** (usina) e **mapa de mercado endereçável** (telhado)
2. **linha do tempo de adoção** por município, com o buraco de set–nov/2025 visível
3. **classificador de prioridade** — não uma nota, uma ordenação com o motivo ao lado
4. **comparador** entre municípios sobre qualquer base do repositório

---

## 8. Ordem

A janela do CIB é ~60 dias e não espera este plano. Então a ordem é por **valor por dia
gasto**, não por elegância:

| # | entrega | dias | por quê nesta posição |
|---|---|---|---|
| ~~1~~ | ~~ANEEL MMGD + tela de adoção~~ | ✅ | **feito em 18/09.** 90.528 conexões, 872,7 MW, 224/224 municípios |
| 1 | **BDGD + tarifas homologadas** | 1,5 | a rede de distribuição e o preço da energia. Sem os dois, o modelo correlaciona; com eles, explica |
| 2 | **Repositório em DuckDB/Parquet** com proveniência e linhagem | 1,5 | sem isto, cada base nova é um script órfão. É a fundação, e cobrar dela agora é mais barato que refazer depois |
| 3 | **LABREN + mercado endereçável de telhado** (CNEFE × irradiação × ANEEL) | 1,5 | primeira resposta que ninguém mais no mercado dá |
| 4 | **Modelo de adoção de GD** com validação temporal | 2 | a predição com rótulo real — agora com tarifa entre as preditoras, que é a variável causal |
| 5 | **SIGEL + aptidão para usina** com pesos declarados | 2 | produto distinto, cliente distinto |
| 6 | SNIS/SINISA: série histórica e custo unitário | 1 | descongela duas coisas do plano 27 |

**Parar depois da 1 e mostrar.** Se a conversa com o parceiro for sobre o que é possível,
a etapa 1 já responde com dado real — e responde melhor do que qualquer maquete.

---

## 9. Critério de aceite

1. Toda tabela do repositório tem `fonte`, `url`, `baixado_em`, `vigencia`, `licenca` e
   `sha256`. Linha sem isso não entra — conferido por teste, não por disciplina.
2. **Toda junção reporta a taxa de não-casamento.** Nenhuma junção silenciosa: se 10,4%
   não casou, o número aparece no relatório de carga.
3. Valor **medido**, valor **estimado** e valor **previsto** têm marcação visual distinta
   e legenda própria em toda tela. Um leitor que chegue por screenshot distingue os três.
4. **Ausência continua não sendo zero** — agora com mais bases e mais chances de errar.
   Teste: agregações sobre coluna com nulo devolvem nulo, nunca zero.
5. O modelo de GD é validado por **corte temporal**, e a tela mostra o erro fora da
   amostra junto do resultado.
6. O resíduo da migração da ANEEL (outubro/2025) aparece **marcado**, nunca interpolado,
   e a queda de 2025 é apresentada como **fato medido**, não atribuída à migração.
9. **Deriva de esquema falha alto.** Toda fonte guarda o hash da lista de colunas; se a
   coluna mudar, a carga **para** em vez de seguir com campo faltando. A ANEEL trocou de
   sistema (SISGD → MMGD) no meio de 2025 — fonte pública muda de forma, e descobrir isso
   por um número errado na tela é caro demais.
10. O alvo do modelo usa **apenas trimestres fechados** pela defasagem da fonte.
7. O painel continua abrindo **sem internet**, com o recorte JSON de hoje.
8. A licença do LABREN está resolvida por escrito antes de qualquer uso comercial.

---

## 10. Riscos

| risco | tamanho | o que fazer |
|---|---|---|
| **Licença do LABREN** veda reprodução comercial sem autorização | alto — pode travar produto pago | pedir autorização ao INPE agora, em paralelo |
| **LABREN indisponível e formato não confirmado** | médio, subiu na revisão | em 18/09 o site recusou conexão em 80 e 443. A lista de fontes afirma NetCDF/GeoTIFF; a evidência anterior indicava CSV e SHP. **Confirmar antes de planejar `xarray`.** Alternativas com licença melhor para uso comercial: **Global Solar Atlas** (CC-BY) e **NASA POWER** (domínio público) |
| Irradiação pode não discriminar dentro do PI | médio | o estado é uniformemente de alta irradiação; se a variação intraestadual for pequena, ela **não ordena municípios** e sai do caminho crítico do produto do Piauí. Medir antes de depender dela |
| Repositório vira fim em si e a janela do CIB fecha | alto | a ordem da §8 existe para isso: etapa 1 em um dia, mostra, decide |
| ANEEL só desce a município e a tela sugere bairro | médio | marcação obrigatória (critério 3); modelado ≠ medido |
| SINISA autodeclarado tratado como medição | médio | duas séries, dois traços, nunca emendadas |
| Prometer "IA" e entregar regressão | médio | é o oposto: chamar regressão de regressão é o diferencial perante TCE |
| Volume: dezenas de bases × histórico | baixo | Parquet e DuckDB resolvem; o gargalo é geografia, não bytes |

---

## 13. Rodada 10 — a revisão que mudou o plano (18/09/2026)

Dois revisores independentes, ambos sem crédito de cliente: **qwen3-coder:30b** local
(custo zero) e **DeepSeek v4-pro** pelo OpenRouter, na chave própria do usuário
(~US$ 0,004). GLM segue fora até 22/09.

### 13.1 Onde os dois convergiram — e eu também

**A fundação em DuckDB não vale agora.** Três leituras independentes chegaram ao mesmo
lugar. O DeepSeek foi o mais direto: *"resolve um problema que você ainda não tem. O
problema real agora é vender, não engenheirar. Quando tiver 3 contratos e 10 fontes, aí
o custo da desorganização supera o de construir."*

**Aceito.** A etapa 2 do §8 sai do caminho crítico. O que sobrevive dela é pequeno e
entra quando a próxima fonte chegar: um carregador compartilhado com proveniência e
conferência de deriva de esquema — que teria evitado o defeito do `CREATE VIEW` de hoje.
Não um armazém.

**Energia é segundo produto, não extensão do primeiro.** Também três vozes.
O DeepSeek desenhou a separação melhor do que eu: *"o comprador do art. 266 é prefeito
com medo de improbidade; o comprador de GD é integrador solar ou distribuidora — outro
ciclo, outro orçamento, outro decisor."* E fechou: *"guarde os dados, volte em janeiro."*

**Aceito.** O que já está construído fica: quatro fontes ingeridas, uma tela, tudo
documentado. **Não se constrói mais energia antes da janela de assinatura fechar.**

### 13.2 O achado sobre o BDGD, que corrige meu entusiasmo

*"Vale mais — para a distribuidora, não para a prefeitura. O art. 266 fala de imóvel
urbano, não de unidade consumidora de energia. Para a prefeitura, zero interesse."*

Correto, e é a distinção que eu não tinha feito com clareza. A lista de 3.284 PJ sem
geração é **lead qualificado para a Equatorial**, não argumento para secretaria de
finanças. Reforça 13.1: persegui-la é vender outro produto a outro comprador.

### 13.3 O achado 5 — a premissa está errada, o raciocínio sobrevive

O DeepSeek levantou o melhor ponto da revisão: *"sua restrição não é técnica, é
orçamentária. Se o município arrecada R$ 80 mil de IPTU no ano inteiro e está em
novembro, o orçamento já foi empenhado."* E concluiu que o mercado não seriam 224
municípios, mas os ~30 que arrecadam acima de R$ 100 mil.

**A conclusão está errada, e dá para medir.** IPTU não é capacidade de pagar — RCL é, e
o próprio painel diz isso na definição do indicador:

| segmento | n | RCL mediana | menor RCL |
|---|---|---|---|
| A | 9 | R$ 327,7 mi | R$ 193,4 mi |
| fronteira | 21 | R$ 96,1 mi | R$ 42,2 mi |
| **B** | **194** | **R$ 41,3 mi** | R$ 5,6 mi |

Um contrato no limite de dispensa de 2026 — **R$ 65.492,11**, não os R$ 59,9 mil de 2025
que ele citou — representa **0,16% da RCL mediana do segmento B**, e 1,17% no pior caso.
**O dinheiro existe.**

**Mas o raciocínio por trás sobrevive, e fica mais afiado do que ele o formulou.**
Acessível não é o mesmo que disponível: a pergunta não é se cabe na RCL, é se há
**dotação não empenhada em novembro**. Isso **não se responde com dado aberto** — é
pergunta para secretário, na primeira ligação.

E há um segundo achado que saiu da mesma medição: **só 122 dos 194 municípios do
segmento B têm RCL reportada.** Os outros 72 são justamente os que não entregaram RREO
2025. Ou seja, **os municípios que mais precisam do produto são os que eu não consigo
qualificar** — a não-entrega é ao mesmo tempo a justificativa da venda e o ponto cego da
qualificação.

### 13.4 Onde ele errou na premissa por falta de um número

*"Perda de participação do Piauí é sinal de mercado fraco."* — mesma premissa do revisor
local, e refutada pela medição da §11 da metodologia: a penetração residencial do Piauí é
**7,42% contra 5,19% do Brasil**, 43% acima. O pacote de revisão foi escrito antes dessa
medição existir; nenhum dos dois tinha o número.

**Mas o conselho de comunicação dele é certo mesmo com a premissa errada:** *"prefeito
ouve 'Piauí perdeu participação' e pensa 'então aqui também não tem mercado'. Use
internamente, nunca em slide de venda."* Vale.

### 13.5 O que muda no plano

| era | fica |
|---|---|
| etapa 2 — repositório DuckDB, 1,5 dia | **adiado.** Um carregador compartilhado quando a próxima fonte chegar |
| etapas 3 a 6 — LABREN, modelo, SIGEL, SNIS | **congeladas até a janela fechar.** Volta em janeiro |
| ordem por valor por dia | **a pergunta orçamentária vem antes de qualquer código** |

**Próxima ação, e não é técnica:** descobrir em quantos municípios do segmento B existe
dotação disponível para contratar ainda em 2026. É uma ligação, não um script.

---

## 14. Rodada 10, segunda volta — o GLM entrou pelo OpenRouter (19/09/2026)

O plano do Z.ai segue esgotado até 22/09, mas **o motivo de não usar OpenRouter caiu**:
o CLAUDE.md o desaconselha porque *"o plano cobre; pagar por token é desperdício"* — e o
plano não está cobrindo. A restrição dos termos do Coding Plan vale para chamar **o
endpoint da Z.ai** de script próprio, não para o OpenRouter, que é outro provedor.

Custo: **US$ 0,013**. A falha documentada apareceu como previsto — **12.408 caracteres de
raciocínio para 1.830 de resposta**. Com `max_tokens` folgado (6.000) a resposta veio
inteira; com o padrão, teria voltado vazia.

### 14.1 Onde ele confirmou o que já se sabia

**Fundação e energia como produto: terceira e quarta confirmações.** Acrescentou um
detalhe prático: *"1,5 dia com 5 scripts legados vira 3–4 na prática"*. E sobre a queda de
participação, repetiu o conselho do DeepSeek — **não colocar no pitch**, usar como
evidência interna.

### 14.2 A ideia que ninguém tinha tido, e que já virou ficha

> *"O único uso que acelera a venda atual é cruzar as 4.230 unidades PJ do BDGD com o
> cadastro municipal: imóveis econômicos fora do IPTU = receita recuperável, convertendo o
> pitch de 'prazo legal' (medo) em 'dinheiro' (ganho)."*

**Testado no dado, e o resultado é forte:**

| município | UC PJ de média/alta tensão | carga | IPTU no ano |
|---|---|---|---|
| **Geminiano** | 59 | 338 kW | **R$ 0** |
| **Simões** | 13 | 92 kW | **R$ 0** |
| **Santa Filomena** | 14 | **912 kW** | **R$ 780** |
| Cajueiro da Praia | 27 | 1.496 kW | R$ 22.047 |
| Ribeiro Gonçalves | 26 | 1.824 kW | R$ 32.663 |

Ligação de média tensão é **comércio ou indústria**, não residência. A mediana estadual é
R$ 13.251 de IPTU por unidade dessas; nos casos acima é zero ou quase.

**Entrou nas fichas** como *"abertura por receita, não por prazo"*, com as duas ressalvas
coladas: a base é **só PJ de média e alta tensão**, e IPTU baixo **também pode ser política
de isenção**. Por isso a ficha manda **perguntar**, não acusar.

### 14.3 Onde ele errou — o mesmo erro do DeepSeek

*"194 municípios com IPTU < R$ 100 mil dificilmente têm dotação"*. Já medido e refutado
(§13.3): IPTU não é capacidade de pagar. A RCL mediana do segmento B é **R$ 41,3 milhões**
e o contrato é **0,16%** dela. Dois revisores independentes cometeram o mesmo erro, o que
sugere que **a confusão IPTU × capacidade é intuitiva** — e que o material de venda
precisa desarmá-la explicitamente.

### 14.4 Os dois riscos novos, e o segundo é o mais sério do dia

1. **O art. 266 tem sanção efetiva?** Se a obrigação não traz penalidade, o prazo não
   compele, e o produto inteiro apoia-se num "deve" sem consequência. **Não verificado.**
2. **E se o estado, ou a APPM, fizer convênio em bloco?** *"Se fizer, seus 224 clientes
   viram 1."*

O segundo inverte uma leitura do projeto. O consórcio aparecia como **oportunidade** — o
art. 75 §2º dobra o limite de dispensa para consórcios públicos, o que favorecia o canal
APPM. Ninguém tinha olhado o mesmo fato como **ameaça**: o mesmo mecanismo que dobra o
contrato pode consolidar a demanda num comprador só, com poder de preço.

**Recomendação:** as duas viram pergunta da primeira ligação à APPM — antes de qualquer
esforço de canal. E a sanção do art. 266 é leitura de texto legal, não pesquisa de campo:
resolve-se numa tarde.
