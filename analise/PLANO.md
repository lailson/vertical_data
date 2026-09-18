# Projeto CERURB — Plano consolidado
**Data:** 2026-09-15 · **Status:** recomendação pré-decisão · **Revisão 2** (pós-rodada 5)

> ⚠️ **CORREÇÃO DE PRAZO — a mais consequente de toda a análise.**
> Versões anteriores deste plano falavam em "~15 meses" até a obrigação do CIB. **Está errado.**
> De 15/09/2026 ao fim do prazo do art. 266 (**31/12/2026**) há **107 dias — 3,5 meses**.
> Descontando outubro (eleição nacional), a **janela prática de assinatura é nov–dez/2026: 60 dias**.
> Isto não é um plano para 2027. É um sprint de Q4/2026.
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
| **Ticket** | **3 módulos:** diagnóstico R$ 3–5 mil · pacote conformidade R$ 12–25 mil · manutenção R$ 4–8 mil/ano | R$ 49,5–58,8 mil diagnóstico · R$ 24–36 mil/ano |
| **Remuneração** | **preço fixo. Zero variável atrelado a IPTU** | fixo + fee de eficiência (10–15% do incremento) |
| **Veículo** | dispensa (abaixo de R$ 65.492,11 (limite 2026, Decreto 12.807/2025)) | dispensa → contrato de eficiência (art. 119, Lei 14.133) |
| **Aceite** | **remessa aceita no CADURB** | idem + metodologia publicável |
| **LTV 5 anos** | R$ 28–57 mil/conta | R$ 145–239 mil/conta |
| **TAM no PI** | R$ 1,7–5,4 mi entrada + R$ 0,9–2,2 mi/ano | Teresina isolada: fee potencial R$ 3,8–5,7 mi/ano |

**A frase de posicionamento** (não improvisar variação):

> *"O convênio com a Receita é gratuito e a API é aberta — o que o município não tem é o cadastro que
> ela aceita. Nós entregamos a remessa aceita no CADURB dentro do prazo de 31/12, para o senhor não
> perder o repasse do IBS nem travar o registro dos imóveis dos seus eleitores."*

Ela abre admitindo o que é de graça (desarma a objeção "o SINTER não cobra nada"), ancora no dano do
comprador (repasse + eleitor — as duas moedas que movem ordenador sem IPTU) e promete só o que tem
aceite objetivo. Nunca "modernização", nunca "painel", nunca "precisão de modelo".

**Não se vende acesso ao CIB — isso é de graça.** Vende-se a *capacidade de cumprir*: sanear o
cadastro, georreferenciar, completar os campos do schema, conduzir a adesão, integrar e sustentar.

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

---

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

---

## 13. REVISÃO 4 — correções jurídicas e de limite (16/09/2026)

### 13.1 Limite de dispensa 2026 — CORRIGIDO
**Decreto nº 12.807/2025** (IPCA-E 4,41%, vigente 01/01/2026):

| Base legal | Objeto | Limite 2026 |
|---|---|---|
| Art. 75, I | obras e serviços de engenharia | **R$ 130.984,20** |
| Art. 75, II | compras e demais serviços | **R$ 65.492,11** |
| Art. 75, II **c/c § 2º** | idem, por **consórcio público** ou autarquia/fundação qualificada como agência executiva | **R$ 130.984,22** |

⚠️ **Os dois valores de ~R$ 131 mil são coisas diferentes** e diferem em 2 centavos por coincidência
aritmética: R$ 130.984,**20** é o teto de *engenharia*; R$ 130.984,**22** é o dobro do teto de
*serviços* para consórcio público. Não confundir num documento que vai ao jurídico.

### 13.2 O § 2º vale para CONSÓRCIO PÚBLICO — não para a APPM
Correção a uma imprecisão minha. O § 2º dobra o limite para **consórcios públicos** — pessoa jurídica
de direito público (Lei 11.107/2005), com estatuto, objeto, adesões formais e rateio. **A APPM é
associação civil**, e contratação *pela APPM como associação* **não** ativa o § 2º — além de que
associação rateando recurso público dos associados é padrão que tribunal de contas questiona.

**A via limpa é o consórcio intermunicipal**, que a APPM pode **induzir ou sediar**, mas não substituir.
Nele: teto de R$ 130.984,22 e a despesa conta no exercício **do consórcio** como unidade gestora
(§ 1º, I), não no dos municípios membros.

**Quanto cabe:** pacote de R$ 15–30 mil por município → **4 a 8 municípios numa dispensa consorciada**.
Sem o § 2º seriam 2–4. É a dobra que torna a via consorciada viável no tamanho que interessa.

**Mas não muda o motor de 2026:** montar consórcio leva semanas a meses e não cabe na janela
20/11 → 10/12. O que fazer agora é **desenhar a oferta já em formato consorciável** — TR modular,
escopo por município aderente, preço unitário por imóvel — que executa igual como dispensa municipal
ou como anexo de rateio. Custo de fazer assim hoje: quase zero. De redesenhar depois: um dossiê inteiro.

**Não vender consórcio como porta de entrada:** é B2B2G, ciclo mais longo e ponto único de falha —
um prefeito trava, todos travam.

### 13.3 Dispensa ÚNICA (laudo + conformidade) — e quem decide é o calendário
| Critério | Dispensa única | Duas encadeadas |
|---|---|---|
| Ciclos de processo na prefeitura | 1 | 2 |
| Cabe na janela 20/11 → 10/12? | **sim** | **não** — o 2º ciclo cai em 2027 |
| Receita da conformidade | caixa 2026 | LOA 2027, dotação nova |
| Exposição de forma (§ 1º, II) | elimina | mantém |

Dois ciclos completos (declaração → parecer → decisão → PNCP → empenho) em três semanas de fim de
exercício: o jurídico de prefeitura pequena não gira. **A escolha "comercial" já estava decidida pelo
calendário.**

**Três condições de redação, não opcionais:** (1) **preço-teto por estimativa do export** — R$/imóvel
× volume do cadastro, declarado no TR; (2) **etapa 1 (laudo) como obrigação**, aceite em 15 dias úteis
do export; (3) **etapa 2 ajustável por medição**, com plano aprovado pelo fiscal — e a **remessa
continua marco condicionado**. A dispensa única não pode engolir essa distinção.

**Consequência:** o pacote único vira o caminho recomendado; **laudo isolado a R$ 3–5 mil é rebaixado
a fallback** para município sem dotação para o pacote. Painel anual: objeto distinto, exercício seguinte.

### 13.4 Cashback morre no setor público — os três efeitos sobrevivem
O reembolso condicionado a contrato futuro **não tem categoria contábil regular** em contratação
pública, e dinheiro de fornecedor no caixa da prefeitura fora do contrato lê-se como vantagem
condicionada. Substitutos:

| Efeito do cashback | Substituto |
|---|---|
| Filtro de compromisso | **empenho único de R$ 15–33 mil** — filtra mais que R$ 4 mil reembolsáveis |
| Risco devolvido | **mini-diagnóstico de 72h sobre o export, na pré-venda** — devolve o risco antes da assinatura |
| Âncora intacta | **desconto formal declarado na estimativa de preço**, nunca devolução |

E o "programa piloto de 10 vagas" deixa de ser promoção e passa a ser **declaração de capacidade
física** (2 contas/mês) — mais difícil de contestar, mais fácil de auditar.
Cashback **continua válido para privados** (cartórios, loteadoras, escritórios).

### 13.5 Formulações seguras para os números não verificados
- **PI:** *"até [data], a base pública do Sinter/RFB registrava cadastro transmitido apenas de
  Teresina"* — com data e fonte no rodapé. Sem verificação a tempo: *"o cadastro transmitido conhecido
  no PI é o de Teresina"*.
- **Brasil:** trocar a contagem exata por **piso percentual datado** — *"menos de 4% dos 5.570
  municípios havia transmitido até [mês/2026]"*. 188/5.570 = 3,4%; o piso absorve variação de até
  +34 municípios sem virar mentira, e continua verdadeiro quando a corrida de dezembro acelerar.
- **Regra fixa:** nenhum número sem [fonte, data de consulta] em rodapé. Fonte que não abre vira
  "dado a confirmar" — ou não entra.

### 13.6 Reordenação de alvos pelo ITBI
Dentro dos 8 do sinal RREO + 2 pilotos, sobem os de razão ITBI/IPTU alta:
**Bom Jesus é o melhor alvo composto** — ITBI R$ 1,77 mi, **R$ 61/hab (2º maior per capita do estado,
atrás só de Teresina)**, 1,7× o IPTU. Depois **Floriano** (R$ 2,13 mi, 1,8×) e **Corrente** (1,6×).
**Cocal (3,3×) é caso de narrativa, não alvo** — ITBI de R$ 3,77/hab é base pequena demais.
