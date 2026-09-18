# Plano — modo demonstração ("as possibilidades", com dado fictício)

**Data:** 2026-09-18 · **Status:** plano, aguardando execução
**Origem:** pedido do parceiro — *"Tem como aqui tu colocar as possibilidades com dados
imaginários?"*, sobre o protótipo `painel-gestao-municipal (1).html`
**Plateia decidida:** o parceiro, para validar a ideia. Não é material de venda.

---

## 1. O que ele está pedindo, de fato

O protótipo original tinha onze telas. O painel de hoje tem onze também, mas **não são
as mesmas**: seis capacidades do protótipo foram congeladas com motivo declarado e
vivem na tela *Fora da v1*. São exatamente essas seis que ele quer ver de novo:

| congelado | por quê foi congelado |
|---|---|
| Simulador de investimento | falta custo unitário auditável |
| Status CERURB / da remessa | depende de convênio; CERURB fora do caminho crítico |
| Educação viva (INEP) | ordem do M0 — entra depois do conector |
| PGV e valor de referência | exige ART de avaliador (CREA) |
| ML e chat | ferramenta interna, nunca promessa contratual |
| Série histórica | o Censo tem **uma** medição; série seria inventada |

Então o pedido não é "inventa uns números". É: **mostra o produto depois do contrato
assinado**, que é justamente o que ainda não tem dado.

---

## 2. A regra que governa — e por que ela não proíbe isto

A regra do projeto não é "nada de dado fictício". É mais precisa, e está escrita na
própria tela *Fora da v1*:

> **nenhuma tela com dado fictício em bairro nomeado**

Ela nasceu de um caso concreto: o protótipo dizia que **Mocambinho** tinha 36% de
pavimentação. O real é **99,6%** — erro de 63,6 pontos *na direção errada*, que
qualquer gestor de Teresina identifica em segundos.

O defeito ali não foi a ficção. Foi a ficção **vestida com um nome real**. Um número
inventado sobre um lugar que existe é uma afirmação falsa sobre o mundo; um número
inventado sobre um lugar que não existe é uma maquete.

Daí a decisão de desenho deste plano.

---

## 3. Decisão: dois regimes, não um

| regime | o que a tela afirma | onde roda |
|---|---|---|
| **Projeção** | "se você investir X, sai de A para B" — parte de um número **medido** e projeta com parâmetros visíveis | município **real**, escolhido no seletor |
| **Maquete** | "é assim que a tela fica" — afirma um estado presente que ninguém mediu | município **inventado**, e só nele |

O simulador é projeção: o ponto de partida ("Teresina, esgoto 32,2%") é dado real do
Censo, e o resultado é função de parâmetros que aparecem na tela e que o leitor pode
mexer. Isso não é uma afirmação falsa sobre o presente — é aritmética declarada.

Status da remessa, série histórica, educação e PGV são maquete: afirmariam um estado de
mundo que não foi medido. Vão para o município inventado.

---

## 4. O município inventado

**Serra do Meio (PI)** · código IBGE **2299999** · 14 bairros

- O código é **impossível** por construção: os 224 municípios reais do PI estão
  catalogados e nenhum termina em `99999`. Quem cruzar com qualquer base oficial não
  acha nada — que é o efeito desejado.
- O nome não colide com nenhum dos 224 (verificado).
- Nos bairros, nomes inventados sem paralelo em Teresina ou Parnaíba.

### Como o dado é gerado

Fictício **não quer dizer arbitrário**. O gerador é calibrado nas distribuições reais
que já estão no repositório:

- uma variável latente de centralidade por bairro governa renda, esgoto, pavimentação e
  iluminação **na mesma direção e com a mesma força** observadas nos 479 bairros reais
  — senão o k-means não acha três grupos e o gráfico renda × esgoto não se parece com
  nada;
- os números fiscais saem das medianas reais do PI para um município daquele porte;
- geometria: malha sintética de 14 polígonos, gerada por semente fixa.

**Consequência prática:** a demonstração se comporta como um município de verdade —
o ranking ordena, os quintis separam, o scatter tem a nuvem certa — sem ser um.

---

## 5. Arquitetura: um conjunto de dados, não um segundo aplicativo

O protótipo antigo era um arquivo separado, e por isso divergiu do produto. Aqui não.

```
demo/gerar_demo.py        → demo/dados/serra-do-meio.json   (mesmo formato do build_dados)
painel/index.html?demo    → carrega o extra e destrava as telas de demonstração
```

**A ficção não entra no conjunto real.** `painel/dados/` continua com 224 municípios e
479 bairros. Serra do Meio só existe quando a flag está ligada.

Vantagem: as telas que já existem (mapa, ranking, perfis, território) renderizam o
município inventado **sem uma linha de código nova**, porque ele tem o formato que elas
já sabem ler. O trabalho novo é só o das telas que não existem.

---

## 6. Telas, em duas etapas

### Etapa 1 — as duas que carregam a conversa

**`#simulador` · Simulador de investimento** (regime projeção, município real)
Move o investimento e vê a cobertura mudar no mapa e no ranking. As premissas ficam
**na tela, editáveis**: custo por ligação, prazo, taxa de adesão. O aviso não é rodapé,
é etiqueta no próprio número: *custo unitário é parâmetro, não medição*.
Sem isso, é um multiplicador de chute com cara de engenharia — que foi exatamente o
motivo do congelamento.

**`#remessa` · Status da coleta e da remessa** (maquete, Serra do Meio)
O painel depois do contrato: coletados / validados / aceitos no CADURB / recusados —
e os recusados **quebrados pela regra que falhou**, usando o vocabulário real do
validador (`CEP fora dos prefixos do município`, `NI do titular inválido`,
`areaTerreno ausente`). Mapa por setor com o progresso.
É a tela mais próxima do que se vende de fato.

### Etapa 2 — as maquetes de forma

**`#serie`** · série histórica, com o aviso de que o Censo tem uma medição só
**`#educacao`** · evasão e cobertura escolar — com a nota de que o dado **existe**
(INEP, 537 MB, baixável) e o que falta é ingestão, não fonte
**`#pgv`** · valor de referência — com a nota de que exige ART de avaliador
**`#risco`** · modelo de risco de não-entrega — **não é maquete, roda em dado real**
(ver §11) · **`#pergunte`** · chat sobre os 224 municípios, com a regra de que o
modelo escolhe a consulta e nunca produz o número (§11.5)

---

## 7. A fronteira, e como ela sobrevive a um screenshot

A plateia é o parceiro, mas **um link encaminhado perde o contexto da conversa** — e
foi assim que Mocambinho circulou. Então, mesmo no regime mais leve:

1. faixa persistente no topo, presente em qualquer recorte, inclusive a 360px;
2. o município inventado carrega o rótulo *município-modelo* no seletor, no título e
   no rodapé de fontes;
3. cada número de maquete nasce com marcação própria, não só aviso de rodapé;
4. a rota é `?demo` — o painel real nunca chega nela sozinho.

---

## 8. Critério de aceite

1. **Sem `?demo`, nada muda**: o painel busca exatamente os mesmos arquivos de hoje
   (verificável na aba de rede) e o contador segue **224 municípios · 479 bairros**.
2. **Nenhum bairro real nomeado exibe número que não venha de `build_dados.py`.**
   Verificação: varredura que cruza todo número renderizado em tela de bairro real
   contra o JSON de origem.
3. Toda tela de demonstração mostra a faixa de fronteira num recorte de 360×640.
4. `gerar_demo.py` é **determinístico**: duas execuções produzem arquivos idênticos
   (`sha256` igual).
5. O gerador reproduz a correlação renda × esgoto dos bairros reais dentro de ±0,1 de
   coeficiente — se não reproduzir, a maquete não passa por município.
6. A sonda de layout passa nas telas novas em **320 a 1920** (o mesmo teste que pegou
   o `all:unset`).
7. `python3 marca/aplicar.py --conferir` continua limpo; nenhuma cor nova fora dos
   tokens da marca.
8. O validador e o laudo **não são tocados** por este trabalho.
9. **Nenhuma feature do modelo de risco é derivada do RREO 2025** — a conferência é
   automática: se a feature estiver preenchida exatamente nos 152 que entregaram, ela
   é vazamento e o treino falha (§11.2).
10. O modelo publica **coeficiente, sinal e intervalo** por variável, e o erro fora da
    amostra (AUC por validação deixa-um-fora). Sem isso não vai para a tela.
11. **O chat nunca emite um número que não esteja no JSON.** Verificação: todo valor da
    resposta casa com o arquivo de origem; pergunta que não mapeia para o dado recebe
    recusa explícita, não uma aproximação.
12. Sem `?demo`, o painel continua **abrindo sem internet** — o chat é a única parte que
    exige rede, e a ausência dele não quebra nenhuma outra tela.

---

## 9. O que este plano NÃO faz

- **Não descongela nada.** As seis capacidades continuam fora da v1; a demonstração
  mostra a *forma* delas, e o texto de cada tela mantém o motivo do congelamento
  visível. Demonstrar não é prometer.
- **Não põe número inventado em Teresina, Parnaíba ou qualquer bairro real.**
- **Não vira material de venda** sem uma segunda passada: se a plateia mudar, o regime
  de projeção sobre município real precisa ser reavaliado, e a marcação endurecida.

---

## 10. Esforço

| etapa | o quê | tamanho |
|---|---|---|
| 0 | `gerar_demo.py` + dado sintético calibrado | meio dia |
| 1 | simulador + status da remessa | um dia |
| 2 | série, educação, PGV | meio dia |
| 3 | modelo de risco (dado real, §11.3) | um dia |
| 4 | chat sobre os dados (§11.5) | um dia |
| — | sonda de layout, fronteira, documentação, deploy | meio dia |

Ordem sugerida: **0 → 1 → mostrar ao parceiro → 2, 3, 4**. A etapa 1 já responde à
pergunta dele. A **3 é a que menos parece demonstração e mais parece produto**, porque
roda em dado real e devolve uma lista de quem ligar primeiro — pode ser antecipada se a
conversa for comercial e não conceitual.

---

## 11. IA, predição e chat — o que tem base hoje e o que continua teatro

O pedido original do projeto era "dashboard com ML, preditivo e chat". A rodada 1 matou
isso com uma frase dura e correta na época:

> **ML/preditivo/chat conversacional na v1 é teatro estatístico.** Com N≈1.800 imóveis,
> um município e sem série histórica, não há base para modelo preditivo defensável;
> chat sobre dados pequenos vira RAG de baixa qualidade.
> — `analise/parecer-r1-deepseek.md`, Achado 4

**Aquele veredito foi dado sobre outro conjunto de dados.** Vale reabrir o caso — com
cuidado, porque parte dele continua de pé.

### 11.1 O que mudou e o que não mudou

| | então (rodada 1) | hoje |
|---|---|---|
| unidades | 1 município, 18 bairros simulados | **224 municípios, 479 bairros reais** |
| endereços | — | **1.891.421** do CNEFE, todos com coordenada |
| série temporal | nenhuma | **RREO 2023/24/25** — três anos, no eixo fiscal |
| desfecho observado | nenhum | **entregou / não entregou**, por município, por ano |

O que **não** mudou: o Censo tem **uma** medição (2022). Não existe série de saneamento,
renda ou pavimentação. Toda previsão de *evolução de cobertura* continua impossível —
é o mesmo motivo pelo qual a série histórica está congelada, e não é um detalhe de
engenharia, é ausência de segunda observação.

Ou seja: **o eixo administrativo ganhou base para previsão; o eixo físico não.**

### 11.2 A armadilha que quase entrou — e já está medida

O alvo natural é *"quem não vai entregar a remessa até 31/12"*. As features óbvias
seriam porte, RCL, IPTU, ITBI, incumbente, bairros, CIB transmitido.

Medido neste repositório:

```
municípios com iptu preenchido ....... 152
municípios que entregaram RREO 2025 .. 152
são o mesmo conjunto? ................ True
```

**`iptu`, `itbi` e `rcl` saem do próprio RREO 2025.** Usá-los para prever a entrega do
RREO 2025 é vazamento de alvo: o modelo aprenderia que "quem tem IPTU preenchido
entregou", acertaria perto de 100% e não teria utilidade nenhuma — com a agravante de
parecer excelente. É o tipo de erro que só aparece depois, no cliente.

**Regra que fica:** feature só entra se existir **antes** do desfecho. Sobram as do Censo
2022, as entregas de 2023 e 2024, e o CIB da RFB — e essas estão completas nos **224**.

### 11.3 Uso 1 — risco de não entregar (tem base, roda em dado real)

Desfecho real, observado, rotulado: **152 entregaram, 72 não**. E o histórico sozinho já
carrega sinal legítimo:

| entregou em 2023, 2024 | entregou em 2025 |
|---|---|
| não, não | 52 de 101 · **51,5%** |
| não, sim | 17 de 21 · 81,0% |
| sim, não | 13 de 21 · 61,9% |
| sim, sim | 70 de 81 · **86,4%** |

Isto **não é demonstração** — é produto. Devolve a lista de quem ligar primeiro, que é
exatamente o que o painel já se propõe a fazer como instrumento de qualificação.

**Método:** regressão logística com **coeficientes publicados na tela**, não caixa-preta.
Com 224 linhas e ~9 variáveis, é o que o N suporta e o que o TCE aceita ler. GBM entra
só como referência de comparação, nunca como o número que se apresenta.

**Como não mentir:** a tela mostra o erro fora da amostra (AUC por validação
deixa-um-fora) ao lado do resultado. E previsão é sobre **comportamento
administrativo**, não sobre o mundo físico — errar aqui custa uma ligação à toa, não uma
afirmação falsa sobre um bairro.

### 11.4 Usos 2 e 3 — onde a IA realmente paga neste negócio

Não é no painel. É no caminho até a remessa aceita.

**Anomalia cadastral, além da regra.** O validador de hoje pega violação de regra: CEP
fora dos prefixos, DV de CPF inválido, campo ausente. Não pega o **estatisticamente
absurdo**: área construída maior que o lote, valor venal fora de qualquer ordem de
grandeza do entorno, mesmo endereço em duas inscrições. A rodada 7 registrou que o
validador ser *"apenas sintático"* é justamente o que dificulta sustentar o preço do
laudo. Isto é o que o torna semântico de verdade.

**Casamento de registros.** O gargalo real da remessa é cruzar a planilha do município —
logradouro abreviado, sem CEP, número com letra — contra os 1,89 milhão de endereços do
CNEFE. É trabalho de *entity resolution*: similaridade de texto com pontuação aprendida,
mais distância geográfica. Sem glamour e com o maior retorno de todos.

**No coletor:** foto do imóvel → leitura do número, sugestão de território × predial,
pré-preenchimento. Extração de PDF de cadastro antigo para campo estruturado. Reduz
tempo de campo, que é o custo dominante da operação.

### 11.5 Chat — não é RAG, é tradução de pergunta em consulta

O veredito da rodada 1 ("RAG de baixa qualidade") descrevia buscar trechos de documento
e pedir ao modelo que resuma. É de fato ruim, e não é o que cabe aqui.

O dado do painel é **tabular e fechado**: ~20 campos × 224 municípios × 479 bairros, com
nome, unidade e fonte conhecidos. Para isso existe um desenho melhor:

> **O modelo escolhe a consulta. O número vem do arquivo.**

O chat traduz *"quais municípios do sul arrecadam mais ITBI que IPTU e não entregaram
RREO?"* numa especificação de filtro e agregação. O painel executa contra o JSON e
renderiza. O modelo **nunca escreve um número** — ele escreve a pergunta em forma de
consulta, e toda resposta sai com campo, fonte e data de consulta, como o resto do
painel. Pergunta que não mapeia para o dado recebe recusa explícita, não uma
aproximação simpática.

Isso elimina a alucinação numérica por construção, e não por instrução ao modelo.

**Onde roda:** o painel hoje é estático e abre sem internet — e isso é uma propriedade,
não um acaso: a demonstração numa prefeitura não pode depender do wifi. O chat quebra
essa propriedade, então entra como **camada opcional**, numa Pages Function ao lado do
`_middleware.js` que já existe. Sem rede, o painel inteiro continua funcionando e só o
chat fica indisponível.

**Modelo:** Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) dá conta do mapeamento
pergunta → consulta, que é a tarefa dominante e barata; Claude Sonnet 5
(`claude-sonnet-5`) para pergunta que exige raciocínio sobre método. A chave é do
projeto — **nunca crédito de provedor que serve cliente**.

### 11.6 O que continua teatro, e por quê

| | por quê |
|---|---|
| **Prever valor venal / PGV** | barreira **legal**, não técnica: exige ART de avaliador (CREA) e metodologia publicável (IAAO / NBR 14653). Modelo não assina ART. |
| **Prever evolução de cobertura** | o Censo tem uma medição. Sem segunda observação, não há o que extrapolar. |
| **GBM ou rede neural como método de vitrine** | o que se apresenta ao TCE precisa ter coeficiente legível. Caixa-preta serve de referência interna, não de argumento. |
| **"IA que descobre padrões no seu município"** | com 479 bairros e 20 campos, o que há para descobrir já está no ranking e no k-means, ambos declarados. Chamar isso de IA é vender embrulho. |

### 11.7 Como isso entra na demonstração

- **`#risco`** — roda em dado real, com coeficientes e erro na tela. É a tela que menos
  parece demonstração e mais parece produto.
- **`#pergunte`** — chat sobre os 224 municípios reais. Também não é ficção: as respostas
  saem do mesmo JSON que o painel já usa.
- **Anomalia, casamento de registros e visão no coletor** — entram como **cartão de
  roteiro**, não como tela. São trabalho de back-office; demonstrá-los seria maquete de
  algo que se prova com um laudo, não com uma interface.

**Consequência para o escopo congelado:** dos seis itens, "ML e chat" deixa de estar
congelado *por falta de base de dados* — passa a estar **delimitado por método**. O
motivo declarado na tela *Fora da v1* precisa ser reescrito para dizer isso, senão o
painel contradiz o próprio produto.
