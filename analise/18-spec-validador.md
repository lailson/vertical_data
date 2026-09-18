# Especificação do que falta no validador — extraída da spec e do manual

O parecer técnico foi direto: *"validação apenas sintática entrega um relatório de `required` que
qualquer um extrai do Swagger — **bloqueante para justificar R$ 3–5 mil**"*. Isto aqui transforma essa
crítica em lista de trabalho.

## 1. O que a spec OpenAPI JÁ oferece além do `required`

Inventário completo do `api-docs`:

| Tipo de regra | Quantidade | Exemplos |
|---|---|---|
| `pattern` | **3** | CIB `^[a-zA-Z0-9]{8}$` · **CEP `\d{8}`** · CNM do RI `\d{15,16}` |
| `maxLength` / `minLength` | **21** | `inscricaoImobiliaria` 0..45 · `nomeLogradouro` 0..150 · `bairro` 0..30 · `nomeTitular` 0..300 · `numMatriculaRI` 0..15 |
| `minimum` / `maximum` | ~8 | **`anoConstrutivo` 1900..2100** · `percTitularidade` 0.0..1.0 · `percTransacionadoITBI` 0.0..1.0 · `tipoDesativacao` 1..2 · `motivoDesativacao` 1..10 · `cnsRI` 1..999999 |
| `enum` | **1** | só `TipoFalhaDTO` (é resposta, não entrada) |

**São ~32 regras verificáveis automaticamente**, todas extraíveis da spec — e o validador deveria
aplicar todas, não só o `required`.

## 2. O buraco: os campos de domínio são `int32` puro na spec

Estes campos **não têm enum** na spec, mas só aceitam valores de tabelas fechadas:

`tipoImovel` · `tpArquitetonico` · `destinacaoImovel` · `padraoConstrutivo` · `tipoLogradouro` ·
`tipoTitularidade` · `docTitularidade` · `bice` · `tpTransacaoITBI`

**As tabelas estão no Manual Operacional, seção 9 — e só lá:**

| Seção | Tabela | Exemplo verificado |
|---|---|---|
| 9.1 | Tipo Imóvel | `01` Territorial (sem edificação) · `02` Predial (com edificação) · `03` Bem imóvel de características especiais |
| 9.2 | Tipo Arquitetônico | `01` Casa · `02` Apartamento · `03` Vaga de garagem … |
| 9.3 | BICE | |
| 9.4 | Destinação do Imóvel | |
| 9.5 | Padrão Construtivo | |
| 9.6 | Tipo de Logradouro | |
| 9.7 / 9.8 | Tipo de Titularidade / Doc Titularidade | |
| 9.11 / 9.13 | Tipo de Operação / Tipo de Transação | |

**Consequência prática:** um validador que lê só a spec **aceita `tipoImovel = 7`**, que a API vai
rejeitar. As tabelas precisam ser extraídas do PDF e versionadas junto — e essa é justamente a parte
que "qualquer um extrai do Swagger" **não** cobre.

## 3. O vocabulário oficial do laudo

`TipoFalhaDTO` traz o enum que a API usa para classificar erro. **O laudo deve usar exatamente estes
rótulos**, para que o relatório offline fale a mesma língua da resposta oficial:

```
CAMPO_NAO_INFORMADO_OU_NULO
CAMPO_COM_FORMATACAO_INVALIDA
CAMPO_COM_TAMANHO_INVALIDO
DATA_COM_FORMATO_INVALIDO
CAMPO_COM_VALOR_INVALIDO
CAMPO_COM_PRRENCHIMENTO_INCOMPATIVEL   ← typo é do próprio SERPRO; reproduzir como está
CAMPO_COM_DV_INVALIDO
```

Alinhar o laudo a este vocabulário tem efeito comercial direto: quando o município rodar a validação
oficial, os erros terão **os mesmos nomes** do laudo que ele comprou. Isso é o que faz o diagnóstico
parecer — e ser — a antecipação fiel do resultado.

E `CAMPO_COM_DV_INVALIDO` revela que **há campos com dígito verificador** a validar (CPF/CNPJ de
titulares e de partes do ITBI, e o próprio CIB).

## 4. As regras semânticas que a spec NÃO tem e são o valor real do diagnóstico

Nenhuma delas é derivável do Swagger — e são elas que justificam o preço:

| Regra | Por que importa |
|---|---|
| **CEP existe e pertence ao município** | CEP com 8 dígitos passa no `pattern` e ainda assim aponta para outra cidade |
| **`tipoLogradouro` + `nomeLogradouro` conferem com a base dos Correios/IBGE** | logradouro inexistente é rejeição na origem |
| **`inscricaoImobiliaria` única no arquivo** | duplicidade é o erro mais comum em cadastro de planilha |
| **CPF/CNPJ com DV válido** (titulares, transmitentes, adquirentes) | `CAMPO_COM_DV_INVALIDO` existe no vocabulário oficial |
| **Coerência `tipoImovel` × `areaConstruida`** | territorial (01) com área construída **não recebe CIB** — regra explícita do manual |
| **Coerência `tipoImovel` × `tpArquitetonico`** | mesma regra, no sentido inverso |
| **`anoConstrutivo` ≤ ano corrente** | a spec aceita até 2100 |
| **Soma de `percTitularidade` = 1,0 por imóvel** | cada campo é 0..1, mas a soma não é validada |
| **Soma de `percTransac…ITBI` = 1,0** | idem |
| **`areaTerreno` > 0 e dentro de faixa plausível** | a spec não impõe mínimo |
| **Cobertura: % de imóveis do cadastro que sequer têm cada campo obrigatório** | **é a métrica-chave do laudo** — o "% de completude por bloco" |

## 5. Três itens bloqueantes antes de vender o laudo

1. **Pinar a spec por hash.** Ela é `0.0.1-SNAPSHOT` e muda sem aviso. Sem um teste que falhe quando
   divergir, o laudo pode ser emitido contra contrato obsoleto — e o cliente descobre isso na
   validação oficial, o que é o pior lugar possível.
2. **Embutir as tabelas de domínio da seção 9** do manual, versionadas.
3. **Implementar as regras semânticas da seção 4 acima.** Sem elas o produto é um `required`-checker.

## 6. Um item que deixa de ser bloqueante se for descopado explicitamente

O fluxo de geometria (`idLotePonto`/`idLotePoligono`, envio por lote + `/vinculacoes/{idLote}`)
**só é bloqueante se o pitch prometer georreferenciamento**. Duas saídas honestas:
- descope explícito — *"diagnóstico alfanumérico"* — e a geometria vira upsell; ou
- implementar lote + vinculação antes de prometer.

O que não pode é vender "conformidade CIB completa" entregando metade. E lembrando: a metade que
falta é justamente a que a REURB entrega paga por lei.
