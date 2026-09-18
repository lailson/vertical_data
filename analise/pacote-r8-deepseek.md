# Rodada 8 — Eixo técnico. O que os documentos comerciais prometem × o que existe.

A credencial (Anexo 1) afirma como "construído e demonstrável hoje": painel de 123 bairros, conector
CADURB, Laudo de Completude, metodologia publicada, dossiê de contratação.

Na rodada 7 você apontou que o validador, se for só sintático, é "um relatório de `required` que
qualquer um extrai do Swagger" e **bloqueante para justificar R$ 3–5 mil**. Eu levantei a
especificação do que falta (Anexo 4): ~32 regras na spec, tabelas de domínio só no manual (seção 9),
vocabulário oficial de falhas (`TipoFalhaDTO`), e 11 regras semânticas.

Responda no máximo 6 achados:

1. **A credencial promete mais do que o M0 entrega?** Compare item a item (Anexo 1 lista 5 itens) com
   o que foi de fato construído. Onde há exagero, aponte a redação honesta.
2. A metodologia é descrita na credencial como **"sem índices de pesos arbitrários"** — mas usa
   k-means, que você mesmo disse que não elimina arbitrariedade (rodada 7, achado 1). **Essa frase é
   defensável num documento comercial?** Proponha a redação correta.
3. Dado o Anexo 4, **qual é o conjunto MÍNIMO de regras** que o laudo precisa ter para que o preço de
   R$ 3–5 mil seja defensável? Ordene por (valor para o cliente ÷ esforço).
4. O laudo promete "classificação de falhas por regra". Usar o vocabulário oficial do `TipoFalhaDTO`
   é suficiente, ou precisa de camada própria? Como estruturar o relatório.
5. "Conector pronto para operar assim que o município adere" — **é verdade?** Considerando os dois
   fluxos (alfanumérico e geometria por lote+vinculação) e a spec `0.0.1-SNAPSHOT` sem teste de
   divergência, o que exatamente está pronto e o que não está.
6. Riscos técnicos de prometer o que está na credencial sem ter testado contra cadastro real.

Adversarial, concreto. Cite "Anexo N".

# ANEXO 1 — OS DOIS DOCUMENTOS EM REVISÃO

# DOCUMENTOS PRODUZIDOS PELA OUTRA SESSÃO (objeto da revisão)

## A — CREDENCIAL TÉCNICA (1 página)
Quem somos: equipe técnica de dados e gestão territorial, trabalho verificado em fonte primária sobre
o art. 266 da LC 214/2025 (CIB/Sinter) e bases públicas do Piauí. Sem vínculo com Foxinline ou CERURB
— complemento, nunca concorrência direta.

Construído e demonstrável hoje:
1. Painel com 123 bairros de Teresina, geometria oficial IBGE, renda mediana, esgoto, água,
   pavimentação, iluminação, calçada, acessibilidade, demografia, agrupamento estatístico de
   prioridade. 100% público, zero negociação.
2. Conector CADURB gerado da spec OpenAPI pública (15 endpoints, inclui endpoint oficial de validação).
3. Laudo de Completude Cadastral — mede distância entre cadastro e leiaute nacional, relatório
   executivo, classificação de falhas por regra.
4. Metodologia de indicadores publicada — denominadores corretos, mediana de renda, universo
   estatístico, "sem índices de pesos arbitrários".
5. Dossiê de contratação: TR, minuta de dispensa (art. 75, II), calendário de empenho.

Oferta: Diagnóstico (Laudo) R$ 3–5 mil · Conformidade (saneamento + conector + remessa aceita em
homologação, marco condicionado) R$ 12–25 mil · Gestão (painel + relatórios + atualização) R$ 4–8 mil/ano.

Governança: LGPD (operador, sem transferência a terceiros, painéis com dado agregado); sem promessa
de prazo alheia; números auditáveis com fonte e data.

Por que agora: 31/12/2026 é o prazo do art. 266. A partir de 2027, imóvel sem CIB "trava registro em
cartório" (o tributo que o interior arrecada é o ITBI, que depende de registro) e condiciona repasses
do IBS. "No Piauí, apenas Teresina transmitiu cadastro — 188 dos 5.570 municípios do Brasil fizeram
o mesmo." Convênio gratuito, API aberta; falta o cadastro que ela aceita.

## B — DOSSIÊ DE DISPENSA
Base legal alegada: dispensa por valor art. 75, II (limite 2026 R$ 65.492,11, Decreto 12.807/2025);
"vedação ao fracionamento: art. 75, §2º"; divulgação no PNCP art. 176; dotação 3.3.90.39.
Passo a passo em 6 etapas (declaração de necessidade → juntada de TR/3 propostas/dotação → parecer
jurídico → decisão de dispensa + PNCP → assinatura → empenho até 10/12).
Calendário: decisão até 20/11 · contrato até 30/11 · empenho até 10/12.
Regra de ouro: obrigação (laudo em 15 dias úteis do export) × marco condicionado (remessa, depende da
adesão do município; aceite = remessa aceita em homologação OU relatório de impedimento).
Alerta próprio: cashback é arriscado no setor público — formatar como desconto formal na estimativa
de preço; cashback só para privados.
Pacote: fichas dos 8 municípios, TR modelo, minuta de decisão, declaração de necessidade.

# ANEXO 2 — MINHA REVISÃO (verificada em fonte primária)

# Revisão — Credencial técnica e Dossiê de dispensa

## 1. ERRO JURÍDICO DE CITAÇÃO — corrigir antes de enviar a qualquer prefeitura

O dossiê afirma:
> *"Vedação ao fracionamento: **art. 75, § 2º** — o valor do objeto não pode ser repartido para caber
> na dispensa."*

**Está errado.** Texto literal da Lei 14.133/2021:

> **Art. 75, § 1º** — *"Para fins de aferição dos valores que atendam aos limites referidos nos
> incisos I e II do caput deste artigo, deverão ser observados: I – o somatório do que for despendido
> no exercício financeiro pela respectiva unidade gestora; II – o somatório da despesa realizada com
> objetos de mesma natureza, entendidos como tais aqueles relativos a contratações no mesmo ramo de
> atividade."*

O **§ 2º** trata de outra coisa: **duplica** os valores dos incisos I e II para contratações por
**consórcios públicos, autarquias e fundações qualificadas como agências executivas**.

**Dois motivos para corrigir já:**
1. O jurídico do município **vai** conferir a citação. Errar o parágrafo num documento que se
   apresenta como "dossiê pronto" custa mais credibilidade do que o erro em si.
2. O § 2º, citado corretamente, é **argumento a favor**: se o município contratar via **consórcio
   intermunicipal** — que é a via de escala recomendada no plano, através da APPM — **o limite
   dobra para R$ 130.984,22**.

## 2. O limite de 2026 está CORRETO — e é melhor do que o plano vinha assumindo

Verificado: **Decreto nº 12.807, de 29/12/2025**, reajuste de **4,41%** (IPCA-E de jul/2024 a
jun/2025), vigente desde 01/01/2026:

| Inciso | Objeto | Limite 2026 |
|---|---|---|
| Art. 75, I | obras e serviços de engenharia | R$ 130.984,20 |
| **Art. 75, II** | **compras e demais serviços** | **R$ 65.492,11** |

O plano consolidado vinha usando **"~R$ 59 mil"**. **Corrigir para R$ 65.492,11** — são R$ 6,5 mil a
mais de espaço, o que importa na soma do item 3.

## 3. O RISCO REAL que o dossiê levanta mas não resolve: a soma dos três produtos

Pelo **§ 1º, II**, somam-se no exercício as despesas com **objetos de mesma natureza** — "contratações
no mesmo ramo de atividade". Os três produtos ofertados são inequivocamente do mesmo ramo:

| Produto | Valor |
|---|---|
| Laudo de Completude | R$ 3–5 mil |
| Conformidade (saneamento + conector + remessa) | R$ 12–25 mil |
| Painel territorial (anual) | R$ 4–8 mil |
| **Soma no exercício** | **R$ 19–38 mil** |

**Boa notícia: cabe no limite de R$ 65.492,11**, com folga. Não há fracionamento ilícito por
estouro — e como a soma não ultrapassa o teto, **não há licitação obrigatória sendo substituída**,
que é o núcleo do que o TCU pune.

**Mas há uma exposição de forma, e ela é evitável:** três dispensas sequenciais, mesmo fornecedor,
mesma natureza, mesmo exercício é o padrão visual que órgão de controle marca primeiro e pergunta
depois. A defesa existe e é boa — **o laudo é o que dimensiona o escopo do segundo contrato; não se
pode precificar saneamento cadastral sem saber o tamanho do problema** — mas ela precisa estar
**escrita no processo**, não improvisada na auditoria.

**Três encaminhamentos, em ordem de preferência:**
1. **Contratar laudo + conformidade numa dispensa só**, com o laudo como primeira etapa do
   cronograma físico e o valor da segunda etapa **ajustável por medição** conforme o resultado do
   laudo. Elimina a exposição e reduz o processo de dois para um.
2. Se forem separados: a declaração de necessidade da segunda contratação **cita o laudo como
   estudo técnico preliminar que a fundamentou** — o encadeamento vira justificativa em vez de
   indício, e o somatório do exercício aparece declarado no processo.
3. O painel anual, por ser objeto distinto (gestão, não conformidade) e recorrente, **contratar em
   exercício seguinte** ou como item separado com justificativa própria.

## 4. O alerta sobre cashback está CERTO e corrige o parecer comercial

O dossiê registra que o cashback é arriscado em contratação pública — *"devolução condicionada a
contrato futuro pode ser vista como desconto irregular"*. **Concordo, e isso supera a recomendação
do parecer de negócio da rodada anterior**, que propôs o cashback sem considerar o regime público.

A saída proposta — **desconto formal justificado na estimativa de preço do pacote** — é a correta,
porque aparece no processo como redução de preço fundamentada, não como devolução condicionada.
Guardar o cashback para clientes privados (cartórios, loteadoras, escritórios) é o encaminhamento
certo.

## 5. Afirmações da credencial que precisam de lastro antes de circular

> *"No Piauí, apenas Teresina transmitiu cadastro — 188 dos 5.570 municípios do Brasil fizeram o mesmo."*

**Não verifiquei nenhum dos dois números**, e eles são o coração do argumento "por que agora".
São exatamente o tipo de dado que o interlocutor pode conferir — e que, se estiver errado, derruba a
credibilidade de tudo que vem antes.

**Antes de circular:** confirmar na página de estatísticas do Sinter, com data de consulta impressa
no rodapé do documento. Se a fonte for o e-SIC ainda não respondido, **escrever "dado a confirmar"**
em vez de afirmar.

Mesmo cuidado com *"a partir de 2027: imóvel sem CIB trava registro em cartório"*. A página oficial
da RFB diz **"terão problemas em transações e regularização"** e **"municípios cujos imóveis não
possuem inscrição no CIB não receberão repasses do IBS"**. "Trava registro" é interpretação
plausível — e provavelmente o que ocorrerá na prática — mas **não é o que a norma diz literalmente**.
Em documento comercial para ente público, usar a formulação oficial e apresentar a consequência
prática como leitura, não como texto de lei.

## 6. O que está bom e deve ser mantido

- **A separação obrigação × marco condicionado** é a melhor decisão dos dois documentos. Protege de
  prometer prazo que depende de ato do próprio contratante, que era o risco jurídico mais provável
  de quebrar o primeiro contrato.
- **O critério de aceite do marco** — *"remessa aceita em homologação OU relatório técnico de
  impedimento"* — é exatamente como se redige obrigação de meio sem virar obrigação de resultado
  sobre ato de terceiro.
- **O calendário de empenho** (decisão até 20/11, contrato até 30/11, empenho até 10/12, evitando a
  quinzena final) demonstra entendimento do ciclo orçamentário — e é o tipo de detalhe que faz um
  secretário confiar no fornecedor.
- **A dotação 3.3.90.39** está correta para serviços de terceiros – PJ.
- **"Sem vínculo com a Foxinline — complemento, nunca concorrência direta"** é o posicionamento certo
  e deve ser dito exatamente assim.

## 7. Ajuste de redação na tabela de oferta

A credencial apresenta:
> *Conformidade — Saneamento + conector + **remessa aceita em homologação** (marco condicionado) — R$ 12–25 mil*

Colocar "remessa aceita" na coluna de **produto** e a condicionalidade entre parênteses cria
ambiguidade justamente no ponto que o dossiê acertou em separar. **Inverter a ênfase:**

> *Conformidade — saneamento cadastral, integração e **apoio à remessa**; entrega condicionada à
> adesão do município ao convênio Sinter. Aceite: remessa aceita em homologação ou relatório de
> impedimento.*

# ANEXO 3 — A LINHA DO DECK VIA ITBI (novo, verificado)

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

# ANEXO 4 — ESPECIFICAÇÃO DO QUE FALTA NO VALIDADOR

# Especificação do que falta no validador — extraída da spec e do manual

O parecer técnico foi direto: *"validação apenas sintática entrega um relatório de `required` que
qualquer um extrai do Swagger — **bloqueante para justificar R$ 3–5 mil**"*. Isto aqui transforma essa
crítica em lista de trabalho.

## 1. O que a spec OpenAPI JÁ oferece além do `required`

Inventário completo do `api-docs`:

| Tipo de regra | Quantidade | Exemplos |
|---|---|---|
| `pattern` | **3** | CIB `^[a-zA-Z0-9]{8}$` · **CEP `\d{8}`** · CNM do RI `\d{15,16}` |
| `maxLength` / `minLength` | **21** | `inscricaoImobiliaria` 0..45 · `nomeLogradouro` 0..150 · `bairro` 0..30 · `nomeTitular` 0..300 · `numMatriculaRI` 0..15 |
| `minimum` / `maximum` | ~8 | **`anoConstrutivo` 1900..2100** · `percTitularidade` 0.0..1.0 · `percTransacionadoITBI` 0.0..1.0 · `tipoDesativacao` 1..2 · `motivoDesativacao` 1..10 · `cnsRI` 1..999999 |
| `enum` | **1** | só `TipoFalhaDTO` (é resposta, não entrada) |

**São ~32 regras verificáveis automaticamente**, todas extraíveis da spec — e o validador deveria
aplicar todas, não só o `required`.

## 2. O buraco: os campos de domínio são `int32` puro na spec

Estes campos **não têm enum** na spec, mas só aceitam valores de tabelas fechadas:

`tipoImovel` · `tpArquitetonico` · `destinacaoImovel` · `padraoConstrutivo` · `tipoLogradouro` ·
`tipoTitularidade` · `docTitularidade` · `bice` · `tpTransacaoITBI`

**As tabelas estão no Manual Operacional, seção 9 — e só lá:**

| Seção | Tabela | Exemplo verificado |
|---|---|---|
| 9.1 | Tipo Imóvel | `01` Territorial (sem edificação) · `02` Predial (com edificação) · `03` Bem imóvel de características especiais |
| 9.2 | Tipo Arquitetônico | `01` Casa · `02` Apartamento · `03` Vaga de garagem … |
| 9.3 | BICE | |
| 9.4 | Destinação do Imóvel | |
| 9.5 | Padrão Construtivo | |
| 9.6 | Tipo de Logradouro | |
| 9.7 / 9.8 | Tipo de Titularidade / Doc Titularidade | |
| 9.11 / 9.13 | Tipo de Operação / Tipo de Transação | |

**Consequência prática:** um validador que lê só a spec **aceita `tipoImovel = 7`**, que a API vai
rejeitar. As tabelas precisam ser extraídas do PDF e versionadas junto — e essa é justamente a parte
que "qualquer um extrai do Swagger" **não** cobre.

## 3. O vocabulário oficial do laudo

`TipoFalhaDTO` traz o enum que a API usa para classificar erro. **O laudo deve usar exatamente estes
rótulos**, para que o relatório offline fale a mesma língua da resposta oficial:

```
CAMPO_NAO_INFORMADO_OU_NULO
CAMPO_COM_FORMATACAO_INVALIDA
CAMPO_COM_TAMANHO_INVALIDO
DATA_COM_FORMATO_INVALIDO
CAMPO_COM_VALOR_INVALIDO
CAMPO_COM_PRRENCHIMENTO_INCOMPATIVEL   ← typo é do próprio SERPRO; reproduzir como está
CAMPO_COM_DV_INVALIDO
```

Alinhar o laudo a este vocabulário tem efeito comercial direto: quando o município rodar a validação
oficial, os erros terão **os mesmos nomes** do laudo que ele comprou. Isso é o que faz o diagnóstico
parecer — e ser — a antecipação fiel do resultado.

E `CAMPO_COM_DV_INVALIDO` revela que **há campos com dígito verificador** a validar (CPF/CNPJ de
titulares e de partes do ITBI, e o próprio CIB).

## 4. As regras semânticas que a spec NÃO tem e são o valor real do diagnóstico

Nenhuma delas é derivável do Swagger — e são elas que justificam o preço:

| Regra | Por que importa |
|---|---|
| **CEP existe e pertence ao município** | CEP com 8 dígitos passa no `pattern` e ainda assim aponta para outra cidade |
| **`tipoLogradouro` + `nomeLogradouro` conferem com a base dos Correios/IBGE** | logradouro inexistente é rejeição na origem |
| **`inscricaoImobiliaria` única no arquivo** | duplicidade é o erro mais comum em cadastro de planilha |
| **CPF/CNPJ com DV válido** (titulares, transmitentes, adquirentes) | `CAMPO_COM_DV_INVALIDO` existe no vocabulário oficial |
| **Coerência `tipoImovel` × `areaConstruida`** | territorial (01) com área construída **não recebe CIB** — regra explícita do manual |
| **Coerência `tipoImovel` × `tpArquitetonico`** | mesma regra, no sentido inverso |
| **`anoConstrutivo` ≤ ano corrente** | a spec aceita até 2100 |
| **Soma de `percTitularidade` = 1,0 por imóvel** | cada campo é 0..1, mas a soma não é validada |
| **Soma de `percTransac…ITBI` = 1,0** | idem |
| **`areaTerreno` > 0 e dentro de faixa plausível** | a spec não impõe mínimo |
| **Cobertura: % de imóveis do cadastro que sequer têm cada campo obrigatório** | **é a métrica-chave do laudo** — o "% de completude por bloco" |

## 5. Três itens bloqueantes antes de vender o laudo

1. **Pinar a spec por hash.** Ela é `0.0.1-SNAPSHOT` e muda sem aviso. Sem um teste que falhe quando
   divergir, o laudo pode ser emitido contra contrato obsoleto — e o cliente descobre isso na
   validação oficial, o que é o pior lugar possível.
2. **Embutir as tabelas de domínio da seção 9** do manual, versionadas.
3. **Implementar as regras semânticas da seção 4 acima.** Sem elas o produto é um `required`-checker.

## 6. Um item que deixa de ser bloqueante se for descopado explicitamente

O fluxo de geometria (`idLotePonto`/`idLotePoligono`, envio por lote + `/vinculacoes/{idLote}`)
**só é bloqueante se o pitch prometer georreferenciamento**. Duas saídas honestas:
- descope explícito — *"diagnóstico alfanumérico"* — e a geometria vira upsell; ou
- implementar lote + vinculação antes de prometer.

O que não pode é vender "conformidade CIB completa" entregando metade. E lembrando: a metade que
falta é justamente a que a REURB entrega paga por lei.

# ANEXO 5 — SEU PARECER DA RODADA 7

Concordo com o Anexo 1 §5 (k-means não elimina arbitrariedade).

1. **k-means** (Anexo 2 §3) afirma “reproduzível” com sementes fixas, mas a normalização min–max usa min/max da amostra; incluir um município muda o intervalo e pode remapear grupos de todos os bairros. Consequência: índice oficial deve usar cortes fixos e pesos declarados; k-means fica só como camada exploratória.

2. **V05000** (Anexo 1 §3): adicionar `cobertura_entorno` é necessário, mas insuficiente. Consequência: o pipeline deve tratar `cobertura < 90%` como dado ausente e excluir o bairro do ranking, não apenas exibir selo; senão o painel de Altos/Guaribas apresenta amostra como censo.

3. **Spec `0.0.1-SNAPSHOT`** (Anexo 1 §7) sem teste de divergência pode gerar laudo contra contrato obsoleto. Consequência: bloqueante para vender diagnóstico; exigir hash pinado da spec e falha explícita no CI antes de qualquer laudo.

4. **Validação apenas sintática** (Anexo 1 §7 item 3) entrega um relatório de `required` que qualquer um extrai do Swagger. Consequência: bloqueante para justificar R$ 3–5 mil; sem CEP, logradouro/município, inscrição única e área/tipologia, o diagnóstico não vale o preço.

5. **Fluxo de geometria** (Anexo 1 §7 item 2; Anexo 4 §4) só é bloqueante se o pitch prometer geometria/REURB. Consequência: ou descope explícito “diagnóstico alfanumérico apenas” no M0, ou a promessa exige implementar lote + vinculação antes de vender.

6. **Erro factual na metodologia** (Anexo 1 §4): Tabajaras tem razão média/mediana 1,11, não “muito inferior”. Consequência: trocar o exemplo por Brasilar/Mocambinho antes de publicar; manter Tabajaras dá munição a qualquer parecer contrário.
