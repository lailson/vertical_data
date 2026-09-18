# M0 — Conector CADURB e Validador de Completude

Construído a partir da **spec pública de homologação** (16/09/2026), sem convênio
e sem custo, conforme o plano. Caminho para a primeira receita: o
**laudo de completude** (`validador_completude.py`) funciona **hoje, offline**;
com a credencial, a mesma base é revalidada no endpoint oficial
`POST /v1/validacao/{ibge}/ui`.

## Arquivos

| Arquivo | O que é |
|---|---|
| `spec/openapi-homologacao.json` | Spec OpenAPI capturada de `hom-sinter2-cadurb.np.estaleiro.serpro.gov.br/api/v3/api-docs` |
| `cadurb_client.py` | Cliente da API (token OAuth client-credentials + 12 endpoints). Sem credencial roda em dry-run contra a URL real |
| `validador_completude.py` | **O produto do diagnóstico**: lê o cadastro municipal em CSV, aplica as regras obrigatórias da spec + regras semânticas, gera `LAUDO-completude.md`. Flag `--online` para a validação oficial |
| `exemplo_base.csv` | Base de demonstração (5 imóveis, mistura de válidos e com falha) |

## Endpoints mapeados na spec (homologação)

`POST /v1/validacao/{ibge}/ui` (valida sem gravar — **a porta do laudo**) ·
`POST /v1/{ibge}/uis` (lote NDJSON) · `PUT /v1/{ibge}/uis` ·
`GET /v1/{ibge}/ui/{inscricao}` · `GET /v1/ui/{cib}` · `GET /v1/{ibge}/uis` ·
`GET /v1/{ibge}/consulta/{idRequisicao}` · `GET /v1/{ibge}/arquivo/{id}/consulta(/depara)` ·
desativações e consulta de vinculações.
Obrigatoriedade da UI: `DadosGeraisImovel{areaTerreno, inscricaoImobiliaria, temBairro,
tipoImovel}` + `EnderecoImovel{cep, nomeLogradouro, tipoLogradouro}`.

## Como usar

```bash
# 1) Laudo hoje, sem credencial (o que se vende no diagnóstico de R$ 3–5 mil)
python3 validador_completude.py cadastro_do_municipio.csv --ibge 2200600

# 2) Cliente em dry-run (mostra a chamada exata contra a homologação)
python3 cadurb_client.py validar ui.json --ibge 2200600

# 3) Com credencial (após adesão gratuita — sinter.df.cocad@rfb.gov.br)
export CADURB_CLIENT_ID=... CADURB_CLIENT_SECRET=...
python3 validador_completude.py base.csv --ibge 2200600 --online
```

## Credencial

A adesão ao convênio Sinter é gratuita; o token OAuth (client_credentials) é
fornecido pelo time do CADURB. Contato: **sinter.df.cocad@rfb.gov.br**
(URL de produção: seção 12.5 do Manual Operacional, `dados/bruto/manuais/manual_cadurb.pdf`).

## Aprendizados de build

- A spec é pública em `/api/v3/api-docs` (Springdoc) — o portal
  `docs.receitafederal.gov.br/sinter` citado pela RFB está 404.
- Regras obrigatórias e tipos foram extraídas **da própria spec** (não copiadas à mão),
  então o validador acompanha mudanças: se a spec evoluir, regenerar as regras.
