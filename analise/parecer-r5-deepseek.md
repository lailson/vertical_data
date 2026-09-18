**Anexo N — Fechamento Técnico da Rodada 5**

**Achado 1 (Anexo N)**  
Diagnóstico: o CADURB é API REST documentada com endpoints de envio, consulta, desativação e lote (Anexo A §2), e o schema inclui o bloco ITBI da última transação (Anexo A §5.7).  
Consequência: o produto de conformidade deixa de ser “implementar formato normatizado do zero” e vira **camada de integração + saneamento cadastral**: conector autenticado por token Bearer, transformador cadastro→schema, validador prévio e pipeline de retorno do CIB. Estimativa de engenharia reutilizável cai para 2–3 semanas; o tempo total por município é dominado por adesão institucional e limpeza do cadastro (6–8 semanas). Caminho crítico real: obter token de homologação via convênio e completar os campos obrigatórios (Anexo A §5.1), não a API.

**Achado 2 (Anexo N)**  
Diagnóstico: Tabajaras tem apenas 19 faces medidas para 293 domicílios (Anexo B §2), e V05408/V05414 (“não declarado”) entram no denominador, subestimando cobertura.  
Consequência: adotar **n ≥ 50 faces** para exibir indicador; entre 50 e 150 marcar como “baixa confiança” com IC 95% binomial; denominador = `V05400 − V05408` para pavimentação e `V05400 − V05414` para iluminação. Bairros com n < 50 saem do ranking e aparecem apenas com selo “amostra insuficiente”.

**Achado 3 (Anexo N)**  
Diagnóstico: renda por bairro existe via V06006 (mediana), com razão média/mediana de até 1,59 (Anexo B §1); a fórmula anterior duplicava esgoto (Anexo E §Ressalvas).  
Consequência: fórmula publicável passa a ser:  
`iv = 100 × (0,30·infra_deficit + 0,25·saneamento_deficit + 0,20·renda_deficit + 0,15·informalidade + 0,10·dependencia)`  
com `infra_deficit` = média de (1−pav), (1−ilum), (1−bueiro); `saneamento_deficit` = média de (1−esgoto_adequado) e (1−água_adequada), **sem duplicar esgoto**; `renda_deficit = max(0, 1 − log1p(V06006)/log1p(mediana_municipal_V06006))`. Justificativa: infra e saneamento respondem por 55% do índice porque são os déficits mais discriminantes por bairro; renda é dimensão transversal com robustez via mediana e compressão logarítmica; informalidade e demografia entram como ajustes porque dependem de camada vetorial/população.

**Achado 4 (Anexo N)**  
Diagnóstico: o bloco ITBI do CADURB (Anexo A §5.7) fornece preço + atributos por imóvel, mas contém **apenas a última transação**, não o histórico completo.  
Consequência: o caminho do dado é: cadastro saneado → remessa via API → CIB retornado → persistência local do bloco ITBI **em tabela com versionamento temporal** (sempre que `dtTransacaoITBI` muda, gravar nova linha) → dataset de treino para regressão hedônica espacial. Com rotatividade de ~3–5% ao ano, apenas municípios com >20 mil imóveis urbanos geram amostra utilizável em 24 meses (Teresina, Parnaíba, Picos, Floriano e talvez Piripiri/Altos); os demais 215 do PI ficam com <200 transações/ano e exigem pooling regional com efeitos fixos, nunca modelo próprio.

**Achado 5 (Anexo N)**  
Diagnóstico: o painel por bairro precisa de agregados censitários; a remessa CADURB precisa de dados por imóvel, incluindo titular e ITBI (Anexo A §5.1–5.7).  
Consequência: modelo de dados em duas camadas: `territorio` (municipio, bairro, setor, face) e `imovel` (unidade_imobiliaria, edificacao, titular, itbi), ligadas por `codigoIbge` e por interseção espacial no PostGIS. O encontro é o georreferenciamento do imóvel dentro de setor/bairro. Não se misturam: o painel lê apenas `agregado_bairro` e `face_entorno` agregada, sem CPF ou valor individual; a remessa lê apenas `imovel`, sem indicadores territoriais. Dados de titular e ITBI são sigilosos e não alimentam o painel público.

**Achado 6 (Anexo N)**  
Diagnóstico: nenhum anexo anterior nomeia riscos de versionamento do schema CADURB, ambiente de homologação sem adesão, viés de subdeclaração no ITBI, limites da API em lote ou sincronização pós-CIB.  
Consequência: o produto precisa de adaptador versionado (v1.12+), contrato municipal para token de homologação, filtro de outliers/auditoria fiscal no `baseCalculITBI` antes de treinar modelo, controle de fila/idempotência nos endpoints de lote e fluxo de atualização da base local com o CIB retornado para evitar duplicidade de inscrição.
