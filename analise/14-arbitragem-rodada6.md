# Arbitragem rodada 6 — método do SICONFI documentado, tenants corrigidos

## 1. A API do SICONFI está funcionando. Método exato, para revalidação

Testado em 2026-09-16, duas variantes de caminho, ambas **HTTP 200 com dado idêntico**:

```
https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo
https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rreo
```

**Parâmetros exatos usados (todos obrigatórios):**
```
an_exercicio=2025
nr_periodo=6
co_tipo_demonstrativo=RREO
no_anexo=RREO-Anexo%2003      ← o %20 é imprescindível; "RREO-Anexo 03" sem encode falha
co_esfera=M
id_ente=<código IBGE de 7 dígitos>
```

Header `User-Agent` de navegador e `Accept-Encoding: identity` (sem isso, o IBGE às vezes devolve
gzip e o parser quebra — problema observado na API de localidades, não no SICONFI).

**Extração do IPTU:** filtrar `items` onde `conta == "IPTU"` **e** `coluna` começa com `<MR`
(as 12 colunas de meses móveis; somar dá o acumulado 12 meses). Filtrar por `coluna` é o que evita
somar linhas de totalização e duplicar valores.

**Resultado de controle:** Teresina 2025 → 427 itens, 12 linhas de IPTU,
**R$ 166.321.115,49** — reproduzido hoje, idêntico ao extraído ontem.

Se o teste da outra sessão voltou vazio para Teresina, a causa está nos parâmetros (o mais provável é
o encode do `no_anexo`) ou em instabilidade momentânea — não no endpoint.

## 2. Os 8 RREO ausentes: NÃO foi falha silenciosa — e o achado se refina

A suspeita era legítima (o script original mascarava exceções com `except Exception`). Reexecutei
**com erro explícito**, por município: todos retornaram **HTTP 200 com `items: []`**. Nenhum timeout,
nenhum HTTPError. A API responde e diz que não há dado. Controle: **Altos** retornou 116 itens na
mesma execução.

Testando três exercícios, o achado se divide em dois grupos com força de sinal diferente:

| Município | 2025 | 2024 | 2023 | Leitura |
|---|---|---|---|---|
| União | 0 | 0 | 0 | **nunca entregou em 3 anos** |
| Água Branca | 0 | 0 | 0 | **nunca entregou em 3 anos** |
| Baixa Grande do Ribeiro | 0 | 0 | 0 | **nunca entregou em 3 anos** |
| Lagoa do Barro do Piauí | 0 | 0 | 0 | **nunca entregou em 3 anos** |
| Simplício Mendes | 0 | 0 | 0 | **nunca entregou em 3 anos** |
| Luís Correia | 0 | 394 | 373 | entregou antes, falhou em 2025 |
| Piracuruca | 0 | 364 | 0 | intermitente |
| Ilha Grande | 0 | 317 | 312 | entregou antes, falhou em 2025 |

**Correção à minha formulação anterior:** eu tratei os 8 como um bloco. São dois grupos.
**Cinco nunca entregaram em três exercícios** — sinal forte de incapacidade estrutural, e o melhor
lead do Segmento B que esta análise produziu. **Três entregavam e pararam em 2025** — sinal moderado,
que pode indicar troca de gestão ou perda de equipe (e o prazo de entrega do 6º bimestre de 2025
venceu em jan/2026, há oito meses: não é atraso de consolidação).

**Ressalva mantida:** ausência do RREO Anexo 03 não é prova absoluta de não-entrega — o município
pode ter entregue em outra periodicidade ou anexo. Confirmar no portal web antes de uso comercial.

## 3. Tenants: ela está certa. Eu superincluí dois, e a causa é identificável

Meu cruzamento normalizava o **último rótulo** do subdomínio, o que gera falso positivo em host de
cartório com padrão `<produto>.<municipio>`. Refiz olhando o **host completo**:

| Município | Hosts encontrados | Veredito |
|---|---|---|
| Piripiri | `piripiri` + `piripiri2oficio` | **tenant municipal** |
| Campo Maior | `campomaior`, `notas.campomaior` | **tenant municipal** |
| Corrente | `corrente` + `1oficiocorrente` | **tenant municipal** |
| União | `uniao` + `2oficiouniao` | **tenant municipal** |
| Brasileira | `brasileira` | **tenant municipal** |
| Ilha Grande | `ilhagrande` | **tenant municipal** |
| **Barras** | `cartoriobarras`, `notarial.barras`, `registral.barras` | **só cartório** ❌ era falso positivo meu |
| **Água Branca** | `registral.aguabranca`, `saopedroaguabranca` | **só cartório** ❌ era falso positivo meu |
| Altos | `2oficioaltos` | só cartório |
| Paulistana | `paulistana2oficio` | só cartório |

**São 6 tenants municipais, não 8** — exatamente a lista dela.

**Detalhe sobre Água Branca:** o host `saopedroaguabranca.foxinline.com` é
**São Pedro da Água Branca — MARANHÃO**, município distinto. Meu match por substring casou
"aguabranca" dentro dele. Dois erros diferentes produzindo o mesmo falso positivo.

## 4. A cega estrutural do PROUrbe — aceita integralmente

`cerurb.prourb.foxinline.com` é host único: municípios atendidos pelo programa estadual da SEAD **não
ganham subdomínio próprio** e são invisíveis a este método. **"Não-tenant" é sempre provisório.**

Isso deve constar como ressalva fixa em qualquer uso comercial da lista. O fechamento dessa lacuna
depende da relação de adesões ao PROUrbe junto à SEAD-PI (e-SIC ou portal da transparência estadual)
— é a pendência de campo mais barata e de maior retorno que resta.

## 5. População de Altos
Censo 2022: **47.453**. O valor 46.826 que usei vem do campo `populacao` do próprio retorno do
SICONFI, que é **estimativa anual do IBGE**, não o Censo. Fontes diferentes, ambas válidas; usar o
Censo em material externo. O rank (7º do PI) confere nas duas.

## 6. O que sobrevive

**Altos segue como melhor candidato a piloto fora da capital** — e agora com evidência mais limpa:
17 bairros, **nenhum host municipal no CT** (só o 2º Ofício), RCL R$ 61,3 mi, IPTU R$ 245 mil
(fronteira A/B), 7º município do estado. Ressalva PROUrbe a confirmar.

**Paulistana** confirma como segundo (17 bairros, só host de cartório).

**Campo Maior sai da frente:** é tenant municipal confirmado **e** Segmento A — dois motivos.

**Nota sobre Altos:** o retorno do SICONFI traz apenas **2 linhas de IPTU** (contra 12–14 dos demais),
o que sugere preenchimento parcial do demonstrativo. Vale confirmar o valor no TCE-PI antes de levar
a número para reunião.
