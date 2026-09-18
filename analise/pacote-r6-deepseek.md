# Rodada 6 — REVISÃO DE EXECUÇÃO. Eixo técnico.

Contexto: o painel FOI CONSTRUÍDO (index.html 494KB + teresina_full.geojson com 123 bairros e
geometria real, 18 indicadores por bairro, export CSV, e marcação "Aguardando fonte" onde falta dado).

E eu errei numa métrica: usei `entorno_FACES` (V05406) quando o correto é `entorno_DOMICÍLIOS`
(V05006). Tabajaras: 36,8% por face vs 95,2% por domicílio. Minha "regra de corte mínimo de faces"
(que você endossou na rodada 5) perde a maior parte da razão de ser (Anexo 1, seção 2).

O plano de execução proposto é: PISTA 1 (decisões humanas: reunião de escopo, e-SIC, e-mail Foxinline)
e PISTA 2 (técnico sem dependência: conector CADURB, INEP 537MB geocodificado, verificação fiscal,
dossiê de dispensa). Calendário: M0 até 15/10, vender diagnóstico 16/10–15/11, contratos 15/11–20/12.

Responda no máximo 6 achados, só o que muda a execução:

1. Concorda que a métrica por domicílio é a correta? Há caso em que a métrica por face é preferível?
   E qual regra de qualidade sobra, agora em domicílios?
2. **O conector CADURB pode ser testado de verdade sem um município conveniado?** O ambiente de
   homologação do SERPRO exige credencial vinculada a convênio? Se exigir, qual o plano B para não
   perder 3 semanas construindo contra um Swagger que não se pode exercitar.
3. O INEP (537 MB + geocodificação) vale a prioridade que recebeu no M0, ou deve ser rebaixado?
   Justifique por esforço × valor para a apresentação.
4. **Metodologia do `iv`**: o painel já mostra "Vulnerabilidade por bairro". O que exatamente precisa
   ser publicado junto para que o índice seja defensável, e quanto tempo isso leva?
5. Olhando as 18 propriedades do GeoJSON (Anexo 1, seção 1), o que está faltando que seria barato
   incluir e aumentaria muito o valor do painel?
6. Riscos técnicos do plano de execução que não estão nomeados nele.

Adversarial, concreto. Cite "Anexo N".

# ANEXO 1 — REVISÃO DA EXECUÇÃO E VALIDAÇÃO DO PAINEL (novo)

# Revisão do plano de execução + validação do painel construído

## 1. O painel existe e é bom

`index.html` (494 KB) + `teresina_full.geojson` (458 KB, **123 features com geometria Polygon**).

Propriedades por bairro: `name, cd, dom, mor, mor_por_dom, agua, esgoto, pav, ilum, calcada, rampa,
bueiro, onibus, arbor_sem, renda, renda_med, idosos_pct, criancas_pct`.

11 telas, fontes tipográficas próprias, **botão de exportar CSV** e — o detalhe que mais importa —
um botão **"Aguardando fonte"**, ou seja, o painel declara o que ainda não tem dado em vez de
inventar. É a correção direta do defeito fatal do protótipo anterior.

## 2. ERRO MEU, encontrado na validação cruzada: usei a métrica errada

Ao confrontar os valores do GeoJSON com os que extraí, a divergência era sistemática:

| Bairro | pav — meu | pav — painel |
|---|---|---|
| Tabajaras | 36,8% | **95,2%** |
| Morros | 46,0% | 81,7% |
| Olarias | 48,6% | 74,7% |
| Brasilar | 44,8% | 70,4% |
| Chapadinha | 36,7% | 46,6% |
| Centro | 100,0% | 100,0% |

Causa: **existem dois arquivos de entorno por bairro, com métricas diferentes**, e eu usei o errado.

| Arquivo | Variáveis | Unidade |
|---|---|---|
| `Agregados_por_bairros_entorno_faces_BR` | V05400+ (pav = **V05406**) | **faces de quadra** |
| `Agregados_por_bairros_entorno_domicílios_BR` | V05000+ (pav = **V05006**) | **domicílios** |

Isto também resolve a discrepância de códigos das rodadas anteriores: a análise paralela citou
V05006/V05012 e eu citei V05406/V05412 — **os dois estavam certos, sobre arquivos diferentes.**

### Por que a métrica por domicílio é a correta

Por face, um segmento de quadra com um terreno baldio pesa igual a um com 50 casas. Por domicílio,
o indicador responde à pergunta que interessa à política pública: **quantas pessoas moram em rua sem
pavimento**.

Tabajaras é a prova: **19 faces (36,8% pavimentadas) mas 293 domicílios (95,2% em face pavimentada)**
— as casas estão concentradas nas poucas faces pavimentadas; o resto são faces de terreno vazio.

**Consequência: o "achado da armadilha de Tabajaras" que registrei na rodada 6 era artefato da minha
escolha de métrica, não uma armadilha do dado.** A regra de corte mínimo de faces que propus — e que
o parecer técnico endossou — **perde a maior parte da sua razão de ser**. O painel já está certo.

O corte continua fazendo sentido, mas **em domicílios, não em faces**, e com limiar muito menor
(bairros com poucas dezenas de domicílios seguem instáveis).

## 3. O plano de execução proposto — avaliação

### Faz sentido, e o sequenciamento está certo
Duas pistas em paralelo (decisões humanas × trabalho técnico sem dependência) é o desenho correto
para uma janela curta. O ponto mais forte: **disparar os e-SIC primeiro**, porque o prazo de 30 dias
é o único item do plano que não se comprime com esforço.

### O que eu mudaria

**a) A prioridade do conector CADURB está certa, mas o pedido de credencial precisa vir antes.**
A adesão ao convênio é ato do **município**, não nosso — e depende de Termo assinado com certificado
ICP-Brasil e publicação no DOU. Construir contra o Swagger de homologação não exige credencial, mas
**testar de verdade exige**. Se a credencial depende de um município conveniado, e nenhum piloto está
definido, o conector fica sem ambiente de teste real. **Isso precisa ser verificado na primeira
semana, não descoberto na quarta.**

**b) O INEP (537 MB, geocodificação) é o item de pior relação valor/esforço do M0.** Educação é uma
tela entre onze, e o painel já tem dez funcionando. Geocodificar escolas e cruzar com polígonos é
meio a um dia de trabalho se tudo der certo, e três se não der. **Sugiro rebaixar para depois do
conector e da verificação fiscal.**

**c) Falta um item que não está em nenhuma das duas pistas: a metodologia publicada do `iv`.**
O painel tem "Vulnerabilidade por bairro" na tela principal. Se o índice não vier com pesos, fontes e
fórmula num documento anexo, ele reproduz — com dado real, o que é pior — o passivo do protótipo
antigo. **É meio dia de trabalho e é bloqueante para apresentar a terceiros.**

**d) O calendário de venda tem um otimismo:** "16/10–15/11: vender o diagnóstico em 5–10 municípios".
São 30 dias corridos para 5–10 contratos com prefeituras, sem referência anterior, em municípios onde
ninguém conhece a empresa. **Com dispensa é rápido de assinar, mas não de decidir.** Sugiro meta de
**2–3 no período**, e tratar 5–10 como cenário otimista — errar a meta para baixo no primeiro mês
contamina a leitura de todo o resto.

**e) A reunião com a Foxinline como "parceria fundiária" é a jogada certa, mas o timing é ruim
agora.** Chegar antes de ter uma remessa aceita é chegar sem ativo de troca. Depois de 2–3 remessas
aceitas em municípios que não são tenants dela, a conversa muda de "queremos seus dados" para "temos
um produto que seus 236 municípios vão precisar até 31/12". **Sugiro adiar para depois do primeiro
aceite no CADURB.**

### O que está certo e não deve mudar
- e-SIC imediato, com a SEAD (lista PROUrbe) como o mais estratégico
- revalidar o método dos RREO antes de uso comercial
- conversa de escopo com o proponente como decisão nº 1
- Altos como piloto, Paulistana como reserva
- o dossiê de dispensa reutilizável — "preencher o caminho orçamentário é parte do produto"

# ANEXO 2 — PLANO CONSOLIDADO

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
| **Veículo** | dispensa (abaixo de ~R$ 59 mil) | dispensa → contrato de eficiência (art. 119, Lei 14.133) |
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

### 11.8 Regras de qualidade obrigatórias no indicador de entorno
Descobertas no cruzamento renda × entorno (Tabajaras: maior renda de Teresina com 19 faces medidas):
- exibir indicador só com **n ≥ 50 faces**; entre 50 e 150, marcar "baixa confiança" com IC 95% binomial
- **denominador = V05400 − V05408** (pavimentação) e **V05400 − V05414** (iluminação) — tirar os
  "não declarado", que hoje subestimam a cobertura
- bairros com n < 50 **saem do ranking** e aparecem só com selo "amostra insuficiente"

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

# ANEXO 3 — PLANO DA APRESENTAÇÃO (2 semanas)

# Plano de 2 semanas — apresentação com dashboard de dados reais
**Data:** 2026-09-16 · **Janela:** 10 dias úteis, full time · **Prazo do art. 266:** 106 dias

> **Resposta curta à pergunta:** sim, dá. E dá com folga para ser bom — porque **~70% do dado já
> está baixado e validado** nesta máquina, durante a análise. O trabalho das 2 semanas é
> transformação, geometria e narrativa, não descoberta de fonte.

---

## 1. O que já está pronto (não gasta dia de trabalho)

| Ativo | Estado | Volume |
|---|---|---|
| Censo 2022 por bairro — básico | baixado, validado | 17.576 bairros BR · **123 Teresina** |
| Censo 2022 por bairro — renda (V06001–V06006) | baixado, validado | 17.378 bairros · **122 Teresina** |
| Censo 2022 por bairro — domicílios 1 e 2 (água, esgoto, banheiro) | baixado | 408 colunas |
| Censo 2022 por bairro — demografia | baixado | idade, sexo |
| Censo 2022 — entorno por face de quadra | baixado, validado | pavimentação, iluminação, bueiro, calçada, rampa, ponto de ônibus, arborização |
| **Malha vetorial de bairros do PI** | baixada, DBF lido | **479 bairros**, chave `CD_BAIRRO`, 355 KB |
| **Favelas e comunidades urbanas (polígonos)** | baixada, DBF lido | 12.348 BR · **170 em Teresina** |
| SICONFI — IPTU e RCL | extraído via API | **224 municípios do PI**, série 2021–2025 |
| ANEEL — geração distribuída | esquema validado | CSV/Parquet, atualização diária |
| ITBI Fortaleza | baixado, analisado | **79.985 transações** com geo e valor venal |
| MUNIC 2021 e 2023 | baixadas | qualificação de municípios |
| Manual Operacional CADURB v1.12 | baixado | 91 páginas, endpoints mapeados |
| Índice de vulnerabilidade | **calculado** | **121 bairros de Teresina** |

**Falta baixar:** INEP Censo Escolar (link direto não confirmou no teste — **é o único risco de fonte
do plano**) e ANEEL Parquet (105 MB, trivial).

---

## 2. Os três entregáveis

### E1 — Painel Territorial de Teresina (a vitrine)
123 bairros, geometria real, dado real. É o protótipo atual **consertado e provado**.
Prova: "sabemos fazer, e o que mostramos é verificável."

### E2 — Diagnóstico de Conformidade CIB (o produto)
Um município pequeno do Segmento B. Mostra o produto que se vende de verdade: % de completude do
cadastro contra o schema do CADURB, o que falta, e o que acontece se não cumprir.
Prova: "temos produto, não só painel."

### E3 — Deck de narrativa (~12 slides)
A tese, os números, a decisão, o prazo. Inclui um-pager de metodologia do índice.
Prova: "sabemos por que isso é um negócio."

**O E2 é o que diferencia esta apresentação de um dashboard bonito.** Se faltar tempo, corta-se
profundidade do E1, nunca a existência do E2.

---

## 3. Cronograma — 10 dias

### Semana 1 — dados e motor

| Dia | Trabalho | Entregável / aceite |
|---|---|---|
| **D1** | **Setup e decisões.** Ambiente Python (faltam `pandas`, `geopandas`, `pyarrow`, `duckdb`, `openpyxl` — nenhum instalado), PostGIS via Docker ou DuckDB+SQLite espacial. Fechar as 3 decisões da seção 6. | ambiente rodando; decisões registradas |
| **D2** | **ETL Censo por bairro.** 6 arquivos → tabela única por `CD_BAIRRO`. Encoding **latin-1** (já confirmado), separador `;`, decimal com vírgula. | tabela `bairro_indicador` com 123 linhas de Teresina e 479 do PI |
| **D3** | **Camada de qualidade.** Regras de corte: n ≥ 50 faces; denominador `V05400 − V05408`/`V05414`; flag de baixa confiança com IC 95%. | nenhum bairro entra no ranking sem passar no corte |
| **D4** | **Geometria.** Shapefile → GeoJSON simplificado, junção com indicadores, polígonos de favelas como camada separada. | mapa real renderizando, 123 bairros + 170 FCUs |
| **D5** | **Motor do índice.** `iv` com a fórmula de 5 dimensões, pesos versionados em código, documento de metodologia. | `iv` reproduzível; ranking bate com o já calculado |

### Semana 2 — produto e narrativa

| Dia | Trabalho | Entregável / aceite |
|---|---|---|
| **D6** | **Camada fiscal e comparativa.** SICONFI: IPTU e RCL dos 224. Tela de posição do município no estado. ANEEL (energia) se sobrar tempo. | série 2021–2025 por município |
| **D7** | **Dashboard — estrutura.** Navegação, mapa, ranking, ficha de bairro. | E1 navegável |
| **D8** | **Dashboard — acabamento.** Fichas, legendas, selos de confiança, rodapé de fonte por indicador. | E1 apresentável |
| **D9** | **E2 — diagnóstico de conformidade** + **E3 — deck.** | E2 e E3 prontos |
| **D10** | **Ensaio e folga.** Rodar a apresentação inteira em voz alta, cronometrar, corrigir. | ensaio feito |

**D10 é folga de verdade, não enfeite.** Em projeto de dados, algo sempre quebra — encoding, junção
de nome de bairro, geometria inválida. Se nada quebrar, D10 vira INEP + energia.

---

## 4. Regras inegociáveis durante as 2 semanas

1. **Nenhum número inventado.** Todo indicador na tela tem fonte e data no rodapé. Foi o defeito
   fatal do protótipo atual; repeti-lo destrói a credibilidade que a apresentação existe para criar.
2. **Selo de confiança visível.** Bairro com amostra insuficiente aparece cinza com "amostra
   insuficiente", nunca com número.
3. **Sem dado pessoal em tela.** O painel lê só agregados de bairro. Sem CPF, sem valor por imóvel.
4. **Metodologia do `iv` publicada junto.** Uma página com pesos, fontes e fórmula. Sem isso, o
   índice é indefensável — e alguém vai perguntar.
5. **Nada de ML, preditivo ou chat.** Não cabe em 10 dias com defensabilidade, e a tese não precisa.

---

## 5. O que fica de fora, e por quê

| Item | Motivo |
|---|---|
| ML / modelo preditivo / chat conversacional | não é defensável em 10 dias; não é a tese |
| Conector CADURB funcionando | é o item nº 1 **depois** da apresentação, não dentro dela |
| Avaliação em massa / PGV | depende de dado municipal que não temos |
| Séries históricas por bairro | Censo é snapshot; só 2010 vs 2022, pouco valor |
| Simulador de investimento | precisa de modelo de custo com fonte; vira ponto fraco em auditoria |
| Integração CERURB | fora do caminho crítico por decisão da análise |

---

## 6. Três decisões que travam o D1

1. **Audiência.** Interno (entender o negócio) ou já serve para levar a um secretário? Muda o tom, o
   nível de detalhe técnico e se o deck fala em preço.
2. **Município do E2.** Guaribas ou N. Sra. de Nazaré (REURB 100% concluída, cadastro já pago) são os
   melhores candidatos técnicos. Se houver um município com relação comercial real, ele ganha.
3. **Formato de entrega.** Página publicada com link compartilhável, ou arquivo local? Link permite
   mandar antes da reunião e abrir no celular; local não depende de nada.

---

## 7. Riscos e planos B

| Risco | Probabilidade | Plano B |
|---|---|---|
| INEP fora do ar / link mudou | média | corta educação do E1; os outros 10 indicadores sustentam |
| Nome de bairro não casa entre malha e agregados | **alta** | junção por `CD_BAIRRO` (código), nunca por nome — já validado |
| Geometria inválida no shapefile | média | `ST_MakeValid` / buffer(0) |
| Ambiente Python sem bibliotecas | **certa** | é o D1; se instalação falhar, DuckDB resolve quase tudo sozinho |
| Encoding quebrado nos CSVs do IBGE | **certa** | latin-1 já confirmado em todos os testes |
| Escopo inflando ("e se colocar também...") | **alta** | a seção 5 é a lista de recusa; consultar antes de aceitar |

---

## 8. Como saber que deu certo

A apresentação funciona se, ao fim dela, a pessoa souber responder:
1. **Onde estão os piores bairros deste município, e por quê** — com número e fonte.
2. **Quanto o município arrecada e onde ele está no estado.**
3. **O que a lei exige até 31/12/2026 e o que acontece se não cumprir.**
4. **O que exatamente nós entregamos, e por quanto.**

Se ela sair achando o painel bonito mas sem saber responder 3 e 4, a apresentação falhou — foi
demonstração de tecnologia, não de negócio.

---

## 9. REVISÃO — decisões tomadas e um achado que muda o E2

**Decisões (16/09/2026):** audiência **interna** (entendimento do negócio) · E2 em **Guaribas ou
N. Sra. de Nazaré** · entrega **publicada + cópia local autocontida**.

### 9.1 ACHADO: só 25 dos 224 municípios do PI têm divisão de bairros no Censo 2022

Verificado no DBF da malha `PI_bairros_CD2022` (479 bairros no estado):

| Município | Bairros |
|---|---|
| Teresina | 123 |
| Parnaíba | 46 |
| Floriano | 40 |
| Piripiri | 30 |
| Picos | 27 |
| Campo Maior | 21 |
| … mais 19 municípios | 2 a 17 |
| **Guaribas, N. Sra. de Nazaré, Coivaras, Juazeiro do Piauí, Tanque do Piauí** | **0** |

**Nenhum dos municípios-piloto do Segmento B tem bairros.** E não é exceção: **199 dos 224 municípios
do Piauí não têm.**

### 9.2 O que isso muda

**Não muda a escolha do E2 — muda o que o E2 é.** O diagnóstico de conformidade CIB nunca dependeu de
bairro: ele compara o *cadastro imobiliário municipal* com o *schema do CADURB*. Isso segue de pé.

O que cai é a ideia de mostrar "um painel territorial de Guaribas". Lá a granularidade disponível é:
- **setor censitário** (existe em todos os 5.570 municípios) — mais fino que bairro, porém sem nome
  reconhecível pelo gestor;
- **município** (comparação com os outros 223 — que é forte, e já está extraída do SICONFI);
- **favelas/comunidades urbanas**: no PI só existem em **Teresina (170), Picos (2) e Parnaíba (1)** —
  Guaribas não tem nenhuma mapeada.

**Consequência para o D4 e o D9:** a geometria do E1 (bairros de Teresina) e a do E2 (setores de
Guaribas) são camadas diferentes e precisam de tratamento separado. Some ~meio dia ao D4.

### 9.3 E isto é, na verdade, um argumento a favor da tese

A bifurcação A/B do plano principal foi deduzida da economia (só 9 municípios do PI têm IPTU
relevante). **Agora ela aparece de novo, de forma independente, pela geografia do dado:** para 199 dos
224 municípios do Piauí, **não existe granularidade intraurbana pública** — logo não existe painel de
gestão territorial para vender a eles.

Para esses municípios o produto é, e só pode ser, **conformidade cadastral**. O painel bonito é
produto dos 25 maiores. Duas evidências independentes apontando para a mesma divisão de mercado é o
sinal mais forte que esta análise produziu.

**Recomendação de narrativa para a apresentação interna:** mostrar exatamente isso, lado a lado —
Teresina com 123 bairros (o que sabemos fazer) e Guaribas sem nenhum (por que o produto é outro). O
contraste é a explicação mais econômica da estratégia inteira.

### 9.4 CORREÇÃO ao item 1 deste plano: o dado NÃO está todo baixado

O diretório de trabalho temporário foi limpo na virada do dia — sobraram só os downloads de hoje
(malha de bairros e favelas). **A afirmação "~70% já está baixado" era verdadeira ontem e falsa hoje.**

Não muda o esforço de forma relevante — todos os downloads foram testados, os caminhos estão
documentados nos arquivos de análise, e rebaixar é questão de minutos a algumas horas (o maior é a
ANEEL, ~105 MB). **Mas muda o D1:** a primeira tarefa passa a ser criar um **diretório persistente do
projeto** (`dados/bruto/`) com um script de ingestão idempotente que rebaixa tudo a partir das URLs
já validadas — e nunca mais depender de área temporária.

Isso é bom: vira o primeiro pedaço do ETL reutilizável em vez de trabalho jogado fora.

# ANEXO 4 — LISTA QUALIFICADA DOS 25 MUNICÍPIOS COM BAIRROS

# Lista qualificada — os 25 municípios do PI com bairros, cruzados com tenant e dado fiscal

Verificado em 2026-09-16: malha `PI_bairros_CD2022` (DBF) × Certificate Transparency `%.foxinline.com`
× SICONFI RREO Anexo 03 (2025).

| Município | Bairros | IPTU 2025 | RCL 2025 | Pop. | Tenant Fox | Segmento |
|---|---|---|---|---|---|---|
| Teresina | 123 | R$ 166.321.115 | R$ 4,80 bi | 868.523 | — | A |
| Parnaíba | 46 | R$ 4.161.751 | R$ 786,0 mi | 163.087 | — | A |
| Floriano | 40 | R$ 1.208.395 | R$ 327,7 mi | 62.593 | — | A |
| Piripiri | 30 | R$ 1.533.757 | R$ 347,1 mi | 65.762 | **SIM** | A |
| Picos | 27 | R$ 7.062.110 | R$ 415,3 mi | 82.028 | — | A |
| Campo Maior | 21 | R$ 1.043.286 | R$ 278,1 mi | 45.252 | **SIM** | A |
| **Altos** | **17** | **R$ 245.127** | **R$ 61,3 mi** | **46.826** | **—** | **fronteira** |
| **Paulistana** | **17** | **R$ 558.221** | **R$ 131,8 mi** | 21.080 | **—** | **fronteira** |
| Barras | 15 | R$ 882.361 | R$ 298,3 mi | 47.909 | **SIM** | fronteira |
| Corrente | 15 | R$ 751.325 | R$ 143,8 mi | 27.419 | **SIM** | fronteira |
| Elesbão Veloso | 15 | R$ 125.340 | R$ 68,6 mi | 13.574 | — | fronteira |
| Bom Jesus | 10 | R$ 1.022.220 | R$ 228,6 mi | 28.857 | — | A |
| São Félix do Piauí | 10 | R$ 40.788 | R$ 31,4 mi | 2.842 | — | B |
| Cocal | 7 | R$ 32.309 | R$ 145,7 mi | 28.121 | — | B |
| Ribeiro Gonçalves | 5 | R$ 32.663 | R$ 81,7 mi | 6.164 | — | B |
| Brasileira | 7 | R$ 9.295 | R$ 54,8 mi | 8.438 | **SIM** | B |
| Simões | 9 | R$ 0 | R$ 104,3 mi | 14.344 | — | B |
| União · Luís Correia · Piracuruca · Água Branca · Baixa Grande do Ribeiro · Ilha Grande · Lagoa do Barro · Simplício Mendes | 3–14 | **sem retorno** | **sem retorno** | — | 4 SIM | B |

## Correção a um dos dois nomes sugeridos

A análise paralela apontou **Campo Maior e Altos** como "tenants Foxinline com bairros". Verificado:
**Campo Maior é tenant; Altos não é.** Tenants com bairros são: Piripiri, Campo Maior, Barras,
Corrente, União, Água Branca, Brasileira, Ilha Grande.

## O melhor candidato a piloto de painel fora da capital: **Altos**

| Critério | Altos |
|---|---|
| Tem bairros (painel funciona) | **17** |
| Não é tenant Foxinline | **✅** |
| RCL confortável | **R$ 61,3 mi** |
| IPTU pequeno mas não nulo | R$ 245 mil — **fronteira A/B** |
| População | 46.826 (7º do estado) |

Altos é o único município do PI que reúne **bairros + ausência do incumbente + porte razoável**.
É onde o painel territorial e a conformidade cadastral podem ser vendidos no mesmo contrato — o que
nenhum outro município da lista permite. **Paulistana** é o segundo (17 bairros, não-tenant,
RCL R$ 131,8 mi), com a ressalva da população menor (21 mil).

## Um sinal que apareceu sem ser procurado

**Oito dos 25 municípios não retornaram RREO 2025 no SICONFI** — União, Luís Correia, Piracuruca,
Água Branca, Baixa Grande do Ribeiro, Ilha Grande, Lagoa do Barro do Piauí, Simplício Mendes.

Município que não publica demonstrativo fiscal obrigatório é município com gestão fiscal frágil e sem
equipe — **exatamente o perfil do comprador do Segmento B**. A ausência de dado no SICONFI vira, ela
mesma, um critério de qualificação de lead: quem não consegue enviar RREO ao Tesouro não vai
conseguir enviar remessa ao CADURB sozinho até 31/12.

## Ressalva de método
Ausência no Certificate Transparency **não prova** que o município não é cliente da Foxinline — ele
pode não ter subdomínio próprio. É evidência forte para a presença, fraca para a ausência. Confirmar
caso a caso antes de usar comercialmente.

# ANEXO 5 — ARBITRAGEM RODADA 6

# Arbitragem rodada 6 — método do SICONFI documentado, tenants corrigidos

## 1. A API do SICONFI está funcionando. Método exato, para revalidação

Testado em 2026-09-16, duas variantes de caminho, ambas **HTTP 200 com dado idêntico**:

```
https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo
https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rreo
```

**Parâmetros exatos usados (todos obrigatórios):**
```
an_exercicio=2025
nr_periodo=6
co_tipo_demonstrativo=RREO
no_anexo=RREO-Anexo%2003      ← o %20 é imprescindível; "RREO-Anexo 03" sem encode falha
co_esfera=M
id_ente=<código IBGE de 7 dígitos>
```

Header `User-Agent` de navegador e `Accept-Encoding: identity` (sem isso, o IBGE às vezes devolve
gzip e o parser quebra — problema observado na API de localidades, não no SICONFI).

**Extração do IPTU:** filtrar `items` onde `conta == "IPTU"` **e** `coluna` começa com `<MR`
(as 12 colunas de meses móveis; somar dá o acumulado 12 meses). Filtrar por `coluna` é o que evita
somar linhas de totalização e duplicar valores.

**Resultado de controle:** Teresina 2025 → 427 itens, 12 linhas de IPTU,
**R$ 166.321.115,49** — reproduzido hoje, idêntico ao extraído ontem.

Se o teste da outra sessão voltou vazio para Teresina, a causa está nos parâmetros (o mais provável é
o encode do `no_anexo`) ou em instabilidade momentânea — não no endpoint.

## 2. Os 8 RREO ausentes: NÃO foi falha silenciosa — e o achado se refina

A suspeita era legítima (o script original mascarava exceções com `except Exception`). Reexecutei
**com erro explícito**, por município: todos retornaram **HTTP 200 com `items: []`**. Nenhum timeout,
nenhum HTTPError. A API responde e diz que não há dado. Controle: **Altos** retornou 116 itens na
mesma execução.

Testando três exercícios, o achado se divide em dois grupos com força de sinal diferente:

| Município | 2025 | 2024 | 2023 | Leitura |
|---|---|---|---|---|
| União | 0 | 0 | 0 | **nunca entregou em 3 anos** |
| Água Branca | 0 | 0 | 0 | **nunca entregou em 3 anos** |
| Baixa Grande do Ribeiro | 0 | 0 | 0 | **nunca entregou em 3 anos** |
| Lagoa do Barro do Piauí | 0 | 0 | 0 | **nunca entregou em 3 anos** |
| Simplício Mendes | 0 | 0 | 0 | **nunca entregou em 3 anos** |
| Luís Correia | 0 | 394 | 373 | entregou antes, falhou em 2025 |
| Piracuruca | 0 | 364 | 0 | intermitente |
| Ilha Grande | 0 | 317 | 312 | entregou antes, falhou em 2025 |

**Correção à minha formulação anterior:** eu tratei os 8 como um bloco. São dois grupos.
**Cinco nunca entregaram em três exercícios** — sinal forte de incapacidade estrutural, e o melhor
lead do Segmento B que esta análise produziu. **Três entregavam e pararam em 2025** — sinal moderado,
que pode indicar troca de gestão ou perda de equipe (e o prazo de entrega do 6º bimestre de 2025
venceu em jan/2026, há oito meses: não é atraso de consolidação).

**Ressalva mantida:** ausência do RREO Anexo 03 não é prova absoluta de não-entrega — o município
pode ter entregue em outra periodicidade ou anexo. Confirmar no portal web antes de uso comercial.

## 3. Tenants: ela está certa. Eu superincluí dois, e a causa é identificável

Meu cruzamento normalizava o **último rótulo** do subdomínio, o que gera falso positivo em host de
cartório com padrão `<produto>.<municipio>`. Refiz olhando o **host completo**:

| Município | Hosts encontrados | Veredito |
|---|---|---|
| Piripiri | `piripiri` + `piripiri2oficio` | **tenant municipal** |
| Campo Maior | `campomaior`, `notas.campomaior` | **tenant municipal** |
| Corrente | `corrente` + `1oficiocorrente` | **tenant municipal** |
| União | `uniao` + `2oficiouniao` | **tenant municipal** |
| Brasileira | `brasileira` | **tenant municipal** |
| Ilha Grande | `ilhagrande` | **tenant municipal** |
| **Barras** | `cartoriobarras`, `notarial.barras`, `registral.barras` | **só cartório** ❌ era falso positivo meu |
| **Água Branca** | `registral.aguabranca`, `saopedroaguabranca` | **só cartório** ❌ era falso positivo meu |
| Altos | `2oficioaltos` | só cartório |
| Paulistana | `paulistana2oficio` | só cartório |

**São 6 tenants municipais, não 8** — exatamente a lista dela.

**Detalhe sobre Água Branca:** o host `saopedroaguabranca.foxinline.com` é
**São Pedro da Água Branca — MARANHÃO**, município distinto. Meu match por substring casou
"aguabranca" dentro dele. Dois erros diferentes produzindo o mesmo falso positivo.

## 4. A cega estrutural do PROUrbe — aceita integralmente

`cerurb.prourb.foxinline.com` é host único: municípios atendidos pelo programa estadual da SEAD **não
ganham subdomínio próprio** e são invisíveis a este método. **"Não-tenant" é sempre provisório.**

Isso deve constar como ressalva fixa em qualquer uso comercial da lista. O fechamento dessa lacuna
depende da relação de adesões ao PROUrbe junto à SEAD-PI (e-SIC ou portal da transparência estadual)
— é a pendência de campo mais barata e de maior retorno que resta.

## 5. População de Altos
Censo 2022: **47.453**. O valor 46.826 que usei vem do campo `populacao` do próprio retorno do
SICONFI, que é **estimativa anual do IBGE**, não o Censo. Fontes diferentes, ambas válidas; usar o
Censo em material externo. O rank (7º do PI) confere nas duas.

## 6. O que sobrevive

**Altos segue como melhor candidato a piloto fora da capital** — e agora com evidência mais limpa:
17 bairros, **nenhum host municipal no CT** (só o 2º Ofício), RCL R$ 61,3 mi, IPTU R$ 245 mil
(fronteira A/B), 7º município do estado. Ressalva PROUrbe a confirmar.

**Paulistana** confirma como segundo (17 bairros, só host de cartório).

**Campo Maior sai da frente:** é tenant municipal confirmado **e** Segmento A — dois motivos.

**Nota sobre Altos:** o retorno do SICONFI traz apenas **2 linhas de IPTU** (contra 12–14 dos demais),
o que sugere preenchimento parcial do demonstrativo. Vale confirmar o valor no TCE-PI antes de levar
a número para reunião.

# ANEXO 6 — API DO CADURB

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
