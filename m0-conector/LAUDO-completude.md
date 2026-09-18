# Laudo de Completude Cadastral — CADURB/Sinter

- Município (IBGE): **2207702**
- Imóveis na base: **5**
- aptos para transmissão (regras obrigatórias): **3 (60.0%)**
- imóveis com falha obrigatória: 2

## Falhas por regra

- areaTerreno ausente: **1** imóveis
- CEP não tem 8 dígitos: **1** imóveis

## Cobertura de campos estratégicos (opcionais na spec, valiosos no cadastro)

- % titularidade: 5 imóveis (100.0%)
- área construída: 5 imóveis (100.0%)
- valor venal: 5 imóveis (100.0%)
- titular (nome): 4 imóveis (80.0%)
- titular (NI): 4 imóveis (80.0%)
- bairro: 4 imóveis (80.0%)
- titularidade em % (a remessa converte para 0–1): 4 imóveis (80.0%)
- georreferência: 2 imóveis (40.0%)

## Consistência

- inscrições duplicadas: **1** (ex.: ['12346'])
- inscrições cuja titularidade não soma ~100%: **1**
- avisos (não bloqueantes): 5
- CEP conferido contra **18 prefixos** do município (CNEFE/IBGE)

## Leitura

Validação semântica: tabela oficial de Tipo de Logradouro (306 códigos, manual CADURB v1.12) aplicada quando o campo é informado. Aptidão estimada para remessa: **60.0%**. Regras obrigatórias derivadas da spec pública de homologação do CADURB (openapi-homologacao.json, 16/09/2026). Com a credencial do convênio, esta mesma base pode ser revalidada no endpoint oficial `POST /v1/validacao/{ibge}/ui` (modo --online deste validador).

Gerado por validador_completude.py · exemplo_base.csv