**1. Sim, a credencial promete mais do que o M0 entrega — nos itens 2, 3 e 4.**  
Diagnóstico: “construído e demonstrável hoje” (Anexo 1: itens 2–4) cobre conector gerado, laudo sintático e metodologia exploratória, não produtos prontos. Consequência: redação honesta — item 1: OK; item 2: “conector gerado da spec pública, ainda não homologado”; item 3: “laudo preliminar alfanumérico, regras semânticas em implementação”; item 4: “metodologia exploratória, índice oficial com pesos declarados pendente”; item 5: OK.

**2. A frase “sem índices de pesos arbitrários” não é defensável como está.**  
Diagnóstico: o k-means com normalização min–max da amostra (Anexo 5: §1) introduz escolhas implícitas de k, semente e intervalo que mudam com a entrada. Consequência: redação correta: “Ranking oficial baseado em cortes fixos e pesos declarados; k-means usado apenas como análise exploratória interna.”

**3. Conjunto mínimo para defender R$ 3–5 mil, em ordem de valor/esforço:**  
(1) unicidade de `inscricaoImobiliaria`; (2) cobertura por campo/bloco obrigatório; (3) tabelas de domínio da seção 9 versionadas (Anexo 4: §2); (4) DV de CPF/CNPJ/CIB; (5) coerência `tipoImovel` × `areaConstruida`/`tpArquitetonico`; (6) `anoConstrutivo` ≤ corrente e `areaTerreno` > 0; (7) soma de `percTitularidade`/`percTransac…ITBI` = 1; (8) CEP existe e pertence ao município. Sem 1–6, continua um required-checker.

**4. `TipoFalhaDTO` é necessário, mas insuficiente.**  
Diagnóstico: é só enum de código de falha (Anexo 4: §3), não estrutura relatório. Consequência: camada própria em três níveis — (a) legenda oficial `TipoFalhaDTO` por erro; (b) agrupamento por bloco/campo/regra com incidência e %; (c) sumário executivo com top falhas impeditivas da remessa.

**5. “Conector pronto para operar assim que o município adere” não é verdade.**  
Diagnóstico: está pronto o scaffold OpenAPI alfanumérico (Anexo 1: item 2); não estão prontos o fluxo de geometria por lote+vinculação (Anexo 4: §6) nem a pinagem da spec `0.0.1-SNAPSHOT` com teste de divergência (Anexo 4: §5). Consequência: redação honesta: “conector alfanumérico gerado da spec pública, pendente de homologação contra cadastro real; geometria fora da promessa atual.”

**6. Risco técnico central: prometer sem testar contra cadastro real valida contra contrato obsoleto e dado fictício.**  
Diagnóstico: Anexo 1: itens 2–3 prometem conector e laudo; Anexo 4: §5 mostra ausência de teste de divergência e de cadastro real. Consequência: a primeira execução real pode ocorrer no cliente — laudo divergindo da validação oficial, remessa recusada em homologação e risco de disputa contratual; mitigação: rodar contra cadastro real em sandbox antes de vender.
