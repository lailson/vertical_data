# As três pendências abertas — o que a medição disse (19/09/2026)

O `analise/25` §5 listava cinco itens. Dois fecharam com a coleta do TCE (§5.2 e §5.4,
ver `docs/metodologia-iv.md` §12.5). Estes são os três que sobravam.

**Nenhum dos três estava resolvível por pedido de dado.** Dois foram resolvidos medindo o
que já havia, e o terceiro mudou de natureza quando se olhou a premissa.

---

## 1. §5.3 — composição urbana × rural do ITBI no sul

### Contexto

Sete municípios do sul do Piauí — a fronteira agrícola do MATOPIBA — arrecadam **ITBI
acima de R$ 200 mil com IPTU abaixo de R$ 50 mil**. Santa Filomena arrecada **R$ 780 de
IPTU no ano inteiro e R$ 2,87 milhões de ITBI**.

A hipótese registrada: o ITBI vem de **terra rural**, não de imóvel urbano — logo o
número não indica mercado urbano, e o painel os marcava como *hipótese*, nunca alvo.

### O que a medição disse

Testável com o CNEFE, que conta estabelecimentos agropecuários por município:

| | os sete | os outros 129 |
|---|---|---|
| ITBI por endereço (mediana) | **R$ 139,70** | R$ 3,90 |
| razão | **36×** | — |
| endereços agropecuários (mediana) | **9,4%** | 13,0% |
| razão | **0,7×** | — |

**A versão simples da hipótese está errada.** Os sete **não** são mais agrícolas que o
resto — são *menos*, por proporção de endereços. O que os distingue é o ITBI por
endereço, 36 vezes maior.

**A leitura que sobrevive à medição:** não é volume de imóveis rurais, é **valor por
transação**. Terra de MATOPIBA vende em dezenas de milhões por fazenda; meia dúzia de
transferências num município de 3.381 endereços produz milhões de ITBI. *(Inferência: a
declaração de ITBI não traz contagem de transações, então o mecanismo não é medido —
apenas é o que resta consistente com as duas medidas acima.)*

**E o IPTU quase nulo é real.** Confirmado nas duas fontes independentes, ao centavo:
Santa Filomena R$ 780 no SICONFI e R$ 780 no TCE; Barreiras do Piauí R$ 200 nas duas.
Não é falha de preenchimento — é ausência de cadastro urbano.

### Recomendação — e ela inverte a anterior

O rótulo *"hipótese, não alvo"* protegia contra o erro certo (vender recuperação de IPTU
a quem arrecada ITBI rural) mas produziu a conclusão errada (afastar-se deles).

Medido: os sete têm **RCL de R$ 33 a 82 milhões**, empenham **R$ 3 a 18 milhões** em
serviços de terceiros PJ, e um contrato no limite de dispensa é **0,08% a 0,20% da RCL**.
Têm dinheiro. Têm a obrigação do art. 266 como todo mundo. E o cadastro urbano deles é
**comprovadamente inexistente**, por duas fontes.

> **São bons alvos de conformidade — e péssimos alvos de recuperação fiscal.**
> A recomendação é manter a marcação, mudando o que ela significa: não *"não procurar"*,
> e sim ***"nunca abrir a conversa por IPTU"***. Com eles o argumento é o prazo e a
> obrigação, e a capacidade de pagar está demonstrada.

**Fica aberto:** a contagem de transações que confirmaria o mecanismo. Não existe em dado
aberto; viria de uma conversa com a secretaria de finanças, não de um pedido de arquivo.

---

## 2. §5.5 — rodar o validador contra cadastro municipal real

### Contexto

*"É o único item que a venda não resolve: hoje a primeira execução real aconteceria no
cliente."* Não há cadastro municipal em mãos, e não haverá antes do primeiro contrato.

### O que foi feito

Não dá para simular cadastro honestamente — inscrição, valor venal, área e titular são
exatamente o que o município traz. **Mas endereço real existe, em volume.** O
`m0-conector/gerar_base_ensaio.py` monta uma base a partir do CNEFE com CEP, tipo e nome
de logradouro **como o IBGE os enumerou**, e deixa **vazios** os campos que o CNEFE não
tem — simulá-los seria inventar o cadastro.

Ensaio em **Floriano: 32.046 endereços**.

| o que se queria saber | resultado |
|---|---|
| aguenta o volume? | **1,1 segundo** para 32 mil |
| a tabela 9.6 cobre o logradouro real? | **32.046 de 32.046 convertidos** — cobertura total |
| o CEP casa com os prefixos do município? | **zero falhas** em 32 mil CEPs reais |
| aparece algo que ninguém previu? | **sim, ver abaixo** |

### O defeito que o ensaio encontrou

**7 endereços reprovaram por `bairro` acima de 30 caracteres** — o limite da spec.
O nome era `BARRA DA ITAUEIRA LADO ESQUERDO`, 31 caracteres, direto do IBGE.

Medido no estado inteiro: **7.058 de 1.891.421 endereços (0,37%), em 64 municípios.**

Quem montar o cadastro a partir da localidade do IBGE — e muitos vão, porque é a
referência disponível — terá 0,37% da remessa recusada por tamanho de campo. A correção é
trivial; **descobrir no cliente não é.**

### Recomendação

> **A pendência baixa de "risco alto" para "risco parcial, declarado".** A metade de
> endereço do validador foi exercitada com dado real em volume e passou, achando um
> defeito que ninguém tinha visto.
>
> **Continua sem ensaio real:** titularidade, dígito verificador, coerência territorial ×
> predial e valor venal — as regras que dependem de campos que só o município tem.
>
> **Próximo passo, e é barato:** pedir a **um** município uma amostra de 200 linhas do
> cadastro, anonimizada, antes de qualquer contrato. Duzentas linhas bastam para exercitar
> as dez regras, e o pedido é pequeno o suficiente para ser deferido numa conversa.

---

## 3. §5.1 — e-SIC à RFB: quem aderiu ao Sinter

### Contexto

*"Sem ele, o denominador do mercado permanece desconhecido."* O arquivo `adesoes.xls`
baixado do portal da RFB acabou não sendo lista de adesão.

### O que a verificação disse

Conferido na fonte: **a página do Sinter para municípios não publica lista de adesões.**
Oferece FAQ, um diagnóstico em formulário, estatística de imóveis urbanos, manual e
tutoriais — e um e-mail de contato, `sinter.df.cocad@rfb.gov.br`.

**Mas a premissa da pendência estava frouxa.** O que se tem é melhor do que parecia:
`inscricoes.csv` lista **188 municípios com inscrição ativa no CIB**, no país inteiro.
Transmitir implica ter aderido — logo **188 é piso de adesões**, e o denominador do
mercado (quem **não** transmitiu) é conhecido com exatidão: **5.382 de 5.570**.

O que a lista de adesões acrescentaria não é denominador, é **segmentação**: separar
*"assinou o convênio e parou"* — que é lead morno, já decidiu — de *"nem assinou"*.

### Recomendação

> **Reclassificar de "bloqueante" para "refinamento de segmentação".** O número que
> sustenta a venda — 5.382 municípios sem cadastro transmitido, e no Piauí **223 de 224** —
> já está medido e não depende deste pedido.
>
> **E trocar o instrumento:** antes do e-SIC formal, escrever para
> `sinter.df.cocad@rfb.gov.br` perguntando se a lista de convênios firmados é pública. É
> um e-mail, responde em dias, e a via formal continua disponível se o e-mail não andar.

---

## Resumo

| pendência | estado | próximo passo |
|---|---|---|
| §5.3 ITBI rural | **resolvida, e inverteu a recomendação** | nenhum — é decisão comercial agora |
| §5.5 validador real | **de risco alto para parcial declarado** | pedir 200 linhas anonimizadas a um município |
| §5.1 adesões Sinter | **rebaixada a refinamento** | um e-mail ao contato da RFB |
