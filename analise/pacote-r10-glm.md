# Rodada 10 — REVISÃO ANTES DE CONSTRUIR A FUNDAÇÃO. Responda AGORA, direto.

## Onde estamos

Produto: conformidade com o art. 266 da LC 214/2025 — todo imóvel urbano no CIB até
31/12/2026. Faltam ~104 dias; a janela prática de assinatura é nov–dez. Mercado: 224
municípios do Piauí, 194 deles arrecadam menos de R$ 100 mil de IPTU/ano.

Existe um painel com dado público real, publicado com senha. Nos últimos dias entraram
quatro fontes de energia da ANEEL (todas ODbL, uso comercial permitido):

- **geração distribuída**: 90.528 conexões no PI, 872,7 MW, 224/224 municípios
- **tarifas homologadas**: R$ 946,69/MWh no consumo comum, R$ 683,83 no regime de quem
  já gera (Equatorial PI responde por 99,65% do estado)
- **BDGD**: 4.230 unidades consumidoras PJ de média/alta tensão, com CEP completo, bairro
  e coordenada. **945 já geram, 3.285 não** — é uma lista de visita com endereço
- **SIGEL**: camada de pontos de GD, ~1,1 km de precisão, 79% de cobertura

Achado comercial: o Piauí caiu de 22.177 para 15.721 conexões em 2025 (−29%) enquanto o
Brasil ficou estável. É **perda de participação** — de 2,44% para 1,73% das conexões
nacionais.

## A decisão a revisar

O próximo passo planejado é **1,5 dia construindo fundação**: repositório em DuckDB +
Parquet, com proveniência por coluna (fonte, url, vigência, licença, sha256) e linhagem.
Hoje são cinco scripts que leem arquivo bruto e escrevem JSON, cada um por conta própria.

## Responda no máximo 5 achados, só o que muda a decisão

1. **Vale parar 1,5 dia para construir fundação agora?** Com 104 dias de prazo e cinco
   fontes funcionando, isso é disciplina ou é procrastinação elegante? O que aconteceria
   se eu simplesmente continuasse com scripts separados até a fonte número dez?
2. **Energia é negócio ou é distração?** O contrato que se vende é conformidade cadastral
   com prazo legal. Geração distribuída é outro comprador (secretaria de meio ambiente?
   empresa de energia?) e outro ciclo. Estou diluindo o foco na pior hora, ou construindo
   a receita recorrente que o produto de prazo não tem?
3. **A lista do BDGD — 3.285 unidades PJ com carga e sem geração, com endereço — vale
   mais que o painel inteiro?** Se vale, para quem se vende: para a prefeitura, para um
   integrador solar, ou para a própria distribuidora? Muda o modelo de negócio?
4. **Perda de participação do Piauí (2,44% → 1,73%)**: isso é argumento de venda para
   prefeitura, ou é argumento contra entrar nesse mercado?
5. Qualquer risco comercial que eu não esteja vendo.
