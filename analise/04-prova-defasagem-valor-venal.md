# Prova quantitativa: a defasagem que o SINTER vai expor — medida hoje, com dado público

Executado em 2026-09-15. **79.985 transações imobiliárias reais analisadas.** Nenhuma negociação,
nenhuma credencial, nenhum contrato.

## A fonte

**Portal de Dados Abertos de Fortaleza** — dataset *"Imposto sobre Transmissão de Bens Imóveis
(ITBI)"*, via API CKAN: *"Relação de transações imobiliárias com recolhimento de ITBI, contendo a
geolocalização e características dos imóveis e informações sobre as operações."*

O esquema é, quase literalmente, a lista de atributos que o **art. 256 da LC 214/2025** manda
considerar na apuração do valor de referência:

| Campo | Papel na avaliação em massa |
|---|---|
| `XSIRGAS2000`, `YSIRGAS2000` | **localização** (coordenada projetada, SIRGAS 2000) |
| `AREA_TERRENO`, `AREA_EDIFICADA`, `FRACAO_IDEAL` | **área** |
| `DATA_CONSTRUCAO`, `NUMERO_PAVIMENTOS`, `QTD_FRENTES` | idade e forma |
| `TIPO_USO_IMOVEL`, `PADRAO_CONSTRUCAO`, `TIPO_TERRENO` | **tipologia, destinação, padrão** |
| `NOME_ZONEAMENTO`, `BAIRRO`, `CEP` | contexto urbano |
| `DATA_DA_TRANSACAO_ITBI` | **data** |
| **`VL_BASE_CALCULO`** | **o alvo: preço praticado no mercado** |
| **`VL_VENAL`**, `VL_LANCAMENTO_IPTU` | o que a prefeitura usa hoje |

Ou seja: **existe base de treino pública, georreferenciada e com variável-resposta** para construir e
validar um modelo de avaliação em massa — sem precisar de contrato com nenhuma prefeitura.

## O resultado

Razão entre **valor venal** (o que a prefeitura usa) e **valor de transação** (o que o mercado pagou):

| Estatística | Valor |
|---|---|
| Mediana | **30,8%** |
| Média | 32,8% |
| p10 / p90 | 1,3% / 54,0% |

**O valor venal em Fortaleza corresponde à mediana de ~31% do preço de mercado observado —
uma defasagem mediana de ~69%.**

Dispersão por bairro (apenas bairros com ≥40 transações):

| Extremo | Bairro | Venal / mercado | n |
|---|---|---|---|
| Maior defasagem | Guajeru | 0,6% | 475 |
| | Barroso | 0,9% | 1.020 |
| | Carlito Pamplona | 1,3% | 1.091 |
| | Antônio Bezerra | 1,5% | 871 |
| Menor defasagem | Mucuripe | 43,0% | 1.199 |
| | Vicente Pinzon | 42,8% | 914 |
| (anomalia) | Parque Manibura | 106,3% | 623 |

## Ressalvas metodológicas — obrigatórias antes de usar este número

1. **A cauda inferior é suspeita de qualidade de dado, não de defasagem real.** Razões de 0,6% a 2%
   provavelmente indicam registros onde o `VL_VENAL` está zerado, desatualizado ou refere-se apenas
   ao terreno, não ao conjunto terreno+edificação. **Não usar o p10 em material comercial.** A
   mediana (30,8%) é a estatística robusta e é a que deve ser citada.
2. **Parque Manibura a 106%** indica o problema inverso (venal acima do declarado) e reforça que há
   ruído nos dois sentidos.
3. **O ITBI é subdeclarado.** O preço declarado tende a ser menor que o preço real, o que significa
   que a defasagem verdadeira é **ainda maior** que a medida — a estimativa é conservadora.
4. Defasagem de valor venal **não converte linearmente em aumento de IPTU**: há alíquotas,
   isenções, limites legais de majoração e o princípio da anterioridade. É indicador de *base de
   cálculo desatualizada*, não uma promessa de receita.
5. A análise cobre a amostra lida (~25 MB do CSV, 88.696 linhas); a base completa é maior.

## Por que isso é a peça central do argumento

A ressalva do documento `02-adendo-reforma-tributaria.md` (seção 6) dizia que talvez não seja o
município quem apura o valor de referência — pode ser a Receita Federal, com os dados de cartório
que a **IN RFB 2.275/2025** passou a exigir.

**Este resultado mostra que, para o negócio, tanto faz quem apura.** Quando o valor de referência de
mercado for publicado no SINTER ao lado do valor venal municipal, a diferença fica visível,
auditável e atribuível — para o TCE, o Ministério Público, a imprensa e a oposição na Câmara. Em
Fortaleza, essa diferença é da ordem de **3 vezes**.

O produto não é "um painel". É: **"medimos sua defasagem antes que a Receita Federal a publique, e
entregamos o plano para fechá-la."** Isso é vendável hoje, com dado público, para qualquer município
que publique ITBI — e é vendável com mais urgência ainda para os que não publicam, porque eles não
fazem ideia do tamanho do próprio buraco.

## Replicabilidade
São Paulo publica transações com ITBI desde 2019; Fortaleza publica com geolocalização. O mesmo
pipeline roda em qualquer município com portal de dados abertos, e o resultado é um número em reais
específico daquele município — obtido **antes da primeira reunião comercial**.
