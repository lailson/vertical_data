# Parecer R5 — FECHAMENTO COMERCIAL. A porta é de graça: o produto é o cadastro que passa por ela. A janela real não é 15 meses — é um trimestre. E o Segmento B acaba de virar o funil e o combustível do Segmento A

Consultor: GLM. Data: 2026-09-15. Rodada 5 (fechamento comercial) do dossiê CERURB: incorpora o
Manual Operacional público do CADURB (Anexo A), a arbitragem que corrige a cadeia tributária e
expõe a armadilha amostral do entorno (Anexo B), e revisa o plano consolidado (Anexo C) e o meu
próprio parecer R4 (Anexo F). Regra da rodada: ≤6 achados, adversarial, quantificado, só o que muda.

**Nota de método, antes de tudo — o enunciado desta rodada contém uma aritmética que não fecha e ela
muda a tese inteira de timing.** O enunciado diz "~66% ainda fora, a 15 meses do prazo
(31/12/2026)". De hoje (15/09/2026) a 31/12/2026 há **107 dias — 3,5 meses**, não 15. Quinze meses
contariam até 31/12/2027, que não é o prazo de nenhum dispositivo citado (Anexo B, seção 3: o fim do
prazo de 24 meses do art. 266 é 31/12/2026, véspera do marco de 01/01/2027 do Anexo C). Este parecer
adota a data normativa. A diferença não é pedantismo: **a venda de adesão do Segmento B não é um
plano de 2027 — é um sprint de Q4/2026, disputado ainda contra uma eleição nacional em outubro.**
Tudo o que segue deriva dessa correção.

---

## Achado 1 — O produto vendável não é acesso nem integração: é a capacidade de cumprir. Proposta de valor em uma frase: "a Receita dá a porta de graça; nós entregamos o município do outro lado dela". Ticket reestruturado em três módulos, com o diagnóstico de R$ 3–5 mil como novo foot-in-the-door

**Diagnóstico:** O Anexo A desfaz o pitch antigo em três camadas. Primeira: adesão ao SINTER é
convênio **gratuito** e a API é fornecida sem custo — vender "acesso ao CIB" é vender o que é de
graa (Anexo A; Anexo B, seção 3). Segunda: o Manual Operacional é **público, com Swagger de
homologação** (Anexo A) — a integração deixou de ser especialização de quem tem spec restrita e virou
trabalho de engenharia comum, verificável programaticamente. Isto me corrige: no R4 herdei do plano a
nota de que "o Roteiro Técnico não é público e isso dá vantagem de informação a quem conduz a adesão"
(Anexo C, seção 10; Anexo F). Estava errado — a spec que importa é pública; **a vantagem informacional
evaporou, e o que sobra de barreira é execução: saneamento de cadastro e serviço de campo.**
Terceira: o que o município-tipo do Segmento B tem é uma planilha desatualizada (Anexo A), e o schema
5.1–5.7 exige inscrição, tipo, áreas, endereço, titulares com documento, CNS de serventia e o bloco
ITBI da última transação (Anexo A). O esforço não está na chamada HTTP — está em pôr o cadastro no
estado em que a API o aceita. Logo, o produto vendável é o **"Pacote Capacidade de Cumprir"**:
diagnóstico de completude contra o schema, saneamento e georreferenciamento, condução dos 16 passos
da adesão, integração e remessa, e o ciclo de atualização. A proposta de valor em uma frase, para o
ordenador de despesa:

> **"O convênio é gratuito e a API da Receita é aberta — o que o município não tem é o cadastro que
> ela aceita; nós entregamos a remessa aceita no CADURB dentro do prazo, para o senhor não perder o
> repasse do IBS nem travar o registro dos imóveis dos seus eleitores."**

**Precificação — três módulos, e uma decisão deliberada de NÃO cortar preço porque a API é de graça:**

| Módulo | Preço | Conteúdo | Justificativa |
|---|---|---|---|
| **Diagnóstico de conformidade** | **R$ 3–5 mil** | cruzamento do cadastro municipal contra os campos obrigatórios do schema 5.1–5.7; laudo com % de completude por bloco e custo estimado do saneamento | dispensa direta, 15 dias; qualifica o alvo e abre a porta (novo — não existia no R4) |
| **Pacote conformidade** | **R$ 12–25 mil** | adesão conduzida (16 passos) + saneamento/geo + 1ª remessa com **aceite objetivo** | 0,026–0,055% da RCL mediana de R$ 45,7 mi (Anexo C); custo alternativo: cadastro completo tipo Geopixel a R$ 270 mil (Anexo B, seção 4); valor do risco: perda de repasse do IBS (LC 214, art. 11, II — Anexo B, seção 3) |
| **Manutenção anual** | **R$ 4–8 mil/ano** | re-remessas, desativações, atualização cadastral, sustentação do convênio | recorrência cadastral do R4 (Anexo F, Achado 1), agora com escopo API (endpoint de desativação — Anexo A) |

Entrada + primeiro ano: R$ 16–33 mil — **cabe inteiro numa dispensa de ~R$ 59 mil** (Anexo C, seção
3), sem licitação, o que é condição de existência do modelo em município sem equipe de compras.
A justificativa de manter a faixa R$ 12–25 mil embora o custo técnico tenha caído: o preço é ancorado
no **risco do comprador** (IBS + entrave de registro — Anexo A) e no **custo alternativo** (saneamento
artesanal ou R$ 270 mil de referência do mercado — Anexo B), não no nosso custo. A API pública não
cutuca nenhuma das duas âncoras. O que a API pública muda é **margem e velocidade** — e o gatilho
competitivo que ela cria está no Achado 5.

**Consequência:** pitch, proposta e site mudam de eixo: nada de "acesso", "integração" ou
"modernização" como substantivo principal; o par verbo-objeto é o mais concreto possível:
**"entregar a remessa aceita"**. O produto de diagnóstico de R$ 3–5 mil passa a ser a unidade de venda inicial
padrão do canal — barato o bastante para decidir em uma reunião, útil o bastante para gerar o
saneamento como venda subsequente. LTV B em 5 anos recalculado: R$ 12–25 mil + 4 × R$ 4–8 mil =
**R$ 28–57 mil/conta** (vs. R$ 24–65 mil do R4 — Anexo F, Achado 1; range mais estreito, mesmo centro).

## Achado 2 — A onda não vem em 2027: o prazo aperta em 107 dias, o gatilho do pânico é o eleitor na porta do cartório, não a norma federal — e pânico é ótimo para equipe pequena APENAS se a entrega for automatizada

**Diagnóstico:** O tamanho: 1.904 aderidos de 5.570 (34,2%) em 14/09/2026 → **3.666 municípios
fora** (65,8%) a 3,5 meses do fim do prazo normativo (Anexo B, seção 4; e a correção da nota de
método acima). Aplicando a média nacional ao PI: **~147 dos 224 municípios fora do SINTER** —
pendência barata de levantar por LAI/painel público no M0–M1 (o plano já prevê qualificar os 224 —
Anexo C, seção 7; agora com mais uma variável: aderido × não-aderido). O estoque de valor da onda no
PI: 147 × R$ 8–25 mil = **R$ 1,2–3,7 mi de entrada**. O timing, em três choques encadeados:
(i) **out/2026** — trimestre final do prazo, mas mês consumido por eleição nacional; a janela prática
de assinatura é **nov–dez/2026, ~60 dias**; (ii) **01/01/2027** — o prazo vira; quem não aderiu entra
na zona de perda de repasse do IBS conforme a ativação da transição (Anexo B, seção 3) e de entraves
de registro/alvará/ITBI (Anexo A); (iii) **2027+** — a materialização do dano. Aqui o ponto que o
enunciado não faz e que decide a campanha de venda: **o pânico municipal não vem de cima, vem de
baixo**. A consequência "perda de repasse do IBS" é real mas escalonada na transição tributária — não
assusta ordenador de despesa em novembro. O que assusta em janeiro é o **cartório recusando ou
questionando registro de imóvel sem CIB** — porque a IN RFB 2.275/2025 obriga os cartórios (Anexo B,
seção 3), e o primeiro eleitor que não conseguir registrar a casa do filho liga para a prefeitura, não
para a Receita. Prefeitura pequena reage ao eleitor na porta, não à norma federal: **o gatilho
operacional do pânico é cartorial, e ele dispara no 1º trimestre de 2027, depois do prazo, quando o
dinheiro da assinatura já precisa estar empenhado em 2026.** Cenário alternativo que não se pode
ignorar: 66% fora a 3,5 meses do fim é o retrato clássico de **prorrogação provável** — prazo
cadastral federal com 2/3 da população fora do compliance desliza historicamente. Os dois cenários
exigem planos diferentes e o Achado 5 os bifurca.

**É bom ou ruim para uma equipe pequena?** As duas coisas, e a fronteira é exatamente a automação.
Bom: pânico comprime o ciclo de venda de meses para dias (a decisão vira "resolva isto"), dispensa <
R$ 59 mil dispensa concorrência, e o aceite objetivo — remessa aceita no CADURB, verificável por API
(Anexo A) — neutraliza a discussão de "qual dashboard é melhor" que favorece incumbente grande
(Anexo F, Achado 4). Ruim: pânico comprime também a paciência da entrega — com capacidade artesanal
de ~2 contas/mês, a janela de 60 dias comporta **7–10 contas, não 147**; e pânico atrai a Foxinline
empacotando "conformidade" a custo marginal para os ~236 tenants dela (Anexo C, seção 2; Anexo F,
Achados 3–4), com estrutura para atender em lote. A conta que fecha a questão: **o B só come a onda
se o conector estiver pronto antes da demanda** — e o Swagger de homologação público (Anexo A) torna
isso possível de fazer agora, sem cliente, sem convênio, sem custo de acesso.

**Consequência:** plano de vendas do Q4/2026 com metas modestas em contagem e duras em aceite:
3–5 pilotos com **remessa aceita (homologação) até 31/12/2026** — não "contratada", como dizia o R4
(Anexo F, Achado 6), mas **aceita**. Pós-prazo, dois playbooks prontos: cenário pânico → produto
"regularização em 90 dias" com sobrepreço de +20–30%, capacidade declarada e lista de espera (escassez
é argumento, não fracasso); cenário prorrogação → o gancho muda de "prazo" para "IBS + cartório", a
venda vira anual e as metas de contagem esticam 2 trimestres. Não se constrói custo fixo contra
nenhum dos dois cenários isoladamente.

## Achado 3 — O Segmento B produz o dado de calibração do Segmento A como subproduto obrigatório: subsidiar sim, mas em produto, não em dinheiro — teto de subsídio R$ 5–10 mil/conta, pago pelo valor esperado do A, com cláusula de finalidade no contrato desde o dia 1

**Diagnóstico:** O bloco 5.7 do schema (baseCalculITBI, valorRefITBI, data, tipo, % transacionado,
partes com CPF/CNPJ) somado aos blocos 5.1–5.6 (endereço, tipo, arquitetônico, destinação, padrão
construtivo, áreas) é exatamente o vetor de features do art. 256 — atributos físicos + preço observado
com data (Anexo A). O município que cumpre o art. 266 monta, sem saber, a base que torna o art. 256
executável (Anexo A). Isso resolve a objeção "não há ITBI aberto no PI" (nenhum município médio de
PI/CE/MA publica — Anexo B, seção 4): o dado não é **aberto**, mas o município **tem**, e a
conformidade o obriga a estruturá-lo (Anexo A). Quem opera o B fica com o pipeline. Quantificado:

- **Por município isolado:** município de 20–50 mil hab. flutua em ~300–1.500 transações ITBI/ano —
  **não calibra um modelo hedônico espacial sozinho** em nível municipal. O dataset local, isolado,
  é ilusão: a ilusão de achar que cada conta B vem com um modelo A embutido.
- **Em pool regional:** 30–50 contratos B × 500–1.500 transações/ano = **15–75 mil observações/ano**
  com estrutura de painel (efeitos fixos por município) — base treinável e defensável, calibrável
  localmente com poucas dezenas de observações. O ativo real do B é o **pool + o acesso contínuo**,
  não o arquivo de cada prefeitura.
- **Valor esperado do A habilitado:** LTV A de R$ 145–239 mil/conta (Anexo C, seção 3), mas no
  beachhead só ~9 municípios + Teresina têm base fiscal para o A agora (Anexo F, Achado 1). Seja
  conservador: p(conversão B→A em 3 anos) = 10–20%, valor líquido por conversão ~R$ 100–150 mil, e
  desconte o risco do motor central da RFB (Anexo C, seção 9) zerar parte do P2-A — digamos −30%.
  **EV do A por conta B ≈ R$ 7–20 mil em 3 anos.** Teto de subsídio defensável: a metade inferior
  disso, **R$ 5–10 mil por conta — e em produto, nunca em desconto no preço.**

Por que em produto: (a) desconto em dinheiro destrói a âncora de risco que sustenta a faixa
R$ 12–25 mil no meio de um mercado em pânico (Achado 1); (b) o piso da faixa (R$ 12 mil para
município com cadastro REURB pronto — Guaribas, N. Sra. de Nazaré, Anexo C, seção 4) **já é**
implicitamente um subsídio: o custo de aquisição do dado é ~zero porque a REURB pagou a cartografia
(Anexo C, seção 8) — o subsídio existe, é racional e está disfarçado de tabela; (c) o formato que
funciona é o **"diagnóstico de valor venal" de cortesia**: com o dado já no pipeline do B, comparar
valor venal municipal × fluxo de transações e entregar ao prefeito uma página com a defasagem local —
é literalmente o produto do Anexo C ("medir a defasagem antes que a Receita a publique") executado
com custo marginal baixo, e é o que abre a conversa do A em 2027 com o cliente já convencido do
número.

**Condição inegociável que acompanha:** o uso do dado para PGV/avaliação tem de estar na
**finalidade declarada do contrato do B desde o dia 1** (o dado é do município, nós operadores,
finalidade declarada — Anexo A), com as cláusulas de LGPD, exportação e PI do Anexo C (seção 8).
Sem a cláusula, o pool não se forma legalmente e o subsídio foi pago por nada.

**Consequência:** a estratégia não é "baratear o B para ganhar o A" — é **cobrar o B cheio e entregar
o A como consequência**: cláusula de finalidade + extração estruturada (schema único desde o primeiro
cliente) + diagnóstico de valor venal como brinde anual. O painel público por bairro com dado real
(Anexos D–E) é o que faz a vitrine; o pipeline ITBI é o que faz o funil. Os dois juntos, e só eles,
justificam chamar o B de "custo de aquisição do A".

## Achado 4 — PROFISCO III sai do plano de financiamento do ano 1: o dinheiro do B no PI é orçamento corrente (FPM/Fundeb) em rubrica de serviços de TI, contratado por dispensa, empenhado em 2026 — e a venda tem de acontecer antes da dotação virar restos a pagar

**Diagnóstico:** PROFISCO III é empréstimo do BID (US$ 278 mi federal + CCLIP US$ 2 bi para
estados), **municípios só na 2ª fase**, exige autorização legislativa (Anexo B, seção 3) — ciclo de
6–18 meses (Anexo C, seção 8, condição 7). Não é dinheiro disponível para o ticket B; tratá-lo como
fonte era o resquício do "dinheiro carimbado" que a arbitragem já corrigiu (Anexo B, seção 3). Onde
está o dinheiro de verdade, dado o par estrutural do PI — RCL mediana **R$ 45,7 mi**, IPTU mediano
**R$ 2.214/ano** (Anexo B, seção 5): 95%+ da RCL é transferência (FPM/Fundeb — Anexo C, seção 2), e o
gasto discricionário de funcionamento cabe em **outras despesas correntes / serviços de terceiros –
PJ** (a rubrica que em todo município pequeno paga software, assessoria e consultoria; a ação 2000 do
PPA, quando usada para inovação em gestão, é o endereço usual da despesa de TI). A entrada de
R$ 12–25 mil = 0,026–0,055% da RCL — grandeza de uma mensalidade de sistema de nota fiscal eletrônica,
não de um investimento que exija crédito suplementar. **Veículo:** dispensa por valor (pacote completo
abaixo de ~R$ 59 mil — Anexo C, seção 3), contratada como serviço técnico; para o canal em lote,
**consórcio intermunicipal via APPM** (compra compartilhada, um instrumento para N municípios) — que é
também a defesa contra o lote da Foxinline (Anexo C, seção 9), porque dá ao canal TJ/APPM um produto
para oferecer antes que a incumbente o empacote (Anexo F, Achado 3). **Calendário — a parte que o
roadmap do Anexo C não explicita e que agora decide:** orçamento municipal tem ano próprio; quem
precisa de dinheiro em 2027 empenha em 2026. Assinatura ideal: **nov–dez/2026, sobre dotação corrente
vigente, com prestação em 2027**; o que escorregar vira dependente da LOA 2027 (aprovada no 1º
semestre, com calendário eleitoral nacional já passado) e adiciona 1–2 trimestres ao ciclo. No
cenário pânico pós-prazo (Achado 2), o município que não empenhou em 2026 compra com o dinheiro que
deveria ter — e aí sim com pressa e sobrepreço.

**Consequência:** nenhuma proposta do B menciona PROFISCO como fonte no ano 1 (menção = presente para
o controle interno adiar); toda proposta traz a rubrica e o veículo prontos ("serviço técnico por
dispensa, ODC/PJ, sem impacto no investimento") porque o secretário de fazenda municipal não tem
equipe para descobrir isso sozinho — **preencher o caminho orçamentário é parte do produto**, e é
grátis de fazer. A Trilha PROFISCO do R4 (Anexo F, Achado 6) é rebaixada a opcional de 2ª fase:
acordos-campeão só quando a fase municipal existir de verdade.

## Achado 5 — Roadmap de 12 meses revisado: o conector CADURB sobe para o M0 (é a única forma de uma equipe pequena comer a onda), a meta do piloto endurece de "contratada" para "aceita", e o pós-prazo vira dois playbooks — mais um gatilho novo: a comoditização da própria integração

**Diagnóstico:** Contra o roadmap do Anexo C (seção 7), cinco mudanças de ordem, prazo ou meta —
nenhuma cosmética:

| # | Mudança | De → Para | Por quê |
|---|---|---|---|
| 1 | **Conector CADURB no M0–M1, antes de qualquer cliente** | não existia no plano → primeira prioridade técnica de out/26 | o Swagger de homologação é público (Anexo A): construir contra ele agora é legal, barato e é a **condição de comer a onda** — capacidade artesanal é 2 contas/mês = 7–10 na janela; conector pronto muda a escala para 10–20/mês (Achado 2) |
| 2 | **Levantar adesão SINTER dos 224 no M0–M1** | variável ausente na qualificação → coluna obrigatória da lista de ~40 alvos | 147 municípios fora do SINTER é o alvo; aderido sem remessa é outro produto (só saneamento) — vender um pelo outro queima a conta |
| 3 | **Meta do piloto endurece** | "3 adesões + remessas **contratadas** até 31/12/2026" (Anexo C, seção 7; Anexo F, Achado 6) → "3–5 pilotos com **remessa aceita em homologação** até 31/12/2026" | contrato não prova nada; aceite programático prova (Anexo A) — e só remessa aceita gera referência vendável no pós-prazo. Janela prática: nov–dez (outubro tem eleição) |
| 4 | **Pós-prazo bifurca em dois playbooks (M3–M6)** | "escalar via APPM" genérica → (a) cenário prorrogação: ganho vira "IBS + cartório", venda anual, metas de contagem +2 trimestres; (b) cenário pânico: "regularização em 90 dias" com +20–30% de preço e lista de espera | 66% fora a 3,5 meses do fim (Anexo B, seção 4) tornam prorrogação plausível; plano único seria aposta contra um cenário de 50% |
| 5 | **Cláusula de finalidade + extração estruturada em TODO contrato B desde o primeiro** | ausente do Anexo C, seção 8 (cláusulas genéricas de LGPD/PI) → inclui finalidade de avaliação e schema único de extração do bloco ITBI | o pool do Segmento A (Achado 3) só se forma se for contratual desde a origem; retrofit de cláusula em 2027 é perda de 100% do dado dos primeiros clientes |

Mantém-se integralmente: consertar o protótipo antes de qualquer demo (bloqueio de processo —
Anexos C e D; Anexo F, Achado 5), a due diligence da IN RFB 2.275/2025 (agora com foco na leitura
**cartorial** — é ela que dispara o pânico local, Achado 2), CERURB fora do caminho crítico
(Anexo F, Achado 3), Teresina como vitrine + conta A de 2027 (Anexo C, seção 4; Anexo F, Achado 2).
As metas de ano 1 do Anexo C — 25–40 contratos B, 1–3 contratos A, R$ 0,3–1,2 mi — **permanecem, com
uma ressalva de distribuição**: a concentração de fechamentos B desloca-se para Q4/26–Q2/27; se o
cenário prorrogação confirmar, a cauda estica e o run-rate ao fim do ano fica no terço inferior da
faixa. **Gatilho novo, que o Anexo A cria e o plano ainda não tem:** a barreira técnica do B caiu
para todos — se em qualquer trimestrefor visto concorrente (de qualquer porte) vendendo "integração
CADURB" por menos de ~R$ 8 mil como produto principal, o B está comoditizando na ponta errada, e a
resposta é acelerar o que não se copia: canal REURB, saneamento de campo e a referência de remessa
aceita — não brigar pelo preço da integração.

**Consequência:** a ordem de execução de outubro fica: conector → diagnóstico nos 2 pilotos REURB
prontos (Guaribas e N. Sra. de Nazaré — cadastro já pago, Anexo C, seção 4) → remessa em homologação
→ THEN a conversa de escala com APPM/canal TJ com aceite na mesa. O produto se prova sozinho antes de
qualquer reunião institucional — que é o único sequencing que funciona para equipe sem marca.

## Achado 6 — Veredito final: MANTIDA a entrada com condições, agora sobre três pernas — prazo real de 107 dias, produto redefinido como capacidade de cumprir, e o B como custo de aquisição do A. A frase para a primeira reunião: "A Receita dá a porta de graça; nós entregamos o município do outro lado dela — cadastro saneado, remessa aceita, IBS preservado."

**Veredito:** ENTRAR COM CONDIÇÕES (mantém Anexos C e F), com a Rodada 5 reancorando o negócio em
quatro pontos que invalidam o pitch anterior e o substituem por um melhor: (1) não se vende acesso —
vende-se capacidade de cumprir, a preço fixo modular, com aceite objetivo programático (Achado 1);
(2) a janela é Q4/2026 — novembro e dezembro — com o pós-prazo bifurcado em pânico × prorrogação e
planos para os dois (Achado 2); (3) o B é, contratualmente e desde o primeiro cliente, o funil e o
pool de dados do A — subsídio em produto até R$ 5–10 mil/conta, nunca em desconto (Achado 3);
(4) o financiamento é orçamento corrente por dispensa, com rubrica e veículo prontos na proposta, e
PROFISCO III fora do ano 1 (Achado 4). Herdadas e intactas: as quatro cláusulas LGPD/PI/exportação/
vedação a concorrentes, a ART de avaliador para o A, a cartografia REURB em formato aberto, ML fora
de SLA e nenhum custo fixo condicionado a convênio (Anexo C, seção 8).

**Frase de posicionamento — a primeira frase da primeira reunião, e o time não improvisa variação:**

> **"O convênio com a Receita é gratuito e a API é aberta — o que o município não tem é o cadastro
> que ela aceita. Nós entregamos a remessa aceita no CADURB dentro do prazo de 31/12, para o senhor
> não perder o repasse do IBS nem travar o registro dos imóveis dos seus eleitores."**

Três propriedades dessa frase, para que ninguém a considere "só marketing": ela **abre admitindo o
que é de graça** (mata na raiz a objeção "o SINTER não cobra nada" e desarma o concorrente que vende
acesso); ela **ancora no dano do comprador** (repasse + eleitor — as duas únicas moedas que movem
ordenador de despesa sem IPTU, Anexos A e B); e ela **promete só o que tem aceite objetivo**
(remessa aceita — verificável por API, Anexo A; nunca "modernização", nunca "painel", nunca
"precisão de modelo").

**Gatilhos de abandono e alerta, revistos:** (i) 3 pilotos B sem assinatura em 90 dias de esforço no
canal REURB → reavaliar a tese B com dado na mesa (mantém — Anexo F); (ii) qualquer arquitetura
condicionada ao CERURB/cláusula 4.1.1 (mantém); (iii) Foxinline fechando "Central CERURB +
conformidade" em lote via APPM/TJ antes de 10 assinaturas nossas → reavaliar em 30 dias (mantém; a
resposta é o consórcio APPM do Achado 4, não guerra de preço); (iv) RFB publicar motor central de
valor de referência (mantém — degrada o A e corta o teto de subsídio do Achado 3 para ~zero);
(v) concorrente vendendo integração CADURB < R$ 8 mil como produto principal → alerta de comoditização
(novo — Achado 5); (vi) protótipo com dado fictício em bairro nomeado = auto-gol, infração de
processo (mantém — Anexos C, D e F); (vii) **prazo do art. 266 prorrogado formalmente** → não é
gatilho de abandono, é o gatilho do playbook B do Achado 5: trocar o gancho "prazo" por "IBS +
cartório" em 48h e seguir — a obrigação não sumiu, só mudou de calendário.

**O que este parecer fecha:** o pacote de cinco rodadas converge para um negócio coerente — produto
de prazo para quem não tem equipe, paid by orçamento corrente, provado por aceite programático, que
constrói no caminho o pool de dados do produto de valor para quem tem base fiscal. A Rodada 5 não
achou uma tese nova; ela tirou da tese os três erros que ainda a sustentavam — vender acesso grátis,
contar com dinheiro emprestado e pensar que havia 15 meses. Não há 15 meses. **Há novembro,
dezembro, e depois há o cadastro de quem ficou fora.**
