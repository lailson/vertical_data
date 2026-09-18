# Adendo — achados que corrigem a Rodada 1

Obtidos por reconhecimento passivo (Certificate Transparency via crt.sh, DNS, HTTP HEAD em
superfície pública, sem autenticação) e por teste direto das APIs públicas.

## A. CORREÇÃO GRAVE: o CERURB TEM camada de API. Ela só não é pública.

Certificate Transparency de `*.foxinline.com` revelou **307 nomes únicos**, entre eles **subdomínios
de API dedicados**:

| Host | DNS | HTTP na raiz | Leitura |
|---|---|---|---|
| `api-exportacao.foxinline.com` | 54.161.19.184 (AWS) | **404** | serviço vivo, rota raiz inexistente |
| `api-cerurbjus-integracao.foxinline.com` | 54.161.19.184 | **502** | serviço registrado, backend fora agora |
| `api-cerurb-relatorioprocesso.foxinline.com` | 54.161.19.184 | **502** | idem |
| `api-mapa.foxinline.com` | 54.161.19.184 | 404 | vivo |
| `api-autenticacao.foxinline.com` | 54.161.19.184 | 404 | vivo |
| `apimapacerurbproprod.foxinline.com` | 54.161.19.184 | 404 | vivo, sufixo "prod" |
| `api-memorial`, `api-spi`, `api-secrel` | mesmo IP | — | demais microserviços |

**Consequência direta:** a conclusão "não há API, logo scraping ou CSV" está ERRADA.
Existe **`api-exportacao`** e existe **`api-...-integracao`**. O pedido à Foxinline deixa de ser
"nos manda um CSV toda semana" e passa a ser **"emita credencial e contrato de uso da API de
exportação já existente"**. Isso é um pedido tecnicamente trivial para eles — o que desloca a
negociação de capacidade técnica para **vontade comercial**. O gargalo é político, não técnico.

## B. CORREÇÃO GRAVE: a Foxinline não é frágil. É incumbente regional.

Dos 307 nomes: **~33 cartórios/ofícios** (1º e 2º ofícios de Teresina, Parnaíba, Luís Correia,
Piracuruca, Corrente, Simplício Mendes, Cocal, União, Altos, Crato, Russas, Barras, Petrolândia,
Serra Talhada, Surubim, Tacaratu, Ibimirim…) e **~236 tenants** que são municípios em **PI, CE, PE,
PA e MA** (Amarante, Campo Maior, Canto do Buriti, Batalha, Beloardim/PE, Bonito/PA, Breves/PA,
Itapipoca/CE, Buriticupu/MA, Assaré/CE…).

A arquitetura do CERURB Pro é **multi-tenant por subdomínio, um por município**
(`barroduro.cerurb`, `saojoaosoter.cerurb`, `santafilomena.cerurb`, `itapipoca.cerurb`,
`cerurb.valefreire`, `cerurb.prourb`, `cerurb.codice`, `cerurb.mapatech`, `sigma.cerurb`).

`cerurbpro.foxinline.com` está **vivo (HTTP 200)**, JSF+PrimeFaces, atrás de **Cloudflare**.
Só a instância `pi-cerurb.foxinline.com` perdeu o registro A — é uma instância, não a empresa.

**Consequência:** a tese do parecer de negócio ("fornecedora pequena, infra fora do ar, pode sumir")
cai. O risco real não é a Foxinline quebrar — é a Foxinline **ser forte o bastante para não precisar
cooperar**, e ter distribuição em 5 estados para lançar o painel dela primeiro. Também significa
que, se houver acordo, o alcance é imediato: ~236 municípios já instrumentados.

## C. A cartografia é subproduto legal obrigatório da REURB
Lei 13.465/2017, **art. 35**: o projeto de regularização exige levantamento **planialtimétrico e
cadastral georreferenciado**, com **ART/RRT**, demonstrando unidades, construções, sistema viário e
áreas públicas. **Art. 40, III**: o CRF traz a **listagem de ocupantes com qualificação e direitos
reais**. Ou seja: o município que faz REURB é obrigado a gerar a base cartográfica, e o custo já está
dentro do contrato de REURB. O módulo de aerolevantamento deixa de ser pré-requisito caro.

## D. O mercado tem incumbentes, incluindo um com o produto exato
- **Geopixel**: +100 municípios, e vende um **"Observatório Municipal de Informações"** — que é
  precisamente o "painel de integração de dados" proposto aqui.
- Também: Geosite CTM, GeoOne, SQLINK, Terracore, Eixo Soluções, CTM Geo.

## E. O ROI é documentado e é o argumento de venda
Recadastramento + PGV: **São Pedro do Iguaçu (PR)** R$ 172,34 mil → R$ 829,91 mil (**+380%**, sem
mudar alíquota); **Santana de Parnaíba (SP)** **+86,6%**; **Amparo (SP)** **+23%** no ano seguinte.

## F. Fontes públicas TESTADAS por mim agora (não é promessa, é resultado)
| Teste | Resultado |
|---|---|
| `servicodados.ibge.gov.br/api/v1/localidades/municipios/2211001` | **200**, JSON completo de Teresina |
| `api/v3/malhas/municipios/2211001?formato=application/vnd.geo+json` | **200**, GeoJSON (5.551 bytes) |
| SICONFI `apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo` RREO-Anexo 03, Teresina 2024 | **200**, 426 itens, **14 linhas de IPTU com valor mensal** (ex.: R$ 46.869.298,89 num mês; R$ 27,2 mi noutro) |
| SICONFI RREO-Anexo 02 | **200**, 1.065 itens |
| ANEEL CKAN `package_show` geração distribuída | **200**, recursos em **CSV e PARQUET** + dicionário de dados |
| IBGE SIDRA v3 agregados | **timeout** — instável, não confiar como dependência dura |

**Consequência:** dá para construir hoje, sem nenhuma negociação, um painel com geometria real,
indicadores censitários por setor, e **a série de arrecadação de IPTU do município** — que é
exatamente o número que interessa ao prefeito e que o protótipo atual não tem.
