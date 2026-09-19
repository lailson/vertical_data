# Laudo de Completude Cadastral — CADURB/Sinter

- Município (IBGE): **2207702**
- Imóveis na base: **5**
- aptos para transmissão (regras obrigatórias): **3 (60.0%)**
- imóveis com falha obrigatória: 2

## Falhas por regra

- areaTerreno ausente: **1** imóveis
- CEP não tem 8 dígitos: **1** imóveis

## Cobertura de campos estratégicos (opcionais na spec, valiosos no cadastro)

- valor venal: 5 imóveis (100.0%)
- área construída: 5 imóveis (100.0%)
- % titularidade: 5 imóveis (100.0%)
- titular (NI): 4 imóveis (80.0%)
- titular (nome): 4 imóveis (80.0%)
- bairro: 4 imóveis (80.0%)
- titularidade em % (a remessa converte para 0–1): 4 imóveis (80.0%)
- georreferência: 2 imóveis (40.0%)

## Consistência

- inscrições duplicadas: **1** (ex.: ['12346'])
- inscrições cuja titularidade não soma ~100%: **1**
- avisos (não bloqueantes): 5
- CEP conferido contra **18 prefixos** do município (CNEFE/IBGE)

## Regras semânticas (R1–R10, spec do CADURB)

- aptos pelas regras semânticas: **0 de 5** (0.0%)
- preenchimento incompatível entre campos: **4**
- CPF/CNPJ com dígito verificador inválido: **4**
- campo obrigatório ausente: **2**
- formato inválido: **1**
- valor fora do domínio ou duplicado: **1**
- campos que mais bloqueiam: `niTitular`, `areaConstruida`, `areaTerreno`, `tpArquitetonico`, `cep`, `inscricaoImobiliaria`

> **O que a tradução fez**, porque muda o resultado e não pode ficar implícito:
> `temBairro` derivado da presença de bairro — o leiaute exige, a planilha não tem.
> 4 registro(s) com titularidade convertida de porcentagem para fração.
> Tipo de logradouro veio **por extenso**: 5 convertido(s) para o código da tabela 9.6.

## Leitura

Duas camadas rodam sobre a base: a de **completude** (obrigatórios, domínios, tabela de Tipo de Logradouro com 306 códigos do manual v1.12) e a de **regras semânticas** (R1–R10), que confere coerência territorial × predial, faixas, dígito verificador, unicidade de inscrição e soma de titularidade. Aptidão estimada para remessa: **60.0%**. Regras obrigatórias derivadas da spec pública de homologação do CADURB (openapi-homologacao.json, 16/09/2026). Com a credencial do convênio, esta mesma base pode ser revalidada no endpoint oficial `POST /v1/validacao/{ibge}/ui` (modo --online deste validador).

Gerado por validador_completude.py · exemplo_base.csv