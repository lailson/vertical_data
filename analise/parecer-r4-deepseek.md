Concordo com as correções 1–3 e com o veredito de protótipo como maquete visual.

**Achado 1 (Q1) — Escopo da v1 muda de 60–90 dias para 3–4 semanas, só Teresina, com dado aberto real.**  
Diagnóstico: `Agregados_por_Bairro`, entorno por face (`V05406`, `V05412`, `V05409`), favelas vetoriais e SICONFI eliminam negociação para 11 indicadores; já estão baixados (Anexo 2 itens 1,4,5; Anexo 3 §9).  
Consequência: v1 vira painel territorial aberto com 123 bairros oficiais, camada de favelas, arrecadação real e `iv` calculado; PGV/ML/CERURB ficam fora até haver cadastro/ITBI local.

**Achado 2 (Q2) — Descartar o HTML como código; manter as 11 telas como wireframe; reimplementar 8, congelar 2, manter 1.**  
Diagnóstico: array hardcoded, 18 registros, `iv` sem fórmula, dados que contradizem o IBGE — Mocambinho protótipo 36% vs real 99,6% (Anexo 3 §3–4, §8).  
Consequência: recriar Painel, Mapa, Ranking, Saneamento, Pavimentação, Educação, Perfis e Séries com backend/PostGIS; congelar Simulador e Status CERURB até haver modelo de impacto e convênio; Relatórios viram exportação com metodologia auditável.

**Achado 3 (Q3) — Fórmula publicável para `iv`, com variáveis que já existem por bairro.**  
Diagnóstico: o índice central era número digitado à mão, sem reprodutibilidade (Anexo 3 §3).  
Consequência: `iv = 100*(0.25*infra_deficit + 0.20*saneamento_deficit + 0.20*renda_vul + 0.20*informalidade + 0.15*dependencia)`; onde `infra_deficit = média(1−pav, 1−ilum, 1−bueiro)`; `saneamento_deficit = % domicílios sem esgoto/água`; `renda_vul = % responsáveis ≤1 SM`; `informalidade = % em favela/comunidade`; `dependencia = (0–14 + 65+)/pop`. Pesos e códigos IBGE versionados em script, reprodutível.

**Achado 4 (Q4) — Agregação setor→bairro tem método correto: interpolação por área, não centroide.**  
Diagnóstico: renda só existe por setor; limite de setor não respeita limite de bairro (Anexo 2 item 2).  
Consequência: usar interpolação areal dos polígonos de setor sobre os 123 bairros, com flag de cobertura; bairro com fração de domicílios alocados <80% aparece como “estimado”, e o painel declara erro ecológico e incerteza agregada.

**Achado 5 (Q5) — Transferir modelo Fortaleza→Piauí não é defensável para valor absoluto; usar para método, não para nível.**  
Diagnóstico: mercados imobiliários distintos; no PI não há ITBI aberto e a mediana de IPTU é R$ 2.214/ano (Anexo 1; Anexo 5).  
Consequência: vender no PI conformidade CIB/cadastro primeiro, não PGV; calibrar só depois com ITBI municipal, cartórios via SINTER (IN RFB 2.275/2025) ou cadastro REURB; Fortaleza serve como pipeline e prova de defasagem, nunca como coeficiente transferido.

**Achado 6 (Q6) — Arquitetura final: data ingestion parametrizado → PostGIS → motor de `iv` → API/GeoJSON → frontend; núcleo reutilizável.**  
Diagnóstico: o que quebra o plano é recortar por município desde o início; dashboard não pode ser HTML hardcoded (Anexo 7 Achados 4–5).  
Consequência: construir na ordem: (1) ETL parametrizado por IBGE, (2) schema `municipio/bairro/setor/indicador/fonte/metodologia`, (3) motor de indicadores e remessa CADURB depois; reutilizável: fetchers, schema, iv, frontend; não reutilizável: regras locais de limpeza de endereço, geometria e acordos institucionais.
