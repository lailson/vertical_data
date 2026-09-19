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

---

## 9. ANEEL — geração distribuída (18/09/2026)

Primeira base de energia no repositório. `painel/build_aneel.py` agrega
`dados/bruto/aneel/*.parquet` em `painel/dados/aneel.json`.

**Fonte:** ANEEL, *Relação de empreendimentos de micro e minigeração distribuída*,
licença **ODbL** — uso comercial permitido, com atribuição. Atualização **diária**;
4,6 milhões de linhas nacionais, **90.528 no Piauí**, todas fotovoltaicas.

**A junção.** A data de conexão **não** está no arquivo principal: está no de
informações técnicas fotovoltaicas, e casa por `CodEmpreendimento` →
`CodGeracaoDistribuida`. No Piauí casa **90.528 de 90.528**, e a `DatConexao`
coincide com `DthAtualizaCadastralEmpreend` em todos os registros.

**Três ressalvas que a tela precisa carregar, e carrega:**

1. **Município é o menor recorte _desta_ base.** O `CodCEP` existe, mas vem mascarado
   nos três últimos dígitos (`64066***`): sobra o prefixo de cinco, o mesmo recorte que já
   se usa para validar CEP.

   **Corrigido em 18/09/2026:** a afirmação valia para a base tabular e foi generalizada
   demais. O **SIGEL** publica camada de **pontos** de GD com `MdaLatitude`/`MdaLongitude`
   (`.../Geracao_distribuida/GD_Sigel/FeatureServer/0`). Medido: 71.558 pontos no PI,
   31.457 em Teresina, mediana de 6,6 km do centro. Mas as coordenadas vêm arredondadas em
   **duas casas (~1,1 km)**, ~0,9% estão grosseiramente fora do município declarado, e a
   cobertura é de **79%** contra a base tabular. Serve para **superfície de densidade**;
   atribuir ponto a bairro seria inventar precisão. Ver `analise/29-analise-fontes-propostas.md`.
2. **Atualização diária não é dado do dia.** A carga é de 18/09/2026 e a conexão mais
   recente é de **30/06/2026** — quase três meses de defasagem. Por isso o último ano
   da série aparece **tracejado e com marcador vazado**: lido como ano inteiro,
   pareceria retração de mercado.
3. **A queda de 2025 é real — e eu atribuí a causa errada primeiro.** A tela dizia que o
   vale era efeito da suspensão da ANEEL (23/09 a 13/11/2025, migração SISGD → MMGD).
   Medido depois: a suspensão derrubou **um mês** — outubro/2025 tem **300** conexões
   contra ~1.100 nos vizinhos. O ano inteiro caiu de **22.177 para 15.721 (−29%)**
   enquanto o **Brasil ficou estável** (909.303 → 906.480). É **perda de participação do
   Piauí**: de **2,44%** das conexões nacionais em 2024 para **1,73%** em 2025.
   Corrigido em 18/09/2026; a tela ganhou o gráfico de participação.

**Dado pessoal:** o arquivo traz `NumCPFCNPJ` e `NomTitularEmpreendimento` de cada
titular. Nenhum dos dois sai do `build_aneel.py` — a leitura seleciona coluna a
coluna e a saída é agregada por município.

**Cor.** A tela estreou os tokens `--vd-cat-1..5`, categóricos **de gráfico**, que não
são os de interface: o teal de texto (`--vd-acento`) tem cromo abaixo do piso e lê como
cinza num preenchimento, então o slot 3 usa o teal de forma. No tema escuro os passos
são **escolhidos**, não invertidos — a faixa de luminosidade para gráfico é L 0,48–0,67,
mais escura que a dos tokens de interface. Validado em faixa, cromo, separação sob
daltonismo e contraste, nos dois temas.

---

## 10. ANEEL — tarifas e BDGD (18/09/2026)

Duas fontes que entraram juntas, porque respondem à mesma pergunta por lados opostos:
quanto vale gerar, e quem tem carga para gerar.

### 10.1 Tarifas homologadas · `painel/build_tarifas.py`

Licença ODbL. Uma distribuidora responde por **99,65%** das conexões do Piauí —
**Equatorial PI** —, o que torna o cruzamento por município quase trivial.

**A armadilha do arquivo.** A mesma tarifa aparece duas vezes por subgrupo:

| `DscDetalhe` | o que é | B1 residencial convencional |
|---|---|---|
| `Não se aplica` | consumo comum | TUSD 647,22 + TE 299,47 = **R$ 946,69/MWh** |
| `SCEE` | regime de quem tem geração própria | TUSD 647,22 + TE 36,61 = **R$ 683,83/MWh** |

São **alternativas, não parcelas**. A primeira leitura somou as duas e produziu
R$ 1.630,52/MWh — um valor que não existe. O filtro correto exige `DscDetalhe`,
`NomPostoTarifario`, `DscModalidadeTarifaria`, `DscClasse` e `DscSubClasse` juntos.

**Payback não é calculado.** A Lei 14.300/2022 tem cronograma de transição do Fio B até
2029 e a regra varia com a data de conexão. Publicar retorno sem essa transição seria
inventar precisão — a tela mostra a tarifa e diz o que falta.

### 10.2 BDGD — unidades consumidoras PJ · `painel/build_bdgd.py`

Licença ODbL. É o que **desce abaixo do município com precisão de verdade**: cada
unidade traz **CEP completo** (não mascarado), **nome do bairro**, **coordenada com 8
casas**, CNAE, carga instalada, consumo mês a mês, e `CEG_GD` — se já tem geração.

No Piauí: **4.228 unidades em 197 municípios · 944 já com geração · 3.284 sem.**

**A ressalva que define o uso:** é só **pessoa jurídica em média e alta tensão**. Contra
as 90.528 conexões do estado, quase todas residenciais, isto é o mercado de
**minigeração** — comércio e indústria —, não o de telhado. A tabela de baixa tensão
(1,2 GB) também é só PJ: residência de pessoa física não é publicada, por privacidade.

**A diferença que eu declarei com a causa errada, e o que ela era de verdade.**
A primeira versão dizia "4.236 lidas, 4.230 agrupadas — 6 descartadas por erro de
formatação". Não era isso.

O agregador criava `CREATE VIEW` sobre `read_csv(..., ignore_errors=true)`. Um agregado
com `DISTINCT` faz o DuckDB **reexecutar o plano filho** — o CSV de 160 MB era varrido
**duas vezes**, e cada varredura descartava um conjunto ligeiramente diferente de linhas
malformadas. Dois municípios perdiam ~8% das unidades, e qual varredura alimentava qual
agregado era indefinido.

Corrigido com `CREATE TABLE`: uma leitura só, materializada. O resultado passou a ser
**4.228 unidades, estável entre execuções** (mesmo `sha256` do JSON em execuções
repetidas), e a conferência `lidas == agrupadas` virou **erro fatal** em vez de nota —
se divergir agora, é problema de verdade.

Vale registrar o padrão: é a segunda vez neste arquivo que eu publico uma **causa
plausível sem medir**. A primeira foi atribuir a queda de 2025 à suspensão da ANEEL.

### 10.3 Onde cada base desce

| base | menor recorte | ressalva |
|---|---|---|
| ANEEL MMGD (tabular) | município | CEP mascarado nos 3 últimos dígitos |
| SIGEL (pontos) | coordenada **~1,1 km** | 79% de cobertura, ~0,9% grosseiramente fora |
| BDGD (UC MT/AT) | **coordenada exata + bairro + CEP** | só PJ de média e alta tensão |

O residencial em massa continua sem recorte submunicipal publicado — e é por isso que a
tela não pinta geração por bairro.

---

## 11. A queda de 2025 é saturação, não fraqueza (18/09/2026)

Terceira leitura da mesma série, e a que finalmente tem base.

| leitura | quem disse | veredito |
|---|---|---|
| "o vale é efeito da suspensão da ANEEL" | eu, na primeira versão da tela | **errado** — a suspensão derrubou um mês (out/2025: 300 conexões contra ~1.100 nos vizinhos), não o ano |
| "é perda de participação, argumento de venda" | eu, na segunda versão | **incompleto** — verdadeiro como aritmética, mas sem causa |
| "é sinal de mercado fraco, alerta contra entrar" | revisor externo (qwen3-coder local) | **errado na premissa** |

O que decide entre as três é um número que ninguém tinha: a **penetração residencial
acumulada**, Piauí contra Brasil. Medida com o mesmo arquivo do IBGE que alimenta o
painel (`municipios_domicilio1_BR.zip`, V00001) e o parquet nacional da ANEEL:

| | domicílios | conexões residenciais | penetração |
|---|---|---|---|
| **Brasil** | 72.438.953 | 3.761.741 | **5,19%** |
| **Piauí** | 1.071.452 | 79.484 | **7,42%** |

**O Piauí está 43% acima da média nacional.** Não é um mercado fraco que ficou para trás
— é um mercado que adotou antes e mais rápido, e agora desacelera de uma base mais alta.
Isso é **saturação do segmento fácil**, não falta de demanda.

**Consequência comercial, e ela é o oposto da leitura do revisor:** o telhado residencial
no Piauí está mais colhido que no resto do país, o que torna o mercado de **minigeração**
— comércio e indústria, os 3.284 do BDGD sem geração — proporcionalmente *mais* valioso,
não menos.

**Padrão a guardar:** as três leituras erradas ou incompletas eram todas *plausíveis*. O
que separou foi medir o denominador que faltava, não argumentar melhor.

---

## 12. TCE-PI — a fonte que fecha o ponto cego (18/09/2026)

O `esic-4-TCE-pi.md` trazia uma nota de rodapé: *"o TCE-PI tem API documentada — vale
tentar a consulta direta antes de protocolar; o pedido formal é o plano B."* O plano B
virou desnecessário.

**A API** (`sistemas.tce.pi.gov.br/api/portaldacidadania`) não pede chave e expõe
`/prefeituras` (224, com `codIBGE`), `/receitas/:id/:exercicio`,
`/despesas/:id/:exercicio/porElemento` e `/licitacoes/:id`. Paginação de 10 em 10 pelo
parâmetro `pagina` — `limit`, `size` e `porPagina` são ignorados pelo servidor.

**Coleta:** 224 de 224, zero falhas, nenhum arquivo com menos linhas que o total
declarado. `dados/baixar_tce.py` (educado: 0,3 s entre chamadas, três tentativas com
espera crescente, cache para retomar) e `painel/build_tce.py`.

### 12.1 A decisão que muda o número

IPTU e ITBI aparecem em **três lançamentos** — principal, dívida ativa, multas e juros.
**Entra só o principal.** Somar os três infla o valor contra o SICONFI, que no
demonstrativo traz o imposto do exercício. A dívida ativa fica em campo próprio porque
também é informação comercial: **município com dívida ativa alta e IPTU baixo tem
cadastro velho, não ausência de contribuinte.**

### 12.2 Validação: duas fontes independentes, 83% de acordo exato

Comparando os **152** municípios que têm IPTU nas duas fontes:

| | |
|---|---|
| razão TCE ÷ SICONFI, mediana | **1,000** |
| dentro de ±1% | **116 de 139** (83%) |
| dentro de ±10% | 120 de 139 (86%) |
| divergem mais de 10% | 19 |

São prestações de contas do **mesmo município a órgãos diferentes**. A concordância na
mediana exata é a validação cruzada mais forte que este projeto conseguiu até agora.

**E a divergência confirma uma suspeita antiga.** O e-SIC ao TCE existia, entre outras
coisas, para checar **Altos**, cujo retorno no SICONFI viera com apenas duas linhas —
sugerindo preenchimento parcial. Confirmado: SICONFI **R$ 245.127**, TCE **R$ 1.310.555**
(5,35×). O demonstrativo estava incompleto, como se previu.

**Regra para as divergências:** nenhuma fonte é autoritativa a priori. Onde as duas
existem e divergem mais de 10%, **as duas aparecem** na ficha, com a diferença declarada.
Escolher uma em silêncio seria inventar hierarquia que não existe.

### 12.3 O que se ganhou

**72 municípios deixaram de vir em branco.** IPTU mediano deles: **R$ 17.084**; apenas um
declara zero.

E um achado que não se procurava: `/despesas/.../porElemento` traz **"Outros Serviços de
Terceiros – Pessoa Jurídica"** — o elemento **3.3.90.39**, exatamente o que o roteiro de
qualificação pergunta na porta 3.

**O limite honesto:** a API expõe `empenhada`, `liquidada` e `paga`, **não a dotação
autorizada**. Logo isto mede o *tamanho do elemento*, nunca o *saldo livre*. A porta 3
continua sendo pergunta de telefone — mas passou a ser pergunta informada: *"vocês
empenharam R$ X aqui; o que proponho é Y% disso"*.

**Ainda aberto:** `/licitacoes/:id` responderia o item 1 do e-SIC — quem já vende cadastro
imobiliário no estado, para quem e por quanto. Não foi coletado ainda.
