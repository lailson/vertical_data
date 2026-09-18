# Parecer R6 — GLM · Eixo negócio · Revisão de execução

**Data:** 2026-09-16 · **Base:** pacote-r6-glm.md (Anexos 1–6) · **Formato:** 6 achados, só o que muda.

**Veredito antecipado (desenvolvido no Achado 6): APROVAR COM AJUSTES.** O desenho de duas pistas
está certo, mas a meta de venda contradiz a capacidade de entrega declarada no próprio plano, faltam
2 e-SIC críticos e o e-mail à Foxinline sai do M0.

---

## 1. Meta de 5–10 diagnósticos em 30 dias: NÃO. Teto realista: 2–3 — e o limite é a ENTREGA, não a venda

**Contradição interna do plano.** O Anexo 2 §11.2 declara capacidade artesanal de **~2 contas/mês**
(7–10 na janela de 60 dias) e só **10–20/mês com conector pronto** — que não existirá antes de
meados de outubro. O calendário R6 pede **5–10 fechamentos em 30 dias: 2,5–5× a capacidade de
entrega do próprio plano, antes do multiplicador existir**. Vender 10 e entregar 3 queima
exatamente os pilotos que deveriam gerar a referência — e "remessa aceita" é o único ativo
vendável no pós-prazo (Anexo 2 §11.1). A meta também é mais agressiva que o roadmap que a gerou:
o Anexo 2 §7 previa **3 adesões em ~90 dias**; a R6 inflou para 5–10 em 30, sem evidência nova —
pelo contrário, o Anexo 1 §3d já recuou para 2–3.

**Matemática da venda.** Janela 16/10–15/11 = **4 semanas úteis líquidas** (2/11 e 15/11 feriados;
outubro reduzido pela eleição nacional — Anexo 2, aviso de prazo). Ciclo por conta sem referência
anterior: 1ª reunião → secretário → prefeito → dossiê + dispensa + empenho ≈ **3–6 semanas**, só
funcionando com pipeline sobreposto. Para fechar 5–10 até 15/11 seriam necessários **~20–40
processos ativos já em 16/10** — data em que nem a apresentação interna (Anexo 3) aconteceu.

**Recomendação:** meta de contrato = **2–3 assinadas até 15/11 + 8–12 propostas vivas + ≥20
primeiras reuniões**; 5–10 vira cenário otimista **condicionado ao conector validado**.

**Para errar a meta sem contaminar a tese:**
- o relógio da tese é o do Anexo 2 §9 (**3 pilotos sem assinatura em 90 dias → reavaliar**), não
  30 dias — 30 dias mede execução, não tese;
- todo não-fechamento **classificado**: atraso de prefeito/orçamento/eleição ≠ rejeição de preço
  com dor confirmada. Só a segunda é evidência contra a tese;
- métricas-leading semanais (reuniões, propostas na mesa, dossiês entregues): meta de contagem
  errada com leading saudáveis = execução; leading zerados = tese.

## 2. Foxinline: ADIAR — chegar agora é entregar roadmap à incumbente

**O custo de falar agora é maior do que o pacote calcula.** A spec é pública (Anexo 6); a barreira
que resta é execução de campo — exatamente o que uma conversa de parceria descreve (Anexo 1 §3e).
O cenário-padrão de uma abordagem sem ativo: **educamos quem tem 236 relacionamentos** (Anexo 2
§2.3) e saímos sem contrato. E o custo real não é o e-mail: é a informação que ele entrega de graça.

**A janela não exige falar agora.** Parceria com incumbente é jogada de escala pós-prova
(Anexo 2 §11.11), e 31/12 continua aberto depois do 1º aceite. O ativo de troca — 2–3 remessas
aceitas em municípios não-tenants (Altos, Paulistana; Anexos 4–5) — chega em **semanas**, não
meses, porque os pilotos têm cadastro REURB pronto ou dor comprovável.

**O risco de esperar é o gatilho do Anexo 2 §9** (lote "Central CERURB + conformidade" via
APPM/TJ antes de 10 assinaturas). Mitigação **sem revelação**: monitoramento passivo semanal (site,
releases, Certificate Transparency — método do Anexo 5 §3) + **gatilho de antecipação**: qualquer
sinal de produto CIB da Foxinline adianta a conversa para o dia seguinte, com o que houver na mesa.

**Trocar o e-mail do M0 por:** deck de parceria pronto (1 página, dois cenários: com e sem remessa
aceita) + rotina de monitoramento. Custo igual, opção preservada.

## 3. Sequência de reuniões: fazenda → prefeito → APPM → planejamento → TJ-PI

1. **Secretário de fazenda do município-alvo.** É onde a dor é comprovável com dado público: 5
   municípios sem RREO em **3 exercícios** e 3 que pararam em 2025 (Anexo 5 §2) são a lista de
   compra pronta. Ele recebe o dossiê de dispensa preenchido ("o caminho orçamentário é parte do
   produto", Anexo 2 §11.7) e vira o proponente interno.
2. **Prefeito, com processo na mesa.** Decisor único da dispensa <R$ 59 mil (Anexo 2 §3). Chamado
   pelo próprio secretário, converte na 1ª reunião; frio e sem marca, é a reunião de **menor**
   conversão da cadeia.
3. **APPM — só com aceite na mesa** (Anexo 2 §11.11). Resolve a falta de referência por endosso e
   é a defesa contra o lote (§11.7). Antes disso é pedir vitrine sem produto.
4. **Secretário de planejamento — fora da venda B.** 199 dos 224 municípios não têm granularidade
   intraurbana pública; painel é produto dos 25 com bairros (Anexo 3 §9.1–9.3). Onde existir, é
   upsell de 2027.
5. **TJ-PI — fora da janela de venda.** O contrato 156/2023 veda repasse (Anexo 2 §2.2); agenda
   institucional de 2027.

A reunião que importa agora **não está na lista**: a de escopo com o proponente REURB (decisão nº 1,
Anexo 1 §3) — precede as cinco.

## 4. Faltam 2 e-SIC críticos — e os 3 municipais de Teresina estão sobre-classificados

- **FALTA: RFB — adesões ao SINTER por município + remessas aceitas.** É o **denominador do mercado
  restante**: cada município aderido com aceite é conta fora da lista B e evidência de concorrente
  ativo. Sem ele, a lista de alvos tem tamanho desconhecido e o gatilho do Anexo 2 §11.12
  (integração comoditizada <R$ 8 mil) fica cego. O próprio pacote admite que a RFB responde.
- **FALTA: SEFAZ-PI — critério e volume do repasse de IBS por município.** "Perda de receita"
  (Anexo 6) é o argumento mais concreto para ordenador; convertido em **R$/município/ano** é a
  linha mais forte do deck — mesmo sabendo que o gatilho emocional de novembro é cartorial
  (Anexo 2 §11.3).
- **REBAIXAR: ETURB, SEMDUH e Águes de Teresina.** Servem à vitrine (painel dos 123 bairros), não
  ao produto (conformidade CIB). Disparam-se porque é grátis, mas **nada da PISTA 1 os espera**; o
  e-SIC que decide alvo é o da SEAD/PROUrbe — a cega estrutural que torna "não-tenant" sempre
  provisório (Anexo 5 §4).
- Opcional: **TCE-PI** — dispensas de software/geoprocessamento 2024–26 (preço praticado e
  concorrência) e, de quebra, validação do IPTU de Altos antes de reunião (Anexo 5 §6).

## 5. Os 30 dias dos e-SIC: o comercial que não depende deles é quase todo o M0

1. **Reunião de escopo com o proponente** (Anexo 1 §3) → abre Guaribas e N. Sra. de Nazaré, onde o
   cadastro REURB **já existe e já foi pago** (Anexo 2 §4). O caminho mais curto até a 1ª remessa.
2. **Ataque direto aos 8 municípios do sinal RREO** (Anexo 5 §2) — a qualificação já está em mãos,
   nenhum e-SIC necessário: 5 nunca entregaram (União, Água Branca, Baixa Grande do Ribeiro, Lagoa
   do Barro do PI, Simplício Mendes), 3 pararam em 2025.
3. **Verificação fiscal de Altos e Paulistana** — SICONFI revalidado com método reproduzível
   (Anexo 5 §1); falta só o TCE para Altos (§6). Únicos não-tenants com bairros e porte (Anexo 4).
4. **Dossiê de dispensa reutilizável + calendário de empenho** — quem precisa de dinheiro em 2027
   empenha em 2026 (Anexo 2 §11.1): outubro é o mês de deixar processos **prontos para assinar
   nov–dez**.
5. **Conector CADURB contra o Swagger de homologação + pedido de credencial na 1ª semana**
   (Anexo 1 §3a; Anexo 6) — é o que tira a capacidade de 2 para 10–20 contas/mês (Anexo 2 §11.2) e
   pré-requisito da meta otimista do Achado 1.
6. **Metodologia do iv publicada** — meio dia de trabalho e **bloqueante para apresentar a
   terceiros** (Anexo 1 §3c); sem ela, o painel repete o passivo do protótipo com dado real — pior.
7. **E2 — diagnóstico de conformidade em Guaribas/Nazaré** (Anexo 3 §2): o produto, não a vitrine.

INEP só depois do conector e da verificação fiscal (Anexo 1 §3b) — mantido.

## 6. Veredito: APROVAR COM AJUSTES

O sequenciamento (duas pistas, e-SIC primeiro, dispensa, Altos piloto) está correto e não se refaz.
Ajustes obrigatórios:

1. **Meta: 2–3 assinadas até 15/11**; 5–10 rebaixado a cenário otimista condicionado ao conector —
   a meta atual excede a capacidade de entrega do próprio plano em 2,5–5× (Achado 1; Anexo 2 §11.2).
2. **Foxinline sai do M0** → deck pronto + monitoramento passivo com gatilho de antecipação
   (Achado 2).
3. **+2 e-SIC: RFB/SINTER (mercado restante) e SEFAZ-PI (IBS em R$)**; rebaixar os 3 municipais de
   Teresina (Achado 4).
4. **`iv` no M0, INEP para depois do conector** (Anexo 1 §3b–c).
5. **Credencial CADURB verificada na 1ª semana** — senão o conector fica sem ambiente de teste real
   e a descoberta cai na semana errada (Anexo 1 §3a).
6. **Consistência documental:** o Anexo 2 §11.8 ainda fixa corte de **"n ≥ 50 faces"** — regra
   caducada pela correção de métrica do Anexo 1 §2 (o corte agora é em **domicílios**, com limiar
   muito menor). Quem executar pelo plano consolidado aplicará a regra errada. Unificar antes de
   qualquer uso.
