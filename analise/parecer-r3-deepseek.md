**Achado 1 (Q1)**  
Diagnóstico: O art. 256 da LC 214/2025 (Anexo A) torna a avaliação em massa anual uma obrigação legal, mas isso **não muda** o escopo da v1 — ML/chat continuam fora porque v1 entrega diagnóstico CIB e baseline fiscal, não PGV.  
Consequência: O método defensável perante TCE é regressão hedônica linear/espacial (CAMA) com coeficientes declarados, diagnóstico de resíduos e validação fora da amostra; GBM fica só como benchmark. Exigível: contribuição por atributo, pesos publicados, mapa de erros e análise de colinearidade.

**Achado 2 (Q2)**  
Diagnóstico: Dados mínimos para calibração: preço de transação (ITBI/escritura), área construída, padrão, tipologia, destinação, data e localização georreferenciada; fontes primárias são ITBI municipal e cartório, com portais de anúncio como suplemento e CERURB como cadastro tipológico.  
Consequência: Com amostra insuficiente (< ~30 por estrato zona×tipologia), usar modelo hierárquico bayesiano com empréstimo de informação entre estratos ou abordagem de custo/renda calibrada, declarando incerteza e não emitindo valor pontual para estrato sem dado.

**Achado 3 (Q3)**  
Diagnóstico: O Roteiro Técnico do CADURB (Anexo A) normatiza a saída e o art. 256 exige valor de referência anual, tornando obsoleto o modelo `setor_censitario`/`imovel_fazenda` do Anexo E, achado 2.  
Consequência: Modelo alvo: `municipio(codigo_ibge)`, `unidade_imobiliaria(cib, setor_id, tipologia, destinacao, padrao, data_construcao, area_construida, geom, valor_referencia, data_referencia)`, `lote_remessa_cadurb(protocolo, status_validacao, data_envio)` e `log_erro_validacao`; toda carga passa a ser desenhada para gerar remessa alfanumérica+georreferenciada validável.

**Achado 4 (Q4)**  
Diagnóstico: O plano v1 (60–90 dias) exige fases: Setup (repo/PostGIS/APIs), Ingestão pública (IBGE malhas/Censo, SICONFI IPTU), Ingestão do cadastro da Fazenda (sanitização/geocodificação), Compatibilização setor×imóvel, Cálculo de gap CIB e Baseline fiscal.  
Consequência: Entregáveis e aceites: scripts versionados (aceite: carga sem erro e checksum), cadastro sanitizado com chave setor (aceite: 100% mapeado ou flag), tabela de cobertura/gap (aceite: domicílios IBGE × imóveis lançados), relatório de potencial com incerteza declarada (aceite: ±30–50% explícito). O prazo quebra se o cadastro não tiver setor/endereço georreferenciável, se a entrega da Fazenda atrasar além da semana 3 ou se >20% exigir geocodificação manual.

**Achado 5 (Q5)**  
Diagnóstico: Ativos reutilizáveis desde o dia 1: dimensão `municipio`, ETL parametrizado por código IBGE, fetcher SICONFI, metodologia de gap CIB e schema CADURB.  
Consequência: Descartável no primeiro cliente: nomes hardcoded de bairros, layout visual do dashboard, regras locais de limpeza de endereço e qualquer acoplamento ao CERURB — manter fora do núcleo.

**Achado 6 (Q6)**  
Diagnóstico: Riscos técnicos novos: homologação CADURB exige certificado digital e-CAC e pode ter schema/validação alterados; art. 256 trata valor de referência de mercado, não valor venal de IPTU; ITBI subdeclarado viésa o modelo para baixo; remessa georreferenciada exige acurácia posicional que cadastros antigos não têm; atualização anual gera drift e exige monitoramento contínuo; scraping de portais de anúncio para calibração pode violar termos/LGPD.  
Consequência: Incluir desde já: ambiente de homologação com certificado municipal, validação de schema versionado, separação explícita entre valor de referência e valor venal, auditoria de subdeclaração por escritura e fonte lícita para dados de anúncio; sem isso a remessa é rejeitada e o modelo não se sustenta.
