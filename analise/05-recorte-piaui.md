# Recorte Piauí — o dimensionamento que corrige os dois pareceres

O go-to-market definido pelo cliente é **Piauí primeiro, depois Ceará e Maranhão**. Ambos os
pareceres (Anexos E e F) foram escritos sobre um mercado genérico de 5.570 municípios. Medi o
mercado real do PI com dado público. **Os números mudam o modelo comercial.**

## 1. Arrecadação de IPTU nos 224 municípios do Piauí (SICONFI, 2025, 12 meses móveis)

Consultei os **224 municípios**, obtive retorno para **224**.

| Posição | Município | IPTU 2025 | População | R$/hab |
|---|---|---|---|---|
| 1 | **Teresina** | R$ 166.321.115 | 868.523 | 191,50 |
| 2 | Picos | R$ 7.062.110 | 82.028 | 86,09 |
| 3 | Parnaíba | R$ 4.161.751 | 163.087 | 25,52 |
| 4 | São Raimundo Nonato | R$ 1.675.238 | 39.036 | 42,92 |
| 5 | Piripiri | R$ 1.533.757 | 65.762 | 23,32 |
| 6 | Floriano | R$ 1.208.395 | 62.593 | 19,31 |
| 7 | Oeiras | R$ 1.099.628 | 38.192 | 28,79 |
| 8 | Campo Maior | R$ 1.043.286 | 45.252 | 23,06 |
| 9 | Bom Jesus | R$ 1.022.221 | 28.857 | 35,42 |

### A distribuição é o achado

| Métrica | Valor |
|---|---|
| **Mediana de IPTU no PI** | **R$ 2.214,26 por ano** |
| Municípios com IPTU < R$ 100 mil/ano | **194 de 224** |
| Municípios com IPTU < R$ 500 mil/ano | **212 de 224** |
| Municípios com IPTU > R$ 1 mi/ano | **9 de 224** |

A mediana não está em milhares: o município mediano do Piauí arrecada **dois mil duzentos reais por
ano** de IPTU. Teresina sozinha responde por mais que todos os outros 223 somados.

## 2. Consequência 1 — o fee de eficiência sobre IPTU NÃO funciona no Piauí

O parecer de negócio (Anexo F, Achado 4; Anexo G, Achado 6) propõe remuneração de **10–15% sobre o
incremento de IPTU acima do baseline SICONFI**, com exemplo de município com IPTU₀ = R$ 20 mi.

**No Piauí, esse município praticamente não existe.** Só Teresina e Picos passariam perto. Num
município com IPTU de R$ 2 mil/ano, 15% de um incremento de 100% são **R$ 300**. O modelo de
eficiência é matematicamente inaplicável a 212 dos 224 municípios do estado.

**Correção:** no beachhead PI, a remuneração tem de ser **preço fixo**. O fee de eficiência fica
reservado a Teresina, Picos, Parnaíba e às capitais de CE e MA (Fortaleza, São Luís) — onde a base
existe.

## 3. Consequência 2 — "aumentar a arrecadação do IPTU" é o argumento errado no interior do PI

A proposta original tem como objetivo declarado aumentar a arrecadação de IPTU. No interior do
Piauí **não há IPTU a aumentar** — e há uma razão política que nenhum modelo resolve: prefeito de
município pequeno **não vai instituir cobrança efetiva de IPTU sobre eleitor de baixa renda**. Vender
recuperação fiscal ali é vender um problema, não uma solução.

**O argumento que funciona no PI é outro: conformidade legal obrigatória.** O CIB vence em
**01/01/2027** para os 224 municípios, independentemente de quanto cada um arrecada. É dever legal,
não oportunidade de receita.

## 4. Consequência 3 — mas a capacidade de pagamento EXISTE, e isso salva a tese

Consultei a Receita Corrente Líquida dos mesmos municípios (152 com retorno):

| Métrica | RCL 2025 |
|---|---|
| **Mediana** | **R$ 45.747.394** |
| p25 / p75 | R$ 35.427.582 / R$ 69.241.799 |

| Ticket | % da RCL mediana |
|---|---|
| R$ 8.000 (adesão SINTER) | 0,017% |
| R$ 15.000 | 0,033% |
| R$ 50.000 (diagnóstico) | 0,109% |
| R$ 58.800 | 0,129% |
| R$ 36.000/ano (P2 anual) | 0,079% |

**O município piauiense mediano tem R$ 45,7 milhões de receita corrente e arrecada R$ 2,2 mil de
IPTU.** O dinheiro vem de FPM, Fundeb e transferências — não de tributo próprio. Um contrato de
R$ 50 mil é **um milésimo** da receita dele.

**Ou seja: os tickets propostos pelo parecer de negócio são pagáveis no Piauí. O que não se sustenta
é a *justificativa* baseada em retorno de IPTU.** O ordenador de despesa precisa comprar
**cumprimento de prazo legal**, e a fonte é orçamento corrente ou PROFISCO III — nunca a promessa de
receita futura de IPTU.

## 5. Consequência 4 — o alerta do parecer sobre o beachhead

O parecer de negócio (Anexo G, Achado 5) recomenda explicitamente **começar fora do Piauí**, porque o
PI é o quintal da Foxinline (~236 tenants, Anexo D). O cliente decidiu o contrário, e há razões
legítimas para isso: relação comercial existente, proximidade, conhecimento do território e o canal
da REURB.

**A decisão é do cliente e é defensável — mas o custo dela precisa estar explícito:** disputar o PI é
disputar onde o incumbente já está instalado, com o argumento fiscal enfraquecido pela ausência de
IPTU. As duas compensações reais são: (a) o canal da REURB, que a Foxinline **não** tem do lado do
serviço de campo do cliente; e (b) o fato de que estar instalado com o sistema de REURB **não**
significa estar instalado com conformidade CIB — que é produto novo para todo mundo.

## 6. Mercado endereçável, por segmento, no beachhead

| Segmento | Nº municípios (PI) | Produto | Ticket |
|---|---|---|---|
| **A — tese fiscal completa** | ~9 (Teresina, Picos, Parnaíba, S. R. Nonato, Piripiri, Floriano, Oeiras, Campo Maior, Bom Jesus) | diagnóstico + PGV + eficiência | alto; fee de eficiência viável |
| **B — conformidade CIB pura** | ~215 | adesão SINTER + remessa CADURB, padronizado e automatizado | baixo (R$ 8–25 mil), volume |
| **C — expansão** | CE (184) + MA (217) | mesmo playbook | após validar B |

O segmento B só fecha conta se for **produto automatizado e replicável**, não serviço sob medida —
com 215 municípios a R$ 15 mil e margem alta, o negócio existe; com 215 projetos artesanais, não.
