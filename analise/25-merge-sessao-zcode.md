# Fusão com o pacote da sessão ZCode — o painel único

**Data:** 2026-09-17 · **Regra seguida:** aditiva. `analise/` e `PLANO.md` não
foram alterados; o pacote original continua intacto em `tmp/sessao-zcode/`.

---

## 1. O que entrou na árvore

| Origem (`tmp/sessao-zcode/`) | Destino | Estado |
|---|---|---|
| `docs/*.md` | `docs/` | íntegro; `metodologia-iv.md` ganhou a §6 de adendos |
| `m0-conector/` | `m0-conector/` | íntegro (spec pinada, validador, laudo) |
| `dossie-dispensa/` | `dossie-dispensa/` | íntegro — TR v2.1 é a versão circulável |
| `apresentacao/` | `apresentacao/` | íntegro |
| `analise-viabilidade-...md` | `analise/26-relatorio-sessao-zcode.md` | referência das 12 rodadas |
| `dados/baixar.py` | `dados/baixar.py` | **estendido** (agregados por município + malha municipal) |
| `dados/inscricoes.csv` · `adesoes.xls` | `dados/bruto/sinter/` | baixados por `dados/baixar.py`; ver correção 3.1 |
| `painel/conversa.html` | `painel/conversa.html` | íntegro — narrativa de 5 telas |
| `painel/painel-v2.html` · `painel/index.html` · `teresina_full.geojson` | **não promovidos** | superados pelo painel único; ficam em `tmp/` como arquivo morto |

O método canônico de indicadores continua sendo `docs/metodologia-iv.md`.

---

## 2. O painel único

`painel/index.html` — uma página, duas escalas, onze telas. Roda em
`python3 -m http.server` na raiz; **não precisa de internet** (o Leaflet foi
vendorizado em `painel/vendor/`, correção de uma dependência que o painel-v2
tinha do CDN — demonstração em prefeitura não pode depender do wifi da sala).

| Escala | Telas | O que responde |
|---|---|---|
| **Estado** (224 municípios) | Mapa de alvos · Carteira e qualificação · Janela de 31/12 | para quem ligar primeiro, e com que número na mão |
| **Município** (25 com bairros; 199 em modo sem-bairro) | Território · Ranking de bairros · Saneamento · Pavimentação e viário · Perfis socioeconômicos | o que o painel-v2 fazia para Teresina, para qualquer município do estado |
| **Referência** | Relatórios exportáveis · Metodologia e fontes · Fora da v1 | de onde veio cada número e o que está congelado, com o motivo |

Cada lado trouxe o que o outro não tinha: a **interatividade e o ETL** vieram do
painel-v2; a **qualificação comercial dos 224** (`dados/qualificacao-pi.csv`),
os segmentos, os pilotos e a reordenação pelo ITBI vieram do PLANO desta árvore.

### Itens do backlog que foram feitos

1. **Seletor de município** — o ETL deixou de filtrar pelo prefixo fixo
   `2211001` e passou a varrer a UF: **479 bairros em 25 municípios, 173 FCU**.
   Um arquivo por município, carregado sob demanda.
2. **Modo "sem bairro"** — resolvido por um caminho mais barato que o proposto:
   os **agregados por município** do Censo 2022 existem e trazem exatamente as
   mesmas variáveis dos agregados por bairro. Os 199 municípios sem recorte
   intraurbano passam a ter os mesmos seis indicadores, calculados pelas mesmas
   regras, sem precisar da malha de setores nem de interpolação areal.
4. **ITBI × IPTU** — o gráfico existe, em escala log, com a diagonal marcando
   ITBI = IPTU: **64 dos 224 arrecadam mais ITBI que IPTU**, dos quais 57
   aparecem no gráfico (a escala log exclui os valores zerados). Os números são
   os do portal SICONFI, e a ressalva de método viaja com eles na metodologia.
5. **Busca** — no mapa do estado e no do município, com seleção cruzada entre
   mapa, ranking, tabela e gráfico.

### O que ficou fora, de propósito

**Educação/INEP (item 3)**. O PLANO §12.5 põe o INEP depois do conector e da
verificação fiscal; antecipá-lo por ser tecnicamente divertido seria furar a
ordem do M0. A tela existe como escopo congelado, com o motivo escrito.

---

## 3. Correções que a fusão produziu

### 3.1 `adesoes.xls` da RFB **não é uma lista de adesões**

O pacote descrevia o arquivo como "listas RFB (adesões; 188 com CIB ativo)". A
segunda parte está certa. A primeira, não: o arquivo tem **5.570 linhas — todos
os municípios do Brasil**, a aba chama-se **TOM** (Tabela de Órgãos e
Municípios) e não há coluna que indique adesão. É tabela de referência.

Consequência prática: **não dá para afirmar quem aderiu ao convênio**, e
portanto o e-SIC nº 2 à Receita (`entregaveis/esic-2-RFB-sinter.md`) **continua
necessário** — a rodada 8 o dava por morto. Se alguém tivesse lido o arquivo como
adesão, a conclusão seria "os 224 municípios do PI já aderiram", que mataria
sozinha o serviço de condução da adesão.

O que o outro arquivo (`inscricoes.csv`) sustenta, esse sim verificado:
**188 municípios no Brasil com CIB ativo, 20,1 milhões de inscrições, e no Piauí
só Teresina (363.805)**. É a formulação segura do deck — "menos de 4% dos 5.570".

### 3.2 O corte de amostra do entorno estava no universo errado

`V05000` é o domicílio *em setor escolhido para aplicação do entorno*, não o
total de domicílios. Detalhe: no PI a cobertura mediana é 1,0 — mas há bairro
com 95 domicílios e **3** no universo do entorno. Ver `docs/metodologia-iv.md` §6.2.

### 3.3 A cor do mapa dizia o contrário do que o painel quer mostrar

O mapa pintava o primeiro quintil de verde em todos os indicadores. Em renda,
isso deixa o centro rico de Teresina vermelho e a periferia verde — a leitura
exatamente invertida num painel cujo objetivo é achar carência. Duas paletas
agora, com a direção declarada na legenda e na metodologia (§6.3).

### 3.4 O rótulo do k-means contradizia os próprios números

A ordenação dos grupos usava só a renda; o grupo rotulado *prioridade alta*
aparecia com esgoto melhor que o *prioridade média*. Passou a usar as quatro
dimensões (§6.5).

### 3.5 Três correções de fato absorvidas do relatório ZCode

- **Altos: 47.453 habitantes** no Censo 2022 (7º do estado) — o 46.826 de
  `analise/13` é estimativa anual. O CSV de qualificação ainda traz o valor
  antigo; o painel mostra o do CSV, e a divergência está registrada aqui e na
  tela de metodologia.
- **Tenants Foxinline entre os 25 com bairros: 6**, não 8 — Barras e Água Branca
  têm só host de cartório. `dados/qualificacao-pi.csv` marca 63 tenants no
  estado inteiro, contagem que não conflita com a correção.
- **§§ do art. 75 verificados no TCU** — §1º fracionamento, §2º consórcio
  (R$ 130.984,22, diferente do teto de engenharia R$ 130.984,20), §3º aviso de
  3 dias úteis. Já refletido no TR v2.1.

---

## 4. Verificação do ETL

O `painel/build_dados.py` reproduz **dígito a dígito** os 123 bairros de Teresina
do `teresina_full.geojson` da sessão ZCode: 11 campos × 123 bairros,
**divergência zero**. A generalização não mexeu no método — só no recorte.

---

## 5. O que continua aberto

1. **e-SIC nº 2 à RFB** — ressuscitado pelo item 3.1. Sem ele, o denominador do
   mercado (quem aderiu) permanece desconhecido.
2. **Validar manualmente os 6 números de IPTU/ITBI no portal SICONFI** antes do
   deck (30 min), como manda `docs/metodo-fiscal-itbi-iptu.md`.
3. **Composição urbana × rural do ITBI** dos sete municípios do sul. Enquanto não
   verificada, o painel os marca como *hipótese*, nunca como alvo.
4. **IPTU e RCL de Altos e Paulistana no TCE-PI** — fronteira A/B, plausíveis e
   não reverificados.
5. **Rodar o validador de completude contra um cadastro municipal real.** É o
   único item que a venda não resolve: hoje a primeira execução real aconteceria
   no cliente.

---

## 6. Rodada de revisão (17/09/2026)

Revisão em três frentes — orquestração por Claude Code, `/code-review` em alto
esforço, e segunda opinião externa (DeepSeek e GLM). O que a revisão mudou:

### 6.1 O defeito mais sério: "3 de 3" era falso para 82 municípios

A coluna `sinal_rreo` de `dados/qualificacao-pi.csv` **só nomeia duas falhas** —
`NUNCA_3ANOS` (49) e `FALHOU_2025` (23). Para todos os outros 152 o campo vem
**vazio**, e o painel lia vazio como "entregou os três anos". Mas dos 152, só
**70** têm `rreo = [1,1,1]`; os outros **82 entregaram 2025 e faltaram em 2023 ou
2024**.

O sintoma era visível na própria tela: o mapa pintava o município de verde
("3 de 3") enquanto a ficha, que imprime o tripé cru, mostrava `✗ ✓ ✓`. Num
painel cuja tese comercial é *"quem não entrega demonstrativo não vai conseguir
enviar remessa"*, classificar errado 82 dos 224 é errar o alvo em 37% do estado.

A classificação agora sai de `rreo2023/2024/2025`:

| Situação | Municípios |
|---|---|
| 3 de 3 | 70 |
| falhou antes de 2025 | 82 |
| falhou em 2025 | 23 |
| nunca em 3 anos | 49 |

O CSV exportado passou a levar as três colunas de ano **mais** a situação
derivada, no lugar do `sinal_rreo;OK` que carimbava "OK" nos 82.

### 6.2 Outros defeitos corrigidos

| Onde | Defeito | Consequência que teria |
|---|---|---|
| troca de município | `SELMUN` mudava antes do `await` do fetch, sem verificar se ainda era a seleção corrente | escolher Teresina e logo outro município misturava 123 bairros de Teresina com o cabeçalho do outro, e quebrava em `BAIRROS[SELMUN].fcus` |
| corte de amostra | `validos()` decidia o universo pela lista de botões; `onibus` e `arbor_sem` não estavam nela | indicador de entorno entrava com o corte de domicílios — Rudiador entrava no ranking com 3 registros e peso 95 |
| ficha do bairro | "Face sem árvores" pintada com a rampa de carência sem inverter; idosos e crianças com rampa de carência | déficit aparecia como bom, e proporção de idosos ganhava juízo de valor que o dado não tem |
| ficha do município | "População (Censo 2022)" era a estimativa anual do CSV | atribuía ao Censo um número que não é dele, e ficava "—" em 72 municípios cujo total de moradores o Censo tem |
| navegação | `ir('territorio')` reenquadrava o mapa 60 ms depois, por cima do pan pedido | clicar numa linha do ranking nunca chegava no bairro escolhido |
| escala log | piso fixo em 10² e rótulos deslocados uma potência (10³ rotulado "10k") | dois municípios sumiam do gráfico sem entrar em nenhuma contagem, e o eixo mentia por um fator de 10 |
| ordenação | nulo tratado como `-1`/`1e15` conforme o sentido | ordenar por IPTU crescente começava com 72 linhas em branco |
| legenda | quintis e categorias vazias exibidas | faixa sem nenhum município na legenda inventa variação que o dado não tem |
| contagens | `224` e `'1 de 224'` escritos à mão ao lado de valores derivados | qualquer regeração dos dados faria o cabeçalho contradizer a tabela |
| `build_dados.py` | `rreo` ausente virava `[0,0,0]`; temporários do shapefile nunca apagados | município fora do CSV seria vendido como "nunca entregou RREO" |

### 6.3 O que a revisão confirmou

`conversa.html` foi verificado e não teve achado. O ETL continua reproduzindo os
123 bairros de Teresina da sessão ZCode com divergência zero, agora com os
temporários limpos.

### 6.4 Segunda opinião: DeepSeek e GLM

Pacote de 109 KB (ETL + painel com número de linha + esta nota + a metodologia)
enviado aos dois. Os dois acharam, cada um por seu caminho, o mesmo defeito do
corte de amostra que o `/code-review` já havia apontado — convergência de três
revisores independentes sobre o mesmo ponto. O que cada um trouxe de novo:

**DeepSeek** (`deepseek-v4-pro`; 40 mil tokens de prompt, 22,5 mil de raciocínio):

- `float(q['iptu'])` direto, sem passar pelo `num()` do próprio ETL: um `X`, um
  travessão ou uma vírgula decimal no CSV derruba a geração inteira. **Corrigido.**
- `Math.min(...[])` devolve `Infinity` se uma das quatro dimensões do k-means for
  toda nula num município; a normalização vira `NaN` e a tela de Perfis quebra.
  **Corrigido** — o universo do agrupamento agora exige as quatro dimensões.
- A metodologia dizia "477 bairros" onde a malha tem **479**. **Corrigido**, com a
  contagem completa (479 · 2 sem `V00001` · 20 com `n_ok=0` · 28 com `n_ok_ent=0`
  · 18 sem registro de entorno).
- "IPTU do estado" somava `||0` sobre os 72 sem RREO. O total está certo — é a
  soma do que foi reportado — mas o rótulo dizia "do estado". **Renomeado** para
  "IPTU reportado", com o número de municípios no título do elemento.

**GLM 5.3** (pelo plano Z.ai, via `opencode`):

- O k-means filtrava só por `n_ok`, mas duas das quatro dimensões vêm do entorno,
  e `nrm` convertia ausência em `0,5` — um valor médio inventado que desloca o
  centróide e, com ele, o rótulo de prioridade. **Corrigido.**
- As faixas etárias do ETL somavam com `or 0`: valor suprimido pelo IBGE viraria
  "0% de idosos" em vez de travessão. **Corrigido.**
- `qT()` e `validos()` refeitos a cada `setStyle` — o mapa municipal rodava em
  O(n² log n) sem necessidade. **Corrigido** com cache por indicador, zerado na
  troca de município.
- Código morto (`alvoB`) e `distrib()` reimplementando `faixa()`. **Removidos.**

### 6.5 O defeito que só o teste de estresse achou

Nenhum dos três revisores pegou este, e ele era o mais destrutivo: **os mapas não
declaravam `maxZoom`**. Sem ele, `getBoundsZoom` de um município pequeno pode
devolver `Infinity`; o mapa fica com `_zoom` inválido e **toda** chamada seguinte
a `getCenter()` lança `Invalid LatLng (NaN, NaN)`. O sintoma: trocar de município
algumas vezes seguidas travava o painel a partir da oitava troca — e ficava
travado, porque o estado inválido persiste.

Achado ao percorrer os 25 municípios com bairros × 5 telas num laço. Corrigido
com `minZoom`/`maxZoom` explícitos, `animate:false` nos enquadramentos e um único
agendamento de reenquadre por vez. A varredura agora passa limpa: **27 trocas de
município × 5 telas, zero erro**.

---

## 7. Ajustes de raiz e revisão do deck (17/09/2026)

### 7.1 População passou a ser a do Censo, e não a estimativa

A divergência de Altos (47.453 × 46.826) estava registrada como ressalva. Ela
tinha solução na raiz: **`V0001` — "total de pessoas" — dos agregados básicos do
IBGE**, que já estavam baixados e não estavam sendo lidos. Consequências:

- os **224** municípios passam a ter população, inclusive os 72 sem RREO, cuja
  coluna `pop` do CSV é vazia;
- **ITBI por habitante é recalculado** sobre ela — o rótulo "÷ população do Censo
  2022" deixou de ser falso;
- a estimativa do CSV vira `pop_csv`, exibida na ficha só quando diverge, e
  exportada como coluna de rastreio;
- os bairros também ganham `pop` e `area_km2` (a malha traz os dois).

Em Teresina o Censo dá 866.300 e a estimativa 868.523; `V00005` (moradores em
domicílios particulares permanentes ocupados) dá 862.879. São três números
diferentes e todos certos — o painel agora diz qual é qual.

### 7.2 O deck publicava as métricas que a metodologia aposentou

`apresentacao/` não tinha passado por revisão. As duas capturas de tela eram do
**dashboard-demo v1**, e o rodapé metodológico impresso nelas dizia, em letra
miúda: `V05006/V05000`, `V05012/V05000` e `V06004`. São exatamente os três
denominadores que a v2 chama de errata. O slide 4 abria com
**"R$ 3.078 · renda média mensal do responsável"**.

Corrigido no arquivo (original preservado com sufixo `-v1`):

| Slide | Era | Virou |
|---|---|---|
| 3 | "cinco indicadores"; 123 bairros; `dashboard-demo/index.html` | onze indicadores; **479 bairros em 25 municípios**; `painel/index.html` |
| 4 | renda **média**, R$ 3.078, `V06004`, Tabajaras R$ 16.629 × Chapadinha R$ 1.112 | renda **mediana**, **R$ 1.212**, `V06006`, Tabajaras R$ 15.000 × Chapadinha R$ 1.200 |
| 4 | "Livramento — bairro com 0% de esgoto" | Livramento **e Triunfo**, 509 domicílios somados (há um terceiro, Redonda, abaixo do corte de amostra) |
| 8 | "priorizar **tenants** Foxinline"; "3–5 pilotos"; "Meta: 3–5 remessas" | priorizar **quem não tem incumbente**; "2–3 contratos"; meta do §12.1 com o otimista condicionado ao conector |
| 11 | "**Sentar** com a Foxinline"; e-SIC para ETURB/SEMDUH/Águas | "**Monitorar** a Foxinline" (§12.2); e-SIC para SEAD/PROUrbe, RFB, SEFAZ-PI, TCE-PI (§12.4) |

As duas capturas foram regeradas do painel atual, nas mesmas dimensões
(1440×1330 e 1440×620), e trocadas dentro do `.pptx`.

**Os dois itens do slide 11 eram os mais caros:** o deck mandava procurar a
Foxinline — o oposto do que o PLANO §12.2 decidiu — e mandava disparar os três
e-SIC que o §12.4 rebaixou, deixando de fora o único que decide alvo.

### 7.3 O que continua fora de alcance daqui

O slide 2 diz "107 dias" e o 8, "nos 107 dias": está certo **na data do deck**
(15/09). Quem apresentar em outubro precisa recontar — não dá para deixar um
número de contagem regressiva fixo num arquivo estático. O painel mostra o
número do dia na barra superior.

---

## 8. CNEFE e tema claro (17/09/2026)

### 8.1 A base que faltava: o volume da remessa

`painel/build_cnefe.py` agrega o **Cadastro Nacional de Endereços para Fins
Estatísticos** do Censo 2022. No Piauí, **1.891.421 endereços, todos com
coordenada**, nos 224 municípios — com tipo e nome de logradouro, CEP, número,
setor, quadra e face, que são justamente os campos da remessa ao CADURB.

Isso ataca a pendência do §5 que a venda não resolvia. O diagnóstico deixa de
depender do export do ERP municipal para existir: dá para chegar na reunião com
**o tamanho da remessa daquele município**, calculado de dado público.

A aferição que sustenta o número: Teresina transmitiu 363.805 CIBs, e o Censo
enumerou 371.548 endereços dentro da malha de bairros — **97,9%**. Onde ninguém
transmitiu nada, a contagem do CNEFE é a melhor estimativa disponível do volume.

E é a unidade que o TR já pedia: o §13.3 do PLANO manda declarar preço-teto por
**R$/imóvel × volume do cadastro**. O volume agora tem fonte pública e datada.

**Cuidado de método:** o CNEFE referencia setores de *coleta*, os agregados usam
setores de *divulgação*, e juntar pelos códigos perde 10,4% dos endereços. Por
isso o corte por bairro é por geometria (ponto em polígono), não por código.

### 8.2 Tema claro

O painel tem os dois temas, com botão no cabeçalho e escolha guardada no
navegador. A mudança de fundo foi tirar a cor do JavaScript: as duas rampas do
mapa, as cores de eixo dos gráficos e os realces viraram **tokens de CSS**, lidos
em tempo de desenho. Antes havia uma paleta no CSS e outra no JS — a segunda não
tinha como seguir o tema.

Motivo prático: projetor de sala de prefeitura lava tema escuro, e a primeira
apresentação presencial é em novembro.

### 8.3 O que isso muda no plano

Nada do que estava congelado descongelou. ML, PGV e chat continuam fora da v1
pelas razões já medidas — em especial a do §11.6: só 15 de 152 municípios do PI
acumulam ≥500 transações de ITBI em 24 meses, e nenhum município pequeno calibra
modelo sozinho. O que mudou é que o **Segmento B** ganhou um número público para
abrir conversa, e o preço-teto do TR ganhou lastro.

---

## 9. Rodada 3 de revisão (17/09/2026)

Revisada a entrega do CNEFE, do tema claro e da publicação. `/code-review` em
alto esforço, DeepSeek (`deepseek-v4-pro`) e a passada própria; GLM 5.3 ainda
rodando quando isto foi escrito.

### 9.1 O defeito que a minha própria correção criou

Ao mover as cores para tokens, uma substituição em massa trocou
`rgba(232,242,236,.08)` por `var(--trilho)` **inclusive nas duas linhas que
definem o token**. O resultado foi `--trilho:var(--trilho)` nos dois blocos de
tema escuro. Token cíclico é inválido em tempo de cálculo, então no tema escuro —
o padrão de quem nunca escolheu tema — **toda barra e todo trilho ficavam sem
fundo**. Lição prática: `replace` global sobre CSS atinge a declaração junto com
o uso.

### 9.2 O achado com maior raio de explosão

`wrangler pages deploy` resolve o diretório `functions/` **a partir do diretório
corrente**, não do diretório publicado. Rodar o comando da raiz do repositório —
em vez de `painel/deploy` — publica só os arquivos estáticos, **sem aviso**, e o
painel inteiro fica aberto. A guarda de 503 não socorre: sem middleware não há
quem responda 503. O `publicar-cf.sh` já faz `cd` para o lugar certo; o que faltava
era a checagem e o aviso para quem digitar o comando à mão.

### 9.3 Demais correções

| Onde | Defeito |
|---|---|
| legenda do mapa estadual | amostras de "piloto" e "host Foxinline" fixavam a cor do tema escuro; depois do ajuste de contraste deixaram de bater com o contorno real |
| troca de tema | a camada de FCU e a do modo sem-bairro guardam a cor de quando nasceram e não eram refeitas |
| ficha do bairro | a barra só sabia escalar percentual e renda: com "Endereços" em milhares, todo bairro com 100+ desenhava barra cheia |
| `P1` | `.replace('.',',')` sobre número que o pt-BR já formatou — 1234,5 virava "1,234,5" |
| ficha e carteira | município sem segmento era rotulado **"segmento B"** — lead inventado |
| CSV de pilotos | saía sem fonte nem data, contra a regra que a própria página anuncia |
| `ir()` | hash que não é identificador CSS derrubava a navegação em silêncio |
| ITBI × IPTU | `5 > null` é `true`: município sem IPTU reportado entraria na conta dos "mais ITBI que IPTU" (latente — hoje os 72 têm os dois campos ausentes) |
| `publicar.py` | removia **toda** `<meta>` do cabeçalho, não só as que a plataforma injeta |
| `build_dados.py` | docstring dizia 2 e 16; o correto, e o que a tela publica, é **8 e 18** |
| `build_cnefe.py` | data de consulta fixa no código; regerar em outro dia publicaria data falsa |
| contraste do tema claro | `--dim` 3,3:1, teal 3,4:1 e âmbar 3,8:1 sobre o painel branco — escurecidos para 5,0 / 5,5 / 5,8:1 |
| tabela da carteira | valores monetários quebrando em duas linhas com a coluna nova de endereços |

### 9.4 GLM 5.3 — e a falha que ele mesmo ilustra

A primeira chamada **voltou vazia**: leu o pacote de 109 KB e não produziu nada,
saindo com código 0. É a falha que o `CLAUDE.md` já registra para esse modelo.
Segunda tentativa com pacote de 31 KB — só o código novo — e pedido de resposta
curta no próprio prompt: **seis achados**, quatro deles válidos.

| Achado | Veredito |
|---|---|
| `URL.revokeObjectURL` na mesma volta do `click()` aborta o download em parte dos navegadores | **procede** — agora revoga depois de 60 s |
| a tela de falha de carga fixava `#FF6B57` e `#54726A`, tons do tema escuro, num elemento que aparece nos dois | **procede** — virou token |
| `bairros[cdb] = {...}` atribui em vez de somar: malha que parta um bairro em duas features subcontaria em silêncio | **procede** — acumula (hoje: 479 features, zero códigos repetidos) |
| `grep "\b$projeto\b"` casa substring com nome hifenizado, e falha passageira do `list` abortava o deploy | **procede** — casamento exato e falha tolerada |
| "não há listener de `prefers-color-scheme`" | **não procede** — existe em `index.html:542`; o recorte enviado não incluía o `carregar()` |
| "`delete IE.end` é irreversível" | **não procede** — o `fetch` é aguardado antes do primeiro desenho, e sem a base o indicador não deve existir mesmo |

Os dois falsos positivos vieram do pacote menor, que foi o preço de fazer o
modelo responder. Vale registrar o custo: **o recorte que destrava a resposta é o
mesmo que produz achado sobre código que o revisor não viu.**

### 9.5 O que a revisão confirmou

A guarda de corrida de `trocarMunicipio`; os quatro CSVs com cabeçalho e linha de
mesma largura; a contagem de 64 municípios com ITBI > IPTU; o ray-casting do
`build_cnefe.py`, inclusive na divisão por zero mascarada; a aferição dos 97,9%; e
a soma dos 123 bairros de Teresina fechando com o agregado municipal. O middleware
de basic auth foi dado por correto pelo DeepSeek, já com a correção do `unescape`.

**Varredura final:** 27 trocas de município × 5 telas, todos os indicadores dos
dois mapas, alternância de tema e um hash inválido de propósito — **zero erro**.


---

## 10. Capturas do deck em tema claro (17/09/2026)

As duas imagens dos slides 3 e 4 foram regeradas com o painel em **tema claro**,
nas mesmas dimensões (1440×1330 e 1440×620), e trocadas dentro do `.pptx`.

Motivo prático, que foi o mesmo que justificou fazer o tema claro: projetor de
sala de prefeitura lava tema escuro. E há um ganho de composição — o deck é
claro, então a captura passou a integrar o slide em vez de brigar com ele.

Ficam guardadas ao lado três gerações da mesma imagem:

| Arquivo | O que é |
|---|---|
| `dash_hero.png` · `dash_scatter.png` | **em uso** — painel atual, tema claro |
| `dash_hero-escuro.png` · `dash_scatter-escuro.png` | painel atual, tema escuro |
| `dash_hero-v1.png` · `dash_scatter-v1.png` | dashboard-demo original, com as métricas aposentadas (V06004 e denominador com "não declarado") — mantido só como registro do que foi corrigido |

---

## 11. Modelo do coletor de campo e o que a revisão dele achou (17/09/2026)

`coletor/index.html` — tela de celular que o parceiro valida antes de a coleta ser
construída. Endereço real do CNEFE (Parnaíba, setor 232), registro de exemplo,
cada campo mapeado ao schema do CADURB. Publicada em `/coletor/`, atrás da mesma
senha do painel.

### 11.1 Dois defeitos que não eram da tela, eram do produto

**A R7 nunca conferia dígito verificador.** A regra percorria
`docTitular`, `cpfCnpjTitular`, `idTransmitenteITBI`, `idAdquirenteITBI` — e o
campo do CPF/CNPJ do titular na spec é **`niTitular`**, que é justamente para
onde `validador_completude.py` mapeia a coluna do CSV. Resultado: **o laudo
declarava "apto" sem nunca ter validado um CPF**. Corrigido e provado: registro
com `niTitular` inválido agora devolve `CAMPO_COM_DV_INVALIDO`.

**A faixa de CEP não existia, e não pode ser intervalo.** A R3 só confere o CEP
se alguém injetar `faixas_cep` no contexto — e ninguém injetava, então a regra era
**pulada em silêncio**. Agora `build_cnefe.py` emite os prefixos observados por
município. E a medição mostrou por que lista, não intervalo: **Parnaíba tem 18
prefixos entre 64200 e 64219 — 64203 e 64214 não são do município.** Validar por
intervalo aceitaria endereço que a Receita recusa. Provado: `64203-100` agora é
recusado.

### 11.2 Achados da tela

| Achado | Origem |
|---|---|
| `percTitularidade` é fração 0–1 na spec; a tela ensinava "100" | próprio |
| `temBairro` é obrigatório e não estava no formulário | próprio |
| `@media` dentro de lista de seletores — regra inválida, descartada | próprio, DeepSeek, GLM |
| "tabela 9.6 · 300 códigos" — são **306** | próprio, DeepSeek, GLM |
| moldura do telefone vazando a largura num telefone de verdade | próprio |
| botão primário branco sobre verde claro no tema escuro | `/code-review` |
| aviso "sem número de porta" **fabricado** — o registro tem número 30 | `/code-review`, DeepSeek, GLM |
| `anoConstrutivo`: a spec vai até 2100 e ano futuro é aviso, não impedimento | `/code-review` |
| `tipoArquitetonico` → o nome real é **`tpArquitetonico`** | `/code-review` |
| `<textarea>` sem indicação de foco | `/code-review` |
| rótulos sem `for`, campos sem `id` | `/code-review` |
| a tela **afirmava** que o campo some quando territorial, e não sumia | DeepSeek |
| rótulo do domínio 9.8 fora da forma do manual | DeepSeek |

A regra R5 agora funciona de verdade na tela: escolher territorial esconde área
construída e tipo arquitetônico. Conferido: 2 campos visíveis → 0 → 2.

### 11.3 Um falso positivo que vale registrar

O GLM apontou que `000.000.000-00` passa no cálculo do dígito verificador — é
verdade no algoritmo puro, mas o `dv_cpf` da casa tem a guarda de dígitos
repetidos e recusa. O parecer raciocinou sobre o **resumo** da regra enviado no
pacote, não sobre o código. Mesmo assim a objeção rendeu: o exemplo passou a ser
`123.456.789-00`, que falha no dígito de verdade (o correto seria 09) — porque
um cliente picuinha faria exatamente a mesma pergunta.

---

## 12. O laudo não estava rodando as regras que justificam o preço (17/09/2026)

Ao fechar os ajustes da revisão do coletor, a investigação abriu num achado maior:
**existem dois validadores**, e o que gera o laudo — o artefato que o cliente
compra — não usava as regras semânticas.

### 12.1 O defeito que teria explodido na primeira execução real

`m0-conector/spec/dominios.json` tinha **175 códigos** de tipo de logradouro;
`entregaveis/dominios_cadurb.json` tinha **306**. Comparadas, a menor é
subconjunto estrito da maior: a extração **parou em 175 (Morro)** e ainda trouxe
cabeçalho de PDF em 8 descrições.

Consequência, medida:

| Tipo | Código | Estava na tabela do validador? |
|---|---|---|
| **Rua** | 250 | **não** |
| **Praça** | 215 | **não** |
| **Travessa** | 273 | **não** |
| **Vila** | 298 | **não** |
| Avenida | 26 | sim |

Numa base municipal, a maioria esmagadora dos logradouros é "Rua". O laudo sairia
com aviso de *"fora da tabela oficial"* em quase toda linha — e a pendência
registrada no §5 era exatamente esta: *"o risco é a primeira execução real
acontecer no cliente"*. Aconteceu aqui, que é onde tinha de acontecer.

### 12.2 As outras três, na mesma função

- **O CPF nunca era conferido.** `ni_valido()` checava só o comprimento: onze
  dígitos inventados passavam e o laudo dizia "apto". Agora usa o `dv_documento`
  das regras semânticas. Provado: `12345678901` é recusado, `52998224725` passa.
- **O CEP não era conferido contra o município.** Agora usa os prefixos do CNEFE.
  Provado: `64203-100` é recusado em Parnaíba — e um intervalo o aceitaria.
- **O percentual de titularidade** era tratado como 0–100, e a spec usa fração
  0–1. O validador passou a aceitar as duas formas e a registrar qual veio.

### 12.3 E o que ainda não é verdade

O laudo continua **sem chamar** `regras_semanticas.validar_base`. O caminho está
aberto (o módulo é importado e já serve o DV), mas as 10 regras — coerência
territorial × predial, faixa de ano, unicidade de inscrição pela regra própria —
seguem em módulo separado. **Enquanto não forem chamadas, o laudo é mais fraco do
que a documentação do produto afirma.** Fica como o próximo item, e não como
concluído.

### 12.4 Tabela 9.13 contaminada

A extração trouxe para dentro de *Tipo de Transação* o texto da seção de
autenticação e os códigos HTTP da API: `400`, `401`, `403`, `404`, `409`, `500`,
`1`, `2`, `4`. Como a R4 valida contra a tabela, **`tipoTransacao = 404` passaria
como transação válida**. Limpa para os 37 códigos do manual, com nota de
procedência no próprio arquivo.
