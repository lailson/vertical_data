# A linha do deck sai hoje, de fonte pública — o e-SIC à SEFAZ não é necessário para ela

## 1. O defeito no e-SIC nº 2, e por que ele mata o pedido

O texto pede à SEFAZ-PI: *"estimativa anual, por município, do IBS vinculado a operações com bens
imóveis para 2027–2032, com metodologia"* e *"impacto estimado da ausência de CIB sobre esses
repasses"*.

**Isso não é pedido de informação — é encomenda de estudo.** A LAI assegura acesso a **documento
existente**; pedido que exige elaboração autoriza a resposta "pedido indevido" — e o órgão ainda
consome os **15 + 10 dias** para dizer isso. São 25 dias queimados exatamente na janela em que o
número precisa estar no deck.

**Reformular:** manter só o item 1 (critério estadual de vinculação do IBS imobiliário, art. 11, II
da LC 214/2025 — isso é documental: portaria ou instrução, resposta rápida). Trocar os itens 2–3 por
pedido de **dado existente**.

## 2. O dado já está público — e na mesma chamada que já usamos

O **SICONFI/RREO Anexo 03 traz `ITBI` por município**, ao lado de `IPTU` e `ISS`. Testado hoje:

| Município | **ITBI 2025** | IPTU 2025 | ITBI/IPTU | ITBI/hab |
|---|---|---|---|---|
| Teresina | **R$ 60.780.169** | R$ 166.321.115 | 0,37 | R$ 69,98 |
| Parnaíba | R$ 3.189.881 | R$ 4.161.751 | 0,77 | R$ 19,56 |
| Picos | R$ 2.026.834 | R$ 7.062.110 | 0,29 | R$ 24,71 |
| **Floriano** | R$ 2.126.558 | R$ 1.208.395 | **1,76** | R$ 33,97 |
| **Bom Jesus** | R$ 1.771.552 | R$ 1.022.220 | **1,73** | R$ 61,39 |
| **Corrente** | R$ 1.172.231 | R$ 751.325 | **1,56** | R$ 42,75 |
| Piripiri | R$ 739.771 | R$ 1.533.757 | 0,48 | R$ 11,25 |
| Campo Maior | R$ 683.900 | R$ 1.043.286 | 0,66 | R$ 15,11 |
| Barras | R$ 262.456 | R$ 882.361 | 0,30 | R$ 5,48 |
| Paulistana | R$ 206.410 | R$ 558.221 | 0,37 | R$ 9,79 |
| **Altos** | R$ 143.990 | R$ 245.127 | 0,59 | R$ 3,08 |
| **Cocal** | R$ 106.109 | R$ 32.309 | **3,28** | R$ 3,77 |

**Zero e-SIC. Meia hora de trabalho. Os 152 municípios de uma vez, se quiser.**

## 3. O achado que sai de graça no caminho

**Em vários municípios do interior o ITBI já supera o IPTU** — Cocal 3,3×, Floriano 1,8×, Bom Jesus
1,7×, Corrente 1,6×, Ribeiro Gonçalves 1,4×.

Isso tem duas leituras, e as duas servem à venda:

1. **O tributo imobiliário que esses municípios efetivamente arrecadam é o ITBI, não o IPTU.**
   Reforça, por outro ângulo, a conclusão do dimensionamento: falar de IPTU no interior do PI é falar
   do tributo errado.
2. **ITBI é transação, e transação exige registro — que é onde o CIB entra.** A ligação com a dor do
   município fica direta: sem CIB, o registro trava; travando o registro, **trava a arrecadação que
   ele de fato tem**. Não é hipótese sobre IBS futuro: é a receita corrente dele, hoje.

**Isso é uma linha de deck melhor do que a que o e-SIC à SEFAZ ia buscar** — porque é receita
realizada e verificável, não estimativa de repasse futuro com ressalva.

## 4. Método declarável para a estimativa de exposição

Tudo auditável, sem pedir nada a ninguém:

```
base transacionada estimada = ITBI municipal ÷ alíquota de ITBI do município (2% típico)
exposição = base transacionada × fração do estoque sem regularidade registral
```

Para a fração sem regularidade, o Censo 2022 publica o corte de **domicílios próprios com e sem
escritura definitiva** — conferir o recorte municipal no SIDRA antes de usar (**pendência: o SIDRA
deu timeout nos testes anteriores; validar por download se necessário**).

"Nossa estimativa, método declarado, fontes oficiais" é mais forte num deck do que um número de
SEFAZ vindo com ressalvas — e chega em meio dia em vez de 25 dias.

## 5. O que fazer com o e-SIC nº 2
- **Manter** o item 1 (critério de vinculação do IBS) — documental, útil, barato.
- **Trocar** itens 2–3 por: *arrecadação de ITBI por município do PI, 2022–2025*, se a SEFAZ
  gerenciar arrecadação delegada — ou **simplesmente não pedir**, já que o SICONFI entrega.
- **Prioridade rebaixada.** Os pedidos que decidem alvo continuam sendo **SEAD/PROUrbe** (primeiro) e
  **RFB/SINTER** (denominador do mercado).
- **Incluir o texto que falta: TCE-PI — dispensas de software/geoprocessamento 2024–26.** É o único
  meio de conhecer preço praticado e concorrência antes de fixar a própria faixa, e alimenta o
  gatilho de comoditização abaixo de R$ 8 mil.
