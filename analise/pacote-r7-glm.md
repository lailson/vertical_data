# Rodada 7 — REVISÃO DO M0. Eixo negócio.

A outra sessão executou: (a) conector CADURB + **validador de completude offline** que gera o laudo
SEM credencial — ou seja, o produto de entrada de R$ 3–5 mil existe hoje; (b) metodologia do índice
publicada; (c) textos de e-SIC prontos para envio (Anexo 3), com a prioridade que você recomendou
(RFB e SEFAZ-PI primeiro, Teresina depois).

Responda no máximo 6 achados, só o que muda a execução comercial:

1. **Com o validador funcionando offline, o produto de entrada pode ser vendido ANTES de qualquer
   credencial ou convênio.** Isso muda a sequência comercial que você definiu na rodada 6 (fazenda →
   prefeito → APPM)? O laudo vira a peça de abertura de reunião? Como precificar um laudo que custa
   quase nada para produzir mas vale muito para o comprador?
2. Os textos de e-SIC (Anexo 3) estão bons? **Falta algum pedido, ou algum deles é desperdício?**
   Avalie especialmente o da SEFAZ-PI (converter perda de IBS em R$/município/ano) — é factível
   esperar resposta útil de uma SEFAZ sobre isso, ou é pedido que morre?
3. O laudo de completude expõe a **fragilidade do cadastro do município**. Isso é argumento de venda
   ou é constrangimento político que trava a compra? Como enquadrar sem ofender o secretário que
   construiu aquele cadastro.
4. Com o M0 pronto e o painel pronto, **o que ainda falta para a primeira reunião comercial
   acontecer?** Liste em ordem, e diga o que NÃO é pré-requisito (para não virar desculpa de adiar).
5. **Preço do laudo:** R$ 3–5 mil foi a faixa definida. Com o validador automatizado, o custo
   marginal é quase zero. Manter o preço, baixar para entrar mais rápido, ou dar de graça como
   isca do pacote de R$ 12–25 mil? Quantifique o trade-off.
6. Veredito: o M0 destrava a venda ou ainda falta algo material?

Adversarial, quantificado. Cite "Anexo N".

# ANEXO 1 — MINHA REVISÃO DO M0 E DOS DOCS (verificada)

# Revisão do M0 e dos documentos produzidos na outra sessão (16/09/2026)

Revisão feita com verificação independente contra fonte primária. Ressalva: **o código do M0
(`cadurb_client.py`, `validador_completude.py`, `spec/openapi-homologacao.json`, `exemplo_base.csv`)
não está nesta máquina** — a revisão do M0 é sobre o que foi descrito e sobre as afirmações técnicas
verificáveis, não sobre o código em si.

## 1. VERIFICADO E CORRETO — obrigatoriedade do CADURB

Alegado: `DadosGeraisImovel{areaTerreno, inscricaoImobiliaria, temBairro, tipoImovel}` e
`EnderecoImovel{cep, nomeLogradouro, tipoLogradouro}`.

Conferido contra `api/v3/api-docs` ao vivo:
```
DadosGeraisImovelDTO  required=['areaTerreno','inscricaoImobiliaria','temBairro','tipoImovel']
EnderecoImovelDTO     required=['cep','nomeLogradouro','tipoLogradouro']
```
**Exato, campo a campo.** E o método declarado — extrair as regras da própria spec em vez de copiar à
mão — é a decisão de engenharia certa: quando a spec evoluir, as regras acompanham.

## 2. VERIFICADO E CORRETO — os 15 códigos de variáveis do entorno

Conferidos um a um contra `dicionario_entorno_domicilios.xlsx`:

| Código | Metodologia alega | Dicionário IBGE |
|---|---|---|
| V05006 / V05007 / V05008 | pav SIM / NÃO / ND | "DOMICÍLIOS EM FACE COM VIA PAVIMENTADA - SIM/NÃO/NÃO DECLARADO" ✅ |
| V05009 / V05010 | bueiro SIM / NÃO | "…COM BUEIRO - SIM/NÃO" ✅ |
| V05012 / V05013 | ilum SIM / NÃO | "…COM ILUMINAÇÃO PÚBLICA - SIM/NÃO" ✅ |
| V05015 / V05016 | ônibus SIM / NÃO | "…COM PONTO DE ÔNIBUS - SIM/NÃO" ✅ |
| V05021 / V05022 | calçada SIM / NÃO | "…COM CALÇADA - SIM/NÃO" ✅ |
| V05027 / V05028 | rampa SIM / NÃO | "…COM RAMPA PARA CADEIRANTE - SIM/NÃO" ✅ |
| V05030 | arborização sem árvores | "…COM ARBORIZAÇÃO - SEM ÁRVORES" ✅ |

**15 de 15 corretos.** A correção do denominador para `SIM/(SIM+NÃO)` também está certa e é mais
rigorosa do que a que eu havia proposto.

## 3. ACHADO NOVO — o que V05000 realmente é, e a ressalva que ninguém registrou

`V05000` não é "total de domicílios do bairro". A descrição completa é:

> **"[Domicílios particulares permanentes ocupados][DOMICÍLIO EM SETOR ESCOLHIDO PARA APLICAÇÃO DO
> ENTORNO]"**

Ou seja: **o levantamento de entorno foi aplicado a setores selecionados**, não a todos. O universo
do indicador de entorno é diferente do universo do Censo.

**Medido em Teresina:** cobertura de **99,9%** (254.855 de 255.192 domicílios); **nenhum** dos 123
bairros abaixo de 90%. Em Teresina, portanto, a limitação é teórica.

**Mas é ressalva obrigatória por município.** Ao rodar o pipeline em Altos, Guaribas ou qualquer
outro, a primeira verificação tem de ser `V05000 / V00001`. Se a cobertura cair, o indicador de
pavimentação/iluminação deixa de representar o bairro e passa a representar uma amostra — e isso
precisa aparecer no painel, não numa nota de rodapé.

**Sugestão concreta:** adicionar `cobertura_entorno` como propriedade do GeoJSON, ao lado de `n_ok`.

## 4. ERRO FACTUAL no `metodologia-iv.md`

O documento justifica o uso da mediana citando:
> *"ex.: Tabajaras, média R$ 16.629 × mediana muito inferior"*

**Medido:** Tabajaras tem média **R$ 16.629** e mediana **R$ 15.000** — razão de **1,11**. Não é
"muito inferior"; é a menor divergência entre os bairros de renda alta.

Os exemplos que sustentam o argumento são outros: **Brasilar** (média R$ 1.926 × mediana R$ 1.212 =
**1,59**) e **Mocambinho** (R$ 2.688 × R$ 1.703 = **1,58**). O caso "Por Enquanto" citado em seguida
(R$ 3.065 × R$ 1.502 = 2,04) está correto.

**Trocar o exemplo.** A decisão de usar mediana está certa; a evidência apresentada para ela, não.

## 5. DISCUTÍVEL — k-means no lugar do índice com pesos

O documento abandona o índice sintético e adota **k-means (k=3)** sobre 4 dimensões normalizadas
min–max, argumentando "sem peso inventado".

**O argumento é parcialmente falso.** O k-means não elimina a arbitrariedade — ele a **desloca e a
esconde**:
- escolha de **k=3** (arbitrária);
- escolha das **4 variáveis** e exclusão de todas as outras (é uma ponderação binária: peso 1 ou 0);
- **normalização min–max**, que é sensível a outliers e faz cada variável pesar conforme sua
  amplitude observada — ou seja, **os pesos existem, são implícitos e não são declaráveis**;
- ordenação dos grupos por carência média ponderada (outra escolha).

**E o problema maior é de defensabilidade.** O parecer técnico de rodadas anteriores recomendou
método com **coeficientes declarados** precisamente pela explicabilidade perante controle externo.
Diante de um vereador ou do TCE:
- com pesos: *"seu bairro tem 42% de esgoto, o peso de saneamento é 0,25, eis a conta"*;
- com k-means: *"o algoritmo agrupou seu bairro no grupo 2"* — que é **indefensável** em audiência
  pública, mesmo sendo reproduzível.

Há ainda **instabilidade estrutural**: em k-means, incluir um município novo ou atualizar o Censo
pode **remapear os grupos de todos os bairros**, sem que nenhum bairro tenha mudado. Um bairro que
era "prioridade média" vira "alta" porque outro bairro entrou na base. Explicar isso a um prefeito
que investiu conforme o painel do ano anterior é um problema sério.

**Recomendação:** manter o k-means como **camada exploratória** (é bom para isso — revela padrões
sem impor estrutura) e **publicar junto um índice aditivo com pesos declarados** como indicador
oficial. O painel mostra os dois; o índice com pesos é o que vai para relatório, e o agrupamento é o
que ajuda a interpretar. Não é redundância: são funções diferentes.

## 6. Os textos de e-SIC — muito bons, com um ponto a verificar

Os três prioritários (RFB, SEFAZ-PI, SEAD/PROUrbe) estão bem redigidos: citam base legal, pedem
formato aberto, pedem dado agregado (o que reduz objeção de LGPD) e o da SEFAZ faz a pergunta certa —
converter "perda de repasse" em **R$/município/ano**, que é a linha mais forte possível do deck.

**A verificar:** o texto afirma que existe um arquivo público mensal `inscricoes_ativas_*.csv` na
página de estatísticas do Sinter. **Não consegui confirmar** — `/sinter/dados-abertos` redireciona
para o portal geral de dados abertos da RFB, e não localizei o arquivo por busca nem por inspeção do
HTML. Se ele existir, **parte do e-SIC nº 1 é dispensável e o dado sai hoje em vez de em 15–30 dias**
— vale 10 minutos de verificação antes de enviar o pedido.

## 7. O M0 — avaliação do que foi descrito

**Acertos de desenho:**
- **O validador offline é a decisão certa.** Gera o laudo sem credencial, que era o caminho crítico.
  Confirma independentemente a conclusão desta análise: o produto de entrada pode ser construído e
  vendido antes de qualquer token.
- Cliente em **dry-run** contra a URL real é boa prática — testa a montagem da requisição sem
  depender de credencial.
- Extrair regras da spec em vez de transcrever é o que torna o validador sustentável.
- Registrar que `docs.receitafederal.gov.br/sinter` está 404 e que a spec viva é `/api/v3/api-docs`
  é o tipo de achado que economiza horas de quem vier depois.

**O que eu verificaria antes de considerar o M0 fechado:**
1. **A spec é de homologação e está versionada como `0.0.1-SNAPSHOT`.** Um artefato SNAPSHOT muda sem
   aviso. O cliente precisa de um teste que falhe explicitamente quando a spec divergir da capturada
   — senão a mudança aparece como erro de negócio em produção.
2. **Os dois fluxos de geometria.** `DadosGeoDTO` tem só `idLotePonto` e `idLotePoligono`: a geometria
   não vai inline, vai por lote, com vinculação posterior. Se o cliente só cobre o fluxo alfanumérico,
   cobre metade do produto — e a metade que falta é a que a REURB entrega de graça.
3. **Validação semântica × sintática.** O laudo de completude vale pelo que checa além do schema:
   CEP existente, logradouro que casa com o município, área compatível com tipologia, inscrição sem
   duplicidade. É aí que está o valor do diagnóstico, não no `required`.
4. O `exemplo_base.csv` com 5 imóveis prova o fluxo, não o produto. **O teste real é rodar contra um
   cadastro municipal de verdade** — e é o que o piloto destrava.

# ANEXO 2 — METODOLOGIA-IV PRODUZIDA PELA OUTRA SESSÃO

# Metodologia dos Indicadores e do IV — v2 (set/2026)

**Estado:** bloqueante resolvida (M0 item 3). Substitui as regras de métrica
anteriores, incluindo a regra caduca "n ≥ 50 **faces**" — o universo agora é
**n ≥ 50 domicílios**. Implementada em `painel-gerencial/build_dados.py` e
refletida no painel regenerado.

## 1. Fontes (todas públicas, baixadas em `dados/bruto/`)

| Tema | Arquivo | Uso |
|---|---|---|
| Domicílios/moradores | CD1 por bairro (V00001, V00005) | denominadores, universo |
| Água e esgoto | CD2 por bairro (V00111, V00309) | saneamento |
| Entorno urbanístico | Entorno por bairro (V0500x) | pavimentação, iluminação, calçada, rampa, bueiro, ônibus, arborização |
| Demografia | Demografia por bairro (V010xx) | idosos 60+ (V01040+41), crianças 0–14 (V01031+32+33) ÷ V01006 |
| Renda | Renda do responsável (V06004 média, V06006 mediana) | perfil socioeconômico |
| Geometria | Malha de bairros CD 2022 (SHP) | mapa |

## 2. Regras de cálculo (as correções)

1. **Entorno — denominador sem "não declarado"**: % = SIM ÷ (SIM + NÃO).
   - Pavimentação: `V05006/(V05006+V05007)`; Iluminação: `V05012/(V05012+V05013)`;
     Calçada: `V05021/(V05021+V05022)`; Rampa: `V05027/(V05027+V05028)`;
     Bueiro: `V05009/(V05009+V05010)`; Ponto de ônibus: `V05015/(V05015+V05016)`.
   - **Errata v1:** usávamos `SIM/V05000`, incluindo "não declarado" no denominador
     (subestimava o indicador). Efeito pequeno em Teresina (não declarado ≈ 0),
     mas a regra correta é esta e vale para qualquer município.
   - Arborização permanece `V05030/V05000` (face **sem** árvores — não há par SIM/NÃO).
2. **Renda — mediana (V06006) é o indicador principal**; a média (V06004) fica como
   secundária. Motivo: robustez a cauda direita (ex.: Tabajaras, média R$ 16.629 ×
   mediana muito inferior; Por Enquanto: média R$ 3.065 × mediana R$ 1.502 — a
   mediana descreve melhor o morador típico do bairro).
3. **Água/esgoto**: % de domicílios ocupados ligados à rede (V00111/V00001; V00309/V00001).
4. **Universo**: bairros com **n ≥ 50 domicílios ocupados** (propriedade `n_ok` no
   geojson; 121 dos 123 de Teresina passam). Bairros abaixo ficam marcados e podem
   ser excluídos da análise — regra que substitui a caduca "n ≥ 50 faces".

## 3. Índice de Vulnerabilidade (IV)

Não há índice sintético com pesos arbitrários. O painel usa **agrupamento k-means
(k=3, 40 iterações, sementes fixas)** sobre 4 dimensões normalizadas por min–max:
`[renda_mediana (invertida), esgoto, pavimentação, iluminação]`. Os grupos são
ordenados por carência média ponderada por domicílios e rotulados
prioridade alta/média/baixa. Vantagens: sem peso inventado; reproduzível;
rastreável (cada bairro aponta o grupo e os valores que o colocaram lá).
Limitação documentada: k-means assume clusters convexos; com k=3 fixo perde
nuance. Quando houver série temporal, reavaliar contra cortes fixos.

## 4. Médias municipais

Sempre **ponderadas por domicílios ocupados** (não média simples de bairros).

## 5. Arquivos correspondentes

- `painel-gerencial/build_dados.py` — ETL idempotente que aplica estas regras
  (entrada: `dados/bruto/ibge/*.zip`; saída: `teresina_full.geojson`).
- `painel-gerencial/index.html` — painel com mediana como principal e
  denominadores corrigidos (v2).
- `dashboard-demo/index.html` — demonstração v1 (métricas antigas); mantida
  apenas como artefato de apresentação; **usar o painel-gerencial como referência**.

# ANEXO 3 — TEXTOS DE E-SIC PRODUZIDOS

# Textos de e-SIC — prontos para envio (16/09/2026)

Prioridade conforme o plano: **RFB e SEFAZ-PI decidem alvo e dimensionam mercado**;
ETURB/SEMDUH/Águas de Teresina servem à vitrine (enviar depois, sem urgência).
Portal: esic.teresina.pi.gov.br (municipal) / Fala.BR (federal) / PI Digital (estadual).
Prazo legal: 15 dias + 10 de prorrogação.

---

## 1. RFB — adesões e remessas por município (o denominador do mercado)

**Órgão**: Receita Federal (coordenação do Sinter) · **Canal**: Fala.BR (https://esic.cgu.gov.br)
**Classificação sugerida**: pedido de acesso à informação

> Solicito, com base na Lei 12.527/2011, as seguintes informações sobre o Sistema
> Nacional de Gestão de Informações Territoriais (Sinter), relativas ao estado do Piauí:
>
> 1. Lista dos municípios piauienses que assinaram o Termo de Adesão ao convênio do
>    Sinter, com a data de adesão de cada um;
> 2. Dos municípios aderidos, quais já concluíram testes de integração no ambiente de
>    homologação do módulo CADURB, com as respectivas datas;
> 3. Quais municípios piauienses já transmitiram unidades imobiliárias em produção
>    (quantidade de CIBs ativos por município e data da primeira transmissão aceita).
>
> As páginas públicas do Sinter divulgam apenas agregados nacionais (1.904 adesões e
> 188 municípios com inscrições ativas em 15/09/2026); o dado por município é essencial
> para dimensionar a aderência ao art. 266 da LC 214/2025 no Piauí.
> Formato preferido: planilha (CSV ou XLSX).

## 2. SEFAZ-PI — repasse de IBS por município (converte "perda" em R$)

**Órgão**: Secretaria da Fazenda do Piauí · **Canal**: PI Digital (https://pidigital.pi.gov.br)

> Com base na Lei 12.527/2011, solicito informações sobre a estimativa de repasse do
> Imposto sobre Bens e Serviços (IBS) aos municípios piauienses nas operações com
> bens imóveis, no marco da LC 214/2025 e do cronograma de transição:
>
> 1. Qual o critério estadual de vinculação e partilha do IBS de operações imobiliárias
>    ao município de situação do imóvel (art. 11, II, LC 214/2025);
> 2. Estimativa anual, por município do Piauí, do IBS vinculado a operações com bens
>    imóveis urbanos para o período 2027–2032 (mesmo estimativa, com metodologia);
> 3. Se disponível, o impacto estimado da ausência de inscrição dos imóveis no
>    Cadastro Imobiliário Brasileiro (CIB) sobre esses repasses.
>
> Formato preferido: planilha por município.

---

## 3. SEAD-PI — municípios do PROUrbe (fecha a cega do `cerurb.prourb`)

**Órgão**: Secretaria de Administração do Piauí (gestora do contrato do Sistema CERURB)

> Solicito a relação dos municípios piauienses habilitados ou aderidos ao Programa
> Estadual de Regularização Fundiária (PROUrbe, Lei estadual 8.153/2023), com a etapa
> em que cada um se encontra (adesão, ADU, MGL, RGO), e quais utilizam o Sistema
> CERURB contratado via SEAD (compra 469/2024, PNCP).

## 4–6. Vitrine (enviar depois dos acima)

- **ETURB (Teresina)**: relação georreferenciada dos núcleos e imóveis regularizados
  (programa Teresina é REURB+): shapefile/SHP dos núcleos, quantidade de títulos por
  núcleo e situação processual agregada (sem dados pessoais).
- **SEMDUH (Teresina)**: situação do Cadastro Municipal de Habitação e sua estrutura
  de campos.
- **Águas de Teresina**: cobertura de água e esgoto por bairro (domicílios atendidos,
  série anual) e geometria da rede, se disponível.

## Notas de uso

- Sempre solicitar **formato aberto (CSV/SHP)** e dado **agregado** — reduz objeções
  de sigilo e LGPD.
- O item 1 (RFB) tem resposta parcial pública: o arquivo mensal
  `inscricoes_ativas_*.csv` (página de estatísticas do Sinter) pode ser anexado ao
  pedido como referência do formato desejado.

# ANEXO 4 — SPEC DO CADURB VERIFICADA

# CADURB — spec OpenAPI obtida e risco de credencial resolvido

Verificado em 2026-09-16, contra o ambiente de homologação do SERPRO.

## 1. A spec OpenAPI é pública e baixável

```
GET https://hom-sinter2-cadurb.np.estaleiro.serpro.gov.br/api/v3/api-docs   → HTTP 200, 64.498 bytes
GET https://hom-sinter2-cadurb.np.estaleiro.serpro.gov.br/api/swagger-ui/index.html → HTTP 200
```

OpenAPI **3.0.1** · *"API de inserção, alteração, exclusão e consulta de Unidades Imobiliárias"* ·
**15 endpoints, 87 schemas**.

### Endpoints
| Método | Rota | Função |
|---|---|---|
| **POST** | **`/v1/validacao/{codigoIbge}/ui`** | **valida uma UI sem inserir** |
| POST | `/v1/{codigoIbge}/ui` · `/uis` | insere uma · **múltiplas** |
| PUT | `/v1/{codigoIbge}/ui/{cib}` · `/uis` | altera uma · múltiplas |
| PUT | `/v1/{codigoIbge}/ui/desativacao` · `/uis/desativacao` | desativa uma · múltiplas |
| GET | `/v1/ui/{cib}` · `/v1/{codigoIbge}/ui/{inscricaoImobiliaria}` · `/uis` | consultas |
| GET | `/v1/{codigoIbge}/arquivo/{idArquivo}/consulta` (+ `/depara`) | resultado de lote |
| GET | `/v1/{codigoIbge}/consulta/{idRequisicao}` · `/elemento/{idElemento}/payload` | rastreio |
| GET | `/v1/{codigoIbge}/vinculacoes/{idLote}` | vinculações de lote |

## 2. O risco levantado pelo parecer técnico: resolvido, e para os dois lados

**A favor:** o manual é explícito na tabela de pré-requisitos —
**`Certificados: Não se aplica`**. A autenticação é **token Bearer via OAuth2 client credentials**,
não certificado ICP-Brasil, e o payload é `application/json`, não arquivo assinado. A hipótese de que
o envio em lote exigiria ICP-Brasil **não se confirma**. O ICP-Brasil é exigido na **adesão ao
convênio** (assinar o Termo no e-CAC) — etapa do município, não da integração.

**Contra:** testei `POST /v1/validacao/2200400/ui` sem token → **HTTP 403 Forbidden**. O
`securitySchemes` declara `oauth2` e todos os endpoints herdam. **Sem credencial não se exercita
nada**, nem o endpoint de validação.

**Conclusão: a spec é pública, a execução é fechada.** O parecer técnico está certo no essencial —
não dá para testar de verdade sem credencial vinculada a convênio — mas o plano B é muito melhor do
que "construir às cegas": **temos o contrato OpenAPI completo**, com os 87 schemas, e dá para gerar
cliente tipado, validador local de payload e suíte de testes contra a spec, tudo antes da credencial.

## 3. Descoberta que muda o desenho do conector

Existe **`POST /v1/validacao/{codigoIbge}/ui`** — endpoint dedicado a **validar sem inserir**.
Isso é exatamente o que um produto de conformidade precisa: rodar o cadastro inteiro do município
contra o validador oficial e produzir o laudo de completude **antes** de qualquer envio real.

**O "diagnóstico de conformidade de R$ 3–5 mil" tem um endpoint oficial dedicado a produzi-lo.**

## 4. A geometria não vai inline

`DadosGeoDTO` tem apenas dois campos: **`idLotePonto`** e **`idLotePoligono`** — referências a lotes
geométricos enviados por outro caminho. A remessa da UI carrega o *ponteiro*, não a geometria.

**Consequência para o conector:** há dois fluxos a implementar, não um — o de dados alfanuméricos
(JSON por UI ou em lote) e o de geometria (por lote, com vinculação posterior via
`/vinculacoes/{idLote}`). O plano assumia um fluxo unitário. **Some esforço ao conector**, e confirma
por que o manual fala em envio "alfanumérico ou alfanumérico + georreferenciado".

## 5. Ordem de trabalho recomendada (revisada)

1. **Gerar cliente e validador local a partir da spec** — não depende de ninguém, é possível hoje.
2. **Em paralelo, obter a adesão do piloto** (é o caminho crítico real: Termo com ICP-Brasil →
   processo no e-CAC → publicação no DOU → token). **Semana 1, não semana 4.**
3. **Construir o "laudo de completude"** rodando o cadastro contra o validador local — que é o
   produto vendável, e não depende de token.
4. Só então integrar de verdade.

O item 3 é o achado prático: **o produto de entrada pode ser construído e vendido antes de haver
qualquer credencial**, porque o laudo é gerado contra o schema, não contra o servidor.

# ANEXO 5 — PLANO CONSOLIDADO (seções 11 e 12)

## 11. REVISÃO 2 — o que a rodada 5 mudou

### 11.1 O prazo: 107 dias, não 15 meses
Erro de aritmética corrigido. Consequências em cadeia:
- A meta do piloto endurece de "3 remessas **contratadas** até 31/12/2026" para
  **"3–5 pilotos com remessa ACEITA em homologação até 31/12/2026"**. Contrato não prova nada;
  aceite programático prova, e é o que gera referência vendável no pós-prazo.
- **Orçamento municipal tem ano próprio: quem precisa de dinheiro em 2027 empenha em 2026.**
  Assinatura ideal nov–dez/2026 sobre dotação corrente vigente. O que escorregar depende da LOA 2027
  e adiciona 1–2 trimestres.

### 11.2 O CADURB é API REST pública — e isso corta nos dois sentidos
Manual Operacional v1.12 (91 páginas, SERPRO, Swagger público, token Bearer) com endpoints de envio,
consulta, desativação e lote. **Duas consequências opostas:**
- **A favor:** dá para construir o conector **agora**, sem cliente, sem convênio, sem custo. Isso sobe
  para **prioridade técnica nº 1 do M0** — é a única forma de uma equipe pequena atender a onda.
  Capacidade artesanal é ~2 contas/mês (7–10 na janela de 60 dias); com conector pronto, 10–20/mês.
- **Contra:** a vantagem informacional que eu havia atribuído a "conduzir a adesão dá acesso à spec"
  **não existe** — a spec que importa é pública. A barreira que sobra é execução: saneamento de
  cadastro e serviço de campo.

### 11.3 O gatilho do pânico é cartorial, não fiscal
A perda de repasse do IBS é real mas escalonada na transição — não assusta ordenador em novembro.
O que assusta é o **cartório recusando registro de imóvel sem CIB** (a IN RFB 2.275/2025 obriga os
cartórios), e **o primeiro eleitor que não conseguir registrar a casa liga para a prefeitura, não
para a Receita**. Prefeitura pequena reage ao eleitor na porta, não à norma federal.
**Isso dispara no 1º trimestre de 2027 — depois do prazo, quando o empenho de 2026 já teria de estar
feito.** Daí a urgência de nov–dez.

### 11.4 Dois playbooks para o pós-prazo (66% fora a 3,5 meses = prorrogação é plausível)
- **Cenário pânico:** produto "regularização em 90 dias", sobrepreço de +20–30%, capacidade declarada
  e lista de espera. Escassez é argumento, não fracasso.
- **Cenário prorrogação:** o gancho muda de "prazo" para "IBS + cartório" em 48h, a venda vira anual,
  metas de contagem esticam 2 trimestres.
Não construir custo fixo contra um só dos cenários.

### 11.5 O subsídio do B pelo A: em produto, nunca em desconto
EV do Segmento A por conta B ≈ **R$ 7–20 mil em 3 anos** (p(conversão) 10–20% × R$ 100–150 mil
líquidos, descontado ~30% pelo risco do motor central da RFB). **Teto de subsídio: R$ 5–10 mil/conta,
e em produto.**

Desconto em dinheiro destrói a âncora de risco que sustenta a faixa de R$ 12–25 mil. O formato certo
é o **"diagnóstico de valor venal" de cortesia**: com o dado já no pipeline do B, comparar valor venal
municipal × fluxo de transações e entregar ao prefeito uma página com a defasagem local. Custo
marginal baixo, e é o que abre a conversa do Segmento A em 2027 com o cliente já convencido do número.

**Cláusula de finalidade em TODO contrato B desde o primeiro cliente.** O pool do Segmento A só se
forma se for contratual desde a origem — retrofit de cláusula em 2027 perde 100% do dado dos
primeiros clientes.

### 11.6 A ponte B→A é estreita, e é exatamente por isso que é um moat
Medido para o PI: só **15 de 152** municípios acumulam ≥500 transações de ITBI em 24 meses;
**120 de 152** ficam abaixo de 200. Nenhum município pequeno calibra modelo hedônico sozinho.

Em **pool regional** (30–50 contratos × 500–1.500 transações/ano = 15–75 mil observações/ano com
efeitos fixos por município), sim. **Quem tem uma conta não consegue; quem tem vinte, consegue — e
cada nova conta melhora a estimativa de todas as outras.**

É a única vantagem estrutural de toda a análise que não depende de relacionamento, preço ou
pioneirismo. Depende de acumular contas — que é o que o Segmento B faz.

### 11.7 O dinheiro: orçamento corrente, não PROFISCO
PROFISCO III sai do plano do ano 1 (empréstimo BID, municípios só na 2ª fase, autorização
legislativa, ciclo 6–18 meses). **Mencioná-lo numa proposta é dar ao controle interno um motivo para
adiar.**

A fonte real: **outras despesas correntes / serviços de terceiros – PJ**, a rubrica que em todo
município pequeno paga software e assessoria. R$ 12–25 mil = 0,026–0,055% da RCL mediana — grandeza
de mensalidade de sistema de nota fiscal, não de investimento que exija crédito suplementar.
Veículo: **dispensa por valor**; para escala, **consórcio intermunicipal via APPM** — que é também a
defesa contra o lote da Foxinline, porque dá ao canal um produto antes que a incumbente o empacote.

**Preencher o caminho orçamentário é parte do produto** — o secretário de fazenda municipal não tem
equipe para descobrir isso sozinho, e é grátis de fazer.

### 11.8 Regras de qualidade no indicador de entorno — ⚠️ REGRA SUBSTITUÍDA (16/09/2026)

> **A versão anterior desta seção estava ERRADA e foi corrigida.** Ela mandava cortar por
> `n ≥ 50 FACES` usando `V05400/V05406/V05412`. **Existem dois arquivos de entorno por bairro**, e o
> que deve ser usado é o de **DOMICÍLIOS**, não o de faces:
>
> | Arquivo | Variáveis | Unidade |
> |---|---|---|
> | `entorno_faces_BR` | V05400+ (pav = V05406) | faces de quadra — **não usar no painel** |
> | **`entorno_domicílios_BR`** | **V05000+ (pav = V05006, ilum = V05012)** | **domicílios — usar este** |
>
> Por face, um segmento com terreno baldio pesa igual a um com 50 casas. Por domicílio, o indicador
> responde "quantas pessoas moram em rua sem pavimento". Tabajaras: **36,8% por face × 95,2% por
> domicílio** — as casas estão nas poucas faces pavimentadas.
>
> **A "armadilha de Tabajaras" registrada na rodada 6 era artefato da métrica errada, não do dado.**

**Regras válidas (em domicílios):**
- exibir indicador só com **n ≥ 50 domicílios**; entre 50 e 150, marcar "baixa confiança" com
  IC 95% binomial
- **denominador = V05000 − V05008** (pavimentação) e **V05000 − V05014** (iluminação) — excluir os
  "não declarado", que subestimam a cobertura
- bairros abaixo do corte saem do ranking e aparecem só com selo "amostra insuficiente"
- usar **V06006 (renda mediana)**, nunca V06004 (média)

### 11.9 Fórmula final do `iv`
```
iv = 100 × (0,30·infra + 0,25·saneamento + 0,20·renda + 0,15·informalidade + 0,10·dependência)

infra       = média[(1−pav), (1−ilum), (1−bueiro)]
saneamento  = média[(1−esgoto_adequado), (1−água_adequada)]     ← sem duplicar esgoto
renda       = max(0, 1 − log1p(V06006)/log1p(mediana_municipal_V06006))   ← MEDIANA, não média
```
Usar **V06006 (mediana)**, não V06004 (média): a razão média/mediana chega a 1,59 e inverte posições.

### 11.10 Separação de camadas — inegociável por LGPD
`territorio` (municipio, bairro, setor, face) e `imovel` (unidade_imobiliaria, titular, itbi), ligadas
por `codigoIbge` e interseção espacial no PostGIS. **O painel lê apenas agregados de bairro — sem CPF,
sem valor individual. A remessa lê apenas `imovel`.** Titular e ITBI são sigilosos e não alimentam o
painel público.

### 11.11 Ordem de execução de outubro
**conector CADURB → diagnóstico nos 2 pilotos com REURB pronta (Guaribas, N. Sra. de Nazaré) →
remessa em homologação → só então a conversa de escala com APPM/canal TJ, com aceite na mesa.**

O produto se prova sozinho antes de qualquer reunião institucional. É o único sequenciamento que
funciona para equipe sem marca.

### 11.12 Gatilho novo
**Concorrente vendendo "integração CADURB" por menos de ~R$ 8 mil como produto principal** = a
integração está comoditizando. A resposta não é guerra de preço: é acelerar o que não se copia —
canal REURB, saneamento de campo e a referência de remessa aceita.

---

## 12. REVISÃO 3 — ajustes de execução (16/09/2026)

### 12.1 CONTRADIÇÃO INTERNA corrigida: a meta de venda excedia a própria capacidade declarada
A seção 11.2 deste plano declara capacidade de **~2 contas/mês** artesanal (10–20/mês só com conector
pronto). O calendário de execução pedia **5–10 diagnósticos fechados em 30 dias** — **2,5 a 5× a
capacidade declarada, antes de o multiplicador existir.**

A janela 16/10–15/11 tem **4 semanas úteis líquidas** (feriados de 2/11 e 15/11; outubro reduzido pela
eleição). Ciclo por conta sem referência anterior: 1ª reunião → secretário → prefeito → dossiê →
dispensa → empenho ≈ **3–6 semanas**. Fechar 5–10 até 15/11 exigiria **20–40 processos ativos já em
16/10** — data em que nem a apresentação interna terá acontecido.

**Meta corrigida:** **2–3 contratos assinados até 15/11**, com **8–12 propostas vivas** e **≥20
primeiras reuniões**. 5–10 vira cenário otimista **condicionado ao conector validado**.

**Para errar a meta sem contaminar a tese:**
- o relógio da tese é o gatilho de 90 dias, não os 30 dias — **30 dias medem execução, não tese**;
- **classificar todo não-fechamento**: atraso de prefeito/orçamento/eleição ≠ rejeição de preço com
  dor confirmada. Só a segunda é evidência contra a tese;
- métricas semanais de leading (reuniões, propostas na mesa, dossiês entregues): contagem baixa com
  leading saudáveis = problema de execução; leading zerados = problema de tese.

### 12.2 Foxinline sai do M0
Propor parceria antes de ter remessa aceita **entrega o roadmap à incumbente de graça** — a spec é
pública, a barreira que resta é execução de campo, e é exatamente isso que uma conversa de parceria
descreve. Sai o e-mail, entra: **deck de parceria pronto** (1 página, dois cenários) + **monitoramento
passivo semanal** (site, releases, Certificate Transparency) com **gatilho de antecipação** — qualquer
sinal de produto CIB da Foxinline adianta a conversa para o dia seguinte. Custo igual, opção preservada.

### 12.3 Sequência de reuniões
**Antes de todas: a reunião de escopo com o proponente REURB.**
1. **Secretário de fazenda do município-alvo** — é onde a dor é comprovável com dado público; recebe
   o dossiê de dispensa preenchido e vira o proponente interno.
2. **Prefeito, com processo na mesa** — decisor único da dispensa. Frio e sem marca, é a reunião de
   **menor** conversão da cadeia; com o secretário puxando, converte na primeira.
3. **APPM — só com aceite na mesa.** Antes disso é pedir vitrine sem produto.
4. **Secretário de planejamento — fora da venda B** (upsell de 2027, só nos 25 com bairros).
5. **TJ-PI — fora da janela** (agenda institucional de 2027).

### 12.4 Dois e-SIC que faltavam, e três que devem ser rebaixados
**Incluir:**
- **RFB — adesões ao SINTER por município + remessas aceitas.** É o **denominador do mercado
  restante**: sem ele a lista de alvos tem tamanho desconhecido e o gatilho de comoditização fica cego.
- **SEFAZ-PI — critério e volume do repasse de IBS por município.** Converte "perda de receita" em
  **R$/município/ano**, que é a linha mais forte possível do deck.
- Opcional: **TCE-PI** — dispensas de software/geoprocessamento 2024–26 (preço praticado e
  concorrência) e validação do IPTU de Altos.

**Rebaixar:** ETURB, SEMDUH e Águas de Teresina servem à **vitrine**, não ao **produto**. Disparar
porque é grátis, mas nada da execução os espera. O e-SIC que decide alvo é o da **SEAD/PROUrbe**.

### 12.5 Ordem final do M0
1. Reunião de escopo com o proponente (destrava Guaribas e N. Sra. de Nazaré)
2. **Credencial CADURB verificada na semana 1** + cliente/validador gerados da spec OpenAPI
3. **Metodologia do `iv` publicada** — meio dia, bloqueante para terceiros
4. Ataque direto aos **8 municípios do sinal RREO** (qualificação já em mãos, nenhum e-SIC necessário)
5. Verificação fiscal de Altos e Paulistana no TCE-PI
6. Dossiê de dispensa reutilizável + calendário de empenho
7. E2 — diagnóstico de conformidade em Guaribas/Nazaré
8. INEP **só depois** do conector e da verificação fiscal
