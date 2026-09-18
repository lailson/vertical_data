1. **Concordo: domicílio é a métrica correta** (Anexo 1, seção 2). Face só é preferível para priorizar obras de pavimentação por custo de via, não para vulnerabilidade ou cobertura. Em domicílios, sobram: n mínimo de 50 domicílios; denominador `V05000 − V05008` (pav) e `V05000 − V05014` (ilum); IC 95% binomial para 50–150. Consequência: substituir já as regras do Anexo 2, seção 11.8 — se ficar o corte de faces, o ranking de bairros com poucos domicílios continuará artefato.

2. **Não dá para testar de verdade sem município conveniado.** O Anexo 6 só documenta token Bearer “fornecido pelo time do CADURB”; no padrão SERPRO, credencial de homologação é vinculada a convênio/adesão do ente, não a um registro avulso. Consequência: obter a adesão do piloto (Guaribas ou N. Sra. de Nazaré) na primeira semana e só então iniciar o conector; se não houver piloto, construir validador offline de schema + mock da API em vez de integrar às cegas, e usar os dias em saneamento cadastral.

3. **INEP deve ser rebaixado.** 537 MB + geocodificação é esforço desproporcional para uma tela entre onze, com risco de custar 1–3 dias sem valor para a tese de conformidade CIB (Anexo 1, seção 3b; Anexo 3, seção 7). Consequência: sai do caminho crítico do M0; entra só em D10 ocioso ou pós-apresentação.

4. **Metodologia do `iv` precisa publicar:** pesos das 5 dimensões, fonte exata de cada variável (arquivo/código IBGE), transformações — inclusive normalização da renda pela mediana municipal com `log1p` —, regras de corte em domicílios (n mínimo, baixa confiança), hash/versão do script e limitações (interpolação areal, erro ecológico, ausência de bairros em 199 municípios). Tempo: 0,5–1 dia, bloqueante para terceiros (Anexo 1, seção 3c).

5. **Faltam duas propriedades baratas no GeoJSON:** área do bairro (m²) e densidade domiciliar (`dom/área`), além de contagem/área de FCUs intersectadas por bairro (Anexo 1, seção 1). Consequência: densidade + favelas mostram em um mapa onde a urbanização informal coexiste com déficit de infra, reforçando a tese REURB com custo de meio dia no D4.

6. **Riscos técnicos não nomeados:**  
   (a) Painel como HTML único de 494 KB não escala para 25+ municípios — cada atualização regenera artefato gigante e torna versionamento/manutenção frágil.  
   (b) O envio em lote no CADURB provavelmente não é só JSON com Bearer: pode exigir arquivo assinado com certificado ICP-Brasil do ente, validação assíncrona e limite de taxa — o que quebra o conector “unitário” assumido no Anexo 6.  
   Consequência: separar dados de frontend já no D7 e construir validador offline de schema antes de depender de endpoint oficial; senão o aceite em homologação atrasa exatamente na janela de 60 dias.
