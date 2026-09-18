# Dossiê de dispensa — contratação direta do diagnóstico cadastral

Pacote pronto para o município contratar o serviço em **~2 semanas**, dentro do
limite de dispensa por valor, com empenho ainda em 2026. "Preencher o caminho
orçamentário é parte do produto" — este dossiê é isso, em papel.

## Base legal (verificar versão vigente com o jurídico do município)

- **Dispensa por valor**: art. 75, inciso II, da Lei 14.133/2021 — compras e
  outros serviços. Limite 2026: **R$ 65.492,11** (Decreto nº 12.807/2025).
- **Vedação ao fracionamento**: art. 75, **§ 1º** — o limite é aferido pelo
  somatório do exercício da unidade gestora e da despesa com objetos de mesma
  natureza (verificar outras contratações do exercício antes de despachar).
- **Consórcio público**: art. 75, **§ 2º** — limites **duplicados** (serviços:
  R$ 130.984,22; não confundir com o teto simples de engenharia, R$ 130.984,20).
  Montar consórcio não cabe na janela 2026; o TR já nasce modular para caber
  quando couber (escopo por aderente, preço unitário por imóvel).
- **Divulgação no PNCP**: art. 176 — os atos da contratação direta devem ser
  publicados no Portal Nacional de Contratações Públicas.
- **Dotação usual**: 3.3.90.39 (Outros Serviços de Terceiros – Pessoa Jurídica),
  dentro de Outras Despesas Correntes — **confirmar a classificação na LOA do
  município**.

## O passo a passo (o que o município faz, em ordem)

| Passo | Quem | Prazo sugerido | O quê |
|---|---|---|---|
| 1 | Secretaria de Fazenda/Planejamento | dia 0 | Assinar a **declaração de necessidade** (modelo anexo) e indicar gestor do contrato |
| 2 | Setor de compras | dia 0–2 | Juntar: TR (anexo), estimativa de preço (3 propostas de fornecedores — a nossa proposta serve como uma), comprovação de dotação (empenho previsto) |
| 3 | Jurídico | dia 3–7 | Parecer jurídico sobre a dispensa (art. 75, II), o TR e a aplicação do **aviso do art. 75, §3º** conforme regulamento municipal |
| 3.5 | Setor de compras | +3 dias úteis | **Aviso de intenção de dispensa (art. 75, §3º)** em sítio oficial: objeto especificado + manifestação de interesse em propostas adicionais; seleciona-se a mais vantajosa. "Preferencialmente" na lei — vários municípios/TCEs tratam como obrigatório: **verificar o regulamento municipal por alvo (item de qualificação de lead)** |
| 4 | Ordenador de despesa | dia 7–10 | **Decisão de dispensa** (minuta anexa), publicar no PNCP e no site oficial |
| 5 | Contratada × Município | dia 8–10 | Assinatura do contrato/termo (prazo de 5 dias úteis da decisão, quando houver pregão — em dispensa, segue o regulamento local) |
| 6 | Contabilidade | **até 10/12** | **Empenho** (nota + liquidação conforme cronograma físico do TR) |

## Calendário da janela (para contratação com empenho em 2026)

- **até 12/11**: aviso de dispensa publicado (art. 75, §3º, +3 dias úteis)
- **até 20/11**: decisão de dispensa assinada
- **até 30/11**: contrato assinado + processo no PNCP
- **até 10/12**: empenho emitido (evitar a quinzena final — guerra de restos a pagar)
- O que escorregar para 2027 depende da LOA — perder 1–2 trimestres.

## Dispensa ÚNICA vence (decidido pelo calendário, não pelo jurídico)

Duas contratações encadeadas exigem 2 ciclos de processo em 3 semanas de fim de
exercício — o jurídico de prefeitura pequena não gira, e a conformidade cairia na
LOA 2027. **Oferta principal = pacote único (R$ 15–33 mil com manutenção)**;
laudo isolado é fallback para município sem dotação (TR alternativo no arquivo 02).

## O aviso público expõe o objeto — e é assim que deve ser

O aviso do §3º torna o objeto "conformidade CIB/CADURB" público antes da
contratação: é o sinal que aciona a vigilância da incumbente (Foxinline). Não é
motivo para evitar — é motivo para chegar preparado: **proposta de referência
pronta**, diferencial técnico explícito no TR (metodologia publicada, pin de
versão da spec oficial, vocabulário oficial de falhas) e preço fundamentado na
estimativa. Ganhar a disputa uma vez valida o produto para os 152.

## Regra de ouro do objeto (herdada do plano)

O contrato separa **obrigação** de **marco condicionado**:
- **Obrigação (prazo nosso)**: entregar o Laudo de Completude em até 15 dias
  úteis do recebimento do export do cadastro.
- **Marco condicionado (sem data prometida)**: apoio à remessa ao CADURB —
  depende da **adesão do próprio município** ao convênio Sinter (Termo de Adesão
  assinado por representante legal com certificado), ato fora do nosso controle.
  Critério de aceite deste marco: *remessa aceita em homologação OU relatório
  técnico de impedimento*.

## ⚠️ Cashback: MORTO para ente público — os três efeitos migram

Devolução condicionada a contrato futuro = desconto irregular em contratação
pública. Substitutos com os mesmos efeitos:

| Efeito do cashback | Substituto |
|---|---|
| Filtro de compromisso | empenho único de R$ 15–33 mil — filtra mais que R$ 4 mil reembolsáveis |
| Risco devolvido ao cliente | **mini-diagnóstico de 72h** sobre o export, na pré-venda, sem custo |
| Âncora de preço intacta | **desconto formal na estimativa**, nunca devolução |

E o "programa piloto de 10 vagas" deixa de ser promoção e vira **declaração de
capacidade física** (2 contas/mês) — mais difícil de contestar, auditável.

## Conteúdo do pacote

- `01-fichas-8-municipios.md` — alvos priorizados (sinal RREO) com dados de contexto
- `02-termo-referencia-modelo.md` — TR pronto (obrigação × marco condicionado)
- `03-minuta-decisao-dispensa.md` — minuta da decisão do ordenador
- `04-declaracao-necessidade.md` — declaração da secretaria solicitante
