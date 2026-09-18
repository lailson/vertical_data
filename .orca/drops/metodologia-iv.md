# Metodologia dos Indicadores e do IV — v2 (set/2026)

**Estado:** bloqueante resolvida (M0 item 3). Substitui as regras de métrica
anteriores, incluindo a regra caduca "n ≥ 50 **faces**" — o universo agora é
**n ≥ 50 domicílios**. Implementada em `painel-gerencial/build_dados.py` e
refletida no painel regenerado.

## 1. Fontes (todas públicas, baixadas em `dados/bruto/`)

| Tema | Arquivo | Uso |
|---|---|---|
| Domicílios/moradores | CD1 por bairro (V00001, V00005) | denominadores, universo |
| Água e esgoto | CD2 por bairro (V00111, V00309) | saneamento |
| Entorno urbanístico | Entorno por bairro (V0500x) | pavimentação, iluminação, calçada, rampa, bueiro, ônibus, arborização |
| Demografia | Demografia por bairro (V010xx) | idosos 60+ (V01040+41), crianças 0–14 (V01031+32+33) ÷ V01006 |
| Renda | Renda do responsável (V06004 média, V06006 mediana) | perfil socioeconômico |
| Geometria | Malha de bairros CD 2022 (SHP) | mapa |

## 2. Regras de cálculo (as correções)

1. **Entorno — denominador sem "não declarado"**: % = SIM ÷ (SIM + NÃO).
   - Pavimentação: `V05006/(V05006+V05007)`; Iluminação: `V05012/(V05012+V05013)`;
     Calçada: `V05021/(V05021+V05022)`; Rampa: `V05027/(V05027+V05028)`;
     Bueiro: `V05009/(V05009+V05010)`; Ponto de ônibus: `V05015/(V05015+V05016)`.
   - **Errata v1:** usávamos `SIM/V05000`, incluindo "não declarado" no denominador
     (subestimava o indicador). Efeito pequeno em Teresina (não declarado ≈ 0),
     mas a regra correta é esta e vale para qualquer município.
   - Arborização permanece `V05030/V05000` (face **sem** árvores — não há par SIM/NÃO).
2. **Renda — mediana (V06006) é o indicador principal**; a média (V06004) fica como
   secundária. Motivo: robustez a cauda direita (ex.: Tabajaras, média R$ 16.629 ×
   mediana muito inferior; Por Enquanto: média R$ 3.065 × mediana R$ 1.502 — a
   mediana descreve melhor o morador típico do bairro).
3. **Água/esgoto**: % de domicílios ocupados ligados à rede (V00111/V00001; V00309/V00001).
4. **Universo**: bairros com **n ≥ 50 domicílios ocupados** (propriedade `n_ok` no
   geojson; 121 dos 123 de Teresina passam). Bairros abaixo ficam marcados e podem
   ser excluídos da análise — regra que substitui a caduca "n ≥ 50 faces".

## 3. Índice de Vulnerabilidade (IV)

Não há índice sintético com pesos arbitrários. O painel usa **agrupamento k-means
(k=3, 40 iterações, sementes fixas)** sobre 4 dimensões normalizadas por min–max:
`[renda_mediana (invertida), esgoto, pavimentação, iluminação]`. Os grupos são
ordenados por carência média ponderada por domicílios e rotulados
prioridade alta/média/baixa. Vantagens: sem peso inventado; reproduzível;
rastreável (cada bairro aponta o grupo e os valores que o colocaram lá).
Limitação documentada: k-means assume clusters convexos; com k=3 fixo perde
nuance. Quando houver série temporal, reavaliar contra cortes fixos.

## 4. Médias municipais

Sempre **ponderadas por domicílios ocupados** (não média simples de bairros).

## 5. Arquivos correspondentes

- `painel-gerencial/build_dados.py` — ETL idempotente que aplica estas regras
  (entrada: `dados/bruto/ibge/*.zip`; saída: `teresina_full.geojson`).
- `painel-gerencial/index.html` — painel com mediana como principal e
  denominadores corrigidos (v2).
- `dashboard-demo/index.html` — demonstração v1 (métricas antigas); mantida
  apenas como artefato de apresentação; **usar o painel-gerencial como referência**.
