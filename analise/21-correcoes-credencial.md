# Correções concretas — credencial técnica e dossiê

Lista de substituições prontas. Cada linha é "trocar X por Y", com o motivo.

## A. Credencial — o que está prometido além do entregue

| # | Como está | Como deve ficar | Por quê |
|---|---|---|---|
| 1 | Painel de gestão territorial com dado real — 123 bairros | **manter como está** | é verdade e verificável ao vivo |
| 2 | "Conector CADURB — **pronto para operar** assim que o município adere" | **"Conector alfanumérico gerado da especificação OpenAPI pública da RFB; pendente de homologação contra cadastro real. Fluxo de geometria fora do escopo atual."** | os dois fluxos (alfanumérico e geometria por lote+vinculação) não estão cobertos, e a spec `0.0.1-SNAPSHOT` não tem teste de divergência |
| 3 | "Laudo de Completude Cadastral — **produto** de diagnóstico" | **"Laudo preliminar de completude (validação alfanumérica); regras semânticas em implementação."** | hoje é validação sintática; o que justifica o preço são as regras semânticas |
| 4 | "Metodologia publicada — **sem índices de pesos arbitrários**" | **"Ranking oficial baseado em cortes fixos e pesos declarados; agrupamento estatístico usado apenas como análise exploratória interna."** | k-means não elimina arbitrariedade — k, semente e normalização min–max da amostra são escolhas implícitas que mudam com a entrada |
| 5 | Dossiê de contratação pronto | **manter como está** | existe e está bom |

**O item 4 é o mais urgente.** "Sem pesos arbitrários" dito a um secretário e depois desmentido por
um assessor técnico é o pior tipo de erro comercial: destrói a credencial inteira, porque sugere que
as outras quatro afirmações também não foram verificadas.

## B. Dossiê — correções jurídicas

| # | Como está | Como deve ficar |
|---|---|---|
| 1 | "Vedação ao fracionamento: **art. 75, § 2º**" | **"art. 75, § 1º"** — e acrescentar: *"§ 2º: os limites são dobrados para contratações por consórcios públicos — via APPM, o teto passa a R$ 130.984,22"* |
| 2 | Limite R$ 65.492,11 | **manter** — verificado (Decreto 12.807/2025, IPCA-E 4,41%, vigente desde 01/01/2026) |
| 3 | Três contratações separadas | **acrescentar seção "somatório do exercício"**: declarar que laudo + conformidade + painel somam R$ 19–38 mil, cabem no limite, e que o laudo é o **estudo técnico preliminar** que fundamenta o escopo do segundo contrato |
| 4 | Tabela de oferta: "Conformidade — … + **remessa aceita em homologação** (marco condicionado)" | **"Conformidade — saneamento cadastral, integração e apoio à remessa; entrega condicionada à adesão do município ao convênio Sinter. Aceite: remessa aceita em homologação ou relatório técnico de impedimento."** |

## C. "Por que agora" — reescrito com o que foi verificado

Como está, apoia-se em dois números não confirmados e numa interpretação apresentada como norma.
Versão que usa só o verificado:

> **Por que agora.** O art. 266 da LC 214/2025 fixa **31/12/2026** como prazo para os municípios
> integrarem o cadastro imobiliário ao CIB. A Receita Federal é explícita quanto à consequência:
> *"municípios cujos imóveis não possuem inscrição no CIB não receberão repasses do IBS"*, e
> *"imóveis sem CIB terão problemas em transações e regularização"*.
>
> Isso atinge a receita que o município já tem hoje — e não apenas a futura. **Em boa parte do
> interior do Piauí o ITBI supera o IPTU**: em Floriano o ITBI é 1,8× o IPTU, em Bom Jesus 1,7×, em
> Corrente 1,6×, em Cocal 3,3× *(SICONFI/RREO Anexo 03, exercício 2025)*. **ITBI depende de
> transação, transação depende de registro, e registro depende do CIB.**
>
> O convênio com a Receita é **gratuito** e a API é **aberta e documentada**. O que falta ao
> município é o cadastro que ela aceita — e é isso que entregamos.

Três ganhos sobre a versão anterior: (1) cita a norma pela formulação oficial; (2) substitui números
não verificados por dados extraídos e conferíveis, com fonte e exercício; (3) liga a exigência à
**receita corrente** do município, que é mais concreto que repasse futuro de IBS.

**Se os números do Sinter forem confirmados** (adesões no PI, 188 no Brasil), acrescentar como
reforço — com data de consulta no rodapé. Sem confirmação, não entram.

## D. Conjunto mínimo de regras para o laudo valer R$ 3–5 mil

Em ordem de valor ÷ esforço:

1. **Unicidade de `inscricaoImobiliaria`** — o erro mais comum de cadastro em planilha
2. **Cobertura por campo e por bloco obrigatório** — a métrica-título do laudo
3. **Tabelas de domínio da seção 9** do manual, versionadas
4. **Dígito verificador** de CPF/CNPJ e CIB (`CAMPO_COM_DV_INVALIDO` existe no vocabulário oficial)
5. **Coerência `tipoImovel` × `areaConstruida` / `tpArquitetonico`** — territorial com área construída
   **não recebe CIB**, é regra explícita do manual
6. **`anoConstrutivo` ≤ ano corrente** e **`areaTerreno` > 0**
7. Soma de `percTitularidade` e `percTransacionadoITBI` = 1,0
8. CEP existe e pertence ao município

**Sem os itens 1 a 6, continua um `required`-checker** — e aí o preço não se sustenta.

## E. Estrutura do relatório (o `TipoFalhaDTO` é necessário, não suficiente)

Três camadas:
- **(a)** legenda oficial por erro, usando os rótulos exatos do `TipoFalhaDTO`
- **(b)** agrupamento por bloco / campo / regra, com incidência absoluta e percentual
- **(c)** sumário executivo com as **top falhas impeditivas da remessa** — que é a página que sobe
  ao prefeito

## F. O risco que sobra, e como fechá-lo antes da primeira venda

Nenhum cadastro real passou pelo validador, e a spec não está pinada. **A primeira execução real
pode acontecer no cliente** — com o laudo divergindo da validação oficial e a remessa recusada em
homologação. É disputa contratual no primeiro contrato, que é o pior lugar possível.

Mitigação, antes de vender: rodar contra **um cadastro real** (os pilotos REURB são a fonte mais
provável) e **pinar a spec por hash com teste de divergência**. É o único item da lista que não pode
esperar a venda para ser resolvido.
