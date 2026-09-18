# Índice de Vulnerabilidade Territorial (IVT) — metodologia publicável

Substitui o k-means como **indicador oficial**. O agrupamento permanece, mas como camada
exploratória, nunca como o número que ordena prioridade de investimento público.

## 1. Por que pesos declarados e não agrupamento

O k-means é reproduzível, mas **não é explicável** — e num produto que ordena investimento público a
segunda propriedade vale mais que a primeira.

| | Com pesos declarados | Com k-means |
|---|---|---|
| Pergunta do vereador *"por que meu bairro está em último?"* | *"esgoto 42%, peso 0,25; pavimentação 61%, peso 0,20 — eis a conta"* | *"o algoritmo agrupou no grupo 2"* |
| Município novo entra na base | **nada muda** nos bairros existentes | min–max muda, **grupos podem remapear todos** |
| Auditoria do TCE | fórmula publicada, recalculável em planilha | exige reproduzir o algoritmo |
| Arbitrariedade | **explícita e discutível** | implícita em k, semente e normalização |

O ponto decisivo: **k-means não elimina arbitrariedade — esconde.** Escolher k=3, escolher 4 variáveis
e descartar as outras, e normalizar por min–max da amostra são decisões de ponderação. Elas apenas
não podem ser declaradas nem defendidas.

## 2. A fórmula

```
IVT = 100 × ( 0,30·D_infra + 0,25·D_saneamento + 0,25·D_renda + 0,20·D_dependência )
```

Todos os componentes no intervalo [0, 1], onde **1 = pior situação**.

### D_infra — déficit de infraestrutura urbana (peso 0,30)
```
D_infra = média[ (1 − pavimentação), (1 − iluminação), (1 − drenagem) ]

pavimentação = V05006 / (V05006 + V05007)
iluminação   = V05012 / (V05012 + V05013)
drenagem     = V05009 / (V05009 + V05010)
```
Fonte: Censo 2022, *Agregados por bairro — entorno dos domicílios*.
**Denominador exclui "não declarado"** (V05008 / V05014 / V05011).
**Unidade: domicílios**, não faces de quadra — o indicador responde "quantas pessoas moram em rua sem
pavimento", e não "quantos segmentos de quadra existem".

### D_saneamento — déficit de saneamento (peso 0,25)
```
D_saneamento = média[ (1 − esgoto_adequado), (1 − água_adequada) ]

esgoto_adequado = (V00309 + V00310) / V00001      ← rede geral/pluvial + fossa ligada à rede
água_adequada   =  V00111 / V00001                 ← rede geral de distribuição
```
Fonte: Censo 2022, *Agregados por bairro — características do domicílio 2*.

### D_renda — déficit de renda (peso 0,25)
```
D_renda = clamp( 1 − log1p(V06006_bairro) / log1p(V06006_municipal) , 0, 1 )
```
Fonte: *Rendimento do responsável*, **V06006 = mediana**.
**Mediana, nunca média (V06004)** — a razão média/mediana chega a 1,59 (Brasilar) e 2,04
("Por Enquanto"), e a média inverte posições no ranking.
A transformação logarítmica comprime a cauda superior: a diferença entre R$ 1.200 e R$ 2.400 pesa
mais que entre R$ 12.000 e R$ 13.200, que é o comportamento desejado.

### D_dependência — dependência demográfica (peso 0,20)
```
D_dependência = (pop 0–14 + pop 65+) / pop total
```
Fonte: Censo 2022, *Demografia por bairro*.

## 3. Justificativa dos pesos — declarada, não escondida

| Componente | Peso | Justificativa |
|---|---|---|
| Infraestrutura | **0,30** | é o que a política pública municipal **executa diretamente** — pavimentar, iluminar, drenar são obras de competência municipal, e o painel existe para priorizar essas obras |
| Saneamento | **0,25** | maior impacto em saúde pública, mas frequentemente de competência da concessionária — o município prioriza, não executa |
| Renda | **0,25** | melhor preditor isolado de vulnerabilidade, porém **indireto**: o município não atua sobre renda no curto prazo |
| Dependência demográfica | **0,20** | crianças e idosos ampliam o impacto de qualquer déficit sobre a mesma população |

**Os pesos são uma escolha normativa, e isto está declarado.** Qualquer usuário pode recalcular com
outros pesos — a planilha de cálculo acompanha o laudo e a soma é 1,00 por construção.

**Regra de governança:** os pesos só mudam por decisão registrada e versionada, com a data e o motivo.
Mudança silenciosa de peso entre edições do painel é o que transformaria o índice em instrumento
manipulável.

## 4. Regras de qualidade (bloqueantes)

1. **n ≥ 50 domicílios** (V00001) para o bairro entrar no ranking. Abaixo disso: exibido com selo
   **"amostra insuficiente"**, sem número e **fora da ordenação**.
2. **Cobertura do entorno**: calcular `V05000 / V00001`. Se **< 90%**, o indicador de entorno
   representa amostra e não o bairro — **excluir do ranking**, não apenas sinalizar.
   *(Teresina: cobertura de 99,9%, nenhum bairro abaixo de 90%. Verificar em cada novo município.)*
3. **Intervalo de confiança**: bairros entre 50 e 150 domicílios exibem IC 95% binomial nos
   componentes de proporção.
4. **Componente ausente**: se qualquer um dos quatro não puder ser calculado, o IVT **não é
   publicado** para aquele bairro. Não há imputação.

## 5. Limitações — publicadas junto, não em nota de rodapé

- **Erro ecológico.** O IVT descreve o bairro, não o domicílio. Um bairro com IVT 20 pode conter um
  núcleo informal severo. **Mitigação:** exibir a camada de favelas e comunidades urbanas do IBGE
  (geometria vetorial) sobreposta ao mapa.
- **Snapshot de 2022.** O Censo é fotografia; obras executadas depois não aparecem. Declarar a data
  de referência em toda tela.
- **Não se aplica aos 199 municípios do PI sem divisão de bairros.** Para eles, o mesmo cálculo roda
  em **setor censitário**, com a ressalva de que setor não tem nome reconhecível pelo gestor.
- **Os pesos são normativos.** Não há "peso correto" derivável do dado — há peso declarado e
  discutível.

## 6. O que fazer com o k-means

**Manter, como camada exploratória**, com rótulo explícito: *"agrupamento estatístico — análise
exploratória, não classificação oficial"*. Ele é bom para revelar padrões que os pesos não capturam
(por exemplo, bairros com renda alta e infraestrutura ruim, que o índice aditivo dilui).

**Nunca usar para ordenar prioridade**, nunca aparecer em relatório que vá a terceiro, e nunca ser
descrito como "sem pesos arbitrários" — porque não é verdade.

## 7. Correção pendente no documento existente
O `metodologia-iv.md` justifica a mediana citando *"Tabajaras, média R$ 16.629 × mediana muito
inferior"*. **Tabajaras tem mediana R$ 15.000 — razão 1,11, a menor divergência entre os bairros de
renda alta.** Trocar por **Brasilar** (R$ 1.926 × R$ 1.212 = 1,59) ou **Mocambinho**
(R$ 2.688 × R$ 1.703 = 1,58).
