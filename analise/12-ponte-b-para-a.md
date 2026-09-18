# A ponte do Segmento B para o A — quantificada, e o efeito de rede que ela cria

O schema do CADURB exige o bloco ITBI da última transação. Isso significa que a conformidade
(Segmento B) produz o dado de calibração da avaliação em massa (Segmento A). A pergunta é: **em
quanto tempo, e em quantos municípios?**

## Estimativa para o Piauí

Premissas: domicílios ≈ população / 3,2 · taxa de urbanização do PI ≈ 70% · rotatividade imobiliária
≈ 4% ao ano · o CADURB guarda **só a última transação** por imóvel, logo a série se acumula pelo
versionamento local a cada mudança de `dtTransacaoITBI`.

| Município | População | Imóveis urbanos (est.) | Transações/ano | **24 meses** |
|---|---|---|---|---|
| Teresina | 868.523 | 189.989 | 7.600 | **15.199** |
| Parnaíba | 163.087 | 35.675 | 1.427 | 2.854 |
| Picos | 82.028 | 17.944 | 718 | 1.435 |
| Piripiri | 65.762 | 14.385 | 575 | 1.151 |
| Floriano | 62.593 | 13.692 | 548 | 1.095 |
| Barras | 47.909 | 10.480 | 419 | 838 |
| Altos | 46.826 | 10.243 | 410 | 819 |
| Campo Maior | 45.252 | 9.899 | 396 | 792 |
| José de Freitas | 42.575 | 9.313 | 373 | 745 |
| Esperantina | 40.968 | 8.962 | 358 | 717 |

**Resultado no estado:**

| Corte | Municípios |
|---|---|
| ≥ 500 transações acumuladas em 24 meses | **15 de 152** |
| < 200 transações em 24 meses | **120 de 152** |

## Consequência 1 — a ponte é real, mas estreita

O entusiasmo com "o B alimenta o A" precisa desta ressalva: **alimenta em ~15 municípios do Piauí**,
não nos 224. Nos demais 120+, a amostra própria nunca chega a ser suficiente para um modelo local —
com menos de 200 transações em dois anos, e distribuídas entre tipologias e zonas, cada estrato fica
com punhados de observações.

Para esses, o método correto é **pooling regional com efeitos fixos por município** — um modelo
hedônico estimado sobre o conjunto dos municípios integrados, com intercepto (e possivelmente
inclinação) próprios para cada um.

## Consequência 2 — e aqui está o moat

**Pooling regional só é possível para quem tem muitos municípios integrados.**

Um concorrente com um município não consegue estimar nada defensável para um município de 5 mil
imóveis. Quem tiver 20 municípios integrados no mesmo estado consegue — e cada novo município
melhora a estimativa de todos os outros.

**O valor do modelo cresce com o número de contas, e o custo marginal de cada nova conta cai.**
Isso é efeito de rede de dados, e é a primeira vantagem estrutural identificada em toda a análise
que **não** depende de relacionamento, preço ou pioneirismo — depende de acumular contas, que é
exatamente o que o Segmento B faz.

**Implicação comercial direta:** isso é o argumento econômico para **subsidiar o Segmento B**. Cada
conta B, mesmo com margem magra, compra uma peça do ativo que torna o Segmento A viável — e o
Segmento A é onde está o LTV de R$ 145–239 mil por conta.

**Implicação de contrato:** a cláusula que permite o uso agregado e anonimizado dos dados de
transação para calibração de modelo — respeitada a LGPD, com o município como controlador — deixa de
ser detalhe jurídico e vira **a cláusula que constitui o ativo da empresa**. Se cada contrato proibir
o uso cruzado, o efeito de rede não existe e sobra uma consultoria que termina.

## Ressalvas
1. As estimativas de imóveis urbanos e rotatividade são grosseiras (±30%). Servem para ordenar
   decisão, não para projeção de receita.
2. `baseCalculITBI` é **subdeclarado** — exige filtro de outliers e auditoria antes de treinar.
3. O bloco ITBI é **opcional** no schema do CADURB. Municípios podem enviar remessa sem ele; garantir
   o preenchimento é parte do serviço, e é o que preserva a ponte.
4. O acúmulo depende de **persistência local versionada**: o CADURB devolve o estado atual, não o
   histórico. Quem não guardar, perde a série.
