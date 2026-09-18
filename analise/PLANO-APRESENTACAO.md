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
