# Índice de vulnerabilidade calculado — 121 bairros de Teresina, dado real, fórmula auditável

Executado em 2026-09-15. Substitui o `iv` digitado à mão do protótipo por um índice reprodutível,
construído só com dado aberto do Censo 2022. **Nenhuma negociação, nenhum ofício, nenhum contrato.**

## Fórmula usada nesta demonstração

```
infra_deficit = [ (1−pavimentacao) + (1−iluminacao) + (1−bueiro) ] / 3
    pavimentacao = V05406 / V05400   (faces com via pavimentada / faces no setor)
    iluminacao   = V05412 / V05400
    bueiro       = V05409 / V05400

saneamento_deficit = [ (1−esgoto_ok) + (1−agua_ok) ] / 2
    esgoto_ok = (V00309 + V00310) / V00001
                (rede geral ou pluvial + fossa séptica ligada à rede)
    agua_ok   = V00111 / V00001        (rede geral de distribuição)

iv = 100 × ( 0,35·infra_deficit + 0,35·saneamento_deficit + 0,30·(1−esgoto_ok) )
```

Fontes: Censo 2022 — `Agregados_por_Bairro` (características do domicílio) e
`Agregados_por_Setores_Censitarios_Caracteristicas_urbanisticas_do_entorno_dos_domicilios`
(entorno por face de quadra). Filtro: bairros com ≥30 domicílios e ≥1 face medida
(121 dos 123 qualificaram).

## Resultado — maior vulnerabilidade

| # | Bairro | IV | Pav. | Ilum. | Bueiro | Esgoto | Água | Domic. |
|---|---|---|---|---|---|---|---|---|
| 1 | Brasilar | 63,8 | 44,8% | 92,8% | 3,6% | **6,5%** | 95,1% | 857 |
| 2 | Olarias | 63,1 | 48,6% | 62,2% | 0,0% | 19,0% | 85,4% | 617 |
| 3 | Chapadinha | 62,8 | **36,7%** | 68,7% | 0,7% | 16,1% | 98,0% | 2.026 |
| 4 | Livramento | 62,1 | 92,9% | 82,1% | 0,0% | **0,0%** | 100,0% | 102 |
| 5 | Verdecap | 59,7 | 46,9% | 91,8% | 16,3% | 29,1% | **48,0%** | 654 |
| 6 | Socopó | 59,3 | 83,6% | 96,0% | 11,9% | 9,6% | 79,1% | 759 |
| 7 | Parque São João | 59,2 | 88,9% | 98,1% | 4,6% | 2,1% | 99,7% | 988 |
| 8 | Parque Jacinta | 59,0 | 78,2% | 96,0% | 21,8% | 1,4% | 99,7% | 349 |
| 9 | Parque Juliana | 58,3 | 78,6% | 97,1% | 15,7% | 4,2% | 99,2% | 240 |
| 10 | **Angelim** | 57,4 | 68,4% | 93,0% | 13,9% | 10,7% | 97,3% | **13.860** |

## Menor vulnerabilidade

| Bairro | IV | Pav. | Ilum. | Esgoto |
|---|---|---|---|---|
| Frei Serafim | 7,3 | 98,0% | 98,0% | 98,0% |
| Jóquei | 8,1 | 99,6% | 99,6% | 99,2% |
| Fátima | 10,0 | 99,5% | 99,5% | 97,6% |
| Pirajá | 10,1 | 100,0% | 100,0% | 97,6% |

Distribuição: **IV mínimo 7,3 · mediana 39,2 · máximo 63,8**.

## Validação de plausibilidade

O resultado é **geograficamente coerente**: Frei Serafim, Jóquei e Fátima são bairros consolidados
de alta renda de Teresina e aparecem no fundo do ranking; Brasilar, Olarias, Chapadinha e Verdecap
são periferia e aparecem no topo. O índice não foi calibrado para produzir esse resultado — ele
emergiu do dado.

**Angelim** é o achado operacional: 13.860 domicílios (o maior volume da lista) com apenas 10,7% de
esgotamento adequado. Em termos de população afetada, é a maior prioridade do município — e é
exatamente o tipo de conclusão que um painel existe para produzir.

## Confirmação do problema do protótipo

O protótipo coloca **Mocambinho** como 2º pior bairro (36% de pavimentação). Com dado real,
Mocambinho tem **99,6% de pavimentação** e **não aparece no top 15** de vulnerabilidade.
**Santa Luzia** aparece só em 15º. Os quatro bairros mais vulneráveis de Teresina — Brasilar,
Olarias, Chapadinha e Livramento — **não estão no protótipo**.

## Ressalvas — esta é uma versão de demonstração, não a fórmula final

1. **Faltam três dimensões** da fórmula proposta no parecer técnico: **renda** (existe só por setor
   censitário, exige interpolação areal), **informalidade** (% em favela/comunidade urbana, exige a
   camada vetorial do IBGE) e **dependência demográfica** (0–14 e 65+, disponível por bairro).
2. **O esgoto está com peso duplicado** (entra em `saneamento_deficit` e de novo no terceiro termo).
   Foi deliberado para esta demonstração, porque esgoto é o discriminante mais forte no dado de
   Teresina — mas **não é defensável numa fórmula publicada**. A versão final precisa de pesos
   justificados, idealmente derivados de método reconhecido (p.ex. análise de componentes principais
   ou pesos normativos declarados), não escolhidos por conveniência.
3. **Bueiro (drenagem) é o indicador mais fraco em todo o município** — mediana muito baixa mesmo em
   bairros nobres (Jóquei 55,4%, Frei Serafim 55,9%). Ele pode estar dominando o `infra_deficit`
   indevidamente. Requer análise de sensibilidade antes de entrar na fórmula final.
4. **Erro ecológico:** o índice descreve o bairro, não o domicílio. Um bairro com IV 20 pode conter
   um núcleo informal severo. A camada de favelas do IBGE corrige parcialmente isso.

**Conclusão prática:** a lacuna metodológica mais grave do protótipo — um índice central sem
fórmula — é resolvível em dias, não meses, e com dado que já está baixado. O que exige cuidado não é
a obtenção do dado; é a **justificativa dos pesos**, que é o que será questionado.
