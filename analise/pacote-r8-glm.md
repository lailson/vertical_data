# Rodada 8 — REVISÃO DOS DOCUMENTOS COMERCIAIS. Eixo negócio/jurídico.

A outra sessão produziu a credencial técnica e o dossiê de dispensa (Anexo 1). Eu verifiquei em fonte
primária e achei (Anexo 2): (a) erro de citação — a vedação ao fracionamento é o **§1º** do art. 75,
não o §2º (o §2º DOBRA o limite para consórcios públicos, o que favorece a via APPM); (b) o limite
2026 é R$ 65.492,11, maior do que vínhamos usando; (c) a soma dos três produtos no exercício
(R$ 19–38 mil) cabe no limite, mas três dispensas sequenciais do mesmo fornecedor é exposição de
forma; (d) o alerta deles sobre cashback em ente público **corrige a sua recomendação da rodada 7**.

Responda no máximo 6 achados, só o que muda:

1. **O cashback que você propôs não serve para município** (Anexo 2, seção 4). Aceite ou conteste.
   Se aceitar, qual o substituto que preserva o efeito (filtro de compromisso + risco devolvido)
   dentro do regime de contratação pública?
2. **§2º dobra o limite para consórcios públicos** → R$ 130.984,22 via APPM. Isso muda a estratégia
   de canal? Vale desenhar a oferta já em formato consorciado desde o início?
3. **Contratar laudo + conformidade numa dispensa só** (com segunda etapa ajustável por medição) vs.
   **duas dispensas encadeadas**. Qual você recomenda comercialmente, considerando que a primeira
   opção pede um compromisso maior logo na entrada?
4. A credencial afirma "apenas Teresina transmitiu cadastro no PI" e "188 de 5.570 no Brasil"
   (Anexo 1) — **não verificados**. Qual o risco de circular número não confirmado, e qual a
   formulação segura que preserva a força do argumento?
5. Com o ITBI por município agora disponível (Anexo 3) e o achado de que **no interior o ITBI supera
   o IPTU** — como isso entra na credencial e no pitch? Reescreva o "Por que agora" em até 5 linhas.
6. Veredito: os dois documentos estão prontos para circular após as correções, ou falta algo material?

Adversarial, quantificado. Cite "Anexo N".

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

# Parecer R7 — GLM · Eixo negócio · Revisão do M0

**Data:** 2026-09-16 · **Base:** pacote-r7-glm.md (Anexos 1–5) · **Formato:** 6 achados, só o que muda a execução comercial.

**Veredito antecipado (Achado 6): O M0 DESTRAVOU A VENDA.** Não resta nenhuma dependência externa
no caminho produto → primeira reunião → contrato. O que falta é ~1 semana de artefato interno
(laudo com cara de produto, linha de R$/ano, dossiê) e decisão de agenda. Duas correções obrigatórias
no pacote: o e-SIC nº 2 como escrito morre por design (Achado 2) e "laudo grátis" do jeito proposto
destrói a âncora que o próprio plano proíbe destruir (Achado 5).

---

## 1. O validador offline muda a ABERTURA da sequência, não a sequência — e o laudo não custa "quase nada"

**A sequência fazenda → prefeito → APPM (parecer R6, Achado 3; Anexo 5 §12.3) continua exatamente
como está.** O que o validador offline muda é o conteúdo da primeira reunião: ela passa a abrir com
um artefato, não com um pitch. A diferença comercial é material — equipe sem marca apresentando
slide é interrupção; equipe sem marco apresentando laudo do próprio cadastro do município é reunião
que marca a si mesma.

**O desenho operacional da abertura, em duas etapas:**
- **Reunião 1 (secretário):** laudo-DEMO sobre base exemplo + o pedido de 30 segundos — *"mande o
  export do seu cadastro; em 72h devolvo o diagnóstico de conformidade com o CADURB"*. O pedido do
  export é o filtro de qualificação mais barato possível: quem manda tem dor; quem não manda não ia
  comprar. E quem cede o arquivo já fez um investimento psicológico no processo.
- **Reunião 2:** laudo DO município na mesa, dossiê de dispensa preenchido (Anexo 5 §11.7) e o
  processo pronto para o prefeito. O laudo abre; o dossiê fecha.

**Desafio à premissa da pergunta: "custa quase nada para produzir" é falso até o E2 existir.** O
custo de PROCESSAMENTO é ~zero; o custo real é a **ingestão semântica do export** — cadastro
municipal vive em formato de ERP/geoprocessamento, e a validação que dá valor ao laudo é a que vai
além do schema: CEP existente, logradouro × município, área × tipologia, inscrição duplicada
(Anexo 1 §7.3). São **1–2 dias de engenharia por município** contra capacidade declarada de ~2
contas/mês (Anexo 5 §11.2). Isso importa três vezes: (i) limita quantos laudos podem sair por mês;
(ii) vira o argumento central de precificação do Achado 5; (iii) o `exemplo_base.csv` de 5 imóveis
prova o fluxo, não o produto (Anexo 1 §7.4).

**Um limite jurídico do "vender antes de credencial":** pode-se vender o LAUDO (offline,
entrega controlável pela Capybara). **Não se pode prometer remessa com data** — a credencial depende
do Termo do município no e-CAC com ICP-Brasil + DOU (Anexo 4 §5.2), fora do controle da Capybara.
O contrato precisa separar as duas entregas: diagnóstico = obrigação; remessa = marco condicionado
à adesão do próprio município. Quem prometer as duas com a mesma caneta vai quebrar prazo no
primeiro cliente.

**Precificação (resumo; detalhe no Achado 5): preço por valor, nunca custo+margem.** O laudo não
vende "um relatório"; vende a dimensão do problema: quantos % do cadastro será rejeitado, quantos
R$/ano de IBS estão sobre imóveis sem inscrição e qual o tamanho do saneamento. É o documento que
dimensiona o contrato de R$ 12–25 mil. R$ 3–5 mil não é preço de relatório — é preço de diagnóstico
que antecipa uma decisão de 3–5× o seu valor.

## 2. e-SIC nº 2 (SEFAZ-PI) como escrito é pedido que morre — e a linha "R$/município/ano" do deck não precisa de e-SIC nenhum

**Os itens 2 e 3 do pedido à SEFAZ pedem que o órgão PRODUZA estudo que não existe.** "Estimativa
anual por município do IBS imobiliário 2027–2032, com metodologia" e "impacto estimado da ausência
de CIB sobre repasses" não são informações — são trabalhos técnicos. A LAI assegura acesso a
documento existente; pedido que exige elaboração dá ao agente de informação a resposta pronta de
**"pedido indevido"** — e a SEFAZ ainda cumpre o prazo com ela. Resultado: **25 dias (15+10, Anexo 3)
queimados** exatamente na janela em que o deck precisa do número.

**A pergunta está certa; o veículo está errado. Reformular para dado existente:**
1. Manter o item 1 (critério estadual de vinculação do IBS imobiliário — art. 11, II, LC 214/2025):
   é informação documental, portaria/instrução, resposta rápida e útil.
2. Trocar itens 2–3 por: **arrecadação de ITBI por município do PI, 2022–2025** (se a SEFAZ
   gerenciar arrecadação delegada/convênio), com formato por município.

**E o achado que muda a semana: o número do deck sai de fonte pública HOJE, sem e-SIC.** O
**SICONFI/FINBRA do Tesouro publica a receita realizada de ITBI por município, ano a ano** — download
público, série histórica, os 152 municípios de uma vez (ferramenta que o projeto já usa: Anexo 5 §1
do pacote-r6 usou SICONFI para Altos/Paulistana). Método para a linha do deck, todo auditável:
**ITBI anual realizado por município** (base imobiliária transacionada em R$) **× cronograma
IBS/ITBI da transição × fração do estoque sem regularidade** — proxy: o Censo 2022 publicou o corte
de domicílios próprios com/sem escritura definitiva (conferir o recorte municipal no SIDRA antes de
usar). "Nossa estimativa, método declarado, fontes oficiais" é MAIS forte no deck do que um número
de SEFAZ vindo com ressalvas grossas — e chega em meio dia, não em 25 dias.

**Demais pedidos do Anexo 3:**
- **Nº 1 (RFB): aprovar** — é o denominador do mercado (188 municípios com inscrições ativas no
  país em 15/09; o restante é endereçável). Antes de enviar, os **10 minutos de verificação do
  `inscricoes_ativas_*.csv`** (Anexo 1 §6): se o arquivo existir, parte da resposta sai no mesmo dia
  e o pedido fica mais cirúrgico.
- **Nº 3 (SEAD/PROUrbe): aprovar e enviar primeiro** — é o que decide alvo (Anexo 5 §12.4), fecha a
  cega do `cerurb.prourb` e não depende de ninguém.
- **Falta um texto pronto: TCE-PI — dispensas de software/geoprocessamento 2024–26** (opcional do
  Anexo 5 §12.4). É o único meio de conhecer preço praticado e concorrência antes de fixar a própria
  faixa — e alimenta o gatilho de comoditização <R$ 8 mil (Anexo 5 §11.12).
- **4–6 (vitrine): manter rebaixados.** Desperdício não é; distração seria.

## 3. Fragilidade do cadastro: é venda se o laudo medir a distância a uma norma NOVA; é constrangimento se medir a qualidade do cadastro

**O erro de enquadramento possível é apresentar o laudo como juízo sobre o trabalho do secretário.
O enquadramento que desarma é a data:** o CIB/CADURB é exigência da **LC 214/2025** — nenhuma
prefeitura construiu cadastro pensado nela; cadastros com uma década raramente têm os campos
obrigatórios no padrão exigido (Anexo 1 §1). O laudo não mede "seu cadastro é ruim"; mede **a
distância entre o cadastro e uma exigência federal com menos de um ano de vida**. O réu na reunião é
o prazo federal e o cartório (Anexo 5 §11.3), nunca a gestão local.

**Cinco regras de apresentação:**
1. **O laudo abre com o que o município TEM** (base existente, campos conformes), depois o que
   falta, depois o plano. Diagnóstico sem plano é crítica; diagnóstico com plano de saneamento é o
   **espelho do escopo do contrato** — cada bloco do laudo é uma linha da proposta.
2. **Linguagem de norma, nunca de juízo:** "não conforme com o campo X do schema" — não
   "incompleto", "defasado", "precarizado".
3. **A versão executiva que sobe ao prefeito é revisada pelo secretário.** A propriedade do
   diagnóstico passa a ser dele — ele vira o proponente interno (Anexo 5 §12.3.1), não o acusado.
4. **Confidencialidade declarada** (laudo confidencial, versão executiva sem dados crus): laudo de
   fragilidade fiscal circulando é presente para a oposição — controle de versão desde o primeiro
   dia.
5. **Começar onde não há dono de cadastro a ofender:** os 2 pilotos REURB (Guaribas, N. Sra. de
   Nazaré — cadastro praticamente inexistente) e os 8 do sinal RREO (cadastro fraco). **Por
   coincidência estratégica, são exatamente os alvos do M0 (Anexo 5 §12.5.4)** — o problema político
   só existe nos municípios que não estão na primeira lista.

## 4. Primeira reunião comercial: falta ~1 semana de artefato e ZERO dependência externa — em ordem

**O que falta, em ordem:**
1. **Laudo-demo com cara de produto** — template executivo (4–6 páginas: resumo, conformidade por
   campo, plano) rodando sobre base exemplo. Hoje existe script + CSV de 5 imóveis (Anexo 1 §7.4);
   isso não é artefato de reunião. 2–3 dias.
2. **Linha R$/município/ano do deck** via FINBRA/SICONFI + Censo (Achado 2). Meio dia.
3. **Dossiê de dispensa preenchido para os 8 do RREO** (Anexo 5 §12.5.6, §11.7 — "o caminho
   orçamentário é parte do produto"). 1–2 dias, reutilizável.
4. **1 página de credencial técnica:** metodologia publicada (M0 item 3) + "spec do CADURB validada
   campo a campo contra o ambiente do SERPRO" (Anexos 1 §1 e 4) — para equipe sem marca, isso é o
   que existe de mais próximo de referência.
5. **Agenda** — e a primeira reunião do cronograma segue sendo a de **escopo com o proponente REURB**
   (Anexo 5 §12.5.1), que destrava os 2 pilotos; as de secretário correm em paralelo.

**O que NÃO é pré-requisito (lista anti-adiamento):**
- **Credencial/token CADURB** — o laudo é offline; a ordem oficial é cliente/validador → laudo →
  integração (Anexo 4 §5).
- **Qualquer resposta de e-SIC** — nenhum item da primeira reunião depende deles; a linha de IBS
  sai do FINBRA (Achado 2).
- **Remessa aceita em homologação** — exigência da conversa com APPM (Anexo 5 §12.3.3), não do
  secretário.
- **APPM, canal TJ, Foxinline** (Anexo 5 §12.2–12.3) — todos pós-prova ou pós-aceite.
- **Disputa k-means × índice com pesos** (Anexo 1 §5) — o painel/IV é produto de 2027, upsell de
  planejamento, fora da venda B (Anexo 5 §12.3.4).
- **Fluxo de geometria do conector, teste de divergência da spec SNAPSHOT** (Anexo 1 §7.1–7.2) —
  bloqueiam a REMESSA, não a venda do laudo.
- **Correção do exemplo Tabajaras** (Anexo 1 §4) — bloqueia a PUBLICAÇÃO da metodologia (meio dia,
  fazer antes do item 4 acima), não a reunião.

**Teste do anti-adiamento: se em 7 dias não houver ≥2 agendas marcadas (proponente + 1 secretário),
o bloqueio não é material — é de execução.** A meta de 2–3 contratos até 15/11 (Anexo 5 §12.1)
exige 20–40 processos ativos; cada semana de artefato sem agenda é semana do ciclo de 3–6 semanas
queimada.

## 5. Preço do laudo: manter R$ 3–5 mil com REEMBOLSO na assinatura — nunca preço-zero declarado

**"Dar de graça" tem dois custos que o pacote não contabiliza:**
1. **Âncora:** preço circula — secretários de fazenda e APPM formam o mercado mais falante do PI.
   Laudo a R$ 0 hoje mata a faixa R$ 3–5 mil **para sempre nos 152**, e arrisca contaminar a
   percepção da faixa R$ 12–25 mil (se o diagnóstico não vale nada, quanto vale a correção?). O
   próprio plano veda subsídio em dinheiro por exatamente esse motivo: "desconto destrói a âncora
   de risco" (Anexo 5 §11.5).
2. **Vazamento:** laudo grátis + spec pública (Anexo 4 §1) entrega à Foxinline o desenho completo do
   diagnóstico — de graça e sem contrato. Laudo PAGO tem controle de versão, NDA e contrapartida.

**E o custo não é zero:** 1–2 dias de ingestão por município (Achado 1) ≈ **R$ 1–1,5 mil por laudo**
em engenharia. Dez laudos grátis = 2–4 semanas da capacidade de 2 contas/mês (Anexo 5 §11.2).

**O formato que resolve os três lados — cashback:**
- **Preço de tabela mantido: R$ 3–5 mil**, dentro da dispensa por valor (0,006–0,011% da RCL
  mediana — subproduto do cálculo do Anexo 5 §11.7).
- **Nos 10 primeiros (8 do RREO + 2 pilotos): "programa piloto"** — laudo pago com **reembolso
  integral na assinatura do pacote em 60 dias** + contrapartidas: **cadastro completo cedido para
  calibração** (que resolve o teste real que falta ao M0 — Anexo 1 §7.4) e depoimento/case se fechar.
  Escassez declarada: 10 vagas, justificadas como orçamento de P&D — não como promoção.

**Por que cashback vence as três alternativas:**
- **vs. grátis antecipado:** devolve ao comprador a objeção de risco ("se fechar, o laudo saiu
  grátis") **sem declarar preço zero** — a âncora fica intacta no papel que circula.
- **vs. pago seco:** elimina a principal resistência (pagar por diagnóstico antes de decidir) porque
  o risco é devolvido — mas mantém o **filtro de compromisso**: quem não empenha R$ 4 mil
  reembolsáveis não ia empenhar R$ 15 mil de pacote. O empenho do laudo é ensaio do empenho do
  contrato.
- **vs. baixar o preço:** não há ganho — a faixa já é pequena para dispensa direta; baixar só
  rebaixa a referência do gatilho de comoditização <R$ 8 mil (Anexo 5 §11.12).

**Trade-off quantificado (hipóteses explícitas, âncora em Anexo 5 §12.1):** conversão de propostas
→contratos do plano é 20–30% (8–12 propostas → 2–3 contratos). Por 10 laudos entregues no programa
piloto: custo R$ 10–15 mil (ingestão) → 2–3 contratos × R$ 15 mil médio = **R$ 30–45 mil**, mais o
ativo não-financeiro que faltava: **10 cadastros reais calibrando o validador** e 1–2 cases com
depoimento para a conversa de APPM. Grátis puro eleva o topo de funil (90% aceitam vs ~50–60% que
empenham) mas derruba a conversão (sem compromisso), vaza o ativo e queima a âncora; pago seco
filtra demais para uma operação que precisa de **cadastro e referência tanto quanto precisa de
caixa**. O cashback paga os dois com o mesmo preço de tabela.

## 6. Veredito: o M0 destravou a venda — o que sobrou é uma semana de artefato e decisão de agenda

**A cadeia produto→venda está sem nenhuma dependência externa:** spec pública com endpoint oficial
de validação sem inserir (Anexo 4 §3) + laudo offline sem credencial (Anexo 4 §5) + alvos já
qualificados sem e-SIC (8 do RREO, 2 pilotos REURB — Anexo 5 §12.5) + linha de IBS por fonte pública
(Achado 2) + caminho orçamentário mapeado (Anexo 5 §11.7). Nenhuma dessas condições melhora com
espera — e a janela de empenho 2026 (Anexo 5 §11.1) corre para trás delas.

**O único risco material remanescente é o que o M0 não testou: nenhum cadastro real passou pelo
validador** (Anexo 1 §7.4). A resposta comercial correta é não tratá-lo como blocker e sim como
**propósito do programa piloto do Achado 5**: cada laudo das 10 vagas é, ao mesmo tempo, venda,
filtro de compromisso e teste real de ingestão. O risco se consome na entrega paga — não em sprint
interno.

**O que NÃO destrava nada e não pode atrasar a semana comercial:** k-means × pesos (Anexo 1 §5 —
importante para 2027, irrelevante para a venda B), exemplo Tabajaras (Anexo 1 §4 — meio dia, antes
de publicar metodologia), `cobertura_entorno` no GeoJSON (Anexo 1 §3 — qualidade do painel, produto
de 2027). Fila separada, meio-dias, depois da agenda marcada.

**Métrica de controle do destravamento:** em 7 dias, ≥2 agendas (proponente REURB + 1 secretário) e
laudo-demo existindo como PDF. Abaixo disso, o gargalo deixou de ser o M0 — e dizê-lo em voz alta é
o que impede a semana perfeita de virar mês.
