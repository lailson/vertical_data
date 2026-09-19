# Pedido de amostra de cadastro — 200 linhas, antes de qualquer contrato

**Status:** rascunho. **Não enviado.**
**Origem:** `analise/30` §2 — o validador foi exercitado com 32.046 endereços reais do
CNEFE e passou, mas as regras que dependem de campos que só o município tem
(titularidade, dígito verificador, coerência territorial × predial, valor venal)
**continuam sem ensaio com dado real**.

**O que este pedido resolve.** Hoje, a primeira execução real do validador aconteceria
**no cliente**, durante a entrega. Duzentas linhas anonimizadas antecipam isso para antes
da proposta — e o custo de errar cai de "credibilidade na entrega" para "meia hora de
ajuste".

**Por que 200 e não a base inteira.** Duzentas linhas exercitam as dez regras e cabem num
anexo de e-mail. Pedir a base inteira levanta questão de LGPD, de autorização e de volume
— e tudo isso transforma um favor de dez minutos numa decisão de gabinete.

---

## A quem pedir

Ao **mesmo contato da porta 3** do roteiro de qualificação — o contador ou o secretário de
finanças —, **depois** de a conversa ter avançado, nunca na primeira ligação. Pedir dado
antes de ter dado algo é o que faz o telefone parar de ser atendido.

Momento certo: quando ele perguntar *"e como vocês sabem se o nosso cadastro está bom?"*.
A resposta é este pedido.

---

## Texto

> **Assunto:** Amostra de 200 linhas do cadastro imobiliário — diagnóstico sem custo
>
> Prezado(a),
>
> Conforme conversamos, consigo rodar um diagnóstico do cadastro do município contra o
> leiaute que a Receita Federal exige para o CIB, e devolver um laudo apontando o que
> passaria e o que seria recusado na transmissão.
>
> Para isso preciso de **uma amostra de 200 registros** do cadastro imobiliário, em CSV ou
> Excel, com estes campos — **sem nome e sem CPF/CNPJ do contribuinte**:
>
> | campo | observação |
> |---|---|
> | inscrição imobiliária | pode vir mascarada, desde que **duas linhas iguais continuem iguais** |
> | tipo do imóvel | territorial ou predial |
> | área do terreno, área construída | — |
> | valor venal | — |
> | tipo e nome do logradouro, número, bairro, CEP | — |
> | percentual de titularidade | se o sistema tiver |
> | ano de construção, tipo arquitetônico | se o sistema tiver |
>
> **Não preciso de nome nem de documento do contribuinte.** Se o sistema exportar esses
> campos junto, pode apagar as colunas antes de mandar — o diagnóstico não depende delas.
>
> As 200 linhas podem ser as primeiras do arquivo; não precisam ser escolhidas. Devolvo o
> laudo em até dois dias úteis, sem custo e sem compromisso.
>
> Atenciosamente,
> Lailson Henrique — Vertical Data

---

## Notas de uso (não enviar)

- **A mascaragem da inscrição precisa preservar a igualdade.** É o que permite rodar a R9,
  de unicidade — a duplicata de inscrição é o defeito mais comum de cadastro em planilha,
  e detectá-la é metade do valor do laudo. Se cada linha vier com um código aleatório
  diferente, a regra não roda.
- **Nome e documento ficam de fora de propósito.** Isso custa a regra R7 (dígito
  verificador), que continuará sem ensaio real. É troca consciente: pedir CPF numa amostra
  de cortesia levanta LGPD e trava o pedido.
- **Se a resposta for "nosso sistema não exporta"** — isso é resposta, e das boas. Dizer
  que o cadastro não sai do sistema é o mesmo que dizer que a remessa não vai sair. Anote
  no registro de ligações e trate como sinal, não como recusa.
