# Método canônico ITBI/IPTU — veredito e regras de uso (16/09/2026)

**Objetivo do item A:** fixar UM método para a linha de R$/município do deck,
auditável por um secretário de fazenda.

## Veredito

**Adotar como canônico o portal SICONFI (consulta "Receitas e despesas dos entes",
classificação por natureza RREO: IPTU 1.1.1.2.1.01 · ITBI 1.1.1.2.1.02)** — o mesmo
método da tabela original (Teresina R$ 166,3/60,8 mi; Cocal 3,28×; Floriano 1,76×…).
É a classificação com que os municípios reportam ao Tesouro e a que o TCE confere.

## Por que NÃO usar a soma direta da API MSC (o campo minado, documentado)

Tentativas reproduzíveis (todas salvas; scripts e dumps em `/tmp` e resumo em
`dados/fiscais-itbi-iptu-mscc.json`):

| Método | Teresina IPTU | Teresina ITBI | Problema |
|---|---|---|---|
| Portal SICONFI (referência, outra sessão) | R$ 166,3 mi | R$ 60,8 mi | método canônico |
| MSCC classe 6, soma 12 meses, códigos 1121.01xx/02xx | R$ 71,7 mi | R$ 44,9 mi | ~43% da referência |
| MSCE period_change | R$ 53,3 mi | R$ 31,2 mi | terceiro valor distinto |

E o defeito que invalidaria um deck: **sob códigos 112102xx, Floriano, Corrente,
Cocal e Altos aparecem com ITBI = R$ 0** (dump de naturezas salvo) — nesses
municípios o ITBI é lançado em outros códigos (fundos/variantes), e a soma ingênua
também arrasta códigos 1.7.x com valores absurdos (Cocal "R$ 114 mi" numa única
natureza — contaminação de categorias). **O insight ITBI>IPTU no interior**
sobrevive direcionalmente (Bom Jesus 2,08× no meu método × 1,73× no deles; Teresina
0,63 × 0,37), mas os valores absolutos da API crua NÃO vão para o deck.

## Regras de uso (deck e reuniões)

1. Números de IPTU/ITBI citados = **export do portal SICONFI** (ou TCE-PI, quando
   conferir), com fonte datada no rodapé do slide.
2. **Nunca misturar** valor de portal com valor de API na mesma tabela.
3. Se automação for necessária (224 municípios): capturar o endpoint real que o
   portal web usa (aba Network do navegador — tarefa de browser) e validar 3
   municípios contra o export manual antes de qualquer uso.
4. Validação de sanidade antes da reunião: IPTU de Teresina 2025 na casa de
   R$ 100–200 mi; ITBI nunca zero em município com cartório ativo.

## Estado dos artefatos

- `dados/fiscais-itbi-iptu-mscc.json` — os 6 municípios pelo método MSCC (mantido
  como evidência da divergência, não para uso comercial).
- API TCE-PI quebrada com sucesso (rotas `/prefeituras` e `/receitas/{id}/{exercicio}`
  extraídas do bundle) — mas o endpoint de receitas só devolve top-10 transferências
  por UG/exercício: serve para qualificação (quem reporta ao TCE), não para IPTU/ITBI.

## Pendência que nasceu daqui

Automatizar o export do portal (browser capture) OU validar manualmente os 6
números (30 min) antes do deck. Recomendo: **manual para o deck de nov–dez,
automação depois**.
