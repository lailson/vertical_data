# Rodada 5 — FECHAMENTO TÉCNICO. Três fatos novos que mudam a engenharia.

1. **O CADURB é uma API REST pública e documentada** (Manual Operacional v1.12, 91 páginas, SERPRO,
   Swagger, token Bearer). Não é layout de arquivo. Endpoints de envio, consulta, desativação e lote
   (Anexo A). Isso derruba a premissa de "formato normatizado a implementar do zero".
2. **O schema do CADURB inclui o bloco ITBI da última transação** (`baseCalculITBI`, `valorRefITBI`,
   `dtTransacaoITBI`, `tpTransacaoITBI`) + tipologia, destinação, padrão, áreas e endereço —
   **exatamente as features do art. 256**. O produto de conformidade gera o treino da avaliação.
3. **Renda POR BAIRRO existe** (eu errei; corrigido no Anexo B). Não precisa interpolação areal.
   E descobri uma armadilha: **o dado de entorno tem bairros com amostra minúscula** — Tabajaras tem
   19 faces para 293 domicílios, produzindo 36,8% de pavimentação num bairro de renda mediana
   R$ 15.000 (a maior de Teresina). Ruído virando ranking.

Responda no máximo 6 achados:

1. Com o CADURB sendo API REST documentada, **refaça a estimativa e a arquitetura do produto de
   conformidade**: o que se constrói, quanto tempo, e qual o caminho crítico real.
2. **Regras de qualidade obrigatórias** para o indicador de entorno: corte mínimo de faces,
   tratamento de "não declarado" (V05408/V05414), e como exibir incerteza sem poluir o painel.
   Proponha valores concretos.
3. Refaça a **fórmula do `iv`** agora com renda por bairro disponível (V06006 mediana, não V06004
   média — razão média/mediana chega a 1,59). Pesos e justificativa.
4. Dado que o bloco ITBI do CADURB dá preço + atributos por imóvel: **desenhe o caminho do dado**
   desde a conformidade até o modelo de avaliação em massa, e diga em quantos municípios/quantos
   anos isso vira amostra utilizável.
5. **Modelo de dados unificado** que sirva ao mesmo tempo ao painel por bairro e à remessa CADURB
   por imóvel. Onde os dois se encontram e onde não se misturam.
6. Riscos de engenharia que ainda não foram nomeados em nenhuma rodada.

Adversarial, concreto. Cite "Anexo N".

# ANEXO A — API DO CADURB (NOVO, decisivo)

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

# ANEXO B — ARBITRAGEM: CORREÇÕES E ARMADILHA NO DADO

# Arbitragem da 2ª rodada da análise paralela — verificações feitas

## 1. ERRO MEU, confirmado: renda POR BAIRRO existe

Afirmei que "não existe arquivo de renda por bairro; o rendimento está só por setor censitário".
**Falso.** A pasta `Agregados_por_Setores_Censitarios_Rendimento_do_Responsavel/` contém:

```
Agregados_por_bairros_renda_responsavel_BR_20260508_csv.zip     ← existe
Agregados_por_distritos_renda_responsavel_BR_20260508_csv.zip
Agregados_por_municipios_renda_responsavel_BR_20260508_csv.zip
Agregados_por_setores_renda_responsavel_BR_20260508_csv.zip
Agregados_por_subdistritos_renda_responsavel_BR_20260508_csv.zip
```

Baixado e validado: **17.378 bairros no Brasil, 122 de Teresina**.

**Causa do erro, e ela se repetiu:** procurei renda dentro de `Agregados_por_Bairro_csv/`, não achei, e
concluí ausência. A pasta irmã eu cheguei a listar, mas não abri. **É o mesmo erro de método que
cometi antes com a granularidade de bairro: inferir inexistência a partir de uma busca incompleta.**
Duas vezes, no mesmo conjunto de dados. Registro para não repetir.

**Consequência prática:** cai a necessidade de interpolação areal setor→bairro para renda, e cai a
ressalva de "estimado" que o parecer técnico exigia para esse indicador. Renda é dado direto por
bairro, um download.

### Dicionário correto (meu parser anterior estava deslocado; a outra análise estava certa)
| Variável | Significado |
|---|---|
| V06001 | Pessoas responsáveis em domicílios particulares permanentes ocupados |
| V06002 | Moradores em domicílios particulares permanentes ocupados |
| V06003 | Variância do número de moradores |
| **V06004** | **Rendimento nominal MÉDIO mensal das pessoas responsáveis** |
| V06005 | Variância do rendimento |
| **V06006** | **Rendimento nominal MEDIANO mensal das pessoas responsáveis** |

### Renda real — Teresina (rendimento mediano, V06006)
| Menores | R$ | Maiores | R$ |
|---|---|---|---|
| Olarias | 1.200 | Zoobotânico | 8.000 |
| Vila São Francisco | 1.200 | Frei Serafim | 9.000 |
| Árvores Verdes | 1.200 | Fátima | 10.000 |
| Chapadinha | 1.200 | Jóquei | 12.000 |
| Alto Alegre | 1.212 | Tabajaras | 15.000 |

**Validação cruzada com o índice calculado:** Chapadinha, Olarias e Árvores Verdes têm a menor renda
**e** aparecem no topo do ranking de vulnerabilidade; Jóquei, Frei Serafim e Fátima têm a maior renda
**e** o menor IV. Duas fontes independentes do Censo concordando — isso valida o índice.

**Usar mediana (V06006), não média (V06004).** Razão média/mediana chega a 1,59 (Brasilar) e 1,58
(Mocambinho) — a média é puxada por outliers e inverte posições no ranking.

## 2. ACHADO NOVO E CRÍTICO — armadilha no dado de entorno: bairros com poucas faces

A anomalia que disparou a investigação: **Tabajaras** tem a **maior renda mediana de Teresina
(R$ 15.000)** e, no meu cálculo, teria só **36,8% de pavimentação** e 57,9% de iluminação —
impossível para um bairro nobre.

Causa verificada:

| Bairro | Faces medidas | Pav. sim | Domicílios | Leitura |
|---|---|---|---|---|
| Centro | 1.521 | 1.521 | 2.838 | robusto (100%) |
| Chapadinha | 761 | 279 | 2.026 | robusto (36,7% é real) |
| Morros | 565 | 260 | 1.761 | robusto |
| Jóquei | 525 | 523 | 2.520 | robusto (99,6%) |
| **Tabajaras** | **19** | 7 | **293** | **não confiável** |

**Tabajaras tem 19 faces medidas para 293 domicílios.** Com n=19, cada face vale 5,3 pontos
percentuais. O número é ruído, não medição.

**Consequência obrigatória para o produto:** o indicador de entorno precisa de **corte mínimo de
faces** (sugestão: n ≥ 50, com faixa de confiança exibida entre 50 e 150) e de tratamento explícito
da categoria **"não declarado"** (V05408/V05414), que hoje entra no denominador e subestima a
cobertura. Sem esses dois cuidados, bairros pequenos aparecem no topo do ranking de prioridade por
puro artefato amostral — e o painel manda investimento público para o lugar errado, que é exatamente
o defeito que estamos corrigindo no protótipo.

**Este é o tipo de erro que só aparece em validação cruzada entre fontes.** Nenhuma das três análises
o teria encontrado sem cruzar renda com entorno.

## 3. Correções que a outra análise faz à cadeia tributária — aceitas

| Minha formulação | Correção |
|---|---|
| "art. 256 obriga o município" | **A obrigação de inscrição no CIB é o art. 265/266.** O art. 256 trata do *valor de referência* — é o que sustenta a tese da PGV, não a do cadastro. Eu misturei os dois papéis. |
| "prazo 01/01/2027" | **31/12/2026** é o fim do prazo de 24 meses do art. 266. Mesmo marco, redação correta importa em proposta. |
| "PROFISCO III, dinheiro carimbado" | **É empréstimo do BID, não repasse a fundo perdido.** US$ 278 mi federal + CCLIP US$ 2 bi para estados; **municípios só na 2ª fase**. Exige autorização legislativa. Não é "dinheiro disponível". |
| "fica inadimplente com a LC 214" | A consequência real é **melhor**: imóvel sem CIB → **o município não recebe o repasse do IBS daquela operação** (LC 214, art. 11, II), além de entraves a registro, alvará e ITBI. Não há multa por "não modernizar". |
| "IN RFB 2.275/2025" | Obriga **cartórios**, não municípios. (Eu havia registrado corretamente no adendo, mas a menção em resumo ficou ambígua.) |

**Correção de posicionamento, e é a mais importante das cinco:** a RFB fornece a integração ao
SINTER **de graça** (convênio gratuito). **Não se vende "acesso ao CIB".** Vende-se
**saneamento, qualificação e georreferenciamento do cadastro** — ou seja, a *capacidade de cumprir*.
Isso muda a frase de venda inteira.

## 4. Dados novos que a outra análise traz e que fortalecem a tese

- **1.904 municípios aderidos ao SINTER em 14/09/2026, de 5.570** → **~66% ainda fora**, a um ano e
  três meses do prazo. É a quantificação da janela que eu não tinha.
- **29,1 milhões de CIBs ativos.**
- **Manual Operacional do CADURB (ENAT, v1.12) é público** — contradiz minha afirmação de que a
  especificação só sai após adesão. *A verificar: minha tentativa de download do "Roteiro Técnico"
  retornou conteúdo restrito; pode haver dois documentos distintos (roteiro restrito × manual
  público).*
- **ITBI aberto em muito mais capitais do que eu havia mapeado:** além de Fortaleza e São Paulo —
  **Recife, Belo Horizonte** (ITBI mensal desde 2008 + CTM com geometria), **Porto Alegre** (IPTU com
  valor venal por imóvel), Rio e Niterói (agregado). **São Paulo tem CTM com 1.687.909 lotes via WFS.**
- **Nenhum município médio do PI/CE/MA publica ITBI** (testados: Teresina, Parnaíba, Timon, Sobral,
  Juazeiro — todos negativos). Confirma: as capitais servem de **treino e referência metodológica**;
  no beachhead o valor venal depende de SEMF ou coleta.
- **Foxinline atende dois tribunais** (TJ-PI e **TJ-MT**) e tem presença também em **TO**.
- **Geopixel:** casos declarados de Amparo (+R$ 10 mi/ano) e Guaratinguetá (arrecadação quase
  dobrou); concentração em municípios médios de SP/MG. Referência de preço do segmento: contrato
  tipo **R$ 270 mil** (cadastro, 2019).

## 5. Onde eu mantenho minha posição

**A tese do art. 256 (valor de referência) não some — ela muda de papel.** A outra análise trata a
correção como se o art. 256 fosse irrelevante. Não é: ele é o que sustenta o **Segmento A** (PGV,
recuperação fiscal, recorrência anual). O que a correção estabelece é que **a razão de compra do
Segmento B é o art. 266** (inscrição no CIB, prazo 31/12/2026), não o 256. São dois produtos com
duas bases legais distintas — e confundi-las foi meu erro, mas descartar o 256 seria o erro oposto.

**O dimensionamento econômico permanece, e a outra análise ainda não o tem:** mediana de IPTU no PI
de R$ 2.214/ano, 194 de 224 municípios abaixo de R$ 100 mil, RCL mediana de R$ 45,7 mi. É o que
determina que no beachhead o modelo é preço fixo, não fee de eficiência — e a análise paralela
continua sem preço, ticket ou LTV.

# ANEXO C — PLANO CONSOLIDADO ATUAL (a ser revisado)

# Projeto CERURB — Plano consolidado
**Data:** 2026-09-15 · **Status:** recomendação pré-decisão
Produto de 4 rodadas de análise cruzada (Claude Code orquestrando, DeepSeek no eixo técnico, GLM no
eixo de negócio), mais uma análise paralela independente, com verificação empírica de cada
afirmação factual.

---

## 1. Veredito

**ENTRAR, COM CONDIÇÕES** — mas não no projeto como está proposto.

A proposta original ("dashboard de gestão municipal alimentado pelo CERURB, com ML, preditivo e chat")
não sobrevive ao exame: o dado do CERURB é contratualmente fechado, a granularidade prometida não
corresponde ao território real, o indicador central não tem metodologia, e o argumento de venda
(aumentar IPTU) não se aplica a 95% do mercado-alvo escolhido.

O que sobrevive, e é melhor do que a proposta original, é isto:

> **O produto é o prazo legal, não o painel. O cliente é o ordenador de despesa sem equipe.
> O aceite é a remessa aceita no CADURB. A cartografia chega paga pela REURB.**

---

## 2. Os cinco fatos que determinam o plano

1. **Obrigação federal com data.** LC 214/2025, arts. 265/266: todo imóvel urbano inscrito no CIB;
   capitais desde 01/01/2026, **todos os demais municípios até 01/01/2027**. A RFB já publicou o
   Roteiro Técnico de remessa ao CADURB (formato normatizado = critério de aceite objetivo) e existe
   **PROFISCO III** (Fazenda + BID) para financiar.
2. **O CERURB não é via de dado.** Stack JSF/PrimeFaces sem API pública; existem microserviços
   internos (`api-exportacao`, `api-cerurbjus-integracao`), mas o contrato TJ-PI 156/2023 **veda
   repasse a outras empresas**. A cláusula 4.1.1 abre a órgãos, não a fornecedores.
3. **A Foxinline é incumbente regional, não startup frágil.** ~236 tenants municipais em PI, CE, PE,
   PA e MA; ~33 cartórios; vende "Central CERURB" a gestores. Mas **CERURB ≠ CIB**: o CERURB cobre
   núcleos de REURB, o CIB cobre **todos** os imóveis urbanos. Conformidade CIB é produto novo para
   todos, inclusive para ela.
4. **O mercado do Piauí não tem IPTU.** Mediana de **R$ 2.214/ano**; 194 de 224 abaixo de R$ 100 mil;
   só 9 acima de R$ 1 mi. **Mas a RCL mediana é R$ 45,7 mi** — o dinheiro existe, vem de FPM/Fundeb.
   Logo: capacidade de pagar sim, justificativa por retorno de IPTU não.
5. **O dado público resolve 11 dos 15 indicadores do painel, hoje.** Inclusive pavimentação e
   iluminação por bairro (Censo 2022, entorno por face de quadra) — que a matriz de fontes do cliente
   dava como dependentes de negociação com secretarias.

---

## 3. O modelo: dois negócios, não um

| | **Segmento B — Conformidade CIB** | **Segmento A — Recuperação fiscal** |
|---|---|---|
| **Quem** | ~215 municípios do PI sem IPTU relevante | ~9 municípios com IPTU > R$ 1 mi |
| **Compra** | cumprir o art. 266 até 01/01/2027 | base de cálculo defensável + receita |
| **Produto** | adesão SINTER (16 passos) + organização do cadastro + 1ª remessa CADURB | diagnóstico + PGV/valor de referência + atualização anual |
| **Ticket** | R$ 8–25 mil entrada · R$ 4–10 mil/ano manutenção | R$ 49,5–58,8 mil diagnóstico · R$ 24–36 mil/ano |
| **Remuneração** | **preço fixo. Zero variável atrelado a IPTU** | fixo + fee de eficiência (10–15% do incremento) |
| **Veículo** | dispensa (abaixo de ~R$ 59 mil) | dispensa → contrato de eficiência (art. 119, Lei 14.133) |
| **Aceite** | **remessa aceita no CADURB** | idem + metodologia publicável |
| **LTV 5 anos** | R$ 24–65 mil/conta | R$ 145–239 mil/conta |
| **TAM no PI** | R$ 1,7–5,4 mi entrada + R$ 0,9–2,2 mi/ano | Teresina isolada: fee potencial R$ 3,8–5,7 mi/ano |

**Erro a não cometer:** vender o Segmento B com argumento de arrecadação. Em município onde o
prefeito não vai cobrar IPTU de eleitor de baixa renda, isso vende um problema, não uma solução.

**Condição de viabilidade do B:** só fecha conta **automatizado**. 215 municípios a R$ 15 mil com
margem alta é negócio; 215 projetos artesanais não é.

---

## 4. Município-piloto — validado com dado

Critérios: IPTU < R$ 100 mil · RCL ≥ R$ 35 mi · REURB ativa pelo canal do cliente · não-tenant
Foxinline · gestor com mandato até 2028.

| Município | IPTU 2025 | RCL 2025 | Status no Programa Regularizar | Veredito |
|---|---|---|---|---|
| **Guaribas** | R$ 4.674 | R$ 41,2 mi | **100% regularizado** | ★ melhor — cadastro REURB pronto |
| **N. Sra. de Nazaré** | R$ 6.762 | R$ 53,2 mi | **100% regularizado** | ★ melhor — cadastro REURB pronto |
| **Juazeiro do Piauí** | R$ 4.251 | R$ 41,0 mi | em tramitação | ✅ aprovado |
| **Coivaras** | R$ 86.144 | R$ 37,9 mi | em tramitação | ✅ aprovado |
| Floresta do Piauí | R$ 200 | R$ 30,9 mi | 100% regularizado | ⚠️ RCL abaixo do corte |
| Tanque do Piauí | **R$ 0,00** | R$ 25,5 mi | em tramitação | ❌ RCL abaixo; IPTU zero |

**Refinamento sobre a recomendação original:** os melhores pilotos não são os *em tramitação* e sim
os **já 100% regularizados** — Guaribas e Nossa Senhora de Nazaré. Neles o cadastro REURB
georreferenciado (obrigatório por lei, art. 35) **já existe e já foi pago**. O caminho até a remessa
CADURB é o mais curto possível: transformar cadastro pronto em remessa normatizada. É a prova de
conceito mais barata do produto B.

**Teresina NÃO é o piloto.** Três razões: (a) a **Lei municipal 6.383/2026** já instituiu CTM + SIG +
IDE na SEMPLAN — há programa institucional próprio, com poder de internalizar ou licitar; (b) o
**IPTU 2026 está suspenso para imóveis edificados sob auditoria do TCE-PI** — vender "aumentar IPTU"
agora é entrar no meio de uma briga política; (c) é onde a Foxinline é mais forte.

Teresina tem três outros papéis: **vitrine** (painel com dado real dos 123 bairros), **conta A de
2027** (quando a cobrança voltar e o TCE exigir base defensável) e **parceira institucional** — a
SEMPLAN precisa da ferramenta que a Lei 6.383 exige; melhor fornecer do que competir com a agenda dela.

---

## 5. Escopo técnico da v1

**Prazo: 3–4 semanas** (não 60–90 dias — os dados já estão baixados e validados).

**Entra:**
- ETL parametrizado por código IBGE (serve qualquer município) → **PostGIS**
- Censo 2022 por bairro: demografia, domicílios, alfabetização, cor/raça
- **Entorno urbanístico por face de quadra**: pavimentação (V05406), iluminação (V05412), bueiro
  (V05409) sobre faces no setor (V05400)
- Camada vetorial de **favelas e comunidades urbanas** (= universo dos núcleos informais da REURB)
- Malha de bairros + geometria real (fim da grade de células ilustrativa)
- **Arrecadação via SICONFI** — a métrica ausente e mais importante
- INEP por escola geolocalizada
- Motor de `iv` com fórmula versionada em script
- Schema: `municipio / bairro / setor / indicador / fonte / metodologia`

**Não entra na v1:** PGV, ML, chat conversacional, cartografia por drone, qualquer integração CERURB.

**Renda:** existe só por setor censitário. Agregar setor→bairro por **interpolação areal** (não por
centroide); bairro com menos de 80% dos domicílios alocados sai marcado como *estimado*, com o erro
ecológico declarado no painel.

**Reutilizável entre municípios:** fetchers, schema, motor de `iv`, frontend.
**Não reutilizável:** regras locais de limpeza de endereço, geometria, acordos institucionais.

---

## 6. O protótipo: o que fazer

**Bloqueio de processo: nenhuma apresentação com dado fictício em bairro nomeado.**

O protótipo diz que Mocambinho tem 36% de pavimentação; o real é **99,6%** — erro de 63,6 pontos na
direção errada. Os quatro bairros mais vulneráveis de Teresina não aparecem nele. Um gestor local
identifica isso em segundos, e o dano atinge a vitrine, a conta A de 2027 e a credencial de
"conhecimento do território" — que é a vantagem declarada do cliente.

Antes de qualquer demonstração:
1. Repovoar com o dado real **já extraído** (11 dos 15 indicadores prontos) — dias, não semanas
2. Adotar os **123 bairros oficiais** + geometria real
3. **Publicar a metodologia do `iv`** (pesos, fontes, fórmula) — item de escopo, não detalhe
4. Converter `idosos`/`criancas` de booleano para proporção
5. Incluir **arrecadação** (uma chamada HTTP)
6. Enquanto 1–5 não fecharem: carimbo inequívoco de "dados ilustrativos" em toda tela

Das 11 telas: reimplementar 8; **congelar 2** (Simulador — precisa de modelo de impacto; Status
CERURB — precisa de convênio); Relatórios viram exportação com metodologia auditável.

---

## 7. Roadmap 12 meses (PI → CE → MA)

| Período | Ações | Marco |
|---|---|---|
| **M0–M1** (out/26) | consertar protótipo; **due diligence: ler IN RFB 2.275/2025 e confirmar a leitura do art. 256**; qualificar os 224 (SICONFI × MUNIC 2021 × tenants Foxinline × Programa Regularizar) | lista ranqueada de ~40 alvos B + protótipo com dado real |
| **M1–M3** (out–dez/26) | fechar pilotos em Guaribas / N. Sra. de Nazaré / Juazeiro / Coivaras pelo canal REURB | **3 adesões + remessas contratadas até 31/12/2026** |
| **M3–M6** (1º sem/27) | produtizar (os 16 passos viram ferramenta; remessa automatizada); escalar via APPM/canal TJ; abrir Trilha PROFISCO com Picos, Parnaíba, Floriano | 15+ contratos B · R$ 200–400 mil acumulados |
| **M6–M9** | Segmento A: Teresina pós-suspensão, Picos, Parnaíba | 1–3 contratos A |
| **M9–M12** | decisão de expansão CE (184) + MA (217) | expandir só se ≥20 assinaturas no PI **e** margem B ≥50% com CAC < R$ 5 mil |

**Metas ano 1:** 25–40 contratos B (R$ 0,2–1,0 mi) + 1–3 contratos A (R$ 100–200 mil) =
**R$ 0,3–1,2 mi**. Run-rate recorrente ao fim: R$ 150–480 mil/ano (B) + R$ 24–108 mil/ano (A).

**A janela é dura:** o art. 266 vira em 01/01/2027. Quem não aderiu até lá compra em pânico ou em
lote — e os dois são outro jogo, favorável a quem tem estrutura.

---

## 8. Condições inegociáveis

1. **CERURB fora do caminho crítico.** Zero engenharia antes de credencial emitida **e** cláusula de
   acesso. O cliente **produz** o geodado via REURB em vez de pedi-lo ao TJ.
2. **Cláusula de entrega da cartografia REURB em formato aberto** (SHP/GeoPackage/GeoJSON, acurácia
   declarada, dicionário de atributos) no contrato do parceiro. Renegociar antes de construir.
3. **Aceite objetivo = remessa aceita no CADURB.** Nunca "modelo acurado a X%".
4. **ART de avaliador parceiro** (CREA) + metodologia publicável (IAAO / NBR 14653) para o
   Segmento A. O valor de referência será contestado; ART de avaliação é de engenheiro, não de
   pipeline.
5. **Quatro cláusulas contratuais:** operação LGPD formalizada (município controlador, empresa
   operadora); base exportável pelo município em formato aberto; PI do software e dos modelos retida;
   vedação de repasse da base a concorrentes — inclusive à Foxinline.
6. **ML fora de SLA.** Ferramenta interna de calibração, nunca promessa contratual. Quando entrar
   (Segmento A), método defensável perante TCE é **regressão hedônica espacial com coeficientes
   declarados**; GBM só como benchmark.
7. **Nenhum custo fixo dependente da aprovação do PROFISCO III** (ciclo de 6–18 meses).

---

## 9. Riscos e gatilhos de abandono

| Risco | Gatilho |
|---|---|
| Canal não vende conformidade | 3 pilotos B sem assinatura em 90 dias → reavaliar a tese B |
| Dependência do CERURB volta ao escopo | qualquer arquitetura condicionada à cláusula 4.1.1 |
| Lote estadual | Foxinline fechando "Central CERURB + conformidade" via APPM/TJ antes de 10 assinaturas → reavaliar em 30 dias |
| **Motor central da RFB** | RFB publicar motor de valor de referência que dispense a estimativa municipal → mata o recorrente do Segmento A e degrada o B a cadastro puro |
| Cartografia sem cláusula | contrato REURB sem cláusula de formato aberto e parceiro recusa renegociar |
| Auto-gol | apresentar o protótipo com dado fictício — infração de processo: quem cometer, para de vender até consertar |

---

## 10. Pendência que precede qualquer proposta

**Ler a íntegra da IN RFB 2.275/2025 e obter o Roteiro Técnico do CADURB.**

Há uma ambiguidade não resolvida no art. 256: ele diz que o valor de referência é apurado "pelas
administrações tributárias", sem especificar o ente. Se a RFB apurar centralmente — usando os dados
de cartório que a IN 2.275 passou a exigir — então a obrigação municipal é **enviar cadastro**, não
**produzir avaliação**, e a recorrência do Segmento A enfraquece.

O que permanece verdadeiro nos dois cenários: o município é obrigado a inscrever todos os imóveis no
CIB (art. 265/266); e quando o valor de referência de mercado for publicado ao lado do valor venal
municipal, **a defasagem fica visível e auditável**. Medida em Fortaleza sobre 79.985 transações
reais: o valor venal é **30,8% do preço de mercado** — defasagem de ~69%, base de cálculo 3× abaixo
do mercado.

O produto, no fim, é esse: **medir a defasagem antes que a Receita Federal a publique.**

**Nota:** o Roteiro Técnico **não é público** — é entregue apenas aos gestores indicados no
requerimento, após a adesão do município ao convênio. Isso reforça o valor de entrar pelo serviço de
condução da adesão: é o que dá acesso à especificação antes dos concorrentes.

# ANEXO D — AUDITORIA DO PROTÓTIPO

# Auditoria do protótipo `painel-gestao-municipal (1).html`

43.163 bytes, sendo 18.721 de JavaScript. Auditado campo a campo e confrontado com dado real.

## 1. Estrutura

11 telas: Painel principal, Mapa territorial, Ranking de bairros, Saneamento, Pavimentação,
Educação, Perfis socioeconômicos, Simulador de investimento, Séries históricas, Status CERURB,
Relatórios exportáveis.

Funções existentes — **todas de apresentação**: `buildMiniMap`, `renderBigMap`, `buildRankMini`,
`colorFor`, `colorForInverse`, `fmtPct`, `prioTag`, `goToPage`, `runSimulation`, `xFor`, `yFor`.
**Nenhuma função de cálculo de indicador.**

## 2. O modelo de dados: 18 registros, 17 campos

```
{nome, iv, saneamento, pavimentacao, evasao, escolas, distEscola, matriculas,
 familias, renda, moradores, idosos, criancas, posse, pendentes, analise, regularizados}
```

| Campo | Domínio no protótipo |
|---|---|
| `iv` (índice de vulnerabilidade) | 9 a 88 — **sem fórmula em lugar nenhum** |
| `saneamento` | 24% a 96% |
| `pavimentacao` | 31% a 96% |
| `evasao` | 1,9% a 14,2% |
| `renda` | "até 1 SM", "1–2 SM", "2–3 SM", "3+ SM" |
| `posse` | Posseiro, Proprietário, Proprietário informal, Cessão |
| `idosos`, `criancas` | booleanos (!) |
| `familias` | 40 a 212 |
| `pendentes` / `analise` / `regularizados` | 0–64 / 1–60 / 39–90 |

## 3. Problema 1 — o indicador central não tem metodologia

O `iv` ordena o ranking, colore o mapa, define as faixas de prioridade (alta/média/baixa) e alimenta
o simulador de investimento. **Ele é um número digitado à mão.** Não há pesos, não há fontes, não há
reprodutibilidade.

Num produto que ordena prioridade de investimento público, isso é passivo contratual: basta um
vereador cujo bairro ficou em último, ou o controle interno, perguntar "como calcularam" — e não há
resposta. **Definir a metodologia do índice é item de escopo, não detalhe de implementação.**

## 4. Problema 2 — os dados fictícios contradizem a realidade, e isso é detectável na hora

Os 18 nomes **são bairros reais de Teresina**. Cruzei com a base do IBGE: **13 casam diretamente**,
2 por variante de grafia (Renascença, Horto) e **3 não são bairros oficiais** (Vila Irmã Dulce,
Vila Nova do Alto da Ressurreição, Parque Piauí) — são vilas/comunidades dentro de bairros.

Confrontando o protótipo com o dado real do Censo 2022 (entorno urbanístico por face de quadra):

| Bairro | Pavimentação no protótipo | **Pavimentação real** | Erro |
|---|---|---|---|
| Mocambinho | 36% | **99,6%** | protótipo diz que é o 2º pior; é dos melhores |
| Santa Luzia | 41% | **78,6%** | subestimado |
| Todos os Santos | — | 62,1% | — |
| Centro | — | 100,0% | — |

E os bairros **realmente** carentes de pavimentação em Teresina — Chapadinha (36,7%), Tabajaras
(36,8%), Brasilar (44,8%), Morros (46,0%), Verdecap (46,9%) — **não aparecem no protótipo.**

**Risco imediato:** qualquer gestor de Teresina que olhe esse painel reconhece que Mocambinho não é
bairro sem pavimentação. O protótipo, apresentado como está, destrói credibilidade na primeira
reunião. Ele precisa ou ser rotulado explicitamente como maquete visual, ou ser repopulado com dado
real antes de qualquer apresentação.

## 5. Problema 3 — a divisão territorial não corresponde a nenhuma base oficial

Teresina tem **123 bairros** (IBGE, Censo 2022). O protótipo usa 18, misturando bairros oficiais com
comunidades. Isso impede junção com qualquer fonte e precisa ser decidido antes de construir:
o recorte é bairro oficial (123), comunidade/núcleo informal, ou setor censitário?

## 6. Problema 4 — campos com tipo inadequado

`idosos: true/false` e `criancas: true/false` tratam presença de idosos e crianças como booleano por
bairro. Não existe bairro sem crianças. O dado correto é **proporção** (o Censo dá por bairro), e o
uso pretendido provavelmente era "concentração acima da média" — o que é outra coisa e precisa de
definição.

## 7. O que o protótipo acerta e deve ser preservado

- **A arquitetura de navegação** (11 telas) é adequada e cobre o módulo 4 da proposta.
- **A escolha de indicadores** é pertinente: saneamento, pavimentação, educação, perfil
  socioeconômico, posse e status de regularização são de fato os eixos certos.
- **O simulador de investimento e os relatórios exportáveis** são diferenciais reais frente a um
  dashboard passivo — mas o simulador precisa de modelo por trás, não de regra ad hoc.
- Como **peça comercial e especificação visual**, cumpre a função.

## 8. Veredito técnico

**O protótipo é uma maquete de interface de boa qualidade, com dados inventados que não sobrevivem
ao confronto com a realidade.** Não serve como base de código (HTML estático, array hardcoded, sem
camada de dados), mas serve como especificação de produto.

**Ação recomendada, em ordem:**
1. Repopular com dado real do IBGE por bairro — **é factível hoje**, os dados existem e foram
   baixados nesta análise (pavimentação, iluminação, bueiro, domicílios, demografia por bairro).
2. Definir e publicar a metodologia do `iv` (pesos, fontes, fórmula).
3. Substituir a grade de células por geometria real (malha de bairros do IBGE + PostGIS).
4. Adotar os 123 bairros oficiais, com camada separada para comunidades/núcleos informais.
5. Adicionar a métrica ausente e mais importante: **arrecadação** (SICONFI, já validado).
6. Até que 1–4 estejam feitos, marcar toda tela com "dados ilustrativos" de forma inequívoca.

## 9. Mapa de cada indicador do protótipo para sua fonte real

| Indicador do painel | Fonte real | Granularidade | Status |
|---|---|---|---|
| Pavimentação | **Censo 2022 — entorno, V05406/V05400** | **bairro** | ✅ pronto |
| Iluminação pública | **Censo 2022 — entorno, V05412** | **bairro** | ✅ pronto |
| Drenagem (bueiro) | Censo 2022 — entorno, V05409 | bairro | ✅ pronto (não está no protótipo) |
| Saneamento (água/esgoto) | Censo 2022 — características do domicílio | bairro | ✅ pronto |
| Densidade, moradores/domicílio | Censo 2022 — demografia/básico | bairro | ✅ pronto |
| Idosos e crianças (proporção) | Censo 2022 — demografia | bairro | ✅ pronto |
| **Renda** | Censo 2022 — Rendimento do Responsável | **só setor censitário** | ⚠️ agregar setor→bairro |
| Escolas, matrículas, distância | INEP Censo Escolar (escola geolocalizada) | ponto → bairro | ✅ pronto |
| Evasão / rendimento escolar | INEP (distorção idade-série, IDEB) | escola | ✅ pronto |
| Energia solar / GD | ANEEL (diário) | município | ⚠️ não desce a bairro |
| **Arrecadação (ausente)** | SICONFI / TCE-PI | município | ✅ validado |
| Núcleos informais / favelas | **Censo 2022 — Favelas e Comunidades Urbanas (vetorial)** | **polígono** | ✅ pronto |
| Status CERURB (regularizados/pendentes) | CERURB | imóvel | ❌ depende de acordo |
| Tipo de posse | CERURB ou coleta própria | imóvel | ❌ depende de acordo |
| Valor venal / PGV | cadastro da Fazenda municipal | imóvel | ❌ via contrato |

**Dos 15 indicadores, 11 são obteníveis hoje com dado aberto.** Só 4 dependem de acordo — e são
exatamente os do núcleo fundiário e fiscal.

# ANEXO E — ÍNDICE CALCULADO COM DADO REAL

# Índice de vulnerabilidade calculado — 121 bairros de Teresina, dado real, fórmula auditável

Executado em 2026-09-15. Substitui o `iv` digitado à mão do protótipo por um índice reprodutível,
construído só com dado aberto do Censo 2022. **Nenhuma negociação, nenhum ofício, nenhum contrato.**

## Fórmula usada nesta demonstração

```
infra_deficit = [ (1−pavimentacao) + (1−iluminacao) + (1−bueiro) ] / 3
    pavimentacao = V05406 / V05400   (faces com via pavimentada / faces no setor)
    iluminacao   = V05412 / V05400
    bueiro       = V05409 / V05400

saneamento_deficit = [ (1−esgoto_ok) + (1−agua_ok) ] / 2
    esgoto_ok = (V00309 + V00310) / V00001
                (rede geral ou pluvial + fossa séptica ligada à rede)
    agua_ok   = V00111 / V00001        (rede geral de distribuição)

iv = 100 × ( 0,35·infra_deficit + 0,35·saneamento_deficit + 0,30·(1−esgoto_ok) )
```

Fontes: Censo 2022 — `Agregados_por_Bairro` (características do domicílio) e
`Agregados_por_Setores_Censitarios_Caracteristicas_urbanisticas_do_entorno_dos_domicilios`
(entorno por face de quadra). Filtro: bairros com ≥30 domicílios e ≥1 face medida
(121 dos 123 qualificaram).

## Resultado — maior vulnerabilidade

| # | Bairro | IV | Pav. | Ilum. | Bueiro | Esgoto | Água | Domic. |
|---|---|---|---|---|---|---|---|---|
| 1 | Brasilar | 63,8 | 44,8% | 92,8% | 3,6% | **6,5%** | 95,1% | 857 |
| 2 | Olarias | 63,1 | 48,6% | 62,2% | 0,0% | 19,0% | 85,4% | 617 |
| 3 | Chapadinha | 62,8 | **36,7%** | 68,7% | 0,7% | 16,1% | 98,0% | 2.026 |
| 4 | Livramento | 62,1 | 92,9% | 82,1% | 0,0% | **0,0%** | 100,0% | 102 |
| 5 | Verdecap | 59,7 | 46,9% | 91,8% | 16,3% | 29,1% | **48,0%** | 654 |
| 6 | Socopó | 59,3 | 83,6% | 96,0% | 11,9% | 9,6% | 79,1% | 759 |
| 7 | Parque São João | 59,2 | 88,9% | 98,1% | 4,6% | 2,1% | 99,7% | 988 |
| 8 | Parque Jacinta | 59,0 | 78,2% | 96,0% | 21,8% | 1,4% | 99,7% | 349 |
| 9 | Parque Juliana | 58,3 | 78,6% | 97,1% | 15,7% | 4,2% | 99,2% | 240 |
| 10 | **Angelim** | 57,4 | 68,4% | 93,0% | 13,9% | 10,7% | 97,3% | **13.860** |

## Menor vulnerabilidade

| Bairro | IV | Pav. | Ilum. | Esgoto |
|---|---|---|---|---|
| Frei Serafim | 7,3 | 98,0% | 98,0% | 98,0% |
| Jóquei | 8,1 | 99,6% | 99,6% | 99,2% |
| Fátima | 10,0 | 99,5% | 99,5% | 97,6% |
| Pirajá | 10,1 | 100,0% | 100,0% | 97,6% |

Distribuição: **IV mínimo 7,3 · mediana 39,2 · máximo 63,8**.

## Validação de plausibilidade

O resultado é **geograficamente coerente**: Frei Serafim, Jóquei e Fátima são bairros consolidados
de alta renda de Teresina e aparecem no fundo do ranking; Brasilar, Olarias, Chapadinha e Verdecap
são periferia e aparecem no topo. O índice não foi calibrado para produzir esse resultado — ele
emergiu do dado.

**Angelim** é o achado operacional: 13.860 domicílios (o maior volume da lista) com apenas 10,7% de
esgotamento adequado. Em termos de população afetada, é a maior prioridade do município — e é
exatamente o tipo de conclusão que um painel existe para produzir.

## Confirmação do problema do protótipo

O protótipo coloca **Mocambinho** como 2º pior bairro (36% de pavimentação). Com dado real,
Mocambinho tem **99,6% de pavimentação** e **não aparece no top 15** de vulnerabilidade.
**Santa Luzia** aparece só em 15º. Os quatro bairros mais vulneráveis de Teresina — Brasilar,
Olarias, Chapadinha e Livramento — **não estão no protótipo**.

## Ressalvas — esta é uma versão de demonstração, não a fórmula final

1. **Faltam três dimensões** da fórmula proposta no parecer técnico: **renda** (existe só por setor
   censitário, exige interpolação areal), **informalidade** (% em favela/comunidade urbana, exige a
   camada vetorial do IBGE) e **dependência demográfica** (0–14 e 65+, disponível por bairro).
2. **O esgoto está com peso duplicado** (entra em `saneamento_deficit` e de novo no terceiro termo).
   Foi deliberado para esta demonstração, porque esgoto é o discriminante mais forte no dado de
   Teresina — mas **não é defensável numa fórmula publicada**. A versão final precisa de pesos
   justificados, idealmente derivados de método reconhecido (p.ex. análise de componentes principais
   ou pesos normativos declarados), não escolhidos por conveniência.
3. **Bueiro (drenagem) é o indicador mais fraco em todo o município** — mediana muito baixa mesmo em
   bairros nobres (Jóquei 55,4%, Frei Serafim 55,9%). Ele pode estar dominando o `infra_deficit`
   indevidamente. Requer análise de sensibilidade antes de entrar na fórmula final.
4. **Erro ecológico:** o índice descreve o bairro, não o domicílio. Um bairro com IV 20 pode conter
   um núcleo informal severo. A camada de favelas do IBGE corrige parcialmente isso.

**Conclusão prática:** a lacuna metodológica mais grave do protótipo — um índice central sem
fórmula — é resolvível em dias, não meses, e com dado que já está baixado. O que exige cuidado não é
a obtenção do dado; é a **justificativa dos pesos**, que é o que será questionado.

# ANEXO F — SEU PARECER DA RODADA 4

Concordo com as correções 1–3 e com o veredito de protótipo como maquete visual.

**Achado 1 (Q1) — Escopo da v1 muda de 60–90 dias para 3–4 semanas, só Teresina, com dado aberto real.**  
Diagnóstico: `Agregados_por_Bairro`, entorno por face (`V05406`, `V05412`, `V05409`), favelas vetoriais e SICONFI eliminam negociação para 11 indicadores; já estão baixados (Anexo 2 itens 1,4,5; Anexo 3 §9).  
Consequência: v1 vira painel territorial aberto com 123 bairros oficiais, camada de favelas, arrecadação real e `iv` calculado; PGV/ML/CERURB ficam fora até haver cadastro/ITBI local.

**Achado 2 (Q2) — Descartar o HTML como código; manter as 11 telas como wireframe; reimplementar 8, congelar 2, manter 1.**  
Diagnóstico: array hardcoded, 18 registros, `iv` sem fórmula, dados que contradizem o IBGE — Mocambinho protótipo 36% vs real 99,6% (Anexo 3 §3–4, §8).  
Consequência: recriar Painel, Mapa, Ranking, Saneamento, Pavimentação, Educação, Perfis e Séries com backend/PostGIS; congelar Simulador e Status CERURB até haver modelo de impacto e convênio; Relatórios viram exportação com metodologia auditável.

**Achado 3 (Q3) — Fórmula publicável para `iv`, com variáveis que já existem por bairro.**  
Diagnóstico: o índice central era número digitado à mão, sem reprodutibilidade (Anexo 3 §3).  
Consequência: `iv = 100*(0.25*infra_deficit + 0.20*saneamento_deficit + 0.20*renda_vul + 0.20*informalidade + 0.15*dependencia)`; onde `infra_deficit = média(1−pav, 1−ilum, 1−bueiro)`; `saneamento_deficit = % domicílios sem esgoto/água`; `renda_vul = % responsáveis ≤1 SM`; `informalidade = % em favela/comunidade`; `dependencia = (0–14 + 65+)/pop`. Pesos e códigos IBGE versionados em script, reprodutível.

**Achado 4 (Q4) — Agregação setor→bairro tem método correto: interpolação por área, não centroide.**  
Diagnóstico: renda só existe por setor; limite de setor não respeita limite de bairro (Anexo 2 item 2).  
Consequência: usar interpolação areal dos polígonos de setor sobre os 123 bairros, com flag de cobertura; bairro com fração de domicílios alocados <80% aparece como “estimado”, e o painel declara erro ecológico e incerteza agregada.

**Achado 5 (Q5) — Transferir modelo Fortaleza→Piauí não é defensável para valor absoluto; usar para método, não para nível.**  
Diagnóstico: mercados imobiliários distintos; no PI não há ITBI aberto e a mediana de IPTU é R$ 2.214/ano (Anexo 1; Anexo 5).  
Consequência: vender no PI conformidade CIB/cadastro primeiro, não PGV; calibrar só depois com ITBI municipal, cartórios via SINTER (IN RFB 2.275/2025) ou cadastro REURB; Fortaleza serve como pipeline e prova de defasagem, nunca como coeficiente transferido.

**Achado 6 (Q6) — Arquitetura final: data ingestion parametrizado → PostGIS → motor de `iv` → API/GeoJSON → frontend; núcleo reutilizável.**  
Diagnóstico: o que quebra o plano é recortar por município desde o início; dashboard não pode ser HTML hardcoded (Anexo 7 Achados 4–5).  
Consequência: construir na ordem: (1) ETL parametrizado por IBGE, (2) schema `municipio/bairro/setor/indicador/fonte/metodologia`, (3) motor de indicadores e remessa CADURB depois; reutilizável: fetchers, schema, iv, frontend; não reutilizável: regras locais de limpeza de endereço, geometria e acordos institucionais.
