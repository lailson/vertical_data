# CADURB — spec OpenAPI obtida e risco de credencial resolvido

Verificado em 2026-09-16, contra o ambiente de homologação do SERPRO.

## 1. A spec OpenAPI é pública e baixável

```
GET https://hom-sinter2-cadurb.np.estaleiro.serpro.gov.br/api/v3/api-docs   → HTTP 200, 64.498 bytes
GET https://hom-sinter2-cadurb.np.estaleiro.serpro.gov.br/api/swagger-ui/index.html → HTTP 200
```

OpenAPI **3.0.1** · *"API de inserção, alteração, exclusão e consulta de Unidades Imobiliárias"* ·
**15 endpoints, 87 schemas**.

### Endpoints
| Método | Rota | Função |
|---|---|---|
| **POST** | **`/v1/validacao/{codigoIbge}/ui`** | **valida uma UI sem inserir** |
| POST | `/v1/{codigoIbge}/ui` · `/uis` | insere uma · **múltiplas** |
| PUT | `/v1/{codigoIbge}/ui/{cib}` · `/uis` | altera uma · múltiplas |
| PUT | `/v1/{codigoIbge}/ui/desativacao` · `/uis/desativacao` | desativa uma · múltiplas |
| GET | `/v1/ui/{cib}` · `/v1/{codigoIbge}/ui/{inscricaoImobiliaria}` · `/uis` | consultas |
| GET | `/v1/{codigoIbge}/arquivo/{idArquivo}/consulta` (+ `/depara`) | resultado de lote |
| GET | `/v1/{codigoIbge}/consulta/{idRequisicao}` · `/elemento/{idElemento}/payload` | rastreio |
| GET | `/v1/{codigoIbge}/vinculacoes/{idLote}` | vinculações de lote |

## 2. O risco levantado pelo parecer técnico: resolvido, e para os dois lados

**A favor:** o manual é explícito na tabela de pré-requisitos —
**`Certificados: Não se aplica`**. A autenticação é **token Bearer via OAuth2 client credentials**,
não certificado ICP-Brasil, e o payload é `application/json`, não arquivo assinado. A hipótese de que
o envio em lote exigiria ICP-Brasil **não se confirma**. O ICP-Brasil é exigido na **adesão ao
convênio** (assinar o Termo no e-CAC) — etapa do município, não da integração.

**Contra:** testei `POST /v1/validacao/2200400/ui` sem token → **HTTP 403 Forbidden**. O
`securitySchemes` declara `oauth2` e todos os endpoints herdam. **Sem credencial não se exercita
nada**, nem o endpoint de validação.

**Conclusão: a spec é pública, a execução é fechada.** O parecer técnico está certo no essencial —
não dá para testar de verdade sem credencial vinculada a convênio — mas o plano B é muito melhor do
que "construir às cegas": **temos o contrato OpenAPI completo**, com os 87 schemas, e dá para gerar
cliente tipado, validador local de payload e suíte de testes contra a spec, tudo antes da credencial.

## 3. Descoberta que muda o desenho do conector

Existe **`POST /v1/validacao/{codigoIbge}/ui`** — endpoint dedicado a **validar sem inserir**.
Isso é exatamente o que um produto de conformidade precisa: rodar o cadastro inteiro do município
contra o validador oficial e produzir o laudo de completude **antes** de qualquer envio real.

**O "diagnóstico de conformidade de R$ 3–5 mil" tem um endpoint oficial dedicado a produzi-lo.**

## 4. A geometria não vai inline

`DadosGeoDTO` tem apenas dois campos: **`idLotePonto`** e **`idLotePoligono`** — referências a lotes
geométricos enviados por outro caminho. A remessa da UI carrega o *ponteiro*, não a geometria.

**Consequência para o conector:** há dois fluxos a implementar, não um — o de dados alfanuméricos
(JSON por UI ou em lote) e o de geometria (por lote, com vinculação posterior via
`/vinculacoes/{idLote}`). O plano assumia um fluxo unitário. **Some esforço ao conector**, e confirma
por que o manual fala em envio "alfanumérico ou alfanumérico + georreferenciado".

## 5. Ordem de trabalho recomendada (revisada)

1. **Gerar cliente e validador local a partir da spec** — não depende de ninguém, é possível hoje.
2. **Em paralelo, obter a adesão do piloto** (é o caminho crítico real: Termo com ICP-Brasil →
   processo no e-CAC → publicação no DOU → token). **Semana 1, não semana 4.**
3. **Construir o "laudo de completude"** rodando o cadastro contra o validador local — que é o
   produto vendável, e não depende de token.
4. Só então integrar de verdade.

O item 3 é o achado prático: **o produto de entrada pode ser construído e vendido antes de haver
qualquer credencial**, porque o laudo é gerado contra o schema, não contra o servidor.
