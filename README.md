# Vertical Data

**Dado público vira cadastro imobiliário aceito pela Receita — antes de 31/12/2026.**

A Lei Complementar 214/2025 (arts. 265 e 266) manda inscrever **todo imóvel urbano do
país no CIB**, o Cadastro Imobiliário Brasileiro. Capitais desde 01/01/2026; os demais
municípios até **01/01/2027**. Quem não entrega não perde uma meta de gestão: perde a
base sobre a qual o IBS/CBS vai incidir.

Os 224 municípios do Piauí chegam nesse prazo em condições muito diferentes, e ninguém
publicou o mapa dessa diferença. Este repositório é esse mapa — e as ferramentas para
atravessá-lo.

> O produto é o prazo legal, não o painel. O cliente é o ordenador de despesa sem
> equipe. **O aceite é a remessa aceita no CADURB** — nunca "modelo acurado a X%".
>
> — `analise/PLANO.md`, §1

---

## O que tem aqui

| | | |
|---|---|---|
| **`painel/`** | 11 telas sobre os 224 municípios do PI | mapa de alvos, carteira, janela de 31/12, território, ranking de bairros, saneamento, viário, perfis socioeconômicos, relatórios, metodologia |
| **`coletor/`** | protótipo da tela de campo | o formulário que um agente preenche no celular, com as regras do CADURB embutidas (não descritas) |
| **`m0-conector/`** | validador de completude | lê o CSV do cadastro do município e emite o **laudo** — o primeiro artefato vendável |
| **`entregaveis/`** | as 10 regras semânticas + domínios oficiais | o que separa isto de um `required`-checker extraído do Swagger |
| **`analise/`** | 26 documentos de análise | o raciocínio inteiro, incluindo o que foi descartado e por quê |
| **`dossie-dispensa/`** | processo de contratação direta | TR v2.1, minuta de decisão, aviso de intenção |
| **`docs/`** | metodologia | `metodologia-iv.md` é a fonte canônica do método dos indicadores |

Análise cruzada: Claude Code orquestrando, **DeepSeek** no eixo técnico, **GLM** no eixo
de negócio — 12 rodadas, cada afirmação factual verificada contra a fonte.

---

## Os números que sustentam o resto

| | |
|---|---|
| **224** municípios do PI, todos com ficha | 25 com malha de bairros (479 bairros) |
| **1.891.421** endereços do CNEFE 2022 no PI | **zero** sem coordenada; 97,6% no melhor nível de geocodificação |
| **97,9%** | as 363.805 inscrições ativas no CIB de Teresina sobre os 371.548 endereços do CNEFE dentro da malha de bairros — é esta aderência que licencia usar o CNEFE como estimativa do volume da remessa |
| **194** municípios com IPTU < R$ 100 mil/ano | o segmento de conformidade: para eles o CIB não é receita, é sobrevivência cadastral |
| **72** municípios sem RREO 2025 | dado **ausente**, não zero — e o painel diz isso em cinza, não em verde |

O que o CNEFE permite dizer numa primeira reunião, antes de qualquer contrato: **o
tamanho da remessa daquele município**.

---

## Rodar

```bash
python3 -m venv .venv && .venv/bin/pip install numpy requests
```

**O painel abre sem baixar nada** — `painel/dados/` está versionado (≈1 MB), e o Leaflet
está em `painel/vendor/`, sem CDN:

```bash
python3 -m http.server 8011 -d painel     # → http://127.0.0.1:8011
```

Para refazer os dados a partir da fonte (≈50 MB de download; `--completo` sobe para ~600 MB):

```bash
python3 dados/baixar.py            # IBGE (agregados, malhas, CNEFE) + SICONFI
.venv/bin/python painel/build_dados.py    # → painel/dados/{municipios,bairros/*,meta}.json
.venv/bin/python painel/build_cnefe.py    # → painel/dados/cnefe.json   (~8 s)
```

`dados/bruto/` não vai para o repositório: é público, grande e idempotente.

### Validar um cadastro municipal

```bash
python3 m0-conector/validador_completude.py m0-conector/exemplo_base.csv \
    --ibge 2207702 --saida /tmp/LAUDO.md
```

Sai o laudo em Markdown e HTML: obrigatórios, domínios oficiais (306 códigos de tipo de
logradouro), **dígito verificador de CPF/CNPJ** e CEP conferido contra os prefixos reais
daquele município — lista de prefixos, não intervalo: em Parnaíba os CEPs vão de 64200 a
64219, mas **64203 e 64214 não são do município**.

### Publicar

```bash
painel/deploy/montar.sh && painel/deploy/publicar-cf.sh
```

Cloudflare Pages com basic auth em `functions/_middleware.js`. ⚠️ O wrangler resolve
`functions/` **relativo ao CWD** — publicar da pasta errada sobe o painel **sem
autenticação, em silêncio**. O script recusa rodar se o middleware não estiver ali.
Detalhes e como criar o token: `painel/deploy/LEIAME.md`.

### Marca e system design

`marca/` é a fonte única de cor, tipografia e símbolo — cores **medidas** do PDF
de logomarcas, não estimadas de screenshot. O contrato completo está em
[`marca/README.md`](marca/README.md).

```bash
python3 marca/aplicar.py              # reescreve os tokens embutidos nas páginas
python3 marca/aplicar.py --conferir    # acusa divergência (montar.sh roda isto)
```

O teal da marca (`#12B0A0`) dá 2,71:1 sobre branco: serve para **forma**, não
para texto. Quem carrega texto no tema claro é `#0D8478`, a 4,58:1. São duas
variáveis porque são dois usos.

---

### Grafo de conhecimento

`graphify-out/` traz o corpus inteiro — 108 arquivos, 278 mil palavras — como grafo
navegável: **759 nós, 1.068 arestas, 64 comunidades**. É mais barato consultá-lo do
que varrer `analise/` arquivo por arquivo.

```bash
graphify query "por que o CERURB saiu do caminho crítico?"
open graphify-out/graph.html          # o grafo, sem servidor
```

`GRAPH_REPORT.md` tem a trilha de auditoria: cada aresta marcada EXTRACTED,
INFERRED ou AMBIGUOUS, com o arquivo de origem.

---

## Regras da casa

1. **Nenhum dado fictício.** Todo número tem fonte e data de consulta. Onde a fonte não
   respondeu, o campo é nulo e a tela mostra cinza.
2. **Ausência não é zero.** 72 municípios sem RREO ≠ 72 municípios com IPTU zero — e
   outros 13 declararam IPTU = 0, o que *é* dado.
3. **Credencial nunca entra no repositório.** Nem valor, nem mensagem de commit, nem
   issue. As do deploy vivem em `~/.cerurb-cf.env` (chmod 600) e como secrets do Pages.
4. **A cor tem direção declarada.** Duas paletas: carência (1º quintil vermelho) e
   magnitude (rampa de matiz único — IPTU baixo é o *alvo*, não um problema). A
   marca trocou o matiz; a direção é da metodologia (`docs/metodologia-iv.md` §6)
   e não muda. Ausência de dado é família própria, fora das duas rampas.
5. **Toda mudança relevante passa por revisão em laço**, até a revisão não apontar mais
   correção. Uma passada só não fecha.

---

## Estado

Aplicado, verificado e no ar. As pendências abertas estão em
`analise/25-merge-sessao-zcode.md` §5 e §12 — a maior delas: o laudo ainda **não chama**
`regras_semanticas.validar_base`, então as 10 regras rodam no módulo e não no relatório
que o cliente lê.
