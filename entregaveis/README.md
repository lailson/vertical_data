# Entregáveis — itens 2 e 3

## Item 2 — e-SIC (prontos para colar, **você envia**)

| Arquivo | Órgão | Prioridade | Por quê |
|---|---|---|---|
| `esic-1-SEAD-prourbe.md` | SEAD-PI | **1ª — enviar hoje** | único que **decide alvo**; fecha a cega do `cerurb.prourb` que torna "não-tenant" provisório, inclusive para Altos |
| `esic-2-RFB-sinter.md` | Receita Federal | **2ª** | **denominador do mercado**; confirmado que é necessário (ver nota abaixo) |
| `esic-3-SEFAZ-pi.md` | SEFAZ-PI | 3ª, opcional | **versão reduzida** — a v1 encomendava estudo e morreria por "pedido indevido" |
| `esic-4-TCE-pi.md` | TCE-PI | 3ª | **novo** — preço praticado e concorrência no estado; valida o IPTU de Altos |

**Nota que mudou o e-SIC 2:** verifiquei a página de estatísticas do Sinter. Ela **é um painel Looker
Studio** (`/sinter/estatisticas` serve o mesmo HTML do Data Studio), **não há CSV público** com
desagregação por município. O pedido à RFB, portanto, **é necessário** — não redundante, como se
cogitou. O texto já cita o painel e pede o arquivo periódico, se existir.

**Não enviei nada.** Protocolo em nome de terceiros é ação sua, nos portais autenticados.

---

## Item 3 — regras semânticas do laudo

| Arquivo | O que é |
|---|---|
| `regras_semanticas.py` | módulo com **10 regras**, sem dependências externas, testado |
| `dominios_cadurb.json` | **11 tabelas de domínio** extraídas do Manual Operacional v1.12 |

### Por que isso existia como bloqueante
O parecer técnico foi direto: *"validação apenas sintática entrega um relatório de `required` que
qualquer um extrai do Swagger — bloqueante para justificar R$ 3–5 mil"*. As tabelas de domínio **não
estão na spec OpenAPI** (os campos são `int32` puro); estão só no PDF do manual. Um validador que lê
só a spec **aceita `tipoImovel = 7`**, que a API rejeita.

### As 10 regras
| # | Regra | Falha |
|---|---|---|
| R1 | obrigatórios do schema (`inscricaoImobiliaria`, `tipoImovel`, `areaTerreno`, `temBairro`, `cep`, `nomeLogradouro`, `tipoLogradouro`) | `CAMPO_NAO_INFORMADO_OU_NULO` |
| R2 | tamanhos máximos declarados na spec | `CAMPO_COM_TAMANHO_INVALIDO` |
| R3 | CEP com 8 dígitos **e dentro da faixa do município** | `FORMATACAO` / `VALOR_INVALIDO` |
| R4 | **9 campos contra as tabelas de domínio** do manual | `CAMPO_COM_VALOR_INVALIDO` |
| R5 | **territorial (01) com área construída ou tipo arquitetônico NÃO recebe CIB**; predial (02) exige ambos | `..._PRRENCHIMENTO_INCOMPATIVEL` |
| R6 | `areaTerreno` > 0; `anoConstrutivo` em 1900–2100 e ≤ ano corrente | `CAMPO_COM_VALOR_INVALIDO` |
| R7 | **dígito verificador** de CPF/CNPJ | `CAMPO_COM_DV_INVALIDO` |
| R8 | percentuais entre 0 e 1 | `CAMPO_COM_VALOR_INVALIDO` |
| R9 | **unicidade de `inscricaoImobiliaria`** na base | `CAMPO_COM_VALOR_INVALIDO` |
| R10 | soma de `percTitularidade` por imóvel = 1,000 | `..._INCOMPATIVEL` |

Mais a **cobertura por campo** (% de registros preenchidos), que é a métrica-título do laudo.

### Decisões de projeto
- **Vocabulário oficial:** os rótulos de falha são os do enum `TipoFalhaDTO` da API. Quando o
  município rodar a validação oficial, **os erros terão os mesmos nomes do laudo que ele comprou**.
  *(O typo em `PRRENCHIMENTO` é do SERPRO e foi mantido de propósito.)*
- **Impeditiva × atenção:** só as impeditivas entram no cálculo de `percentual_apto`. Ano construtivo
  futuro, por exemplo, é atenção — não bloqueia a transmissão.
- **Sem dependências.** Roda em Python 3.9+ puro.
- **`faixas_cep` é injetada por contexto** — não embuti base de CEP; passar as faixas do município
  via `ctx={"faixas_cep": [(64000000, 64099999)]}`.

### O que ainda falta (não coberto por este módulo)
1. **Pin da spec por hash** com teste de divergência — a spec é `0.0.1-SNAPSHOT` e muda sem aviso.
2. **Fluxo de geometria** (`idLotePonto`/`idLotePoligono` + `/vinculacoes/{idLote}`) — decidir entre
   descope explícito ("diagnóstico alfanumérico") ou implementar antes de prometer.
3. **Rodar contra cadastro real** — é o único item que a venda não resolve, e o risco é a primeira
   execução real acontecer no cliente.
4. **Mapeamento de colunas do ERP municipal → schema CADURB** — é aqui que estão os 1–2 dias de
   ingestão por município.

---

## Correções pendentes nos documentos comerciais
Diffs prontos em `../analise/`:
- `21-correcoes-credencial.md` — redações honestas dos itens 2, 3 e 4 da credencial (o item 4,
  *"sem índices de pesos arbitrários"*, é o mais urgente) + "Por que agora" reescrito com o ITBI
- `22-revisao-tr-v2.md` — encoding corrompido, gatilho dos 70%, mini-diagnóstico fora do TR,
  cláusulas de PI e de calibração, art. 75 §3º
