# Revisão do M0 e dos documentos produzidos na outra sessão (16/09/2026)

Revisão feita com verificação independente contra fonte primária. Ressalva: **o código do M0
(`cadurb_client.py`, `validador_completude.py`, `spec/openapi-homologacao.json`, `exemplo_base.csv`)
não está nesta máquina** — a revisão do M0 é sobre o que foi descrito e sobre as afirmações técnicas
verificáveis, não sobre o código em si.

## 1. VERIFICADO E CORRETO — obrigatoriedade do CADURB

Alegado: `DadosGeraisImovel{areaTerreno, inscricaoImobiliaria, temBairro, tipoImovel}` e
`EnderecoImovel{cep, nomeLogradouro, tipoLogradouro}`.

Conferido contra `api/v3/api-docs` ao vivo:
```
DadosGeraisImovelDTO  required=['areaTerreno','inscricaoImobiliaria','temBairro','tipoImovel']
EnderecoImovelDTO     required=['cep','nomeLogradouro','tipoLogradouro']
```
**Exato, campo a campo.** E o método declarado — extrair as regras da própria spec em vez de copiar à
mão — é a decisão de engenharia certa: quando a spec evoluir, as regras acompanham.

## 2. VERIFICADO E CORRETO — os 15 códigos de variáveis do entorno

Conferidos um a um contra `dicionario_entorno_domicilios.xlsx`:

| Código | Metodologia alega | Dicionário IBGE |
|---|---|---|
| V05006 / V05007 / V05008 | pav SIM / NÃO / ND | "DOMICÍLIOS EM FACE COM VIA PAVIMENTADA - SIM/NÃO/NÃO DECLARADO" ✅ |
| V05009 / V05010 | bueiro SIM / NÃO | "…COM BUEIRO - SIM/NÃO" ✅ |
| V05012 / V05013 | ilum SIM / NÃO | "…COM ILUMINAÇÃO PÚBLICA - SIM/NÃO" ✅ |
| V05015 / V05016 | ônibus SIM / NÃO | "…COM PONTO DE ÔNIBUS - SIM/NÃO" ✅ |
| V05021 / V05022 | calçada SIM / NÃO | "…COM CALÇADA - SIM/NÃO" ✅ |
| V05027 / V05028 | rampa SIM / NÃO | "…COM RAMPA PARA CADEIRANTE - SIM/NÃO" ✅ |
| V05030 | arborização sem árvores | "…COM ARBORIZAÇÃO - SEM ÁRVORES" ✅ |

**15 de 15 corretos.** A correção do denominador para `SIM/(SIM+NÃO)` também está certa e é mais
rigorosa do que a que eu havia proposto.

## 3. ACHADO NOVO — o que V05000 realmente é, e a ressalva que ninguém registrou

`V05000` não é "total de domicílios do bairro". A descrição completa é:

> **"[Domicílios particulares permanentes ocupados][DOMICÍLIO EM SETOR ESCOLHIDO PARA APLICAÇÃO DO
> ENTORNO]"**

Ou seja: **o levantamento de entorno foi aplicado a setores selecionados**, não a todos. O universo
do indicador de entorno é diferente do universo do Censo.

**Medido em Teresina:** cobertura de **99,9%** (254.855 de 255.192 domicílios); **nenhum** dos 123
bairros abaixo de 90%. Em Teresina, portanto, a limitação é teórica.

**Mas é ressalva obrigatória por município.** Ao rodar o pipeline em Altos, Guaribas ou qualquer
outro, a primeira verificação tem de ser `V05000 / V00001`. Se a cobertura cair, o indicador de
pavimentação/iluminação deixa de representar o bairro e passa a representar uma amostra — e isso
precisa aparecer no painel, não numa nota de rodapé.

**Sugestão concreta:** adicionar `cobertura_entorno` como propriedade do GeoJSON, ao lado de `n_ok`.

## 4. ERRO FACTUAL no `metodologia-iv.md`

O documento justifica o uso da mediana citando:
> *"ex.: Tabajaras, média R$ 16.629 × mediana muito inferior"*

**Medido:** Tabajaras tem média **R$ 16.629** e mediana **R$ 15.000** — razão de **1,11**. Não é
"muito inferior"; é a menor divergência entre os bairros de renda alta.

Os exemplos que sustentam o argumento são outros: **Brasilar** (média R$ 1.926 × mediana R$ 1.212 =
**1,59**) e **Mocambinho** (R$ 2.688 × R$ 1.703 = **1,58**). O caso "Por Enquanto" citado em seguida
(R$ 3.065 × R$ 1.502 = 2,04) está correto.

**Trocar o exemplo.** A decisão de usar mediana está certa; a evidência apresentada para ela, não.

## 5. DISCUTÍVEL — k-means no lugar do índice com pesos

O documento abandona o índice sintético e adota **k-means (k=3)** sobre 4 dimensões normalizadas
min–max, argumentando "sem peso inventado".

**O argumento é parcialmente falso.** O k-means não elimina a arbitrariedade — ele a **desloca e a
esconde**:
- escolha de **k=3** (arbitrária);
- escolha das **4 variáveis** e exclusão de todas as outras (é uma ponderação binária: peso 1 ou 0);
- **normalização min–max**, que é sensível a outliers e faz cada variável pesar conforme sua
  amplitude observada — ou seja, **os pesos existem, são implícitos e não são declaráveis**;
- ordenação dos grupos por carência média ponderada (outra escolha).

**E o problema maior é de defensabilidade.** O parecer técnico de rodadas anteriores recomendou
método com **coeficientes declarados** precisamente pela explicabilidade perante controle externo.
Diante de um vereador ou do TCE:
- com pesos: *"seu bairro tem 42% de esgoto, o peso de saneamento é 0,25, eis a conta"*;
- com k-means: *"o algoritmo agrupou seu bairro no grupo 2"* — que é **indefensável** em audiência
  pública, mesmo sendo reproduzível.

Há ainda **instabilidade estrutural**: em k-means, incluir um município novo ou atualizar o Censo
pode **remapear os grupos de todos os bairros**, sem que nenhum bairro tenha mudado. Um bairro que
era "prioridade média" vira "alta" porque outro bairro entrou na base. Explicar isso a um prefeito
que investiu conforme o painel do ano anterior é um problema sério.

**Recomendação:** manter o k-means como **camada exploratória** (é bom para isso — revela padrões
sem impor estrutura) e **publicar junto um índice aditivo com pesos declarados** como indicador
oficial. O painel mostra os dois; o índice com pesos é o que vai para relatório, e o agrupamento é o
que ajuda a interpretar. Não é redundância: são funções diferentes.

## 6. Os textos de e-SIC — muito bons, com um ponto a verificar

Os três prioritários (RFB, SEFAZ-PI, SEAD/PROUrbe) estão bem redigidos: citam base legal, pedem
formato aberto, pedem dado agregado (o que reduz objeção de LGPD) e o da SEFAZ faz a pergunta certa —
converter "perda de repasse" em **R$/município/ano**, que é a linha mais forte possível do deck.

**A verificar:** o texto afirma que existe um arquivo público mensal `inscricoes_ativas_*.csv` na
página de estatísticas do Sinter. **Não consegui confirmar** — `/sinter/dados-abertos` redireciona
para o portal geral de dados abertos da RFB, e não localizei o arquivo por busca nem por inspeção do
HTML. Se ele existir, **parte do e-SIC nº 1 é dispensável e o dado sai hoje em vez de em 15–30 dias**
— vale 10 minutos de verificação antes de enviar o pedido.

## 7. O M0 — avaliação do que foi descrito

**Acertos de desenho:**
- **O validador offline é a decisão certa.** Gera o laudo sem credencial, que era o caminho crítico.
  Confirma independentemente a conclusão desta análise: o produto de entrada pode ser construído e
  vendido antes de qualquer token.
- Cliente em **dry-run** contra a URL real é boa prática — testa a montagem da requisição sem
  depender de credencial.
- Extrair regras da spec em vez de transcrever é o que torna o validador sustentável.
- Registrar que `docs.receitafederal.gov.br/sinter` está 404 e que a spec viva é `/api/v3/api-docs`
  é o tipo de achado que economiza horas de quem vier depois.

**O que eu verificaria antes de considerar o M0 fechado:**
1. **A spec é de homologação e está versionada como `0.0.1-SNAPSHOT`.** Um artefato SNAPSHOT muda sem
   aviso. O cliente precisa de um teste que falhe explicitamente quando a spec divergir da capturada
   — senão a mudança aparece como erro de negócio em produção.
2. **Os dois fluxos de geometria.** `DadosGeoDTO` tem só `idLotePonto` e `idLotePoligono`: a geometria
   não vai inline, vai por lote, com vinculação posterior. Se o cliente só cobre o fluxo alfanumérico,
   cobre metade do produto — e a metade que falta é a que a REURB entrega de graça.
3. **Validação semântica × sintática.** O laudo de completude vale pelo que checa além do schema:
   CEP existente, logradouro que casa com o município, área compatível com tipologia, inscrição sem
   duplicidade. É aí que está o valor do diagnóstico, não no `required`.
4. O `exemplo_base.csv` com 5 imóveis prova o fluxo, não o produto. **O teste real é rodar contra um
   cadastro municipal de verdade** — e é o que o piloto destrava.
