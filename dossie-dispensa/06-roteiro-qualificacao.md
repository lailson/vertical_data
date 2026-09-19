# Roteiro de qualificação — a ligação que decide a ordem

**Data:** 2026-09-18 · **Origem:** rodada 10 (`analise/28` §13)

Este roteiro existe porque a revisão externa acertou uma coisa que nenhum dado aberto
responde: **a restrição não é preço, é dotação.**

Está medido que o preço não é o obstáculo. Um contrato no limite de dispensa de 2026 —
**R$ 65.492,11** — representa **0,16% da RCL mediana** do segmento B (R$ 41,3 milhões), e
1,17% no pior caso. **O dinheiro existe.** O que não se sabe é se, em novembro, ainda há
**dotação não empenhada** num elemento que sirva.

Essa pergunta não tem fonte pública. Tem telefone.

---

## 1. Para quem ligar

O plano diz que o cliente é **o ordenador de despesa sem equipe**. Mas quem sabe da
dotação não é ele — é o **contador** ou o **secretário de finanças**. Em município do
segmento B costumam ser a mesma pessoa, ou o contador é terceirizado e atende vários.

**Ordem prática:** secretaria de finanças → contador → prefeito. Chegar no prefeito antes
de saber se há dotação é gastar a única conversa que ele vai dar.

---

## 2. A ligação, em quatro portas

O roteiro é desenhado para **terminar cedo quando for não**. Cada porta que fecha poupa a
janela para o próximo município.

### Porta 1 — a obrigação é conhecida?

> "O senhor já foi informado que, pela Lei Complementar 214, todo imóvel urbano do
> município precisa estar inscrito no Cadastro Imobiliário Brasileiro até 31 de dezembro?"

- **"Já, estamos tratando"** → pergunte com quem. Pode ser incumbente. Vá à porta 2.
- **"Não sabia"** → é a melhor porta que existe. **Não venda ainda.** Explique em duas
  frases e pergunte se pode mandar por escrito. A venda é da segunda conversa.
- **"Isso não se aplica aqui"** → aplica. Não discuta na ligação; mande o art. 266.

### Porta 2 — já existe alguém fazendo?

> "Hoje o cadastro imobiliário roda em algum sistema contratado?"

A ficha diz se há **host municipal da Foxinline** detectado. É evidência forte para
presença e fraca para ausência — se a ficha disser que há, confirme; se disser que não,
**não afirme que não há**.

- **Tem fornecedor** → a pergunta muda: *"o contrato atual cobre a remessa ao CADURB?"*
  Quase nunca cobre. O produto vira complemento, não substituição.
- **Não tem** → siga.

### Porta 3 — a dotação (é esta a ligação)

> "Para contratar um serviço de consultoria e remessa de dados neste exercício, existe
> saldo em elemento de serviços de terceiros — pessoa jurídica? Ou precisaria de
> suplementação?"

O elemento típico é **3.3.90.39**. O que se quer saber, em ordem:

1. **Há saldo não empenhado?** Se sim, a contratação cabe em 2026.
2. **Se não, dá para suplementar?** Suplementação por decreto é rápida; por lei, não cabe
   na janela.
3. **Quantos dias leva a dispensa aqui?** Inclua o aviso de intenção do **art. 75, §3º**
   da Lei 14.133 — ele consome prazo e é obrigatório.

**Se a resposta for "só no orçamento do ano que vem":** isso **não é um não**. É um sim
com data. Anote e volte em janeiro — e registre, porque muda a previsão inteira.

### Porta 3-bis — a abertura que vale mais que a dispensa

Se em algum momento ele perguntar **"e como vocês sabem se o nosso cadastro está bom?"**,
essa é a melhor pergunta da ligação. A resposta não é uma promessa — é um pedido:

> "Me manda 200 linhas do cadastro, sem nome e sem CPF, e eu devolvo em dois dias um laudo
> dizendo o que passaria e o que a Receita recusaria."

O texto pronto está em `entregaveis/pedido-amostra-cadastro.md`. **Duas coisas que não
podem faltar no pedido:** que a inscrição pode vir mascarada **desde que duas linhas
iguais continuem iguais** — sem isso a regra de duplicidade não roda, e é ela que acha o
defeito mais comum —, e que **nome e documento ficam de fora**, para não levantar LGPD
num favor de dez minutos.

**E se a resposta for "nosso sistema não exporta":** isso é resposta, e das boas. Cadastro
que não sai do sistema é remessa que não vai sair. Anote como sinal, não como recusa.

### Porta 4 — quem assina

> "A dispensa é assinada pelo prefeito ou há delegação para a secretaria?"

Sem essa resposta não há proposta, só conversa.

---

## 3. O que a ficha traz, e o que cada número serve para dizer

| número | de onde vem | para que serve na ligação |
|---|---|---|
| **endereços no CNEFE** | IBGE, Censo 2022 | **o mais importante.** É o tamanho da remessa. Diz-se: *"são N imóveis a inscrever"*, e o interlocutor reconhece a ordem de grandeza da própria cidade |
| domicílios, população | Censo 2022 | contexto |
| IPTU e ITBI 2025 | SICONFI/RREO | só se ele perguntar de receita. **Não abrir com isto** no segmento B — a venda não é arrecadação |
| RCL 2025 | SICONFI/RREO | responde "não temos dinheiro" com ordem de grandeza, sem confrontar |
| entrega do RREO 23/24/25 | SICONFI | uso **interno**. Quem não entrega há três anos provavelmente não executa contrato |
| incumbente Foxinline | Certificate Transparency | porta 2 |
| CIB transmitido | RFB/Sinter | no Piauí é zero em 223 de 224. É o fato que sustenta a urgência |

---

## 4. Ordem de chamada — e o que ela não é

A ficha vem ordenada por um **índice declarado**, com três fatores e pesos visíveis:

| fator | peso | por quê |
|---|---|---|
| entregou RREO 2025 | 3 | sinal mais forte de que existe gestão capaz de executar contrato |
| sem incumbente detectado | 2 | menos atrito |
| volume de endereços (quintil) | 1 | tamanho do contrato |

**A RCL ficou de fora de propósito.** Foi medida e não discrimina: o contrato é 0,16% dela
na mediana. Incluir capacidade financeira num índice em que ela nunca é o obstáculo seria
teatro de rigor.

**E o índice não prevê dotação** — que é justamente o que decide. Ele ordena **quem
atender primeiro**, não quem vai comprar.

---

## 5. O ponto cego, declarado

**72 dos 194 municípios do segmento B não entregaram o RREO 2025** — e por isso não têm
IPTU, ITBI nem RCL nesta base. São, ao mesmo tempo:

- os que **mais precisam** do produto (não entregar demonstrativo é o mesmo sintoma de não
  ter cadastro em ordem), e
- os que **menos consigo qualificar** antes de ligar.

Para eles a ficha vem com os campos fiscais em branco, e isso é informação — não é falha.
A ligação com esses 72 tem de começar pela porta 1, sem número fiscal na mão, e a primeira
pergunta útil é outra: *"quem responde pela contabilidade hoje?"*
