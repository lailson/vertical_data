# Arbitragem da 2ª rodada da análise paralela — verificações feitas

## 1. ERRO MEU, confirmado: renda POR BAIRRO existe

Afirmei que "não existe arquivo de renda por bairro; o rendimento está só por setor censitário".
**Falso.** A pasta `Agregados_por_Setores_Censitarios_Rendimento_do_Responsavel/` contém:

```
Agregados_por_bairros_renda_responsavel_BR_20260508_csv.zip     ← existe
Agregados_por_distritos_renda_responsavel_BR_20260508_csv.zip
Agregados_por_municipios_renda_responsavel_BR_20260508_csv.zip
Agregados_por_setores_renda_responsavel_BR_20260508_csv.zip
Agregados_por_subdistritos_renda_responsavel_BR_20260508_csv.zip
```

Baixado e validado: **17.378 bairros no Brasil, 122 de Teresina**.

**Causa do erro, e ela se repetiu:** procurei renda dentro de `Agregados_por_Bairro_csv/`, não achei, e
concluí ausência. A pasta irmã eu cheguei a listar, mas não abri. **É o mesmo erro de método que
cometi antes com a granularidade de bairro: inferir inexistência a partir de uma busca incompleta.**
Duas vezes, no mesmo conjunto de dados. Registro para não repetir.

**Consequência prática:** cai a necessidade de interpolação areal setor→bairro para renda, e cai a
ressalva de "estimado" que o parecer técnico exigia para esse indicador. Renda é dado direto por
bairro, um download.

### Dicionário correto (meu parser anterior estava deslocado; a outra análise estava certa)
| Variável | Significado |
|---|---|
| V06001 | Pessoas responsáveis em domicílios particulares permanentes ocupados |
| V06002 | Moradores em domicílios particulares permanentes ocupados |
| V06003 | Variância do número de moradores |
| **V06004** | **Rendimento nominal MÉDIO mensal das pessoas responsáveis** |
| V06005 | Variância do rendimento |
| **V06006** | **Rendimento nominal MEDIANO mensal das pessoas responsáveis** |

### Renda real — Teresina (rendimento mediano, V06006)
| Menores | R$ | Maiores | R$ |
|---|---|---|---|
| Olarias | 1.200 | Zoobotânico | 8.000 |
| Vila São Francisco | 1.200 | Frei Serafim | 9.000 |
| Árvores Verdes | 1.200 | Fátima | 10.000 |
| Chapadinha | 1.200 | Jóquei | 12.000 |
| Alto Alegre | 1.212 | Tabajaras | 15.000 |

**Validação cruzada com o índice calculado:** Chapadinha, Olarias e Árvores Verdes têm a menor renda
**e** aparecem no topo do ranking de vulnerabilidade; Jóquei, Frei Serafim e Fátima têm a maior renda
**e** o menor IV. Duas fontes independentes do Censo concordando — isso valida o índice.

**Usar mediana (V06006), não média (V06004).** Razão média/mediana chega a 1,59 (Brasilar) e 1,58
(Mocambinho) — a média é puxada por outliers e inverte posições no ranking.

## 2. ACHADO NOVO E CRÍTICO — armadilha no dado de entorno: bairros com poucas faces

A anomalia que disparou a investigação: **Tabajaras** tem a **maior renda mediana de Teresina
(R$ 15.000)** e, no meu cálculo, teria só **36,8% de pavimentação** e 57,9% de iluminação —
impossível para um bairro nobre.

Causa verificada:

| Bairro | Faces medidas | Pav. sim | Domicílios | Leitura |
|---|---|---|---|---|
| Centro | 1.521 | 1.521 | 2.838 | robusto (100%) |
| Chapadinha | 761 | 279 | 2.026 | robusto (36,7% é real) |
| Morros | 565 | 260 | 1.761 | robusto |
| Jóquei | 525 | 523 | 2.520 | robusto (99,6%) |
| **Tabajaras** | **19** | 7 | **293** | **não confiável** |

**Tabajaras tem 19 faces medidas para 293 domicílios.** Com n=19, cada face vale 5,3 pontos
percentuais. O número é ruído, não medição.

**Consequência obrigatória para o produto:** o indicador de entorno precisa de **corte mínimo de
faces** (sugestão: n ≥ 50, com faixa de confiança exibida entre 50 e 150) e de tratamento explícito
da categoria **"não declarado"** (V05408/V05414), que hoje entra no denominador e subestima a
cobertura. Sem esses dois cuidados, bairros pequenos aparecem no topo do ranking de prioridade por
puro artefato amostral — e o painel manda investimento público para o lugar errado, que é exatamente
o defeito que estamos corrigindo no protótipo.

**Este é o tipo de erro que só aparece em validação cruzada entre fontes.** Nenhuma das três análises
o teria encontrado sem cruzar renda com entorno.

## 3. Correções que a outra análise faz à cadeia tributária — aceitas

| Minha formulação | Correção |
|---|---|
| "art. 256 obriga o município" | **A obrigação de inscrição no CIB é o art. 265/266.** O art. 256 trata do *valor de referência* — é o que sustenta a tese da PGV, não a do cadastro. Eu misturei os dois papéis. |
| "prazo 01/01/2027" | **31/12/2026** é o fim do prazo de 24 meses do art. 266. Mesmo marco, redação correta importa em proposta. |
| "PROFISCO III, dinheiro carimbado" | **É empréstimo do BID, não repasse a fundo perdido.** US$ 278 mi federal + CCLIP US$ 2 bi para estados; **municípios só na 2ª fase**. Exige autorização legislativa. Não é "dinheiro disponível". |
| "fica inadimplente com a LC 214" | A consequência real é **melhor**: imóvel sem CIB → **o município não recebe o repasse do IBS daquela operação** (LC 214, art. 11, II), além de entraves a registro, alvará e ITBI. Não há multa por "não modernizar". |
| "IN RFB 2.275/2025" | Obriga **cartórios**, não municípios. (Eu havia registrado corretamente no adendo, mas a menção em resumo ficou ambígua.) |

**Correção de posicionamento, e é a mais importante das cinco:** a RFB fornece a integração ao
SINTER **de graça** (convênio gratuito). **Não se vende "acesso ao CIB".** Vende-se
**saneamento, qualificação e georreferenciamento do cadastro** — ou seja, a *capacidade de cumprir*.
Isso muda a frase de venda inteira.

## 4. Dados novos que a outra análise traz e que fortalecem a tese

- **1.904 municípios aderidos ao SINTER em 14/09/2026, de 5.570** → **~66% ainda fora**, a um ano e
  três meses do prazo. É a quantificação da janela que eu não tinha.
- **29,1 milhões de CIBs ativos.**
- **Manual Operacional do CADURB (ENAT, v1.12) é público** — contradiz minha afirmação de que a
  especificação só sai após adesão. *A verificar: minha tentativa de download do "Roteiro Técnico"
  retornou conteúdo restrito; pode haver dois documentos distintos (roteiro restrito × manual
  público).*
- **ITBI aberto em muito mais capitais do que eu havia mapeado:** além de Fortaleza e São Paulo —
  **Recife, Belo Horizonte** (ITBI mensal desde 2008 + CTM com geometria), **Porto Alegre** (IPTU com
  valor venal por imóvel), Rio e Niterói (agregado). **São Paulo tem CTM com 1.687.909 lotes via WFS.**
- **Nenhum município médio do PI/CE/MA publica ITBI** (testados: Teresina, Parnaíba, Timon, Sobral,
  Juazeiro — todos negativos). Confirma: as capitais servem de **treino e referência metodológica**;
  no beachhead o valor venal depende de SEMF ou coleta.
- **Foxinline atende dois tribunais** (TJ-PI e **TJ-MT**) e tem presença também em **TO**.
- **Geopixel:** casos declarados de Amparo (+R$ 10 mi/ano) e Guaratinguetá (arrecadação quase
  dobrou); concentração em municípios médios de SP/MG. Referência de preço do segmento: contrato
  tipo **R$ 270 mil** (cadastro, 2019).

## 5. Onde eu mantenho minha posição

**A tese do art. 256 (valor de referência) não some — ela muda de papel.** A outra análise trata a
correção como se o art. 256 fosse irrelevante. Não é: ele é o que sustenta o **Segmento A** (PGV,
recuperação fiscal, recorrência anual). O que a correção estabelece é que **a razão de compra do
Segmento B é o art. 266** (inscrição no CIB, prazo 31/12/2026), não o 256. São dois produtos com
duas bases legais distintas — e confundi-las foi meu erro, mas descartar o 256 seria o erro oposto.

**O dimensionamento econômico permanece, e a outra análise ainda não o tem:** mediana de IPTU no PI
de R$ 2.214/ano, 194 de 224 municípios abaixo de R$ 100 mil, RCL mediana de R$ 45,7 mi. É o que
determina que no beachhead o modelo é preço fixo, não fee de eficiência — e a análise paralela
continua sem preço, ticket ou LTV.
