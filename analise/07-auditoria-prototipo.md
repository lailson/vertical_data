# Auditoria do protótipo `painel-gestao-municipal (1).html`

43.163 bytes, sendo 18.721 de JavaScript. Auditado campo a campo e confrontado com dado real.

## 1. Estrutura

11 telas: Painel principal, Mapa territorial, Ranking de bairros, Saneamento, Pavimentação,
Educação, Perfis socioeconômicos, Simulador de investimento, Séries históricas, Status CERURB,
Relatórios exportáveis.

Funções existentes — **todas de apresentação**: `buildMiniMap`, `renderBigMap`, `buildRankMini`,
`colorFor`, `colorForInverse`, `fmtPct`, `prioTag`, `goToPage`, `runSimulation`, `xFor`, `yFor`.
**Nenhuma função de cálculo de indicador.**

## 2. O modelo de dados: 18 registros, 17 campos

```
{nome, iv, saneamento, pavimentacao, evasao, escolas, distEscola, matriculas,
 familias, renda, moradores, idosos, criancas, posse, pendentes, analise, regularizados}
```

| Campo | Domínio no protótipo |
|---|---|
| `iv` (índice de vulnerabilidade) | 9 a 88 — **sem fórmula em lugar nenhum** |
| `saneamento` | 24% a 96% |
| `pavimentacao` | 31% a 96% |
| `evasao` | 1,9% a 14,2% |
| `renda` | "até 1 SM", "1–2 SM", "2–3 SM", "3+ SM" |
| `posse` | Posseiro, Proprietário, Proprietário informal, Cessão |
| `idosos`, `criancas` | booleanos (!) |
| `familias` | 40 a 212 |
| `pendentes` / `analise` / `regularizados` | 0–64 / 1–60 / 39–90 |

## 3. Problema 1 — o indicador central não tem metodologia

O `iv` ordena o ranking, colore o mapa, define as faixas de prioridade (alta/média/baixa) e alimenta
o simulador de investimento. **Ele é um número digitado à mão.** Não há pesos, não há fontes, não há
reprodutibilidade.

Num produto que ordena prioridade de investimento público, isso é passivo contratual: basta um
vereador cujo bairro ficou em último, ou o controle interno, perguntar "como calcularam" — e não há
resposta. **Definir a metodologia do índice é item de escopo, não detalhe de implementação.**

## 4. Problema 2 — os dados fictícios contradizem a realidade, e isso é detectável na hora

Os 18 nomes **são bairros reais de Teresina**. Cruzei com a base do IBGE: **13 casam diretamente**,
2 por variante de grafia (Renascença, Horto) e **3 não são bairros oficiais** (Vila Irmã Dulce,
Vila Nova do Alto da Ressurreição, Parque Piauí) — são vilas/comunidades dentro de bairros.

Confrontando o protótipo com o dado real do Censo 2022 (entorno urbanístico por face de quadra):

| Bairro | Pavimentação no protótipo | **Pavimentação real** | Erro |
|---|---|---|---|
| Mocambinho | 36% | **99,6%** | protótipo diz que é o 2º pior; é dos melhores |
| Santa Luzia | 41% | **78,6%** | subestimado |
| Todos os Santos | — | 62,1% | — |
| Centro | — | 100,0% | — |

E os bairros **realmente** carentes de pavimentação em Teresina — Chapadinha (36,7%), Tabajaras
(36,8%), Brasilar (44,8%), Morros (46,0%), Verdecap (46,9%) — **não aparecem no protótipo.**

**Risco imediato:** qualquer gestor de Teresina que olhe esse painel reconhece que Mocambinho não é
bairro sem pavimentação. O protótipo, apresentado como está, destrói credibilidade na primeira
reunião. Ele precisa ou ser rotulado explicitamente como maquete visual, ou ser repopulado com dado
real antes de qualquer apresentação.

## 5. Problema 3 — a divisão territorial não corresponde a nenhuma base oficial

Teresina tem **123 bairros** (IBGE, Censo 2022). O protótipo usa 18, misturando bairros oficiais com
comunidades. Isso impede junção com qualquer fonte e precisa ser decidido antes de construir:
o recorte é bairro oficial (123), comunidade/núcleo informal, ou setor censitário?

## 6. Problema 4 — campos com tipo inadequado

`idosos: true/false` e `criancas: true/false` tratam presença de idosos e crianças como booleano por
bairro. Não existe bairro sem crianças. O dado correto é **proporção** (o Censo dá por bairro), e o
uso pretendido provavelmente era "concentração acima da média" — o que é outra coisa e precisa de
definição.

## 7. O que o protótipo acerta e deve ser preservado

- **A arquitetura de navegação** (11 telas) é adequada e cobre o módulo 4 da proposta.
- **A escolha de indicadores** é pertinente: saneamento, pavimentação, educação, perfil
  socioeconômico, posse e status de regularização são de fato os eixos certos.
- **O simulador de investimento e os relatórios exportáveis** são diferenciais reais frente a um
  dashboard passivo — mas o simulador precisa de modelo por trás, não de regra ad hoc.
- Como **peça comercial e especificação visual**, cumpre a função.

## 8. Veredito técnico

**O protótipo é uma maquete de interface de boa qualidade, com dados inventados que não sobrevivem
ao confronto com a realidade.** Não serve como base de código (HTML estático, array hardcoded, sem
camada de dados), mas serve como especificação de produto.

**Ação recomendada, em ordem:**
1. Repopular com dado real do IBGE por bairro — **é factível hoje**, os dados existem e foram
   baixados nesta análise (pavimentação, iluminação, bueiro, domicílios, demografia por bairro).
2. Definir e publicar a metodologia do `iv` (pesos, fontes, fórmula).
3. Substituir a grade de células por geometria real (malha de bairros do IBGE + PostGIS).
4. Adotar os 123 bairros oficiais, com camada separada para comunidades/núcleos informais.
5. Adicionar a métrica ausente e mais importante: **arrecadação** (SICONFI, já validado).
6. Até que 1–4 estejam feitos, marcar toda tela com "dados ilustrativos" de forma inequívoca.

## 9. Mapa de cada indicador do protótipo para sua fonte real

| Indicador do painel | Fonte real | Granularidade | Status |
|---|---|---|---|
| Pavimentação | **Censo 2022 — entorno, V05406/V05400** | **bairro** | ✅ pronto |
| Iluminação pública | **Censo 2022 — entorno, V05412** | **bairro** | ✅ pronto |
| Drenagem (bueiro) | Censo 2022 — entorno, V05409 | bairro | ✅ pronto (não está no protótipo) |
| Saneamento (água/esgoto) | Censo 2022 — características do domicílio | bairro | ✅ pronto |
| Densidade, moradores/domicílio | Censo 2022 — demografia/básico | bairro | ✅ pronto |
| Idosos e crianças (proporção) | Censo 2022 — demografia | bairro | ✅ pronto |
| **Renda** | Censo 2022 — Rendimento do Responsável | **só setor censitário** | ⚠️ agregar setor→bairro |
| Escolas, matrículas, distância | INEP Censo Escolar (escola geolocalizada) | ponto → bairro | ✅ pronto |
| Evasão / rendimento escolar | INEP (distorção idade-série, IDEB) | escola | ✅ pronto |
| Energia solar / GD | ANEEL (diário) | município | ⚠️ não desce a bairro |
| **Arrecadação (ausente)** | SICONFI / TCE-PI | município | ✅ validado |
| Núcleos informais / favelas | **Censo 2022 — Favelas e Comunidades Urbanas (vetorial)** | **polígono** | ✅ pronto |
| Status CERURB (regularizados/pendentes) | CERURB | imóvel | ❌ depende de acordo |
| Tipo de posse | CERURB ou coleta própria | imóvel | ❌ depende de acordo |
| Valor venal / PGV | cadastro da Fazenda municipal | imóvel | ❌ via contrato |

**Dos 15 indicadores, 11 são obteníveis hoje com dado aberto.** Só 4 dependem de acordo — e são
exatamente os do núcleo fundiário e fiscal.
