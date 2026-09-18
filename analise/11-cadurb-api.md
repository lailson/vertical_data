# O CADURB é uma API REST pública e documentada — e isso reescreve a viabilidade do produto

Verificado em 2026-09-15 por download direto.

## O documento existe e é público

`enat.receita.economia.gov.br/pt-br/area_nacional/areas_interesse/sinter/manual-operacional/at_download/file`
→ **HTTP 200, PDF, 91 páginas**: *"Manual Operacional – Integração da API de Unidades Imobiliárias
(CADURB)"*, **versão 1.12, de 11/12/2025**.

**Correção do que eu havia afirmado:** eu disse que a especificação técnica só era liberada após a
adesão do município ao convênio, com base numa tentativa de download que retornou conteúdo restrito.
**Estava errado** — há dois artefatos distintos: o *Roteiro Técnico de Integração* (restrito, enviado
aos gestores indicados) e este **Manual Operacional, público**. O manual é o que importa.

## Não é layout de arquivo — é API REST com Swagger

Construído pelo **SERPRO** (`estaleiro.serpro.gov.br`). Autenticação por **token Bearer** fornecido
pelo time do CADURB. Ambiente de homologação com **Swagger UI** publicado.

Endpoints identificados:

| Método | Rota | Função |
|---|---|---|
| POST | `/api/v1/{codigoIbge}/ui` | envia Unidade Imobiliária |
| GET | `/api/v1/{codigoIbge}/ui/{cib}` | consulta por CIB |
| GET | `/api/v1/{codigoIbge}/ui/{inscricaoImobiliaria}` | consulta por inscrição municipal |
| POST | `/api/v1/{codigoIbge}/ui/desativacao` | desativa UI |
| GET | `/api/v1/{codigoIbge}/uis` | lista |
| GET | `/api/v1/arquivos/{codigoIbge}` | envio em lote por arquivo |
| GET | `/api/v1/{codigoIbge}/arquivo/{idArquivo}/consulta` | status do lote |
| GET | `/api/v1/{codigoIbge}/consulta/{idRequisicao}` | status da requisição |

Códigos de erro documentados (400 parâmetros inválidos, 401 token ausente/expirado), tabela de
códigos de falha, tipos de operação, e o CIB retornado no formato de 8 caracteres
(`M65SBES1`, `X455X55C`, `PSV5VXBR`).

**Consequência:** o produto de conformidade é **integração com uma API REST documentada**, não
engenharia reversa de formato proprietário. Isso reduz muito o risco técnico e o prazo do Segmento B,
e torna o "aceite objetivo = remessa aceita pelo CADURB" verificável de forma programática.

## O schema exigido — e por que ele fecha a tese

**5.1 DadosGeraisImovel:** `inscricaoImobiliaria` (chave municipal, obrigatório), `tipoImovel`
(1 territorial / 2 predial / 3 outro, obrigatório), `tpArquitetonico`, `destinacaoImovel`
(residencial/comercial/serviço), **`areaTerreno` (obrigatório)**, `areaConstruida` (obrigatório se
predial), padrão construtivo.
**5.2** AreaConstruidaCompl · **5.3** EnderecoImovel · **5.4** Titular (lista, com tipo de
titularidade e documento) · **5.5** ServicoRegistroImovel (CNS da serventia) · **5.6** CartorioNotas.

**5.7 ITBI — "devem ser informados os dados da última transação":**

| Campo | Conteúdo |
|---|---|
| `baseCalculITBI` | **base de cálculo do ITBI** |
| `valorRefITBI` | **valor de referência do ITBI** |
| `dtTransacaoITBI` | data da transação |
| `tpTransacaoITBI` | tipo de transação |
| `percTransacionadoITBI` | percentual transacionado |
| Transmitentes / Adquirentes | nome + CPF/CNPJ (listas) |

### O achado estratégico

Os campos que o CADURB exige **são exatamente os atributos que o art. 256 manda considerar** na
apuração do valor de referência — localização (endereço), tipologia (`tipoImovel`,
`tpArquitetonico`), destinação (`destinacaoImovel`), padrão construtivo, área (terreno e construída)
— **mais o preço observado** (`baseCalculITBI`, com data).

Ou seja: **o Segmento B (conformidade CIB) produz, como subproduto obrigatório, exatamente o
conjunto de treino do Segmento A (avaliação em massa / PGV).** O município que cumpre o art. 266
está, sem saber, montando a base que torna o art. 256 executável.

Isso resolve a objeção técnica mais séria levantada na rodada anterior — "no Piauí não há ITBI aberto
para calibrar o modelo". Não há **aberto**; mas o município tem, e a conformidade CIB obriga ele a
estruturá-lo. **Quem faz a conformidade fica com o pipeline do dado de calibração.**

É a ponte entre os dois segmentos, e é defensável: o dado é do município, nós somos operadores, e o
uso é a finalidade declarada no próprio contrato.

## Consequência oficial da ausência de CIB (confirmado na página da RFB)

> "Perda de receita: municípios cujos imóveis não possuem inscrição no CIB **não receberão repasses
> do Imposto sobre Bens e Serviços (IBS)**."
> "Imóveis sem CIB terão problemas em transações e regularização."

Não é multa, e essa distinção importa na proposta: **é perda de receita**, que é argumento mais forte
e mais concreto para um ordenador de despesa do que "inadimplência".

## Ajuste no posicionamento comercial

A adesão ao SINTER é por **convênio gratuito** com a RFB, e a API é fornecida sem custo.
**Não se vende "acesso ao CIB" — isso é de graça.**

O que se vende é a **capacidade de cumprir**: sanear o cadastro municipal, georreferenciar,
completar os campos obrigatórios do schema, conduzir a adesão, integrar com a API e sustentar o
ciclo de atualização. Em municípios onde o cadastro é uma planilha desatualizada — a maioria dos 215
do Segmento B — é aí que está todo o trabalho e todo o valor.
