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
| **ANEEL — MMGD** ([portal](https://dadosabertos.aneel.gov.br/dataset/relacao-de-empreendimentos-de-geracao-distribuida)) | cada empreendimento de micro/minigeração: fonte, potência em kW, **data de conexão**, classe, distribuidora | **município** | CSV e **Parquet**, atualização **diária**. ⚠️ houve **interrupção de 23/09 a 13/11/2025** na migração SISGD → MMGD: buraco na série que precisa aparecer no gráfico, não ser interpolado |
| **LABREN / INPE — Atlas Solar** ([portal](https://labren.ccst.inpe.br/atlas_2017.html)) | irradiação global horizontal, direta normal, plano inclinado, difusa | grade + **sedes municipais** | CSV e SHP. ⚠️ **licença restringe reprodução para fim comercial sem autorização do INPE** — usar como *insumo* citando a fonte é permitido; republicar a base, não. Isto precisa de decisão antes de virar produto pago |
| **SNIS / SINISA** ([resultados](https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/sinisa/resultados-sinisa/resultados-sinisa-2025)) | água, esgoto, resíduos, drenagem, gestão — **série desde 1995** | município, **autodeclarado pelo prestador** | O SNIS encerrou em 2023; o **SINISA** assumiu em 2024. Em 2024, **3.396 de 5.570** municípios têm todos os componentes — ausência é a regra, não a exceção |
| **ANEEL — SIGEL / SIGET** ([portal](https://dadosabertos-aneel.opendata.arcgis.com/)) | subestações, linhas de transmissão, usinas | **geometria** | SHP/GeoJSON/KML. É o que torna possível falar de usina em solo |
| **CNEFE 2022** (já no repositório) | 1,89 mi de endereços no PI, coordenada, **tipo de edificação** | **endereço** | já baixado e agregado |
| **Censo 2022** (já no repositório) | renda, domicílios, entorno | bairro / município | já baixado |
| **SICONFI / RREO** (já no repositório) | IPTU, ITBI, RCL, 2023–2025 | município | já baixado |

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

> Priorizar GD em **Piripiri**: 34.533 endereços, 8.200 com telhado próprio e sem
> geração, irradiação 5,7 kWh/m²·dia. *Premissa: tarifa do grupo B mantida; se a
> distribuidora reclassificar, a conta muda.*

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
| 1 | **ANEEL MMGD ingerida** + tela de adoção de GD no PI | 1 | dado real, atualização diária, e é o assunto que ele quer ver. Prova o conceito sem prometer nada |
| 2 | **Repositório em DuckDB/Parquet** com proveniência e linhagem | 1,5 | sem isto, cada base nova é um script órfão. É a fundação, e cobrar dela agora é mais barato que refazer depois |
| 3 | **LABREN + mercado endereçável de telhado** (CNEFE × irradiação × ANEEL) | 1,5 | primeira resposta que ninguém mais no mercado dá |
| 4 | **Modelo de adoção de GD** com validação temporal | 2 | a predição com rótulo real |
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
6. O buraco da ANEEL (23/09–13/11/2025) aparece como **falha na série**, nunca
   interpolado.
7. O painel continua abrindo **sem internet**, com o recorte JSON de hoje.
8. A licença do LABREN está resolvida por escrito antes de qualquer uso comercial.

---

## 10. Riscos

| risco | tamanho | o que fazer |
|---|---|---|
| **Licença do LABREN** veda reprodução comercial sem autorização | alto — pode travar produto pago | pedir autorização ao INPE agora, em paralelo; ter alternativa (Global Solar Atlas, NASA POWER) mapeada |
| Repositório vira fim em si e a janela do CIB fecha | alto | a ordem da §8 existe para isso: etapa 1 em um dia, mostra, decide |
| ANEEL só desce a município e a tela sugere bairro | médio | marcação obrigatória (critério 3); modelado ≠ medido |
| SINISA autodeclarado tratado como medição | médio | duas séries, dois traços, nunca emendadas |
| Prometer "IA" e entregar regressão | médio | é o oposto: chamar regressão de regressão é o diferencial perante TCE |
| Volume: dezenas de bases × histórico | baixo | Parquet e DuckDB resolvem; o gargalo é geografia, não bytes |
