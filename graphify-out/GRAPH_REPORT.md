# Graph Report - projeto-cerurb  (2026-09-18)

## Corpus Check
- 108 files · ~277,714 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 759 nodes · 1068 edges · 64 communities (58 shown, 6 thin omitted)
- Extraction: 81% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 197 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Spec CADURB e conector M0
- Telas do painel em imagem
- Contexto CERURB e concorrência
- Rodada 1 — viabilidade bruta
- Cliente da API CADURB
- Eixo de negócio e parcerias
- Credencial técnica e dispensa
- Pedidos de e-SIC
- Regras semânticas e dígito verificador
- Coletor de campo e laudo
- Eixo técnico — dados do Censo
- Foxinline e acesso ao CERURB
- Termo de referência e art. 75
- Conector e método do índice
- CNEFE e aferição
- Método fiscal e corte por bairro
- ETL build_dados
- Avaliação em massa e ativos reutilizáveis
- Plano comercial e PROFISCO III
- ITBI no SICONFI
- Pareceres finais — o produto vendável
- Rito da dispensa
- Fórmula do IV e cortes de amostra
- Semântica de cor e ausência de dado
- Metodologia do IV
- ML descartado e roteiro CADURB
- Janela regulatória e modelo de receita
- Protótipos anteriores
- Fontes fiscais e lista qualificada
- SINTER, CIB e segmentos
- Beachhead Piauí e tenants
- Ponte do Segmento B para o A
- Pesos declarados versus k-means
- Redução de escopo da v1
- Mercado e capacidade de pagamento
- Deck e apresentação
- Merge da sessão ZCode
- Deploy com autenticação
- Prazo legal e CNEFE no README
- Painel: operação e narrativa
- Agrupamento e universo amostral
- Plano: posicionamento e LGPD
- Propriedade do dado como ativo
- PGV e defasagem do valor venal
- Reforma tributária e NT da CNM
- Vereditos do eixo de negócio
- Cashback e dispensa única
- Entregáveis do M0
- REURB e erro ecológico
- Números da credencial
- Entregas e cronograma
- Risco Foxinline
- ETL build_cnefe
- Basic auth do Cloudflare Pages
- Coleta própria via REURB
- Scripts de publicação
- ETL parametrizável
- Consórcio intermunicipal
- Mini-diagnóstico e cashback
- Portaria MCid 3.242/2022
- Tela de pavimentação e viário
- Tela de saneamento

## God Nodes (most connected - your core abstractions)
1. `Termo de Referência modelo v2.1 — Pacote de Conformidade CADURB/Sinter` - 16 edges
2. `CadurbClient` - 14 edges
3. `Índice de Vulnerabilidade Territorial (IVT)` - 14 edges
4. `Dossiê de dispensa — processo passo a passo` - 12 edges
5. `Rodada 4 — final, eixo negócio (beachhead Piauí e contexto institucional)` - 10 edges
6. `Rodada 5 — fechamento comercial (quatro fatos que reprecificam o Segmento B)` - 10 edges
7. `validar_registro()` - 9 edges
8. `Spec OpenAPI do CADURB (pública)` - 9 edges
9. `Painel único (painel/index.html)` - 9 edges
10. `Rodada 2 — convergência, eixo negócio/risco/estratégia` - 9 edges

## Surprising Connections (you probably didn't know these)
- `Símbolo scatter / linha de pontos` --conceptually_related_to--> `Renda mediana × esgoto em rede, por bairro`  [AMBIGUOUS]
  .orca/drops/Vertical-Data-Logomarcas.pdf → apresentacao/dash_scatter.png
- `Vocabulário oficial de falhas (enum TipoFalhaDTO)` --semantically_similar_to--> `Índice de Vulnerabilidade (k-means k=3)`  [INFERRED] [semantically similar]
  entregaveis/README.md → docs/metodologia-iv.md
- `Painel Gerencial — Gestão Territorial Teresina (protótipo com dado real)` --semantically_similar_to--> `Agrupamento k-means (k=3, sementes fixas)`  [INFERRED] [semantically similar]
  .orca/drops/index.html → painel/index.html
- `Laudo em HTML (artefato entregável)` --semantically_similar_to--> `Conversa — narrativa de cinco telas (Teresina)`  [INFERRED] [semantically similar]
  m0-conector/LAUDO-completude.html → painel/conversa.html
- `Marca Vertical Data` --conceptually_related_to--> `Painel CERURB — Piauí, 224 municípios`  [AMBIGUOUS]
  .orca/drops/Vertical-Data-Logomarcas.pdf → apresentacao/dash_hero.png

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Cadeia normativa CIB/SINTER que sustenta o produto de conformidade** — analise_02_adendo_reforma_tributaria_lc_214_2025, analise_02_adendo_reforma_tributaria_art_265_266, analise_02_adendo_reforma_tributaria_art_256, analise_02_adendo_reforma_tributaria_cadurb, analise_00_dossie_contexto_sinter, analise_00_dossie_contexto_cib, analise_02_adendo_reforma_tributaria_in_rfb_2275_2025 [EXTRACTED 1.00]
- **Segmentação comercial do beachhead Piauí** — analise_05_recorte_piaui_segmento_a, analise_05_recorte_piaui_segmento_b, analise_05_recorte_piaui_segmento_c, analise_05_recorte_piaui_beachhead_piaui, analise_05_recorte_piaui_rcl_mediana, analise_05_recorte_piaui_fee_eficiencia_inaplicavel [EXTRACTED 1.00]
- **Cadeia de erros metodológicos identificados e corrigidos entre rodadas** — analise_00_dossie_contexto_gargalo_granularidade_bairro, analise_10_arbitragem_rodada2_erro_inferir_inexistencia, analise_10_arbitragem_rodada2_armadilha_poucas_faces, analise_15_revisao_execucao_erro_metrica_faces_domicilios, analise_14_arbitragem_rodada6_correcao_tenants [INFERRED 0.85]
- **Pipeline do laudo de completude (spec, domínios, vocabulário, regras)** — analise_16_cadurb_spec_verificada_laudo_completude, analise_18_spec_validador_regras_da_spec, analise_18_spec_validador_tabelas_dominio_secao9, analise_18_spec_validador_tipofalhadto, analise_18_spec_validador_regras_semanticas, analise_21_correcoes_credencial_conjunto_minimo_regras_laudo, analise_25_merge_sessao_zcode_dois_validadores [EXTRACTED 1.00]
- **Arcabouço legal da dispensa (art. 75 §§1º–3º, limite 2026, consórcio, dispensa única)** — analise_20_revisao_credencial_dossie_art75_par1_fracionamento, analise_20_revisao_credencial_dossie_art75_par2_consorcio, analise_20_revisao_credencial_dossie_limite_dispensa_2026, analise_22_revisao_tr_v2_art75_par3_aviso, analise_plano_consorcio_intermunicipal, analise_plano_dispensa_unica [EXTRACTED 1.00]
- **Composição do Índice de Vulnerabilidade Territorial** — analise_24_indice_pesos_declarados_ivt, analise_24_indice_pesos_declarados_d_infra, analise_24_indice_pesos_declarados_d_saneamento, analise_24_indice_pesos_declarados_d_renda, analise_24_indice_pesos_declarados_d_dependencia, analise_24_indice_pesos_declarados_regras_qualidade_ivt [EXTRACTED 1.00]
- **Correções factuais que derrubaram premissas de rodadas anteriores** — analise_pacote_r2_deepseek_api_exportacao, analise_pacote_r4_deepseek_agregados_por_bairro_censo_2022, analise_pacote_r5_deepseek_api_rest_do_cadurb, analise_pacote_r6_deepseek_metrica_por_domicilio_versus_por_face, analise_pacote_r5_deepseek_renda_por_bairro_v06006 [INFERRED 0.85]
- **Cadeia do dado: conformidade CIB alimenta a avaliação em massa** — analise_pacote_r5_glm_segmento_b_conformidade_cib, analise_pacote_r5_deepseek_bloco_itbi_do_schema_cadurb, analise_pacote_r3_deepseek_avaliacao_em_massa, analise_pacote_r5_glm_segmento_a_recuperacao_fiscal, analise_pacote_r3_deepseek_lc_214_2025_art_256 [EXTRACTED 1.00]
- **Artefatos do M0 sob revisão nas rodadas 6 a 8** — analise_pacote_r6_deepseek_painel_teresina_123_bairros, analise_pacote_r6_deepseek_conector_cadurb, analise_pacote_r7_glm_validador_de_completude_offline, analise_pacote_r7_glm_laudo_de_completude, analise_pacote_r8_deepseek_credencial_tecnica, analise_pacote_r6_glm_dossie_de_dispensa [EXTRACTED 1.00]
- **Indice iv sem metodologia: do numero digitado a mao a formula publicavel com cortes fixos** — analise_parecer_r4_deepseek_formula_publicavel_do_indice_iv, analise_parecer_r4_glm_prototipo_com_dado_ficticio_e_risco_comercial_desproporcional, analise_parecer_r5_deepseek_formula_do_iv_revisada_com_renda_v06006_sem_duplicar_esgoto, analise_parecer_r6_deepseek_metodologia_do_iv_precisa_ser_publicada, analise_parecer_r7_deepseek_kmeans_com_minmax_da_amostra_nao_e_reproduzivel, analise_parecer_r8_deepseek_frase_sem_indices_de_pesos_arbitrarios_nao_e_defensavel [INFERRED 0.85]
- **CERURB/Foxinline fora do caminho critico: de risco de integracao a risco de mercado, a mandato contratual e a adiamento do contato** — analise_parecer_r1_deepseek_integracao_cerurb_tempo_real_e_ilusao, analise_parecer_r1_glm_risco_foxinline_e_de_mercado_nao_de_integracao, analise_parecer_r2_glm_foxinline_forte_inverte_o_risco_integrar_sob_mandato, analise_parecer_r4_glm_clausula_411_confirma_cerurb_fora_do_caminho_critico, analise_parecer_r6_glm_foxinline_adiar_o_contato_e_monitorar_passivamente [INFERRED 0.85]
- **Laudo de conformidade CADURB: o que ele precisa validar, quanto pode custar e por qual veiculo contratual** — analise_parecer_r5_glm_o_produto_vendavel_e_capacidade_de_cumprir, analise_parecer_r7_deepseek_validacao_apenas_sintatica_nao_justifica_o_preco, analise_parecer_r7_glm_preco_do_laudo_com_cashback_nunca_preco_zero, analise_parecer_r8_deepseek_conjunto_minimo_de_regras_semanticas_para_defender_o_preco, analise_parecer_r8_glm_cashback_morre_como_instrumento_no_setor_publico, analise_parecer_r8_glm_dispensa_unica_vence_pelo_calendario_de_2026 [INFERRED 0.85]
- **Rito completo da dispensa por valor (art. 75, II)** — dossie_dispensa_04_declaracao_necessidade_declaracao_de_necessidade, dossie_dispensa_02_termo_referencia_modelo_termo_de_referencia, dossie_dispensa_05_aviso_intencao_dispensa_modelo_de_aviso, dossie_dispensa_03_minuta_decisao_dispensa_minuta_de_decisao, dossie_dispensa_00_processo_passo_a_passo_calendario_da_janela_2026 [EXTRACTED 1.00]
- **Cortes estatísticos e leitura honesta do painel** — docs_metodologia_iv_universo_n_maior_igual_50_domicilios, docs_metodologia_iv_n_ok_ent, docs_metodologia_iv_denominador_sem_nao_declarado, docs_metodologia_iv_legenda_sem_classe_vazia, docs_metodologia_iv_paletas_carencia_e_magnitude [EXTRACTED 1.00]
- **Os quatro e-SIC como sistema de inteligência de mercado** — entregaveis_esic_1_sead_prourbe_pedido_sead_prourbe, entregaveis_esic_2_rfb_sinter_pedido_rfb_sinter, entregaveis_esic_3_sefaz_pi_pedido_sefaz_reduzido, entregaveis_esic_4_tce_pi_pedido_tce_pi, docs_esic_textos_formato_aberto_e_dado_agregado [EXTRACTED 1.00]
- **Caminho até a remessa aceita no CADURB** — coletor_index_coletor_de_campo, m0_conector_leiame_validador_completude, m0_conector_laudo_completude_laudo_de_completude_cadastral, m0_conector_spec_pin_spec_openapi_de_homologacao, m0_conector_leiame_endpoint_de_validacao_ui [INFERRED 0.85]
- **As onze telas do painel** — painel_index_mapa_de_alvos, painel_index_carteira_e_qualificacao, painel_index_janela_de_31_12, painel_index_territorio, painel_index_ranking_de_bairros, painel_index_saneamento, painel_index_pavimentacao_e_viario, painel_index_perfis_socioeconomicos, painel_index_relatorios_exportaveis, painel_index_metodologia_e_fontes, painel_index_fora_da_v1 [EXTRACTED 1.00]
- **Disciplina do dado ausente (cinza, nunca zero)** — readme_regras_da_casa, painel_index_ausencia_nao_e_zero, painel_index_classificacao_do_sinal_rreo, painel_index_modo_sem_bairro, painel_index_fora_da_v1 [INFERRED 0.85]

## Communities (64 total, 6 thin omitted)

### Community 0 - "Spec CADURB e conector M0"
Cohesion: 0.05
Nodes (45): Adesão ao convênio Sinter (ICP-Brasil, e-CAC, DOU), DadosGeoDTO (idLotePonto / idLotePoligono), POST /v1/validacao/{codigoIbge}/ui — validar sem inserir, Fluxo de geometria por lote e vinculação, Laudo de completude cadastral, Autenticação OAuth2 client credentials (token Bearer), Produto vendável antes da credencial, Spec OpenAPI do CADURB (pública) (+37 more)

### Community 1 - "Telas do painel em imagem"
Cohesion: 0.09
Nodes (30): Screenshot do painel territorial (tema claro), Categoria "amostra insuficiente" (n < 50, cinza), Corte vermelho = 20% mais carentes, ETL painel/build_dados.py (série local, sem servidor), Faixa de KPIs do topo (IPTU, ITBI, CIB, dias até 31/12), Indicador Renda mediana, Legenda por faixas com contagem de bairros, Lista de indicadores de infraestrutura urbana (+22 more)

### Community 2 - "Contexto CERURB e concorrência"
Cohesion: 0.09
Nodes (29): Gargalo de granularidade: dado público para no município, Geopixel (concorrente, Observatório Municipal de Informações), IBGE Censo 2022 — agregados por setor censitário, Módulo 2 — Cadastro Técnico Multifinalitário (CTM), Plataforma de Gestão Territorial Municipal (proposta 4 módulos), Protótipo painel-gestao-municipal.html, ANEEL — geração distribuída (CKAN, diário), iv sem metodologia como passivo contratual (+21 more)

### Community 3 - "Rodada 1 — viabilidade bruta"
Cohesion: 0.12
Nodes (23): Aposta de coleta própria no ato da REURB, ML/preditivo/chat conversacional na v1 com N≈1.800 imóveis, Estratégia de obtenção do dado do CERURB (JSF/PrimeFaces stateful, sem REST), Rodada 1 — parecer técnico, eixo Arquitetura e Dados, Stack mínimo para painel + CTM + PGV sem dívida técnica, Dependência da Foxinline/CERURB, fornecedor que é também concorrente adjacente, Janela regulatória CIB/SINTER, Modelo de receita: projeto único × SaaS recorrente × licenciamento por município (+15 more)

### Community 4 - "Cliente da API CADURB"
Cohesion: 0.14
Nodes (10): CadurbClient, POST /v1/validacao/{codigoIbge}/ui — valida sem gravar (a porta do laudo)., exemplo_ui(), faixas_cep_do_municipio(), main(), ni_valido(), Prefixos de CEP observados no CNEFE daquele município, como faixas. Tem de ser…, Comprimento E dígito verificador. Antes só o comprimento: um CPF de 11 dígitos… (+2 more)

### Community 5 - "Eixo de negócio e parcerias"
Cohesion: 0.13
Nodes (22): Propriedade do dado: cláusulas contratuais, LGPD e Lei 14.133, Competir, integrar ou fazer parceria/revenda sobre a base da Foxinline, Contrato TJ-PI 156/2023 e a cláusula 4.1.1 como porta formal para o dado CERURB, Consequência oficial da falta de CIB é perda de repasse do IBS, não multa, Dossiê de dispensa de licitação, Pedidos e-SIC (ETURB, SEMDUH, Águas de Teresina, SEAD/PROUrbe, RFB), Rodada 6 — revisão de execução, eixo negócio, Sequência de reuniões: prefeito, fazenda, planejamento, APPM, TJ-PI (+14 more)

### Community 6 - "Credencial técnica e dispensa"
Cohesion: 0.16
Nodes (21): Art. 266 da LC 214/2025 (integração ao CIB), Censo 2022 / geometria oficial do IBGE, Credencial Técnica — Projeto Painel Territorial, Postura de governança LGPD (atuação como operador), Painel de gestão territorial (123 bairros de Teresina), Prazo 31/12/2026 de integração ao CIB, Art. 75, II, Lei 14.133/2021 (dispensa por valor), Decreto nº 12.807/2025 (limites de dispensa) (+13 more)

### Community 7 - "Pedidos de e-SIC"
Cohesion: 0.13
Nodes (21): Regra: formato aberto e dado agregado, Arquivo mensal inscricoes_ativas_*.csv (estatísticas do Sinter), Lei 12.527/2011 (Lei de Acesso à Informação), Pedido RFB — adesões e remessas por município, Pedido SEAD-PI — municípios do PROUrbe, Pedidos de vitrine (ETURB, SEMDUH, Águas de Teresina), PROUrbe (Lei estadual 8.153/2023), Sistema CERURB (compra SEAD 469/2024, PNCP) (+13 more)

### Community 8 - "Regras semânticas e dígito verificador"
Cohesion: 0.15
Nodes (15): cep_do_municipio(), _cobertura(), _cod(), dv_cnpj(), dv_cpf(), dv_documento(), Falha, _num() (+7 more)

### Community 9 - "Coletor de campo e laudo"
Cohesion: 0.14
Nodes (20): Coletor de campo CADURB, Coletor multifacetário — camadas ao redor, nunca dentro, Modo só-telefone (?tela), Quatro origens de campo (CNEFE, ERP, campo, RFB), Regra R5 — territorial não tem área construída, Regras do CADURB embutidas no formulário, Validação de CEP por lista de prefixos, não por intervalo, Aptidão estimada para remessa (+12 more)

### Community 10 - "Eixo técnico — dados do Censo"
Cohesion: 0.16
Nodes (19): Desalinhamento de granularidade: painel por bairro × fonte por município/setor, Arquitetura de ingestão mínima e resiliente (SIDRA instável; onde não usar BigQuery), Roteiro Técnico da RFB para remessa ao módulo CADURB, Agregação setor censitário → bairro e o erro que introduz, Censo 2022 Agregados_por_Bairro — 17.576 bairros no Brasil, 123 em Teresina, Auditoria do protótipo HTML (11 telas, dados fictícios detectáveis), Entorno urbanístico por face de quadra (V05406, V05412, V05409 sobre V05400), Metodologia do índice de vulnerabilidade (iv): variáveis, pesos e auditabilidade (+11 more)

### Community 11 - "Foxinline e acesso ao CERURB"
Cohesion: 0.12
Nodes (18): Conclusão inicial: ausência de API REST pública no CERURB, CERURB, Exportação periódica via DataExporter do PrimeFaces, Foxinline Technologies, LGPD sobre dado de cadastro fundiário, Stack JSF + PrimeFaces 15 do CERURB, Tese da coleta própria de campo (ser originador do dado), api-exportacao.foxinline.com (camada de API não pública) (+10 more)

### Community 12 - "Termo de referência e art. 75"
Cohesion: 0.14
Nodes (16): e-SIC TCE-PI — dispensas de software 2024–26, Dossiê de dispensa, Art. 75, §3º — aviso de intenção por 3 dias úteis, Cláusula de uso de dados agregados para calibração, Cláusula de propriedade intelectual, Tenants municipais Foxinline no PI (63), CERURBJus (TJ-PI, stack JSF/PrimeFaces), Contrato TJ-PI 156/2023 (cláusula 4.1.1 e sigilo) (+8 more)

### Community 13 - "Conector e método do índice"
Cohesion: 0.19
Nodes (16): Conector CADURB, As 18 propriedades do GeoJSON e o que falta que seria barato incluir, INEP (537 MB) geocodificado — esforço × valor no M0, Testar o conector sem município conveniado: homologação SERPRO exige credencial?, Plano de execução em duas pistas (decisões humanas × técnico sem dependência), M0 até 15/10, Rodada 6 — revisão de execução, eixo técnico, Fluxo de geometria (idLotePonto/idLotePoligono, envio por lote + vinculação), k-means × índice com pesos declarados (arbitrariedade escondida e instabilidade) (+8 more)

### Community 14 - "CNEFE e aferição"
Cohesion: 0.13
Nodes (16): Conector CADURB, Laudo de Completude Cadastral, Sem promessa de prazo alheia, Aferição do CNEFE contra o CIB de Teresina (97,9%), painel/build_cnefe.py, CNEFE 2022 (Cadastro Nacional de Endereços para Fins Estatísticos), Consórcio público (art. 75, §2º — limites duplicados), Regra de ouro: obrigação × marco condicionado (+8 more)

### Community 15 - "Método fiscal e corte por bairro"
Cohesion: 0.14
Nodes (16): Pedido SEFAZ-PI sobre IBS — morto por design (v2), Soma direta da API MSC/MSCC (rejeitada), Classificação por natureza RREO (IPTU 1.1.1.2.1.01 · ITBI 1.1.1.2.1.02), dados/fiscais-itbi-iptu-mscc.json, Insight ITBI > IPTU no interior, Método canônico SICONFI para ITBI/IPTU, Regras de uso dos números fiscais no deck, Corte por bairro geométrico, não por código de setor (+8 more)

### Community 16 - "ETL build_dados"
Cohesion: 0.17
Nodes (14): anel(), carregar(), dp(), g(), indicadores(), ler_shp(), num(), pct_sim_nao() (+6 more)

### Community 17 - "Avaliação em massa e ativos reutilizáveis"
Cohesion: 0.17
Nodes (15): Menor escopo que fecha o primeiro contrato, Diagnóstico de conformidade CIB sobre dado aberto como v1 (60–90 dias), O que construir como ativo reutilizável multi-município desde o dia 1, Avaliação em massa (mass appraisal): regressão hedônica × GBM e explicabilidade perante TCE, LC 214/2025, art. 256 — valor de referência anual de todos os imóveis do CIB para o IBS, Plano de execução da v1 (diagnóstico CIB + baseline fiscal, 60–90 dias), Rodada 3 — fechamento, eixo técnico (fato novo + pedido de plano), Base pública de valor venal + transação por imóvel (ITBI Fortaleza e São Paulo) (+7 more)

### Community 18 - "Plano comercial e PROFISCO III"
Cohesion: 0.18
Nodes (15): Pagamento atrelado a resultado (fee de eficiência sobre incremento de IPTU), Gatilho de abandono (v): incumbente lançar módulo CIB antes da primeira assinatura, Produto de prazo (evento 2027) × receita recorrente estrutural, PROFISCO III (Fazenda + BID) como crédito para financiar a obrigação, Rodada 3 — fechamento, eixo negócio (art. 256 como fato novo), Escolha do município-piloto (Teresina é oportunidade ou armadilha?), ETURB — quem executa a REURB em Teresina, não o CERURB, Lei 6.383/2026 — Teresina institui CTM + SIG + IDE (+7 more)

### Community 19 - "ITBI no SICONFI"
Cohesion: 0.16
Nodes (14): Textos de e-SIC (RFB, SEFAZ-PI, SEAD/PROUrbe), e-SIC nº 2 à SEFAZ-PI (pedido de estudo), ITBI supera IPTU no interior do Piauí, Método declarável de estimativa de exposição, SICONFI/RREO Anexo 03 — ITBI e IPTU por município, "Por que agora" reescrito com o verificado, IN RFB 2.275/2025 (obrigação dos cartórios), ITBI aberto das capitais (Fortaleza, SP, BH, Recife, POA) (+6 more)

### Community 20 - "Pareceres finais — o produto vendável"
Cohesion: 0.18
Nodes (14): Achado 1 (R5/DeepSeek): o CADURB e API REST documentada - o produto deixa de ser implementar formato e vira camada de integracao + saneamento cadastral, Achado 1 (R5/GLM): adesao ao SINTER e gratuita e o Swagger e publico - a vantagem informacional evaporou; o produto e 'capacidade de cumprir', com diagnostico de R$ 3-5 mil como foot-in-the-door, Achado 6b (R6/DeepSeek): o envio em lote do CADURB pode exigir arquivo assinado com ICP-Brasil, validacao assincrona e limite de taxa, quebrando o conector unitario, Achado 4 (R6/GLM): faltam 2 e-SIC criticos - RFB (adesoes ao SINTER, denominador do mercado) e SEFAZ-PI (IBS em R$); rebaixar os tres municipais de Teresina, Achado 4 (R7/DeepSeek): validacao apenas sintatica entrega um relatorio de 'required' que qualquer um extrai do Swagger - nao vale R$ 3-5 mil, Achado 2 (R7/GLM): o e-SIC a SEFAZ-PI como escrito morre por design - pede que o orgao produza estudo; a linha de R$/municipio/ano sai hoje do SICONFI/FINBRA, Achado 6 (R7/GLM): o M0 destravou a venda; o unico risco material e que nenhum cadastro real passou pelo validador, Achado 1 (R8/DeepSeek): a credencial promete mais do que o M0 entrega nos itens 2, 3 e 4 - conector nao homologado, laudo preliminar, metodologia exploratoria (+6 more)

### Community 21 - "Rito da dispensa"
Cohesion: 0.15
Nodes (14): Foxinline (incumbente do sistema CERURB), Posicionamento de complemento (não concorrência com a Foxinline), Aviso de intenção de dispensa (art. 75, §3º), O aviso público expõe o objeto — e deve ser assim, Calendário da janela 2026 (aviso 12/11 → empenho 10/12), Dispensa única como oferta principal, Detecção da Foxinline por Certificate Transparency, Qualificação de lead pelo regulamento municipal de compras (+6 more)

### Community 22 - "Fórmula do IV e cortes de amostra"
Cohesion: 0.18
Nodes (13): Achado 3 (R4/DeepSeek): formula publicavel para o indice iv com cinco dimensoes e pesos versionados - o indice central era numero digitado a mao, Achado 2 (R5/DeepSeek): Tabajaras tem 19 faces medidas para 293 domicilios - adotar n >= 50 faces, IC 95% binomial e excluir 'nao declarado' do denominador, Achado 3 (R5/DeepSeek): formula do iv revisada - pesos 0,30/0,25/0,20/0,15/0,10, renda por V06006 com log1p e sem duplicar esgoto, Achado 1 (R6/DeepSeek): domicilio e a metrica correta, nao a face - substituir a regra de n>=50 faces por corte em domicilios com denominador V05000 menos nao declarado, Achado 3 (R6/DeepSeek): INEP deve ser rebaixado - 537 MB e geocodificacao para uma tela entre onze, sem valor para a tese de conformidade CIB, Achado 4 (R6/DeepSeek): a metodologia do iv precisa publicar pesos, fontes, transformacoes, cortes, hash do script e limitacoes - meio dia, bloqueante para terceiros, Achado 5 (R6/GLM): quase todo o M0 comercial nao depende dos e-SIC - pilotos REURB, 8 municipios do sinal RREO, dossie de dispensa, conector e metodologia do iv, Achado 6 (R6/GLM): inconsistencia documental - o plano consolidado ainda fixa corte de 'n >= 50 faces', regra caducada pela correcao para domicilios (+5 more)

### Community 23 - "Semântica de cor e ausência de dado"
Cohesion: 0.19
Nodes (13): Superfície fixa fora do tema (barra e botão verde), Foxinline — fornecedora e concorrente ao mesmo tempo, Geopixel — concorrente direto, Ausência não é zero, Carteira e qualificação, Classificação do sinal RREO pelo tripé de entregas, Mapa de alvos, Paleta de carência (CAR) (+5 more)

### Community 24 - "Metodologia do IV"
Cohesion: 0.17
Nodes (13): Água e esgoto (V00111/V00001, V00309/V00001), painel/build_dados.py (ETL idempotente), Denominador do entorno sem 'não declarado', Índice de Vulnerabilidade (k-means k=3), Legenda sem classe vazia, Mediana de renda V06006 como indicador principal, Corte próprio do entorno (n_ok_ent sobre V05000), Ordenação dos grupos do k-means pelas quatro dimensões (+5 more)

### Community 25 - "ML descartado e roteiro CADURB"
Cohesion: 0.20
Nodes (12): Achado 4 (R1/DeepSeek): ML/preditivo/chat na v1 e teatro estatistico com N~1.800 imoveis e sem serie historica, Achado 2 (R2/DeepSeek): o diagnostico CIB de 60-90 dias so e construivel se o cadastro da Fazenda vier tabular com chave geografica (setor), Achado 1 (R3/DeepSeek): o art. 256 nao muda o escopo da v1; o metodo defensavel perante TCE e regressao hedonica/CAMA com coeficientes declarados, GBM so como benchmark, Achado 4 (R3/DeepSeek): fases e criterios de aceite do plano v1 de 60-90 dias; o prazo quebra se o cadastro nao tiver setor ou se >20% exigir geocodificacao manual, Achado 6 (R3/DeepSeek): riscos novos - homologacao CADURB exige e-CAC/certificado, valor de referencia != valor venal, ITBI subdeclarado enviesa o modelo, Achado 3 (R3/DeepSeek): o Roteiro Tecnico do CADURB torna obsoleto o modelo setor_censitario/imovel_fazenda - alvo passa a ser unidade_imobiliaria com CIB e lote_remessa_cadurb, Achado 4 (R3/GLM): avaliacao em massa anual quebra em mercado fino, responsabilidade tecnica (ART) e cadastro sujo; aceite = remessa aceita no CADURB, Achado 5 (R5/DeepSeek): modelo em duas camadas - territorio (painel publico) e imovel (remessa, com titular e ITBI sigilosos); nao se misturam (+4 more)

### Community 26 - "Janela regulatória e modelo de receita"
Cohesion: 0.18
Nodes (12): Achado 2 (R1/GLM): a janela CIB/SINTER (jan/2027, ~5.540 municipios) cria comprador novo (Fazenda) e produto novo, e a proposta ignora, Achado 4 (R2/GLM): fee de eficiencia sobre incremento de IPTU so sobrevive com baseline SICONFI publico, exclusao de aliquota e teto, Achado 2 (R3/DeepSeek): dados minimos de calibracao vem de ITBI municipal e cartorio; com <30 por estrato usar modelo hierarquico bayesiano, Achado 2 (R3/GLM): dois produtos - diagnostico de entrada + atualizacao anual do valor de referencia; LTV esperado R$ 145-200 mil por municipio, Achado 3 (R3/GLM): PROFISCO III nao derruba o teto da dispensa, cria a segunda trilha - contratos-programa de R$ 250-450 mil com ciclo de 6-18 meses, Achado 5 (R4/DeepSeek): transferir o modelo Fortaleza->Piaui nao e defensavel para valor absoluto - serve como metodo, nunca como coeficiente, Achado 1 (R4/GLM): correcao formal do R3 - o Piaui real sao dois negocios; com IPTU mediano de R$ 2.214/ano o fee de eficiencia morre em 212 de 224 municipios, Achado 4 (R5/DeepSeek): o bloco ITBI do CADURB traz apenas a ultima transacao - exige versionamento temporal local e pooling regional em municipios pequenos (+4 more)

### Community 27 - "Protótipos anteriores"
Cohesion: 0.21
Nodes (12): Análise de Viabilidade — Dashboard de Gestão Municipal, CERURB não tem API pública, Plano de três fases (dado público, coleta própria, ML), Matriz de Responsabilidade — Fontes de Dados, Negociações institucionais por domínio de dado, Protótipo de 18 bairros com dado ilustrativo, Simulador de investimento (parâmetros inventados), Três números da conversa (13/16 · 0 APIs · 107 dias) (+4 more)

### Community 28 - "Fontes fiscais e lista qualificada"
Cohesion: 0.18
Nodes (11): SICONFI / Tesouro Nacional, Fontes públicas testadas (IBGE, SICONFI, ANEEL, SIDRA), Pipeline replicável por código IBGE (5.570 municípios), Série de arrecadação de IPTU de Teresina (2021–2025), Mapa indicador → fonte real (11 de 15 com dado aberto), APIs descontinuadas (INEP, DataSUS, Atlas Brasil, SNIS), API pública do TCE-PI (Portal da Cidadania), Altos como melhor candidato a piloto fora da capital (+3 more)

### Community 29 - "SINTER, CIB e segmentos"
Cohesion: 0.20
Nodes (11): SINTER (Decreto 8.764/2016), CADURB — Módulo Cadastro Urbano do SINTER, Roteiro Técnico de Integração ao SINTER (restrito), Segmento B — conformidade CIB pura (~215 municípios), Segmento C — expansão CE e MA, 1.904 municípios aderidos ao SINTER (66% ainda fora), API REST do CADURB (SERPRO, token Bearer, Swagger), Manual Operacional CADURB v1.12 (público, 91 páginas) (+3 more)

### Community 30 - "Beachhead Piauí e tenants"
Cohesion: 0.20
Nodes (11): Reconhecimento por Certificate Transparency (307 subdomínios), Foxinline como incumbente regional (~236 tenants em 5 estados), Arquitetura multi-tenant por subdomínio do CERURB Pro, Beachhead Piauí (custo explícito de disputar o quintal do incumbente), Erro de método: inferir inexistência a partir de busca incompleta, Aceite objetivo: remessa aceita pelo CADURB, Lista qualificada dos 25 municípios do PI com bairros, Ressalva: ausência no Certificate Transparency não prova não-cliente (+3 more)

### Community 31 - "Ponte do Segmento B para o A"
Cohesion: 0.24
Nodes (11): Art. 256 — valor de referência anual dos imóveis, Avaliação em massa (CAMA / mass appraisal), LC 214/2025, Base de treino pública georreferenciada para avaliação em massa, ITBI Fortaleza (dados abertos, 79.985 transações), ITBI aberto em capitais (Recife, BH, Porto Alegre, SP), Bloco ITBI do schema CADURB (§5.7), Ponte: conformidade CIB produz o conjunto de treino da PGV (+3 more)

### Community 32 - "Pesos declarados versus k-means"
Cohesion: 0.22
Nodes (11): V05000 e cobertura do entorno por município, Variáveis de entorno do Censo 2022 (V05006–V05030), D_dependência — dependência demográfica (0,20), D_infra — déficit de infraestrutura urbana (0,30), D_saneamento — déficit de saneamento (0,25), Governança dos pesos (mudança versionada), Índice de Vulnerabilidade Territorial (IVT), k-means como camada exploratória (+3 more)

### Community 33 - "Redução de escopo da v1"
Cohesion: 0.24
Nodes (11): Achado 5 (R1/DeepSeek): stack minimo e PostGIS + ETL + BI; descartar o prototipo HTML estatico como base tecnica, Achado 3 (R2/DeepSeek): ingestao minima deve evitar SIDRA em runtime, usar cache/retry e PostGIS; Base dos Dados/BigQuery nao serve ao ativo central, Achado 2 (R4/DeepSeek): descartar o HTML como codigo - array hardcoded, 18 registros, dados que contradizem o IBGE; reimplementar 8 telas, congelar 2, Achado 1 (R4/DeepSeek): a v1 encolhe de 60-90 dias para 3-4 semanas, so Teresina, com Agregados_por_Bairro, entorno por face e SICONFI ja baixados, Achado 6 (R4/GLM): veredito mantido sobre o modelo bifurcado, com plano de 12 meses PI->CE->MA e gatilhos revistos, Achado 5 (R4/GLM): o prototipo com dado ficticio queima a vitrine - Mocambinho 36% no prototipo contra 99,6% real, erro de 63,6 pontos na direcao errada, Achado 2 (R4/GLM): Teresina nao e o piloto - Lei 6.383/2026, IPTU suspenso sob auditoria do TCE-PI e forca da Foxinline; piloto sao 2-3 municipios do Programa Regularizar, Achado 5 (R5/GLM): o conector CADURB sobe para o M0 e a meta do piloto endurece de 'contratada' para 'remessa aceita em homologacao' (+3 more)

### Community 34 - "Mercado e capacidade de pagamento"
Cohesion: 0.20
Nodes (10): CIB — Cadastro Imobiliário Brasileiro, Janela regulatória como argumento comercial, Art. 265/266 — inscrição obrigatória no CIB e prazos, MUNIC/IBGE como motor de qualificação comercial, Conformidade legal obrigatória como argumento de venda no PI, Fee de eficiência sobre IPTU é inaplicável no PI, Mediana de IPTU no PI: R$ 2.214/ano, Mercado do Piauí — 224 municípios medidos (+2 more)

### Community 35 - "Deck e apresentação"
Cohesion: 0.20
Nodes (10): Erro factual do exemplo Tabajaras (média × mediana), Encoding não uniforme dos arquivos do IBGE, D_renda — déficit de renda (0,25, mediana V06006), docs/metodologia-iv.md, painel/build_dados.py (ETL), apresentacao/ — deck com capturas do painel, Inventário de bases públicas verificadas, dados/bruto/ com script de ingestão idempotente (+2 more)

### Community 36 - "Merge da sessão ZCode"
Cohesion: 0.22
Nodes (10): dados/qualificacao-pi.csv — 224 municípios qualificados, Ressalva: ITBI rural × CADURB urbano, Segmento ITBI alto com IPTU nulo (sul do PI), Sinal RREO — município que não entrega demonstrativo fiscal, Classificação RREO derivada dos três exercícios, Defeito de maxZoom no Leaflet (getBoundsZoom Infinity), Painel único (painel/index.html), publicar-cf.sh / wrangler pages deploy (+2 more)

### Community 37 - "Deploy com autenticação"
Cohesion: 0.20
Nodes (10): Laudo em HTML (artefato entregável), Armadilha do CWD do wrangler, Escolha do Cloudflare Pages em vez da Vercel, Middleware de basic auth (_middleware.js), Publicar o painel com usuário e senha, Token de API em vez de wrangler login, Exportação de CSV com proveniência no cabeçalho, Fallback de download em sandbox (+2 more)

### Community 38 - "Prazo legal e CNEFE no README"
Cohesion: 0.22
Nodes (10): O gargalo é a transmissão, não a adesão, Janela de 107 dias e assinatura em nov–dez, Pedido à RFB — adesões e remessas por município, Pedido à SEFAZ-PI — repasse de IBS por município, Textos de e-SIC prontos para envio, Janela de 31/12, CIB — Cadastro Imobiliário Brasileiro, CNEFE como estimativa do volume da remessa (+2 more)

### Community 39 - "Painel: operação e narrativa"
Cohesion: 0.28
Nodes (9): Validação offline no aparelho, Painel Gerencial — Gestão Territorial Teresina (protótipo com dado real), Conversa — narrativa de cinco telas (Teresina), Três entregas (painel, conformidade CIB, coleta própria), Painel CERURB (aplicação de arquivo único), As onze telas, Operação sem internet (Leaflet vendorizado), Painel CERURB · Piauí (LEIAME) (+1 more)

### Community 40 - "Agrupamento e universo amostral"
Cohesion: 0.28
Nodes (9): Entorno — denominador sem "não declarado", Índice de Vulnerabilidade por k-means, sem pesos inventados, Metodologia dos Indicadores e do IV — v2, Universo n ≥ 50 domicílios (substitui n ≥ 50 faces), Agrupamento k-means (k=3, sementes fixas), Dois cortes de universo (n_ok e n_ok_ent), Metodologia e fontes, Perfis socioeconômicos (+1 more)

### Community 41 - "Plano: posicionamento e LGPD"
Cohesion: 0.25
Nodes (8): Limitações do IVT (erro ecológico, snapshot 2022), Modo sem-bairro (agregados por município), Fases 1/2/3 (bases públicas → coleta própria → ML), Parâmetros LGPD do desenho, Só 25 dos 224 municípios do PI têm divisão de bairros, Frase de posicionamento, Segmento B — Conformidade CIB, Separação de camadas território × imóvel (LGPD)

### Community 42 - "Propriedade do dado como ativo"
Cohesion: 0.29
Nodes (8): Achado 6 (R1/DeepSeek): ativo indefensavel sem contrato de titularidade e base legal LGPD - municipio e controlador, Foxinline e concorrente, Achado 3 (R1/DeepSeek): a granularidade 'bairro' prometida nao existe nas fontes publicas - setor censitario != bairro, Achado 5 (R1/GLM): menor escopo que fecha contrato e o diagnostico de conformidade CIB sobre dado aberto, 60-90 dias, um municipio, Achado 3 (R1/GLM): propriedade do dado e o unico ativo defensavel; armadilhas sao LGPD e Lei 14.133 - quatro clausulas inegociaveis, Achado 6 (R2/DeepSeek): 'formato aberto' sem schema versionado, dicionario de dados e chave geografica nao e ativo defensavel; exportacao inutil, Achado 4 (R2/DeepSeek): 'potencial de IPTU nao arrecadado' nao e subtracao direta - exige domicilios IBGE x imoveis lancados e margem declarada de +/-30-50%, Achado 5 (R2/GLM): preco de tabela da v1 R$ 49,5-58,8 mil, calibrado para caber na dispensa por valor (~R$ 59 mil), Achado 4 (R4/DeepSeek): a agregacao setor->bairro correta e interpolacao por area, nao centroide, com flag de cobertura e erro ecologico declarado

### Community 43 - "PGV e defasagem do valor venal"
Cohesion: 0.33
Nodes (7): Módulo 3 — Planta Genérica de Valores (PGV), ROI documentado de recadastramento + PGV, Exposição da defasagem como mecanismo de recorrência, IN RFB 2.275/2025 (cartórios compartilham operações imobiliárias), PGV como obrigação anual recorrente (tese otimista), Proposta de valor: medir a defasagem antes da Receita publicá-la, Segmento A — tese fiscal completa (~9 municípios)

### Community 44 - "Reforma tributária e NT da CNM"
Cohesion: 0.29
Nodes (7): Adesão ao Convênio SINTER em 16 passos, Condução da adesão como produto de entrada, Nota Técnica CTAT nº 05/2025 da CNM, PROFISCO III (Ministério da Fazenda / BID), Correções à cadeia tributária (art. 266, prazo 31/12/2026, PROFISCO), Vende-se a capacidade de cumprir, não o acesso ao CIB, Credencial CADURB depende de município conveniado

### Community 45 - "Vereditos do eixo de negócio"
Cohesion: 0.38
Nodes (7): Achado 6 (R1/GLM): sinais de nao entrar e criterio de saida - sem contrato com dotacao em 45 dias, abortar, Achado 2 (R2/GLM): no 'Observatorio Municipal' puro o diferencial e zero - a Geopixel ja vende isso com +100 municipios, Achado 6 (R2/GLM): veredito ENTRAR COM CONDICOES - seis condicoes verificaveis e cinco gatilhos de abandono, Achado 1 (R3/GLM): correcao formal do R2 - o art. 256 da LC 214/2025 torna a tese receita recorrente por lei, nao 'produto de prazo'; gatilho (v) invalidado, Achado 5 (R3/GLM): a vantagem de ser primeiro dura um mandato por conta e e ~zero por mercado; o que comprime a janela e o lote estadual, Achado 6 (R3/GLM): veredito revisado ENTRAR COM CONDICOES - risco reprecificado de commoditizacao por prazo para lote estadual e motor central da RFB, Achado 4 (R4/GLM): a unica posicao que nenhum incumbente ocupa e o prazo legal do municipio sem cadastro, sem IPTU e sem equipe; CERURB != CIB

### Community 46 - "Cashback e dispensa única"
Cohesion: 0.29
Nodes (7): Achado 3 (R6/GLM): sequencia de reunioes fazenda -> prefeito -> APPM -> planejamento -> TJ-PI; a reuniao de escopo com o proponente REURB precede as cinco, Achado 3 (R7/GLM): o laudo e venda se medir a distancia a uma norma nova e constrangimento se medir a qualidade do cadastro - cinco regras de apresentacao, Achado 1 (R7/GLM): o validador offline muda a abertura, nao a sequencia - laudo-demo e pedido de export em 72h; e o laudo nao custa quase nada (1-2 dias de ingestao semantica por municipio), Achado 5 (R7/GLM): manter R$ 3-5 mil com reembolso na assinatura - laudo gratis mata a ancora para sempre e vaza o desenho do diagnostico, Achado 1 (R8/GLM): acato a correcao - reembolso condicionado a contrato futuro nao tem categoria contabil em ente publico; substituir por dispensa unica e desconto formal, Achado 3 (R8/GLM): dispensa unica vence - dois ciclos de processo nao cabem na janela decisao 20/11 -> empenho 10/12; encadeadas jogam a conformidade para 2027, Achado 2 (R8/GLM): o paragrafo 2 dobra o limite para consorcio publico (R$ 130.984,22), nao para a APPM, que e associacao civil; muda a escala de 2027, nao o motor de 2026

### Community 47 - "Entregáveis do M0"
Cohesion: 0.29
Nodes (7): Cobertura por campo (métrica-título do laudo), dominios_cadurb.json (11 tabelas de domínio), faixas_cep injetada por contexto, Fluxo de geometria (idLotePonto/idLotePoligono, /vinculacoes/{idLote}), Falha impeditiva × atenção, Manual Operacional CADURB v1.12, regras_semanticas.py (10 regras do laudo)

### Community 48 - "REURB e erro ecológico"
Cohesion: 0.33
Nodes (6): Lei 13.465/2017 (REURB, CRF, art. 35 e 40), Módulo 1 — Base Cartográfica Digital, Defasagem do valor venal (mediana 30,8% do mercado), Ressalvas metodológicas da medição de defasagem, Favelas e Comunidades Urbanas do Censo 2022 (vetorial), Erro ecológico do índice por bairro

### Community 49 - "Números da credencial"
Cohesion: 0.40
Nodes (6): Credencial técnica (1 página), Números do Sinter sem lastro (188 no Brasil; só Teresina no PI), Ranking oficial com pesos declarados (correção de credencial), Verificação do Sinter por fonte pública (não possível), adesoes.xls da RFB não é lista de adesões (tabela TOM), 188 municípios com CIB ativo (inscricoes_ativas)

### Community 50 - "Entregas e cronograma"
Cohesion: 0.33
Nodes (6): Protótipo HTML de 18 bairros (dado fictício), Cronograma de 10 dias (D1–D10), E1 — Painel Territorial de Teresina, E2 — Diagnóstico de Conformidade CIB, Regras inegociáveis (nenhum número inventado), Município-piloto (Guaribas, N. Sra. de Nazaré)

### Community 51 - "Risco Foxinline"
Cohesion: 0.40
Nodes (6): Achado 1 (R1/DeepSeek): integracao CERURB em tempo real e ilusao - nao ha REST, o trafego e JSF/PrimeFaces com ViewState, scraping autenticado quebra a cada mudanca de tela, Achado 1 (R1/GLM): o risco Foxinline e de mercado, nao de integracao - ela acumula fornecedora do dado, unico canal e concorrente adjacente, Achado 1 (R2/DeepSeek): com api-exportacao viva, a via primaria e pedir credencial e contrato de uso; scraping so como ultimo recurso, Achado 1 (R2/GLM): corrige o R1 - Foxinline com ~236 tenants nao vai quebrar; integrar so sob mandato contratual do municipio, OEM como opcao de 30 dias, Achado 3 (R4/GLM): a clausula 4.1.1 abre o dado CERURB a orgaos, nao a empresas; e o produto B nao precisa do CERURB porque a REURB gera o insumo, Achado 2 (R6/GLM): adiar o e-mail a Foxinline - chegar sem ativo educa quem tem 236 relacionamentos; trocar por deck pronto e monitoramento passivo

### Community 52 - "ETL build_cnefe"
Cohesion: 0.40
Nodes (4): aneis_do(), dentro(), Anéis externos do polígono, como arrays Nx2. Ignora buracos: um endereço num…, Regra par-ímpar, vetorizada por aresta. px/py já filtrados pela bbox.

### Community 53 - "Basic auth do Cloudflare Pages"
Cohesion: 0.70
Nodes (4): b64utf8(), igual(), NEGADO(), onRequest()

### Community 54 - "Coleta própria via REURB"
Cohesion: 0.67
Nodes (4): Achado 2 (R1/DeepSeek): coleta propria nao e feature, e outro produto - exige app de campo offline-first, sync, georreferenciamento, LGPD e equipe, Achado 4 (R1/GLM): o modelo de receita e projeto unico disfarcado - aerolevantamento domina o custo e ML/chat inflam custo fixo sem receita, Achado 5 (R2/DeepSeek): coleta minima e PWA offline-first de 10-15 campos acoplado ao levantamento planialtimetrico da REURB, nao sistema paralelo, Achado 3 (R2/GLM): a cartografia obrigatoria da REURB destroi a estrutura de preco - o aerolevantamento ja esta pago no contrato do parceiro

### Community 56 - "ETL parametrizável"
Cohesion: 0.67
Nodes (3): Achado 5 (R3/DeepSeek): ativos reutilizaveis (ETL por codigo IBGE, fetcher SICONFI, metodologia de gap, schema CADURB) versus descartaveis (bairros hardcoded, layout), Achado 6 (R4/DeepSeek): arquitetura final - ETL parametrizado por IBGE -> PostGIS -> motor de iv -> API/GeoJSON -> frontend; nucleo reutilizavel, Achado 5 (R6/DeepSeek): faltam duas propriedades baratas no GeoJSON - area do bairro e densidade domiciliar, mais FCUs intersectadas por bairro

## Ambiguous Edges - Review These
- `validador_completude.py` → `k-means × índice com pesos declarados (defensabilidade)`  [AMBIGUOUS]
  analise/17-revisao-m0-outra-sessao.md · relation: conceptually_related_to
- `Marca Vertical Data` → `Painel CERURB — Piauí, 224 municípios`  [AMBIGUOUS]
  .orca/drops/Vertical-Data-Logomarcas.pdf · relation: conceptually_related_to
- `Paleta navy profundo + teal` → `Tema claro do painel`  [AMBIGUOUS]
  .orca/drops/Vertical-Data-Logomarcas.pdf · relation: conceptually_related_to
- `Símbolo pin de mapa` → `Mapa coroplético de bairros de Teresina`  [AMBIGUOUS]
  .orca/drops/Vertical-Data-Logomarcas.pdf · relation: conceptually_related_to
- `Símbolo scatter / linha de pontos` → `Renda mediana × esgoto em rede, por bairro`  [AMBIGUOUS]
  .orca/drops/Vertical-Data-Logomarcas.pdf · relation: conceptually_related_to

## Knowledge Gaps
- **94 isolated node(s):** `Portaria MCid 3.242/2022 (diretrizes do CTM)`, `ANEEL — geração distribuída (CKAN, diário)`, `RCL mediana do PI: R$ 45,7 mi (capacidade de pagamento)`, `Segmento C — expansão CE e MA`, `matriz-responsabilidade-fontes-dados.md (matriz de fontes do cliente)` (+89 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `validador_completude.py` and `k-means × índice com pesos declarados (defensabilidade)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Marca Vertical Data` and `Painel CERURB — Piauí, 224 municípios`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Paleta navy profundo + teal` and `Tema claro do painel`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Símbolo pin de mapa` and `Mapa coroplético de bairros de Teresina`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Símbolo scatter / linha de pontos` and `Renda mediana × esgoto em rede, por bairro`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `Índice de Vulnerabilidade Territorial (IVT)` connect `Pesos declarados versus k-means` to `Spec CADURB e conector M0`, `Deck e apresentação`, `Plano: posicionamento e LGPD`, `Números da credencial`, `Entregas e cronograma`, `ITBI no SICONFI`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Why does `Spec OpenAPI do CADURB (pública)` connect `Spec CADURB e conector M0` to `ITBI no SICONFI`, `Deck e apresentação`?**
  _High betweenness centrality (0.008) - this node is a cross-community bridge._