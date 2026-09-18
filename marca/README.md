# Vertical Data — system design

Base: `.orca/drops/Vertical-Data-Logomarcas.pdf`, 18 lockups. As cores aqui foram
**medidas do PDF**, descomprimindo os streams e lendo os operadores `rg` — não
amostradas de screenshot, que teria dado valores próximos e errados.

---

## 1. A marca

Quatro barras que sobem — *vertical* — e formam um gráfico — *data*. O ponto
destacado no topo da mais alta lê como marcador de mapa, que é o negócio.

O ponto é **separado** da barra de propósito: a 16px, o que sobrevive de qualquer
símbolo é a silhueta, e um ponto encostado vira só uma barra mais alta.

| arquivo | uso |
|---|---|
| `simbolo.svg` · `simbolo-escuro.svg` | só o símbolo, 32×32 |
| `lockup.svg` · `lockup-escuro.svg` | símbolo + assinatura, 230×64 |
| `favicon.svg` | aba do navegador — **fundo navy fixo** |

**Por que o favicon tem fundo próprio:** a aba não herda o tema da página. Sem o
bloco navy, o símbolo desaparece numa aba clara.

**Por que existe variante escura:** no lockup claro a barra mais alta é navy. Em
fundo escuro ela sumiria — então o gradiente inverte o destino, de navy para
`#EAF2F8`. Nas páginas isso sai de graça: o gradiente aponta para `--vd-tinta`,
que já troca com o tema.

---

## 2. Cor

Três valores são a marca e não se ajustam:

| | | |
|---|---|---|
| navy | `#0B2545` | a tinta, e a superfície do painel no tema escuro |
| teal | `#12B0A0` | o acento |
| azul de apoio | `#12689F` | terceira categoria, quando duas não bastam |

### O teal tem dois papéis, e por isso duas variáveis

`#12B0A0` dá **2,71:1 sobre branco**. Isso reprova para texto, e não é defeito da
cor: é o que ela é. Então:

- `--vd-acento-forma` = `#12B0A0` — logo, barra, preenchimento de mapa. Forma não
  tem exigência de contraste de texto.
- `--vd-acento` = `#0D8478` — texto, link, foco, estado ativo. **4,58:1**, passa AA.

No tema escuro os dois convergem em `#2FD5C0` (8,35:1 sobre o navy), porque ali a
cor clara é justamente quem carrega o texto.

### Medido, não estimado

Todo par que carrega texto foi verificado:

| token | claro sobre `#FFFFFF` | escuro sobre `#0B2545` |
|---|---|---|
| `--vd-tinta` | 15,39:1 | 13,16:1 |
| `--vd-tinta2` | 7,36:1 | 6,41:1 |
| `--vd-tinta3` | 5,48:1 | 4,84:1 |
| `--vd-acento` | 4,58:1 | 8,35:1 |
| `--vd-azul` | 5,99:1 | 6,95:1 |
| `--vd-ambar` | 5,78:1 | 8,40:1 |
| `--vd-vermelho` | 5,42:1 | 6,02:1 |

O `--vd-tinta3` do tema escuro nasceu em `#6B8299` (3,87:1) e subiu para `#7C93A9`
porque rótulos de 9px em versalete são exatamente onde 3,87 dói.

### As rampas de dado não mudaram de direção

Duas, e a diferença entre elas é semântica, não estética:

- **CAR (carência)** — divergente, 1º quintil vermelho. O pior é o mais quente.
- **MAG (magnitude)** — matiz único, o teal da marca. IPTU baixo é o **alvo
  comercial**, não um problema: pintar de vermelho mentiria sobre o que a tela diz.

A marca trocou o **matiz**; a direção é da metodologia (`docs/metodologia-iv.md` §6)
e continua igual.

**Ausência de dado é família própria:** `--vd-semdado`, cinza frio, fora das duas
rampas. Um município sem RREO não é um município com IPTU zero.

---

## 3. Tipografia

| | |
|---|---|
| títulos e texto | **Inter** 400/500/600/700/800 |
| número, código, rótulo em versalete | **IBM Plex Mono** 400/500/600 |

Inter é a grotesca mais próxima do wordmark do PDF. O mono não é enfeite: as
tabelas do painel têm coluna de dinheiro, e `font-variant-numeric: tabular-nums`
é o que faz `R$ 194,3 mi` e `R$ 86,49 mi` alinharem na vírgula.

---

## 4. Como aplicar

`vertical-data.css` é a **fonte única**. As páginas não fazem `<link>` para ele:
trazem uma cópia embutida entre `/* VD:INICIO */` e `/* VD:FIM */`, escrita por:

```bash
python3 marca/aplicar.py              # reescreve o bloco nas páginas
python3 marca/aplicar.py --conferir   # só acusa divergência; sai 1 se houver
```

**Por que embutido e não `<link>`:** painel e coletor são aplicações de arquivo
único de propósito — abrem por `file://` numa prefeitura sem wifi, e o painel é
demonstrado assim. Um CSS irmão obrigatório quebraria isso, e no deploy o painel
fica na raiz enquanto o coletor fica um nível abaixo, então nem o caminho relativo
serviria para os dois.

`painel/deploy/montar.sh` roda `--conferir` antes de montar. Editar o bloco
embutido à mão é o único jeito de as páginas divergirem — e o script recusa
publicar quando isso aconteceu.

Cada página mantém o próprio vocabulário (`--panel` no painel, `--papel` no
coletor) e apenas **aponta** para os `--vd-*`. Os apelidos são declarados uma vez
só: como os `--vd-*` já trocam com o tema, não existe mais um bloco de tema por
página — eram três, viraram um.

### Onde a marca chega

| superfície | o que tem |
|---|---|
| `painel/index.html` | tokens, Inter/Plex Mono, símbolo no cabeçalho, favicon |
| `coletor/index.html` | idem; moldura do telefone em navy, ação em teal escuro |
| laudo HTML (gerado por `m0-conector/validador_completude.py`) | tokens fixos claros, símbolo no cabeçalho — é impresso e anexado a processo |

### Os dois fixos que sobraram, de propósito

No coletor, `.barra` (moldura do telefone) e `.bt.ok` (ação primária) têm hex
literal. Ambos carregam **texto branco**, e um token que clareia no tema escuro
faria o branco sumir por cima. São navy `#0B2545` (15,4:1) e teal escuro `#0B6E64`
(6,1:1) — os dois da própria marca.
