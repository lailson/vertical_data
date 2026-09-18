# Análise de Viabilidade — Dashboard de Gestão Municipal (projeto CERURB/Reurb)

**Data:** 15/09/2026 · **Status:** avaliação pré-decisão
**Observação:** os arquivos referenciados (`/home/lailson/projetos/projeto-cerurb/.orca/drops/...`) não existem nesta máquina; a análise do protótipo usa o resumo fornecido na conversa.

---

## 1. Resumo executivo (veredito)

**O projeto é viável, mas não do jeito que está premisso.** O dashboard não pode ser construído sobre "consumir dados do CERURB" — isso não existe tecnicamente (não há API pública) nem juridicamente (o contrato do TJ-PI com a Foxinline veda repasse de dados a terceiros). A saída correta é exatamente a que você intuiu:

1. **Fase 1 — Dashboard 100% sobre bases públicas** (IBGE por bairro, INEP por escola, ANEEL energia solar, TCE-PI/SICONFI fiscal, SINISA saneamento, OSM/ESRI cartografia). Isso já sustenta um produto demonstrável **hoje, sem nenhuma negociação**.
2. **Fase 2 — Módulo de coleta próprio** (família, saúde, educação, avaliação do imóvel), alimentando base própria com consentimento LGPD. É o diferencial competitivo e a independência estratégica.
3. **Fase 3 — ML/preditivo/chat** sobre o data warehouse resultante.

**Condição de entrada (go/no-go):** se a contraparte insistir que o núcleo do projeto é "puxar dados do CERURB", o projeto só é viável com acordo formal (município/TJ como controlador autorizando). Sem isso, redirecionar o escopo para o modelo acima ou não entrar.

---

## 2. Respostas diretas às perguntas levantadas

### "Existe API no CERURB? Podemos criar usuários e acessar?"

**Não existe API pública.** Verificado por inspeção passiva em 15/09/2026:

- O sistema em produção é o **CERURBJus** (`https://cerurbjus.tjpi.jus.br/`, contexto `/cerurb-usucapi/`), do TJ-PI, desenvolvido pela **Foxinline** (Parnaíba-PI, CNPJ 29.139.662/0001-29).
- Stack: **Java/Jakarta Faces + PrimeFaces 15**, autenticação server-side (`j_security_check`). Testamos `/api`, `/swagger`, `/openapi.json`, `/graphql`, `/rest`, `/mapa.xhtml`, `/painel` — **todos 404**. Sem bundle JS de aplicação para inspecionar (não é SPA).
- O Termo de Referência da SEAD-PI confirma: a "API" é a **CERURB-WEB interna** (armazenamento dos dados coletados), sincronizada com o app **CERURB-MOBILE**. Integrações existentes: PJe, cartórios, Receita Federal, OAB. Tudo privado.
- **Existe cadastro público aberto** (`cadastrar.xhtml`: nome, CPF, telefone, e-mail, login) — é porta para advogados/agentes credenciados, não acesso a dados. Não criamos conta (limite ético/legal).
- **O "baixar dados pelo navegador/Playwright" de antes não se aplica mais**: a porta atual é login + dados pessoais de posseiros protegidos por cláusula de sigilo. Scraping aqui = violação de contrato + LGPD (dados pessoais/sensíveis de titulares que não consentiram com vocês). Não é rota.

### "Pegamos dados do CEHURB?"

**CEHURB não existe no Piauí** — é a companhia habitacional do Espírito Santo (provável mistura de siglas). No contexto local os órgãos corretos são:
- **Estadual:** ADH-PI (Agência de Desenvolvimento Habitacional, sucessora da COHAB-PI)
- **Municipal (Teresina):** SEMDUH (habitação) e **ETURB** (regularização fundiária — quem opera o Reurb em Teresina)
- No mundo fundiário, a sigla parecida real é **CERURBJus** (TJ-PI).

### "Dados de energia renovável / usina fotovoltaica / investimento?"

**Sim, públicos e atualizados.** ANEEL Dados Abertos (`https://dadosabertos.aneel.gov.br/`):
- Dataset **Relação de Empreendimentos de Geração Distribuída** — CSV/Parquet (~110 MB, Brasil), granularidade por **empreendimento** com município, potência, data de conexão, fonte. Atualizado em 15/09/2026 (dia da pesquisa). Dataset específico de **fotovoltaica** com informações técnicas.
- Como não há consulta por linha, o fluxo é baixar o arquivo e filtrar por município. Permite curvas de crescimento de geração distribuída por bairro/município e **proxy de investimento** (potência instalada × custo médio R$/kWp).
- Complementos: painel EPE de micro/minigeração (`https://www.epe.gov.br/pt/publicacoes-dados-abertos/publicacoes/painel-de-dados-de-micro-e-minigeracao-distribuida-pdgd-`) e o catálogo de empreendimentos de geração centralizada (usinas) no mesmo portal ANEEL.
- Distribuidora local: **Equatorial Piauí** (ex-CEPISA). Iluminação pública em Teresina é PPP municipal — dados por bairro só via e-SIC.

### "Temos outras bases? Base pública cruzando dados?"

Sim — inventário verificado na seção 4. O cruzamento **por bairro** já é possível hoje com IBGE (Censo 2022 divulga agregados por bairro e setor, incluindo renda) + INEP por escola (geolocalizada) + ANEEL por empreendimento (endereçável).

---

## 3. O que o CERURB realmente é — e o que isso muda no projeto

**Contexto em Teresina:** quem faz Reurb na capital é a **ETURB** (LC 5.444/2019, Lei Federal 13.465/2017; programa "Teresina é REURB+"; 1.600 títulos em entrega em 2026). O CERURBJus é o sistema do **TJ-PI** (Programa Regularizar, Provimentos 89 e 96/2023), apresentado à ETURB como ferramenta de celeridade. Ou seja: no cliente-provável (Teresina), o CERURB é ferramenta do Judiciário, não a base municipal.

**Quem usa CERURB (documentado):**
- **TJ-PI** — Contrato 156/2023 (R$ 1,19 mi, prorrogável até 10 anos). **Cláusula 4.1.1: o TJ pode autorizar uso por outros órgãos** — porta formal para acesso municipal.
- **Governo do PI (SEAD)** — comprou o CERURB para o PROUrbe (R$ 400 mil, 1ª etapa).
- **Prefeitura de Parnaíba**, cartório 4º Ofício de Parnaíba, **ADECE-Ceará**.
- Via Programa Regularizar: **Guaribas, N. Sra. de Nazaré e Floresta do Piauí** 100% regularizados (79 mil famílias no estado); **Teresina, Tanque do Piauí, Juazeiro do Piauí e Coivaras** em tramitação.

**O que o CERURB coleta (cláusula 3.4 do contrato):** núcleos/quadras/lotes/edificações, **cadastro socioeconômico com renda familiar e programas sociais**, características do imóvel, documentos digitalizados, **shapefiles/polígonos georreferenciados e memoriais descritivos**. Isso confirma sua hipótese: a renda familiar **é** campo do sistema, e o dado é rico — mas **inacessível sem convênio**. A cláusula de sigilo veda "repasse das informações a outras empresas".

**Rotas reais para dados CERURB (se o projeto exigir):**
1. **Município adere ao Programa Regularizar** (formulário APPM/TJ-PI) e solicita acesso/view via cláusula 4.1.1.
2. **e-SIC ao TJ-PI/SEAD** para dados agregados.
3. **API DataJud do CNJ** + Consulta Pública PJe — métricas processuais de Reurb (nº de processos, tempo, sentenças) **públicas agora**.
4. **Negociação direta com a Foxinline** (contatos: notario@foxinline.com, contato@foxinline.com, +55 86 98837-4045; fiscal do contrato TJ-PI: yara.mota@tjpi.jus.br). Atenção: a Foxinline **já vende "Central CERURB" para gestores municipais** — é parceira em potencial **e concorrente direta** no dashboard.

**Sobre sua ideia do município repassar a base cartográfica quando contratar:** procede. Os dados de Reurb produzidos nesses contratos pertencem aos entes públicos; um contrato municipal pode incluir cessão de uso dos geodados (você como operador, município como controlador). É o mesmo modelo recomendado para o módulo de coleta.

---

## 4. Inventário de bases verificadas (15/09/2026, URLs testadas)

### Federais

| Domínio | Fonte | Granularidade | Acesso | Situação |
|---|---|---|---|---|
| População, renda, alfabetização, domicílios | IBGE Censo 2022 — agregados por **bairro e setor** (`ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/` + pasta de renda) | Bairro/setor | Download CSV/XLSX/GPKG | OK (atualizações 2026) |
| Indicadores por município | IBGE SIDRA API (`servicodados.ibge.gov.br/api/v3/agregados/...`) | Município | API JSON | OK (1.388 agregados) |
| Malhas de bairros/setores | IBGE (`geoftp.ibge.gov.br/.../bairros/shp/UF/PI_bairros_CD2022.zip`) | Bairro/setor | SHP/GPKG/KML | OK |
| Educação | INEP Censo Escolar 2025, IDEB 2025, distorção idade-série 2006–2025 (`download.inep.gov.br`) | Escola | Download CSV (API morreu) | OK |
| Saúde | DEMAS/MS API (`apidadosabertos.saude.gov.br`, ex.: `/v1/vacinacao/doses-aplicadas-pni-2026`) + TabNet SIM/SINASC | Município; bairro só via microdados DBC | API JSON + TabNet | OK (APIs antigas mortas) |
| Energia (GD solar/usinas) | ANEEL (`dadosabertos.aneel.gov.br/dataset/relacao-de-empreendimentos-de-geracao-distribuida`) | Empreendimento | CKAN + arquivo CSV/Parquet | OK (atualizado na data) |
| Saneamento | SINISA (`sinisa.cidades.gov.br`, painel 2025) + série SNIS legada (`dadosabertos.cidades.gov.br`) | Município/prestador | Portal/planilhas | SNIS encerrado 2023 |
| Fiscal/IPTU/arrecadação | SICONFI API (`apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/`) e **TCE-PI com API documentada** (`sistemas.tce.pi.gov.br/api/portaldacidadania/docs/`) | Município/unidade gestora | API JSON | OK |
| IDHM/indicadores sociais | Atlas Brasil (`atlasbrasil.org.br/consulta/planilha`, domínio antigo morto) | Município + UDH | Planilha | OK |
| Cartografia colaborativa | OpenStreetMap/Overpass (Teresina: 21.589 vias, 125 bairros) + ESRI World Imagery (ortofotos grátis c/ atribuição; tiles do Google não são livres) | Logradouro/bairro | API/tiles | OK |

### Locais (Teresina)

| Domínio | Fonte | Situação |
|---|---|---|
| **Cartografia oficial** | SEMPLAN "Mapas de Teresina" (`teresina.pi.gov.br/semplan/mapas-de-teresina/`) — shapefile completo, bairros 2013 (KMZ), perímetro urbano 2022, zoneamento, mapa PDF de esgoto 2016 e posteamento 2016 | **Pública, download direto** (maior ativo local) |
| Reurb (núcleos, títulos) | ETURB | Sem catálogo público → **e-SIC** |
| Habitação/cadastro | SEMDUH (novo Cadastro Municipal de Habitação em preparação); ADH-PI | **e-SIC** |
| Saneamento por bairro | Águas de Teresina (Aegea; esgoto 19%→59% 2017-2024 agregado) | Agregado público; por bairro → **e-SIC** |
| Iluminação pública | PPP municipal / SEMOP | **e-SIC** |
| Educação municipal | SEMEC | Sem datasets → **e-SIC** (INEP cobre por escola) |
| Canal legal | **e-SIC Teresina no ar** (`esic.teresina.pi.gov.br`, Decreto 14.605/2014); LAI: 15 dias + 10 de prorrogação | Funcionando |
| Portal dados abertos municipal | **Não existe** (`dadosabertos.teresina.pi.gov.br` fora do ar); PI Digital vazio | Gap = oportunidade |

**Descontinuados confirmados** (importante para o plano técnico): `api.opendata.inep.gov.br`, `api.datasus.gov.br`, `imunizacao.esusab.ufsc.br`, `apis.tesouro.net`, `atlasbrasil.ipea.gov.br`, app série histórica SNIS, ENEM por Escola pós-2015.

---

## 5. Cruzamento com o protótipo e a proposta (gaps)

Sua análise dos módulos ausentes está correta e a pesquisa a reforça:

| Módulo da proposta | Viabilidade real encontrada |
|---|---|
| **Base cartográfica (drone/ortofoto)** | Não precisa de drone para começar: IBGE 2022 + SEMPLAN + OSM + ESRI Imagery entregam mapa real de bairros/quadras viárias. Drone/aerolevantamento vira **serviço premium** por município contratante (com cessão dos geodados). O "grade ilustrativa" do protótipo pode ser trocada por geometria real **já na próxima versão** — ganho imediato de credibilidade. |
| **CTM (cadastro multifinalitário)** | Depende de dado municipal (SEMDUH/ETURB) → e-SIC + parceria. **Atenção: a Lei Municipal 6.383/2026 (jul/2026) já institui CTM + SIG + IDE na SEMPLAN** — o município está montando exatamente isso. |
| **PGV (valores venais)** | Nenhuma base pública tem valor venal por imóvel. Só via convênio com o fisco municipal (SEMFIN) ou coleta própria. Manter como módulo condicionado. |
| **IPTU/arrecadação** | **Viável em nível municipal agora** via TCE-PI (API) e SICONFI. Contexto: o TCE-PI auditou o IPTU de Teresina e a PMT **suspendeu a cobrança do IPTU 2026** para imóveis edificados — tema politicamente quente e ótimo argumento de venda de "justiça fiscal", mas exige cuidado no discurso. |
| **Território do protótipo (18 bairros)** | Teresina oficial tem **123 bairros (IBGE 2022) / 5 SDUs**. Os "18 bairros" não batem com a divisão oficial — confirmar com o cliente qual município/área é o alvo real (Teresina capital? interior via TJ-PI? outro estado?). A estratégia de dados muda completamente conforme a resposta. |

---

## 6. LGPD — parâmetros para o desenho

- **Bases públicas agregadas** (IBGE, INEP, ANEEL, SICONFI): uso livre — sem dado pessoal.
- **Dados de família/saúde/renda individual**: só com **consentimento na coleta**, finalidade declarada, e o **município como controlador** quando houver contrato (vocês como operadores). É o modelo do módulo de coleta.
- **Dados CERURB**: pessoais + cláusula contratual de sigilo. Só via acordo formal entre entes.
- **Chat conversacional/ML**: manter dados pessoais fora do contexto do LLM — consultar o warehouse agregado (text-to-SQL/RAG sobre agregados). Modelos preditivos familiares só quando a coleta própria escalar.
- **Microdados SIM/SINASC por bairro** e **INEP sensível**: tratamento de anonimização antes de exibir.

---

## 7. Riscos estratégicos

1. **Foxinline é concorrente e fornecedora ao mesmo tempo.** Ela tem os dados e já vende "Central CERURB" para gestores municipais. Se o projeto depender dela, vocês ficam downstream. **Mitigação:** posicionar como camada que ela não tem (multi-fonte: saúde, educação, fiscal, energia, ML/chat) ou negociar parceria explícita (eles ficam no fundiário, vocês na inteligência territorial).
2. **Lei 6.383/2026 (CTM/IDE na SEMPLAN)**: janela de oportunidade (prefeitura com agenda de dados) e risco (ela pode internalizar a plataforma ou licitar). Time-to-market importa — e uma licitação futura favorece quem já opera.
3. **Modelo territorial indefinido** (18 bairros × 123 bairros × qual município?): decidir o piloto antes de prometer indicadores.
4. **Dependência de e-SIC** para tudo que é municipal por bairro (prazo 15+10 dias, qualidade variável). Mitigação: módulo de coleta própria.

---

## 8. Plano recomendado

**Fase 0 — Due diligence (2–4 semanas, custo baixo):**
- e-SIC em paralelo à ETURB (base Reurb georreferenciada), SEMDUH (cadastro habitacional), SEMOP (pontos de luz), Águas de Teresina (cobertura por bairro). Prazo ~30 dias.
- Reunião com a Foxinline (contatos acima) para entender a "Central CERURB" e espaço de parceria/integração.
- Confirmar com o proponente (Eric) **qual município é o cliente-alvo** e se ele aceita a premissa "dados públicos + coleta própria" no lugar de "consumir CERURB".

**Fase 1 — Dashboard sobre bases públicas (imediato):**
- Camada geoespacial: bairros IBGE 2022 (geometria real, PostGIS) + ESRI/OSM de fundo.
- Indicadores por bairro: IBGE Censo 2022 (renda, domicílios, alfabetização, densidade), ANEEL GD solar (crescimento por município/bairro via CEP), INEP por escola (geocodificada), TCE-PI/SICONFI (arrecadação municipal), SINISA (saneamento), DataJud (processos de Reurb).
- Isso substitui a "grade ilustrativa" por dados reais sem nenhuma dependência externa.

**Fase 2 — Módulo de coleta próprio (o diferencial):**
- Formulário de campo que estende o modelo CERURB além do imóvel: família, saúde, educação, fiscal/tributos, avaliação do imóvel.
- Saída em padrões interoperáveis: SHP/UTM + memorial descritivo (mesmo padrão que cartórios/TJ usam) + schema de sincronização.
- Contrato municipal com cessão de geodados e município como controlador LGPD.

**Fase 3 — ML/preditivo/chat:**
- Preditivo sobre séries públicas (arrecadação, GD solar, cobertura de esgoto × IDHM).
- Chat (text-to-SQL/RAG) sobre o warehouse agregado.
- Modelos familiares quando a coleta escalar.

---

## 9. Critérios de decisão (go/no-go)

**ENTRAR se:** o proponente aceitar o escopo "bases públicas + coleta própria" como núcleo; houver um município-piloto definido; e idealmente um contrato (mesmo pequeno) que formalize acesso a dados municipais/cessão de geodados.

**RENEGOCIAR ESCOPO se:** a premissa continuar sendo "integração com CERURB" — nesse caso exigir carta/intenções formalizando que o município ou TJ autorizará o acesso (cláusula 4.1.1 do contrato TJ-PI é a porta).

**NÃO ENTRAR se:** o projeto preservar a promessa de consumir dados do CERURB sem acordo formal, ou competir frontalmente com a Foxinline no nicho dela (ferramenta fundiária de escritório) sem parceria.

---

## 10. Fontes principais

- CERURBJus (sistema): https://cerurbjus.tjpi.jus.br/ · App: https://play.google.com/store/apps/details?id=com.foxinline.cerurbjus_app
- Contrato TJ-PI/Foxinline (PNCP): https://pncp.gov.br/pncp-api/v1/orgaos/06981344000105/contratos/2023/44/arquivos/1
- TR SEAD-PI CERURB/PROUrbe (PNCP): https://pncp.gov.br/pncp-api/v1/orgaos/06553481000149/compras/2024/469/arquivos/1
- Programa Regularizar TJ-PI: https://www.tjpi.jus.br/portaltjpi/programa-regularizar/ · CNJ (79 mil famílias): https://www.cnj.jus.br/programa-regularizar-tribunal-piauiense-garante-emissao-do-registro-de-imoveis-a-79-mil-familias/
- ETURB regularização fundiária: https://www.teresina.pi.gov.br/eturb/regularizacao-fundiaria/
- SEMPLAN Mapas de Teresina: https://www.teresina.pi.gov.br/semplan/mapas-de-teresina/
- Lei municipal CTM/SIG/IDE: https://www.teresina.pi.gov.br/semplan/prefeitura-de-teresina-institui-plataforma-para-integrar-dados-e-modernizar-o-planejamento-urbano-da-capital/
- e-SIC Teresina: https://esic.teresina.pi.gov.br/
- IBGE agregados por bairros/setores: https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/
- ANEEL GD: https://dadosabertos.aneel.gov.br/dataset/relacao-de-empreendimentos-de-geracao-distribuida
- TCE-PI API: https://sistemas.tce.pi.gov.br/api/portaldacidadania/docs/ · SICONFI: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/entes
- INEP microdados: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados
- Saúde API: https://apidadosabertos.saude.gov.br/ · SINISA: https://sinisa.cidades.gov.br/
- Atlas Brasil: https://www.atlasbrasil.org.br/consulta/planilha
- Foxinline Cidade Verde (Central CERUB p/ gestores): https://cidadeverde.com/ultimas/438046/foxinline-empresa-revoluciona-regularizacao-fundiaria-no-piaui

---
---

# RODADA 2 — Arbitragem com a segunda análise (15/09/2026, verificada em fonte primária)

Uma segunda investigação independente (outra sessão) criticou esta análise. Todos os pontos em disputa foram re-verificados hoje com download de arquivos, crt.sh e fontes primárias (Planalto, DOU, portais de dados). Placar:

## 1. Onde a segunda análise está certa (esta análise foi corrigida)

**a) Pasta de entorno urbanístico do IBGE — CONFIRMADO, achado valioso.**
`Agregados_por_Setores_Censitarios_Caracteristicas_urbanisticas_do_entorno_dos_domicilios/` existe no FTP do Censo 2022, **com versão por bairro** (`Agregados_por_bairros_entorno_domicílios_BR.zip`, `..._faces_BR.zip`, `..._moradores_BR.zip` + dicionário). Dicionário verificado: V05006–V05008 = "face com VIA PAVIMENTADA", V05012–V05014 = "face com ILUMINAÇÃO PÚBLICA", bueiro, calçada, rampa, obstáculo, ponto de ônibus, ciclovia, arborização (faixas). 17.577 bairros, **123 de Teresina presentes**. Métrica = % de domicílios em face com o atributo (proxy de cobertura), snapshot 2022, universo = setores urbanos pesquisados.
→ **Impacto na matriz: pavimentação e iluminação pública saem da lista de negociações institucionais (e-SIC) e viram dado aberto.** Restam como dependência: saneamento por bairro, dados municipais de saúde/educação, base fiscal por imóvel.

**b) Favelas e comunidades urbanas com vetores — CONFIRMADO.**
`Favelas_e_comunidades_urbanas_Resultados_do_universo/arquivos_vetoriais/` no FTP. Delimitação geométrica do universo informal → dimensionamento de mercado de Reurb por município antes de qualquer contato.

**c) Valor venal público — EU ERREI.** "Nenhuma base pública tem valor venal por imóvel" é falso. Verificado com download:
- **Fortaleza**: ITBI por transação, CSV CC-BY (95 mil transações 2022–2026), colunas `VL_VENAL`, `VL_BASE_CALCULO`, coordenadas SIRGAS2000, áreas, zoneamento (`dados.fortaleza.ce.gov.br`).
- **São Paulo**: ITBI 2006–2026 (xlsx) com **Valor de Transação declarado + Valor Venal de Referência + Valor Financiado**; IPTU com valor venal por imóvel em CSV desde 1995 (GeoSampa); CTM com 1.687.909 lotes via WFS.
- Também publicam: Recife (ITBI+IPTU), BH (ITBI mensal desde 2008 com Valor Declarado + cadastro CTM com geometria), POA (IPTU com vlr_venal por imóvel), Rio e Niterói (agregado).
- **Ressalva estratégica que se mantém**: nenhum município médio do PI/CE/MA publica (testado: Teresina, Parnaíba, Timon, Sobral, Juazeiro — todos negativos). Para o produto no Piauí, valor venal segue dependendo de SEMF/coleta — mas as bases das capitais servem de **treino para modelo de avaliação** (transferência) e referência metodológica de PGV.

**d) Reforma tributária como eixo de compra — EU FALTEI, a tese se sustenta (com correções).** Verificado em fonte primária:
- **LC 214/2025**: art. 59 (integração/sincronização obrigatória de cadastros entre entes), art. 265 (todos os imóveis devem se inscrever no **CIB** — Cadastro Imobiliário Brasileiro, "CPF do imóvel"), art. 266 (**prazo: 24 meses para os demais municípios incluírem o CIB em seus sistemas = 31/12/2026**; capitais/DF e cartórios: 12 meses = jan/2026).
- **Sinter** (Sistema Nacional de Gestão de Informações Territoriais, RFB, Decreto 11.208/2022): opera o CIB; **1.904 municípios aderidos em 14/09/2026** (de 5.570 — ~66% ainda fora); 29,1 milhões de CIBs ativos. Adesão por convênio gratuito com a RFB; integração via **API do CADURB** (módulo urbano do Sinter), com Manual Operacional público (ENAT, v1.12).
- **Consequência oficial RFB**: imóvel sem CIB → **município não recebe repasse do IBS** daquela operação (LC 214, art. 11, II) + entraves a registro/alvará/ITBI.
- **Correções obrigatórias ao pitch** (a segunda análise citou distorcido): a base da obrigação é o **art. 266** (o art. 256 é "valor de referência"); Sinter é **sistema**, não superintendência; IN RFB 2.275/2025 obriga **cartórios** (não municípios); PROFISCO III é **empréstimo do BID** (US$ 278 mi federal + linha CCLIP US$ 2 bi p/ estados; municípios em 2ª fase), não grant; **não há multa** por "não modernizar" — a perda é de IBS (alíquota municipal 0,05% em 2027-28; partilha relevante a partir de 2029); e a **RFB fornece a integração de graça** — o que se vende é **saneamento/qualificação/georreferenciamento do cadastro** (capacidade de cumprir), não "acesso ao CIB".
- **Janela comercial**: prazo geral 31/12/2026 + maioria dos municípios ainda não aderida = onda de demanda com data. Referências de preço do segmento: contratos Geopixel tipo R$ 270 mil (cadastro, 2019, valores maiores hoje).

**e) Escala real da Foxinline — EU SUBESTIMEI.** crt.sh (`%.foxinline.com`): **307 subdomínios únicos**, incluindo dezenas de tenants municipais e cartorários em PI, CE, PE, PA, MA, TO; `cerurb.<tenant>.foxinline.com` (buriticupu/MA, prourb, joaoxxiii, santafilomena, valefreire, mapatech…); `pi.cerurb.foxinline.com` (PROUrbe/SEAD); **`tjpi` e `tjmt`** (dois tribunais como clientes); produto comercial `cerurbpro.foxinline.com` no ar; **microsserviços confirmados**: `api-exportacao`, `api-autenticacao`, `api-auditoria`, `api-mapa`, `api-mapeia`, `api-memorial`, `api-cerurb-relatorioprocesso`, `api-cerurbjus-integracao`, `api-spi` (SPU) — todos vivos (404 na raiz = comportamento normal de serviço de API). Meus "~6 clientes documentados no PNCP" eram só a ponta com contratos públicos; a infraestrutura privada é muito maior.

**f) Geopixel — concorrente direto confirmado.** Geointeligência p/ prefeituras (desde 2007, SJC/SP): CTM + PGV + monitoramento por satélite + alvará digital + observatório imobiliário + módulos IPTU/ITBI/ISS; "+100 municípios" autodeclarado, concentrado em médios de SP/MG; casos: Amparo +R$ 10 mi/ano, Guaratinguetá arrecadação quase dobrou. **O mercado-alvo (médio, NE) é exatamente onde não há dado público de valor venal nem dashboards maduros.**

## 2. Onde a segunda análise ERROU (verificado)

**"Não há arquivo de renda por bairro" — FALSO.** O FTP tem `Agregados_por_bairros_renda_responsavel_BR_20260508_csv.zip` (pasta `..._Rendimento_do_Responsavel/`). Baixado e verificado: **17.379 bairros, 122 de Teresina com dados reais** (responsáveis por faixa, rendimento médio etc.; 474 bairros no PI). A renda por bairro **é direta**, sem necessidade de agregar setor→bairro. Provavelmente a segunda análise só olhou a pasta `Agregados_por_Setores_Censitarios/` (onde renda realmente não está) e não viu a pasta irmã. **O indicador central do painel segue disponível em dado aberto, por bairro, com um único download.**

**Cadeia tributária com artigos/nomes distorcidos** — corrigidos acima (art. 266, não 256; Sinter sistema; IN 2.275 é p/ cartórios; PROFISCO III = BID/empréstimo; sem multa; sem "dinheiro carimbado" a fundo perdido vigente em 2026).

## 3. Síntese pós-arbitragem — plano consolidado

As duas investigações + arbitragem convergem:

1. **Não construir sobre extração do CERURB** (sem API pública; cláusula de sigilo; scraping = risco) — **triplamente confirmado**.
2. **Fase 1 do produto = dado público por bairro** (IBGE: básico + renda + entorno + favelas/vetores; INEP; ANEEL; TCE-PI/SICONFI; SINISA; DataJud) — agora **com pavimentação e iluminação incluídas** e a grade ilustrativa substituível por geometria real.
3. **Razão de compra = conformidade LC 214 (art. 266, prazo 31/12/2026) + arrecadação**; **entrega visível = dashboard de gestão territorial**; **independência = módulo de coleta próprio** (família/saúde/educação/avaliação) compatível com SHP/UTM/memorial e alimentando o ciclo CIB/Sinter (o município precisa de cadastro saneado para transmitir).
4. **PGV**: treinar modelo de avaliação nas bases abertas das capitais (SP/Fortaleza/Recife/BH/POA), aplicar no cliente-PI com dados locais via SEMF/coleta.
5. **Foxinline**: tratar como fornecedora de fundiário em potencial parceria (ela tem a coleta e os geodados; vocês, a inteligência multi-fonte) — e como concorrente se o escopo for a ferramenta fundiária em si. A escala real dela (307 hosts) reforça: não competir no nicho dela.
6. **Geopixel**: benchmark de posicionamento e preço; diferencial nosso = custo de entrada baixo com dado público + conformidade com prazo + camada social (saúde/educação/família) que nenhum dos dois cobre.

**Critério de decisão atualizado:** entrar se (a) o proponente aceitar o eixo "conformidade CIB + dashboard + coleta própria" e (b) houver município-piloto definido. A quarta rodada de análise não é necessária — os pontos factuais foram arbitrados em fonte primária; o que resta é trabalho de campo (Fase 0): e-SIC (ETURB, SEMDUH, Águas de Teresina, e agora "quantos municípios do PI aderiram ao Sinter" — pergunta à RFB/sinter.df.cocad@rfb.gov.br), reunião Foxinline, conversa de escopo com o proponente.

## Fontes novas (Rodada 2)

- Entorno por bairro: `https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios_Caracteristicas_urbanisticas_do_entorno_dos_domicilios/Agregados_por_Bairro_csv/`
- Renda por bairro (arquivo): `https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios_Rendimento_do_Responsavel/Agregados_por_bairros_renda_responsavel_BR_20260508_csv.zip`
- Favelas (vetores): `https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Favelas_e_comunidades_urbanas_Resultados_do_universo/arquivos_vetoriais/`
- LC 214/2025: `https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp214.htm` · Sinter/CIB RFB: `https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/sinter` · Manual CADURB (ENAT): `https://www.enat.receita.economia.gov.br/pt-br/area_nacional/areas_interesse/sinter/manual-operacional/at_download/file`
- Sem CIB, sem repasse IBS: `https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/sinter/entenda/o-que-acontece-se-meu`
- IN RFB 2.275/2025 (cartórios): `https://www.in.gov.br/en/web/dou/-/instrucao-normativa-rfb-n-2.275-de-15-de-agosto-de-2025-648868175`
- Fortaleza ITBI: `https://dados.fortaleza.ce.gov.br/dataset/dados_abertos_itbi_transacoes_imobiliarias` · SP ITBI: `https://prefeitura.sp.gov.br/web/fazenda/w/acesso_a_informacao/31501` · BH: `https://dados.pbh.gov.br/dataset/itbi-relatorios` · Recife: `https://dados.recife.pe.gov.br/dataset/imposto-sobre-transmissao-de-bens-imoveis-itbi` · POA: `https://dadosabertos.poa.br/dataset/iptu`
- Geopixel: `https://geopixel.com.br` · PROFISCO III/BID: `https://www.iadb.org/pt-br/noticias/brasil-vai-fortalecer-sua-gestao-fiscal-com-credito-de-us-278-milhoes-do-bid`

---
---

# RODADA 3 — Análise direta do protótipo HTML e da matriz (15/09/2026)

Arquivos localizados em `~/Downloads/` e analisados na íntegra: `painel-gestao-municipal (1).html` (708 linhas, SPA vanilla JS) e `matriz-responsabilidade-fontes-dados.md`.

## O que o protótipo contém de fato

11 páginas: Painel principal (4 KPIs + mini-mapa + ranking + 3 perfis), Mapa territorial (4 camadas: vulnerabilidade/saneamento/pavimentação/evasão), Ranking (tabela 8 colunas), Saneamento, Pavimentação (com km estimados), Educação (evasão/distância/matriculas), Perfis socioeconômicos, Simulador de investimento (4 tipos, custo/família), Séries históricas (1 gráfico SVG), Status CERURB (regularizado/análise/pendente por bairro + tempo médio), Relatórios exportáveis (6 modelos). Todo o dado é um array hardcoded de 18 bairros **com nomes reais de Teresina** (Mocambinho, Cabral, Jóquei, Noivos, Fátima, Centro...), declarado como ilustrativo no rodapé ("Fonte planejada: CERURB (Foxinline)").

## Mapa campo-a-campo: dado do protótipo × fonte real verificada

| Campo no `bairros[]` | Fonte real hoje | Status |
|---|---|---|
| `nome` (18 bairros) | IBGE 2022: Teresina oficial tem 123 bairros — os 18 são subconjunto real; **decidir escopo** (cidade inteira × área de Reurb) | ⚠ decisão |
| `iv` (vulnerabilidade) | Composto construível: renda + alfabetização + densidade + entorno (todas por bairro, verificado) | ✅ público |
| `saneamento` | **Censo 2022 CD2 por bairro: V00309 (esgoto rede geral/pluvial) + V00111 (água rede geral) + lixo** — verificado com dicionário; concessionária só p/ série atualizada/rede física | ✅ público (2022) |
| `pavimentacao` | **Entorno por bairro V05006/07 (face com via pavimentada)** — verificado | ✅ público |
| Iluminação (só no simulador hoje) | Entorno por bairro V05012/13 (face com iluminação pública) — verificado; ganha página própria de graça | ✅ público |
| `evasao` | INEP por escola (distorção/abandono 2006–2025) agregado por bairro via geocodificação — "evasão por bairro" não existe como produto oficial | 🔶 proxy |
| `escolas`, `distEscola`, `matriculas` | INEP Censo Escolar 2025 (escola geolocalizada) + centroides de bairro IBGE → distância computável | ✅ público |
| `familias` | Censo 2022 básico por bairro (domicílios ocupados) | ✅ público |
| `renda` (faixa) | **Renda por bairro (arquivo próprio, 122 bairros de Teresina, V06004 = rendimento médio)** | ✅ público |
| `moradores` (morad./domicílio) | CD1 por bairro (moradores ÷ domicílios ocupados) | ✅ público |
| `idosos`, `criancas` | Demografia por bairro (60+ / 0–14) | ✅ público |
| `posse` (tipo de posse) | **Não existe em fonte pública** → CERURB (convênio) ou módulo de coleta própria | ❌ coleta |
| `pendentes/analise/regularizados` + tempo médio | **Não público por bairro** → DataJud/PJe (agregado, metadados públicos), ETURB via e-SIC, convênio Foxinline ou coleta própria | ❌ parceria/coleta |
| Simulador (R$/família por tipo) | Parâmetros inventados — validar com SNIS/SINISA (investimento per capita), tabelas de custo de obra | ⚠ negócio |
| Série histórica saneamento | SNIS/SINISA municipal; por bairro: 2010 vs 2022 (2 pontos) + e-SIC concessionária | 🔶 parcial |

**Placar: dos 16 grupos de campo do protótipo, 13 têm fonte pública por bairro verificada hoje; 2 dependem de CERURB/coleta (posse e status por bairro); 1 é parâmetro de negócio.** Ou seja: o dataset mockado pode ser trocado por dado real em ~80% sem nenhuma negociação institucional.

## Impacto na matriz de responsabilidade (correções)

| Item da matriz | Antes | Agora |
|---|---|---|
| 3. Pavimentação — Secretaria de Obras (prioridade média-alta) | Ofício + shapefile | **RESOLVIDO por IBGE entorno** — remove da lista de ofícios; secretaria vira fonte só p/ malha viária por trecho |
| 5. Iluminação — Serviços Urbanos (segunda fase) | Ofício + pontos de luz | **RESOLVIDO p/ baseline (entorno)** — pontos de luz/manutenção segue e-SIC |
| 2. Saneamento — concessionária (prioridade alta) | Ofício, prioridade máxima | **Baseline RESOLVIDO (Censo CD2 por bairro, 2022)** — concessionária só p/ cobertura atualizada e rede física |
| 4. Educação — SEMEDUC | INEP como alternativa | **INEP como principal** (por escola, geocodificado); SEMEDUC só p/ dado administrativo interno |
| 6. IBGE — "setores + SIDRA" | camada-base | **Ampliar**: pacote por bairro (básico, renda, CD1/2/3, entorno, demografia) + favelas com vetores (dimensionamento de mercado) + malha GPKG |
| 1. Foxinline/CERURB | prioridade alta | Mantém — mas como **parceria formal** (cláusula 4.1.1/e-SIC/negociação), não como fonte técnica; só posse e status por bairro dependem dela |

**Negociações institucionais necessárias: caem de 5 para 2** (concessionária p/ série atualizada + CERURB/ETURB p/ posse/status — e esta última é exatamente o que o módulo de coleta própria substitui).

## Observações estruturais do protótipo

1. **Grade 6×3 sem significado geográfico** → substituir por geometria real: malha de bairros IBGE 2022 (GPKG/SHP) ou SEMPLAN; o rodapé já promete PostGIS.
2. **Rodapé "Fonte planejada: CERURB (Foxinline)"** → trocar para "IBGE · INEP · ANEEL · TCE-PI + coleta própria; CERURB via parceria" — alinha o pitch à realidade verificada.
3. **Módulos ausentes vs proposta** (confirma a análise da outra sessão, agora com caminho de correção): PGV (treinar em ITBI aberto das capitais + dados locais SEMF), arrecadação/IPTU (TCE-PI API + SICONFI), CTM por imóvel (módulo coleta + Sinter/CADURB), cartografia real (IBGE+SEMPLAN+ESRI), iluminação como página (entorno), energia solar (ANEEL), camada de favelas/comunidades (IBGE vetores), módulo "conformidade CIB" (razão de compra, prazo 31/12/2026).
4. **Dado mock perfeitamente correlacionado** (IV cresce linearmente com tudo) — dado real terá ruído e inversões; preparar a conversa com o cliente para isso.
5. **Simulador**: conceito bom ("critério técnico auditável"), parâmetros precisam de fonte (senão vira ponto fraco em auditoria).
6. Ponto positivo a preservar: rodapés honestos sobre dado ilustrativo, navegação por hash, filters por zona — estrutura pronta para plugar dado real.

---
---

# RODADA 4 — Sprint Q4/2026: a janela real e o mercado real (15/09/2026)

Correção de cronologia aceita e verificada: **15/09 → 31/12/2026 = 107 dias**; eleição presidencial 04/10; janela prática de assinatura **nov–dez (~60 dias)**. Nuance relevante: 31/12/2026 é a meta prática de integração (comunicação RFB/CNM/ABRASF); a data **legal** do art. 266, II, LC 214 (24 meses da publicação de 16/01/2025) é **16/01/2027** — importa para o playbook de prorrogação.

## Verificações da rodada

**1. Swagger do CADURB — público; credencial, não.** O Manual Operacional (ENAT, 91 págs., v1.12, salvo em `dados-sinter/manual_cadurb.pdf`) publica a URL do Swagger de homologação: `https://hom-sinter2-cadurb.np.estaleiro.serpro.gov.br/api/swagger-ui/index.html`, autenticação OAuth client-credentials com **token fornecido pelo time do CADURB** (contato: sinter.df.cocad@rfb.gov.br). Conclusão: o **conector pode ser construído hoje, sem convênio e sem custo** (spec + Swagger públicos); para **testar** chamadas autenticadas é preciso a credencial, que vem da adesão gratuita. O portal `docs.receitafederal.gov.br/sinter` citado pela RFB está 404 — a fonte viva é o PDF do ENAT + Swagger. **Conector = prioridade nº 1 do M0 confirmada.**

**2. O tamanho real da onda (listas oficiais baixadas hoje, corte 15/09/2026 11:52, salvas em `dados-sinter/`):**
- `adesoes_setembro_2026_2.xls` — 5.571 municípios listados (todos, incluindo os 224 do PI). Inconsistente com o contador "1.904 municípios com adesão" da página principal do Sinter — tratar **adesão como passo de papel trivial** (não é o funil que importa).
- `inscricoes_ativas_setembro_2026_2.csv` — **apenas 188 municípios no Brasil com CIBs ativos** (transmissão real concluída). Concentração: RS 31, PR 27, SC 22, MG 19, SP 16 + todas as grandes capitais (São Paulo 3,99 milhões de CIBs, RJ 2,14 mi, Brasília 1,05 mi...). **Nordeste inteiro: 36 municípios. Piauí: somente Teresina (363.805 CIBs ativos).**
- **Consequência 1 — corrige o "66% fora"**: o gargalo real não é adesão (≈ universal ou trivial), é **transmissão: ~97% dos municípios do país sem nenhum CIB ativo**. A barreira é execução (saneamento de cadastro + campo), como concluído na rodada anterior — agora com número.
- **Consequência 2 — Teresina já entregou**: a capital transmitiu 363.805 CIBs. O gancho "conformidade com prazo" **não vende em Teresina** — lá o produto é o dashboard/coleta (a base já existe e é Rica). O sprint de conformidade vende no **interior: 223 municípios do PI sem transmissão**, com overlap com os tenants Foxinline mapeados no crt.sh (coivaras, joaquim Pires, Lagoa Alegre, Campo Maior...) e com os municípios do Programa Regularizar (Guaribas, N. Sra. Nazaré, Floresta, Tanque, Juazeiro, Coivaras).

**3. Dispensa/ticket — verificado.** Limite de dispensa para compras e serviços em 2026 (art. 75, II, Lei 14.133, Decreto 12.807/2025): **R$ 65.492,11**. Ticket proposto (diagnóstico R$ 3–5 mil; conformidade R$ 12–25 mil; manutenção R$ 4–8 mil/ano) **cabe folgado** — entrada + 1º ano no máximo ~R$ 33 mil. O produto deve incluir o dossiê de contratação (minuta de dispensa + estimativa de preço) — "preencher o caminho orçamentário é parte do produto". **PROFISCO III fora do discurso do ano 1** (empréstimo BID; dá ao controle interno motivo para adiar).

**4. Playbooks confirmados com tripwires.**
- **Cenário pânico**: gancho "registro dos imóveis dos seus eleitores travado no cartório em jan/2027" (IN 2.275: cartórios integrados até 30/09/2026; exigibilidade plena jan/2027; recusa de registro sem CIB). O gatilho cartorial independe de prorrogação do prazo — o pânico dispara de qualquer forma no Q1/2027, mas o dinheiro de 2026 só pode ser empenhado até 31/12. Daí nov–dez.
- **Cenário prorrogação**: plausível (LC 214 já alterada 2×; 97% sem transmissão a meses do fim). Tripwire: monitorar CNM/ABRASF/notícias RFB; se prorrogação publicada, trocar o gancho de "prazo" para "IBS + cartório" em 48h e vender contrato anual.
- Meta do piloto endurecida: **3–5 municípios com remessa ACEITA em homologação até 31/12/2026** (aceite programático, não contrato). Capacidade artesanal ~2 contas/mês; com conector CADURB, 10–20/mês.

**5. Frase de reunião — validada ponto a ponto** (convênio gratuito ✓ API aberta ✓ repasse IBS ✓ registro cartorial ✓). Único ajuste: prometer como SLA contratual a **"remessa aceita em homologação até [data]"** — critério objetivo e verificável, sem prometer o que depende da qualidade do cadastro alheia.

## Fontes novas (Rodada 4)

- Manual CADURB (ENAT): `https://www.enat.receita.economia.gov.br/pt-br/area_nacional/areas_interesse/sinter/manual-operacional/at_download/file` (cópia local: `dados-sinter/manual_cadurb.pdf`)
- Swagger homologação: `https://hom-sinter2-cadurb.np.estaleiro.serpro.gov.br/api/swagger-ui/index.html`
- Estatísticas Sinter: `https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/sinter/estatisticas-imoveis-urbanos` → `adesoes_setembro_2026_2.xls` e `inscricoes_ativas_setembro_2026_2.csv` (cópias em `dados-sinter/`)
- Dispensa 2026: Decreto 12.807/2025 (art. 75, II = R$ 65.492,11) — [ConLicitação](https://conlicitacao.com.br/nova-lei-de-licitacoes-2026/)

---
---

# RODADA 5 — Geografia do dado confirma a bifurcação A/B (16/09/2026, verificada)

## Verificações (fonte primária, nesta máquina)

**1. Bairros no Piauí — CONFIRMADO com exatidão.** Leitura direta do DBF da malha `PI_bairros_CD2022.shp`: **apenas 25 dos 224 municípios têm divisão de bairros** no Censo 2022. Ranking: Teresina 123 · Parnaíba 46 · Floriano 40 · **Piripiri 30** · Picos 27 · **Campo Maior 21** · **Altos 17** · Paulistana 17 … Guaribas, N. Sra. de Nazaré, Coivaras e Juazeiro do Piauí: **0 bairros**. Detalhe estratégico do complemento: Campo Maior e Altos (com bairros) são tenants Foxinline mapeados no crt.sh — candidatos naturais a piloto de dashboard **fora** da capital.

**2. Favelas/comunidades no PI — CONFIRMADO com exatidão.** Polígonos oficiais (`poligonos_FCUs_shp.zip`): só 3 municípios do PI têm FCUs mapeadas — **Teresina 170, Picos 2, Parnaíba 1**.

## Arbitragem da inferência

A conclusão da outra sessão ("para 199 dos 224 não existe granularidade intraurbana pública, logo não existe painel de gestão territorial para vender") é **direção certa com uma correção de precisão**: existe granularidade intraurbana pública sim — setor censitário (todos os municípios, mais fino que bairro), **concentrações urbanas** (footprint urbano oficial, 40 MB, já baixado em `dados/bruto/ibge/`) e, sobretudo, **núcleos de Reurb** (a unidade nativa do CERURB e do gestor de regularização no interior). O que não existe é a *unidade bairro com nome que o gestor reconhece*.

Reformulação aceita e registrada: **no Segmento B o produto principal é conformidade cadastral; o painel não desaparece — muda de unidade (núcleo/zona urbana/setor) e vira subproduto/relatório do trabalho de conformidade.** No Segmento A (25 municípios com bairros), o dashboard por bairro segue como produto de entrada. A bifurcação A/B, antes deduzida da economia (IPTU relevante em ~9 municípios), agora aparece de forma independente pela geografia do dado — duas evidências independentes convergindo permanece o achado mais forte da análise.

Custo registrado: +meio dia no D4 para suportar duas geometrias (bairro e setor) — os dois insumos já estão em `dados/bruto/`.

## D1 executado nesta máquina também (lição do /tmp aplicada)

Criado `dados/bruto/` (116 MB preservados) com **`baixar.py` idempotente** — todas as URLs validadas nas rodadas 1–5, skip de arquivos existentes, flag `--completo` para ANEEL (~110 MB) e INEP (~537 MB). Validado em duas rodadas (segunda pulou tudo). Nota embutida no script: os nomes de arquivo do Sinter mudam por mês; ANEEL exige descobrir a URL vigente via CKAN (comando curl documentado no próprio arquivo). Estrutura: `ibge/` (agregados por bairro, dicionários, malha de bairros, FCUs, concentrações urbanas), `sinter/` (adesões e inscrições), `manuais/` (CADURB).

---
---

# RODADA 6 — Piloto fora da capital: Altos; correções de tenant; RREO não verificável (16/09/2026)

## 1. Correção de erro PRÓPRIO (Rodada 5)

Eu afirmei que "Altos é tenant Foxinline" citando `2oficioaltos.foxinline.com` — **padrão cartório (produto Notário), não municipal**. Correção da outra sessão procede e está registrada aqui: **Altos não tem host municipal no CT**.

## 2. Cruzamento completo: os 25 com bairros × hosts municipais Foxinline (crt.sh fresco, 16/09)

Com normalização de nomes, hosts municipais (plano ou `cerurb.<mun>`) entre os 25: **Piripiri, Campo Maior, Corrente, União, Brasileira e Ilha Grande (6)** — a lista da outra sessão (8) **superinclui Barras e Água Branca**, que no CT só têm hosts cartório (`cartoriobarras`, `notarial.barras`, `registral.aguabranca`). Teresina e Parnaíba também não têm host municipal plano (capital usa TJ-PI; Parnaíba tem contrato antigo, atestado 2023).

**Duas ressalvas estruturais sobre "não-tenant":** (a) ausência no CT é evidência fraca (subdomínio próprio não é obrigatório); (b) **cega do PROUrbe**: `cerurb.prourb.foxinline.com` é um host único — municípios do programa estadual não têm subdomínio próprio e ficam invisíveis ao método. Confirmar caso a caso antes de uso comercial (como a outra sessão já anotou).

## 3. Altos como candidato nº 1 fora da capital — verificado o que é verificável

- Bairros: **17** ✓ (malha CD2022). · População: **47.453 no Censo 2022 — 7º do PI** ✓ (o valor "46.826" da outra sessão deve ser estimativa anual; o rank confere; acima de União e Campo Maior, abaixo de Barras).
- Não-tenant per CT ✓ (sob as ressalvas acima). · RCL R$ 61,3 mi e IPTU R$ 245 mil (fronteira A/B): **não reverificados nesta rodada** — plausíveis, confirmar via TCE-PI antes da reunião.
- Paulistana como segundo: 17 bairros ✓, não-tenant per CT (só `paulistana2oficio` = cartório) ✓.
- Lógica "bairros + ausência de incumbente + porte": sustentada. Campo Maior = Segmento A com incumbente instalado — concordamos em não ser o primeiro.

## 4. Alegação dos 8 sem RREO 2025 no SICONFI — NÃO VERIFICÁVEL e com alerta de método

A API (`apidatalake.tesouro.gov.br/.../siconfi/tt/rreo`) retorna **vazio até para Teresina** (que certamente entrega RREO) em todas as variantes de período testadas; `extrato_entregas` também veio vazio. Ou o endpoint mudou de forma de novo, ou exige parâmetros diferentes dos documentados. Consequências:
- A lista dos 8 (União, Luís Correia, Piracuruca, Água Branca, Baixa Grande do Ribeiro, Ilha Grande, Lagoa do Barro, Simplício Mendes) **não pode ter vindo deste caminho quebrado** — o método da outra sessão precisa ser revalidado (portal SICONFI web?) antes de virar critério comercial.
- Coincidência notável: dos 6 nomes da lista que estão entre os 25 com bairros, 3 (União, Água Branca, Ilha Grande) foram justamente os de classificação tenant ambígua — se o método deles veio de consulta que falha silenciosamente, os dois achados se contaminam mutuamente. Revalidar primeiro, usar depois.
- A **ideia** (ausência de demonstrativo fiscal obrigatório = município sem equipe = lead de serviço integral, não de ferramenta) continua boa — se medida de forma confiável.

---
---

# RODADA 7 — M0 executado (16/09/2026)

Meta de venda ajustada e aceita sem reserva: **2–3 assinadas até 15/11** (8–12 propostas vivas, ≥20 primeiras reuniões), com classificação de não-fechamento (atraso ≠ rejeição) e relógio da tese = gatilho de 90 dias. Posição Foxinline endurecida e aceita: sem proposta de parceria agora; deck de 1 página pronto + monitoramento semanal via CT com gatilho de antecipação.

**Executado nesta rodada (ordem do plano):**

1. **Conector CADURB (`m0-conector/`)**: spec OpenAPI capturada (pública, `hom-sinter2-cadurb.../api/v3/api-docs`) — 15 endpoints mapeados incluindo `POST /v1/validacao/{ibge}/ui`. Cliente Python com OAuth + dry-run validado contra a URL real de homologação. O portal `docs.receitafederal.gov.br/sinter` segue 404 — a spec viva é o Springdoc.
2. **Validador de completude (`validador_completude.py`)**: regras extraídas da própria spec (não copiadas à mão) + regras semânticas (CEP, titularidade ≈100%, duplicidade, CPF/CNPJ). Gera `LAUDO-completude.md`. **Funciona hoje, offline, sem credencial — é o produto do diagnóstico de R$ 3–5 mil**; `--online` revalida no endpoint oficial quando a credencial chegar (pedido: sinter.df.cocad@rfb.gov.br).
3. **Metodologia do IV publicada (`docs/metodologia-iv.md`) — bloqueante resolvida**: denominadores do entorno corrigidos (SIM/(SIM+NÃO), sem "não declarado"); **mediana V06006 como indicador principal** (Por Enquanto: média R$ 3.065 × mediana R$ 1.502); universo n ≥ 50 **domicílios** (121/123 bairros de Teresina passam). ETL idempotente (`painel-gerencial/build_dados.py`) lendo de `dados/bruto/`; painel regenerado e validado **11/11 páginas sem erro**.
4. **e-SIC redigidos (`docs/esic-textos.md`)**: RFB (adesões/remessas por município — denominador do mercado), SEFAZ-PI (repasse IBS por município — converte perda em R$), SEAD (lista PROUrbe — fecha a cega do `cerurb.prourb`); ETURB/SEMDUH/Águas rebaixados para vitrine, textos prontos.

**Pendências da rodada:** credencial CADURB (e-mail a enviar), verificação fiscal Altos/Paulistana no TCE-PI (portal é SPA — precisa browser), revalidação do método RREO antes de atacar os 8 municípios, dossiê de dispensa, E2 em Guaribas/Nazaré, INEP (último).
