# Metodologia dos Indicadores e do IV — v2 (set/2026)

**Estado:** bloqueante resolvida (M0 item 3). Substitui as regras de métrica
anteriores, incluindo a regra caduca "n ≥ 50 **faces**" — o universo agora é
**n ≥ 50 domicílios**. Implementada em `painel-gerencial/build_dados.py` e
refletida no painel regenerado.

## 1. Fontes (todas públicas, baixadas em `dados/bruto/`)

| Tema | Arquivo | Uso |
|---|---|---|
| Domicílios/moradores | CD1 por bairro (V00001, V00005) | denominadores, universo |
| Água e esgoto | CD2 por bairro (V00111, V00309) | saneamento |
| Entorno urbanístico | Entorno por bairro (V0500x) | pavimentação, iluminação, calçada, rampa, bueiro, ônibus, arborização |
| Demografia | Demografia por bairro (V010xx) | idosos 60+ (V01040+41), crianças 0–14 (V01031+32+33) ÷ V01006 |
| Renda | Renda do responsável (V06004 média, V06006 mediana) | perfil socioeconômico |
| Geometria | Malha de bairros CD 2022 (SHP) | mapa |

## 2. Regras de cálculo (as correções)

1. **Entorno — denominador sem "não declarado"**: % = SIM ÷ (SIM + NÃO).
   - Pavimentação: `V05006/(V05006+V05007)`; Iluminação: `V05012/(V05012+V05013)`;
     Calçada: `V05021/(V05021+V05022)`; Rampa: `V05027/(V05027+V05028)`;
     Bueiro: `V05009/(V05009+V05010)`; Ponto de ônibus: `V05015/(V05015+V05016)`.
   - **Errata v1:** usávamos `SIM/V05000`, incluindo "não declarado" no denominador
     (subestimava o indicador). Efeito pequeno em Teresina (não declarado ≈ 0),
     mas a regra correta é esta e vale para qualquer município.
   - Arborização permanece `V05030/V05000` (face **sem** árvores — não há par SIM/NÃO).
2. **Renda — mediana (V06006) é o indicador principal**; a média (V06004) fica como
   secundária. Motivo: robustez a cauda direita (ex.: Tabajaras, média R$ 16.629 ×
   mediana muito inferior; Por Enquanto: média R$ 3.065 × mediana R$ 1.502 — a
   mediana descreve melhor o morador típico do bairro).
3. **Água/esgoto**: % de domicílios ocupados ligados à rede (V00111/V00001; V00309/V00001).
4. **Universo**: bairros com **n ≥ 50 domicílios ocupados** (propriedade `n_ok` no
   geojson; 121 dos 123 de Teresina passam). Bairros abaixo ficam marcados e podem
   ser excluídos da análise — regra que substitui a caduca "n ≥ 50 faces".

## 3. Índice de Vulnerabilidade (IV)

Não há índice sintético com pesos arbitrários. O painel usa **agrupamento k-means
(k=3, 40 iterações, sementes fixas)** sobre 4 dimensões normalizadas por min–max:
`[renda_mediana (invertida), esgoto, pavimentação, iluminação]`. Os grupos são
ordenados por carência média ponderada por domicílios e rotulados
prioridade alta/média/baixa. Vantagens: sem peso inventado; reproduzível;
rastreável (cada bairro aponta o grupo e os valores que o colocaram lá).
Limitação documentada: k-means assume clusters convexos; com k=3 fixo perde
nuance. Quando houver série temporal, reavaliar contra cortes fixos.

## 4. Médias municipais

Sempre **ponderadas por domicílios ocupados** (não média simples de bairros).

## 5. Arquivos correspondentes

- `painel-gerencial/build_dados.py` — ETL idempotente que aplica estas regras
  (entrada: `dados/bruto/ibge/*.zip`; saída: `teresina_full.geojson`).
- `painel-gerencial/index.html` — painel com mediana como principal e
  denominadores corrigidos (v2).
- `dashboard-demo/index.html` — demonstração v1 (métricas antigas); mantida
  apenas como artefato de apresentação; **usar o painel-gerencial como referência**.

---

## 6. Adendos da fusão (17/09/2026)

Esta seção foi **acrescentada** quando o pacote da sessão ZCode entrou nesta
árvore. Nada acima foi alterado; o que segue corrige caminhos e acrescenta duas
regras que a v2 não tinha.

### 6.1 Caminhos (a §5 vale, com estes nomes)

| Na v2 | Nesta árvore |
|---|---|
| `painel-gerencial/build_dados.py` | **`painel/build_dados.py`** — mesmo método, generalizado por município |
| `painel-gerencial/index.html` | **`painel/index.html`** — painel unificado (estado + município) |
| `dashboard-demo/index.html` | não promovido; a demonstração v1 fica em `tmp/sessao-zcode/painel/` como arquivo morto |

### 6.2 O universo do entorno não é o universo do domicílio — `n_ok_ent`

`V05000` é *"domicílio em setor **escolhido** para aplicação do entorno"*, não o
total de domicílios do bairro. O corte `n ≥ 50` da §2.4 é válido para renda, água
e esgoto (denominador `V00001`), mas **os indicadores de entorno precisam do seu
próprio corte**, sobre `V05000`.

Medido no Piauí inteiro (**479 bairros** na malha CD 2022, dos quais 477 com
contagem de domicílios): a cobertura mediana `V05000/V00001` é **1,0** —
praticamente total, como a v2 supunha. Mas o corte separa casos reais:

| Bairro | Domicílios (V00001) | Universo do entorno (V05000) |
|---|---|---|
| Rudiador | 95 | **3** |
| Pedreiras | 85 | **36** |

**Oito bairros passam em `n_ok` e falham em `n_ok_ent`**, e outros **18 não têm
registro nenhum de entorno**. Sem o segundo corte, esses bairros entram no
ranking de pavimentação com uma amostra de três domicílios. O geojson passa a
carregar `n_ent`, `n_ok` e `n_ok_ent`, e o painel usa o corte certo para cada
indicador — inclusive em ponto de ônibus e arborização, que não aparecem na
barra de indicadores mas vêm do mesmo universo.

**Contagens do Piauí, para conferência:** 479 bairros · 2 sem `V00001` ·
20 com `n_ok = 0` · 28 com `n_ok_ent = 0` · 18 sem registro de entorno.

### 6.3 A cor tem direção, e a direção é declarada

Duas paletas, porque são duas leituras diferentes:

- **carência** (renda, esgoto, água, pavimentação, iluminação, calçada): o
  **primeiro quintil é vermelho**. É o que o painel existe para achar.
- **magnitude** (IPTU, ITBI, RCL, contagens): rampa de um tom só, do escuro ao
  claro. Ali "pouco" **não** é "ruim" — município com IPTU baixo é o alvo do
  Segmento B, não um problema a corrigir.

A versão anterior do mapa pintava o primeiro quintil de verde para todos os
indicadores, o que fazia o mapa de renda de Teresina aparecer com o centro rico
em vermelho — legível como emergência exatamente onde não há nenhuma.

### 6.4 Legenda sem classe vazia

Com empate de quintil — em Teresina a mediana de renda é o salário mínimo em
metade dos bairros — duas quebras coincidem e uma classe fica sem nenhum bairro.
A legenda passa a omitir a classe vazia e a mostrar a contagem de cada faixa.
Mostrar uma faixa que não contém nada é inventar variação que o dado não tem.

### 6.5 Ordenação dos grupos do k-means

A §3 ordena os grupos "por carência média ponderada por domicílios". A
implementação anterior ponderava **só pela renda**, e o resultado rotulava como
*prioridade alta* um grupo cujo esgoto era melhor que o do grupo *prioridade
média* — o rótulo contradizia os números impressos abaixo dele. A carência passa
a ser a média das **quatro** dimensões normalizadas.

---

## 7. CNEFE 2022 — o volume da remessa (17/09/2026)

O **Cadastro Nacional de Endereços para Fins Estatísticos** do Censo 2022 traz,
por município, os endereços que o recenseamento enumerou. No Piauí:
**1.891.421 endereços, nenhum sem coordenada** (97,6% no melhor nível de
geocodificação). Campos: tipo e nome de logradouro, CEP, número, setor, quadra,
face, latitude, longitude, espécie e tipo de edificação.

### 7.1 O que é e o que não é

É o **volume** que a remessa ao CADURB tem de cobrir, e é a unidade em que o TR
mede preço-teto (R$/imóvel × volume do cadastro). **Não é** cadastro imobiliário:
não tem inscrição, titular nem geometria de lote. Serve para medir a distância
até o cadastro do município — não para substituí-lo.

### 7.2 O corte por bairro é geométrico, não por código

O CNEFE referencia **setores de coleta**; os agregados do Censo usam **setores de
divulgação**. Juntar pelos códigos perde **10,4%** dos endereços do Piauí. Por
isso `painel/build_cnefe.py` faz ponto-em-polígono sobre a malha oficial de
bairros. Como bairro é recorte urbano, a contagem por bairro é a contagem urbana;
o que cai fora aparece como *fora da malha de bairros*, sem classificação
inventada.

### 7.3 A aferição que dá confiança ao número

Teresina transmitiu **363.805** inscrições CIB ativas. O Censo enumerou
**371.548** endereços dentro da malha de bairros do município. São **97,9%** —
o que sustenta usar a contagem do CNEFE como estimativa do tamanho da remessa em
municípios que ainda não transmitiram nada.

| Município | Endereços | Domicílios particulares | Em bairro |
|---|---|---|---|
| Teresina | 415.723 | — | 371.548 |
| Altos | 26.166 | 20.923 | 16.517 |
| Bom Jesus | 15.911 | 12.147 | 11.791 |
| N. Sra. de Nazaré | 3.359 | 2.231 | sem malha de bairros |
| Guaribas | 2.414 | 1.943 | sem malha de bairros |

### 7.4 Tema claro

O painel passou a ter os dois temas. Toda cor — inclusive as duas rampas do mapa
e as cores de eixo dos gráficos — vira **token de CSS**, lido pelo JavaScript em
tempo de desenho. Não existe paleta de CSS e outra de JavaScript. A escolha do
leitor fica no `localStorage`; sem ele, o painel segue o tema do sistema.

---

## 8. Marca aplicada (18/09/2026)

O projeto passou a se chamar **Vertical Data** e ganhou system design próprio
(`marca/README.md`). Para a leitura das telas, o que importa é o que **não**
mudou:

- **A direção das rampas é a mesma.** CAR segue divergente com o 1º quintil
  vermelho; MAG segue de matiz único, porque IPTU baixo é o alvo comercial e não
  um problema. Trocou o matiz da MAG — era verde, virou o teal da marca.
- **Ausência de dado continua em família própria**, agora `#C6CED6` no claro e
  `#34404E` no escuro: cinza frio, fora das duas rampas. Os 72 municípios sem
  RREO 2025 continuam legíveis como *sem dado*, nunca como valor baixo.
- **Os cortes de amostra (`n_ok`, `n_ok_ent`) não foram tocados.**

O que mudou de fato: o par de tons que carrega texto. O teal da marca
(`#12B0A0`) tem 2,71:1 sobre branco e só é usado como **preenchimento**; texto,
link e foco usam `#0D8478` (4,58:1) no claro e `#2FD5C0` (8,35:1) no escuro. A
tabela de contraste medido está em `marca/README.md` §2.
