# Rodada 9 — REVISÃO DE PLANO. Eixo negócio/risco. Responda AGORA, direto ao ponto.

## Situação

Produto: conformidade com o art. 266 da LC 214/2025 — todo imóvel urbano inscrito no CIB até
**31/12/2026**. Faltam ~105 dias. Mercado: 224 municípios do Piauí, dos quais 194 arrecadam
menos de R$ 100 mil de IPTU ao ano (para esses o CIB não é receita, é sobrevivência cadastral).
O que se vende é a **remessa aceita no CADURB**, não um painel.

Já existe um painel com dado público real (Censo 2022 por bairro, CNEFE com 1,89 mi de
endereços, RREO/SICONFI, RFB/Sinter), publicado com senha. Ele tem dois papéis: vitrine e
instrumento de qualificação. Não é o produto.

**Um protótipo anterior quase queimou o projeto:** usava dado fictício e dizia que o bairro
Mocambinho tinha 36% de pavimentação. O real é 99,6%. Qualquer gestor de Teresina identifica
em segundos. Desde então vale a regra: *nenhuma tela com dado fictício em bairro nomeado*.

## O pedido

Um parceiro comercial viu o painel e pediu: **"tem como colocar as possibilidades com dados
imaginários?"** — ele quer ver as seis capacidades que foram congeladas (simulador de
investimento, status da remessa, educação, PGV, ML/chat, série histórica).

## O que decidi

**Dois regimes.**
- **Projeção**: parte de número medido e projeta com parâmetros visíveis e editáveis na tela.
  Roda em município **real**. Exemplo: simulador de investimento sobre Teresina (esgoto 32,2%
  é Censo; o resto é aritmética declarada).
- **Maquete**: afirma um estado presente que ninguém mediu. Roda só em município **inventado**
  — "Serra do Meio", código IBGE 2299999, impossível por construção. Exemplo: status da
  remessa, série histórica, PGV.

**Fronteira:** faixa persistente que sobrevive a recorte de 360px, rótulo "município-modelo"
no seletor e no rodapé, marcação no próprio número (não só rodapé), rota `?demo` separada.

**Plateia decidida:** só o parceiro, para validar a ideia. Não é material de venda.

**Sobre IA:** medi que há base real para um modelo de risco de não-entrega (RREO 2023/24/25 dá
desfecho observado: 152 entregaram, 72 não). Isso deixa de ser demonstração e vira produto —
devolve a lista de quem ligar primeiro. Chat desenhado para que o modelo escolha a consulta e
o número venha sempre do arquivo.

## Responda no máximo 6 achados, só o que muda a decisão

1. **O regime duplo é engenhoso demais?** Município real e município inventado convivem no
   mesmo seletor. O parceiro — e quem ele encaminhar — vai distinguir, ou vou reproduzir
   Mocambinho com outra roupa?
2. **"Só o parceiro" é premissa estável?** Ele pediu para mostrar possibilidades; é plausível
   que o destino final seja uma prefeitura. Devo desenhar já para a plateia pior?
3. **Demonstrar capacidade congelada cria promessa comercial?** O painel diz hoje, por escrito,
   que essas seis coisas estão fora da v1 com motivo declarado. Se eu demonstro a forma delas,
   crio expectativa que o contrato não cobre — com risco de virar obrigação implícita?
4. **Simulador de investimento.** Foi congelado por falta de custo unitário auditável. Minha
   mitigação é deixar o custo como parâmetro visível e editável. Isso basta comercialmente, ou
   o gestor vai ler a saída como previsão de qualquer jeito? Vale buscar custo unitário
   publicado (SNIS, PAC, Funasa) para virar referência declarada?
5. **Prioridade, com 105 dias de janela.** Vale gastar 4 dias nisso agora? O que eu deveria
   estar fazendo em vez disso — ou o que dentro do plano deveria ser cortado?
6. Qualquer risco comercial ou jurídico que eu não listei.
