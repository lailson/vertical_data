# Análise da lista de fontes proposta

**Data:** 2026-09-18 · Verificado na fonte, não de memória.

Veredito curto: **a lista está majoritariamente certa, erra em quatro pontos, omite quatro
bases — e uma omissão vale mais que todo o resto.** Além disso, uma verificação feita
durante esta análise **derruba uma limitação que eu mesmo declarei ontem**.

---

## 1. O achado que muda o plano: GD tem coordenada

Eu escrevi na tela de energia e em `docs/metodologia-iv.md` §9 que *"município é o menor
recorte desta base"*. **Isso vale para a base tabular da ANEEL, e só para ela.**

O SIGEL — que a lista cita, mas por causa da rede de transmissão — publica uma camada de
**pontos** de geração distribuída, consultável por ArcGIS REST:

```
https://sigel.aneel.gov.br/arcgis/rest/services/Geracao_distribuida/GD_Sigel/FeatureServer/0
campos: MdaLatitude, MdaLongitude, DthConexao, MdaPotenciaInstalada,
        CodMunicipioIbge, DscClasseFornecimento, SigTipoGeracao, CodGD
```

Medido agora, não suposto:

| | |
|---|---|
| pontos no Piauí | **71.558** |
| pontos em Teresina | **31.457** |
| distância ao centro de Teresina | mediana **6,6 km** · p90 **11,1 km** |
| dentro de 30 km do centro | **1.982 de 2.000** na amostra |

As coordenadas são reais. Mas **três ressalvas decidem o que se pode fazer com elas:**

1. **Precisão de ~1,1 km.** Lat/lon vêm arredondadas em **duas casas** (`-5.04, -42.81`).
   Isso é mais grosso que muitos bairros de Teresina. Serve para **superfície de
   densidade**; não serve para atribuir ponto a bairro — atribuir seria inventar precisão,
   que é a família de erro do Mocambinho.
2. **~0,9% dos pontos estão no lugar errado**, alguns a centenas de quilômetros do
   município declarado. Precisa de filtro por distância ao município, declarado.
3. **Cobertura de 79%.** 71.558 no SIGEL contra **90.528** na base tabular. São recortes
   diferentes do mesmo fenômeno: **nunca somar nem comparar totais entre os dois**.

**Conclusão:** a limitação cai pela metade. Dá para mapear GD abaixo do município como
densidade — não como contagem por bairro. A tela de energia precisa de correção no texto.

---

## 2. O que a lista acertou

| fonte | veredito |
|---|---|
| **ANEEL — portal CKAN** | Correto. **72 pacotes** no catálogo. Parquet, CSV, XML, ZIP. Já integrado (`painel/build_aneel.py`). Licença **ODbL** — a lista não cita, e é o que permite uso comercial. |
| **SIGEL — ArcGIS REST** | Correto e no ar. Pastas: `BDGD`, `DadosAbertos`, `Geracao_distribuida`, `SFG`, `SGO_GEO`… |
| **MapBiomas via GEE** | Plausível e é o caminho certo para raster grande. Ver ressalva de licença em §5. |
| **Base dos Dados / BigQuery** | Existe. Ver ressalva em §5. |

---

## 3. Os quatro erros

**a) A URL do SINISA é a de quem PREENCHE, não a de quem baixa.**
`…/snis/area-do-prestador-e-municipios` é o formulário de coleta — atualização cadastral
de prestadores, Google Forms de resíduos sólidos, telefones de suporte. Não há dado
publicado ali.

**b) "SINISA: REST APIs, OData" — não encontrei documentação de nenhuma das duas.**
O que existe é planilha e relatório em `resultados-sinisa`, e a aplicação web de série
histórica do SNIS legado. Planejar ETL contra uma API que talvez não exista é o tipo de
premissa que só falha na hora de escrever o código.

**c) "SIGEL: WFS, WMS" — não confirmado.**
O `GetCapabilities` genérico de WFS devolve **HTTP 400**. O ArcGIS Server expõe WFS por
serviço, quando habilitado, então pode existir em alguma camada — mas não é o caminho.
O que **funciona e foi usado nesta análise** é o endpoint REST `/query`, com `where`,
`outFields`, `geometry` e paginação de 2.000 em 2.000.

**d) `EPSG:31983` (SIRGAS 2000 / UTM 23S) não cobre o Piauí.**
A zona 23 vai de **−48° a −42°**. O Piauí vai de **−46,03° a −40,58°** — o terço leste cai
na **zona 24**. Reprojetar o estado inteiro para 23S distorce progressivamente para o
leste, e área é exatamente o que se calcula errado.

- Para **Teresina sozinha** (−42,80°), 31983 está certo — o que denuncia o escopo da
  lista: ela fala em "sistema preditivo em Teresina", mas o projeto são **224 municípios**.
- Para o **estado**: manter SIRGAS 2000 geográfico (**EPSG:4674**) e calcular distância e
  área por método geodésico, ou usar projeção equivalente em área (Policônica do Brasil,
  **EPSG:5880**) quando o cálculo exigir.

---

## 4. As quatro omissões — e a primeira é a que dói

**a) BDGD — Base de Dados Geográfica da Distribuidora.** Licença ODbL, no catálogo como
`base-de-dados-geografica-da-distribuidora-bdgd`, atualizada em 01/09/2026.

É a rede de distribuição **georreferenciada**: transformadores, alimentadores, unidades
consumidoras. Para geração distribuída isso é mais relevante que a transmissão do SIGEL —
telhado não se conecta a linha de 500 kV, conecta-se ao transformador da esquina. Uma
lista feita para analisar GD que traz SIGEL e não traz BDGD inverteu a prioridade.

**b) Tarifas homologadas das distribuidoras** (`tarifas-distribuidoras-energia-eletrica`,
atualizada **hoje**). Sem tarifa não se calcula **payback**, e payback é o que decide
adoção. É a variável que falta para o modelo preditivo sair do descritivo.

**c) SIGA** (`siga-sistema-de-informacoes-de-geracao-da-aneel`) — usinas de geração
centralizada, com versão **diária**. É o complemento do lado da usina em solo.

**d) `atendimento-mmgd`** — segundo conjunto de geração distribuída no mesmo portal, que
precisa ser comparado com o que já ingerimos antes de assumir equivalência.

---

## 5. Licença e custo: três coisas que a lista trata como detalhe e não são

**LABREN/INPE.** A restrição mais importante da lista inteira está ausente: a base **não
pode ser reproduzida para fim comercial sem autorização expressa do INPE**. Usar como
insumo, citando, é permitido; republicar, não. Para produto pago isso é decisão, não nota
de rodapé. (Registrado no plano 28 §10 como risco alto.)

*Não consegui reverificar os formatos hoje — `labren.ccst.inpe.br` recusou conexão em 80
e 443.* A busca anterior indicava **CSV (grade completa e sedes municipais) e SHP**; a
lista afirma **NetCDF e GeoTIFF**. **Quem planejar `xarray` deve confirmar antes**, porque
sem NetCDF a biblioteca não tem o que fatiar.

**Google Earth Engine.** O nível gratuito é para pesquisa, ensino e uso sem fins
lucrativos; **uso comercial exige licença paga** do Google Cloud. Para um produto vendido
a prefeituras, isso é uma linha de custo recorrente, não um detalhe de stack.

**BigQuery / Base dos Dados.** Cobra por volume consultado acima da cota gratuita. E, no
caso específico deste projeto, seria **pagar nuvem por dado do IBGE que já se baixa direto
do FTP do IBGE** — com o agravante de que qualquer dependência de nuvem quebra a
propriedade de **o painel abrir sem internet**, que é o que permite demonstrar numa
prefeitura sem wifi.

---

## 6. Sobre a stack proposta

| proposto | observação |
|---|---|
| `dask` | Desnecessário. O DuckDB lê Parquet maior que a memória e já é o motor escolhido no plano 28. Acrescentar dask é complexidade sem problema correspondente. |
| `GeoPandas` | Traz GDAL e PROJ junto. O projeto hoje tem **zero dependência geoespacial** — `build_cnefe.py` faz ponto-em-polígono em numpy puro para 1,89 milhão de pontos, em 8 segundos. Antes de instalar a pilha inteira, avaliar a **extensão espacial do DuckDB**, que cobre reprojeção e predicados sem o inferno de build do GDAL. |
| `xarray` | Só se o NetCDF do LABREN se confirmar (§5). |
| `requests` + `pandas` | Já resolvido por `urllib` e DuckDB. |

---

## 7. O que fazer com isto

1. **Corrigir a tela de energia e a §9 da metodologia**: "município é o menor recorte"
   vale para a base tabular, não para o SIGEL. Correção de texto, não de número.
2. **Ingerir BDGD e tarifas** antes de qualquer modelo — são o que falta para prever
   adoção com causa, e não só descrever o passado.
3. **Não reprojetar o estado para UTM 23S.**
4. **Resolver a licença do LABREN por escrito** antes que ele entre em produto pago.
5. **Não adicionar GEE nem BigQuery** sem decisão explícita de custo e de dependência
   de nuvem.

---

## 8. Rodada 10 — tentativa de revisão externa (18/09/2026)

| eixo | ferramenta | resultado |
|---|---|---|
| negócio | GLM 5.3 · Z.ai Coding Plan | **Weekly/Monthly Limit Exhausted** — volta em **22/09/2026 00:08** |
| técnico | DeepSeek `deepseek-v4-pro` | **HTTP 402** — chave sem saldo |
| técnico | Kimi | **403** — cota mensal esgotada |

Pacote pronto e versionado em `analise/pacote-r10-glm.md`. **Cinco perguntas de negócio
seguem sem resposta externa** — e são as que eu menos consigo responder sozinho, porque
sou parte interessada:

1. Vale parar 1,5 dia para construir fundação com 104 dias de prazo?
2. **Energia é negócio ou distração?** O contrato que se vende é conformidade cadastral
   com prazo legal; geração distribuída é outro comprador e outro ciclo.
3. A lista do BDGD — 3.285 unidades PJ com carga e sem geração, com endereço — vale mais
   que o painel? E se vale, vende-se para prefeitura, para integrador solar ou para a
   distribuidora?
4. A perda de participação do Piauí é argumento **a favor** de entrar nesse mercado ou
   **contra**?
5. Risco comercial não listado.

Nada foi cobrado de crédito de provedor que serve cliente.
