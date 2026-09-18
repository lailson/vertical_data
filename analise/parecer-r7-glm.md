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
