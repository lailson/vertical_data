# Painel CERURB · Piauí

Painel único, duas escalas. Funde a interatividade do `painel-v2.html` da sessão
ZCode com a qualificação comercial dos 224 municípios desta árvore
(`dados/qualificacao-pi.csv`) e com o escopo de onze telas do painel-produto.

## Rodar

```
cd ~/projetos/projeto-cerurb
python3 -m http.server 8000
# abrir http://localhost:8000/painel/
```

Precisa de HTTP porque os dados vêm por `fetch` (abrir o arquivo direto com
`file://` é bloqueado pelo navegador). **Não precisa de internet**: o Leaflet
está vendorizado em `vendor/`. As fontes vêm do Google Fonts e, sem rede, caem
para as do sistema sem quebrar a página.

Link direto para um município: `?m=<código IBGE>#territorio` —
ex.: `http://localhost:8000/painel/?m=2200400#territorio` (Altos).

## Regenerar os dados

```
python3 dados/baixar.py                      # idempotente; pula o que já existe
python3 -m venv .venv && .venv/bin/pip install pyshp
.venv/bin/python painel/build_dados.py       # --uf 22 é o padrão
```

Saída em `painel/dados/`:

| Arquivo | Conteúdo |
|---|---|
| `municipios.json` | 224 municípios: população do Censo (V0001), indicadores do Censo no agregado municipal, IPTU/ITBI/ISS/RCL, tenant, entregas de RREO por ano, CIB ativo, papel comercial |
| `bairros/<ibge>.json` | um por município com bairros (25 no PI) — 479 bairros e os polígonos de FCU |
| `cnefe.json` | endereços do Censo 2022 por município e por bairro — o volume da remessa ao CADURB |
| `meta.json` | contagens, índice de municípios e a tabela de fontes com data de consulta |

Para o CNEFE: `.venv/bin/python painel/build_cnefe.py` (precisa de `numpy`, e do
`dados/bruto/cnefe/22_PI.zip` baixado uma vez do FTP do IBGE).

`pyshp` é a única dependência do ETL principal. O resto é Python padrão — inclusive a
simplificação de geometria (Douglas-Peucker) que faz o mapa do estado caber em
348 KB.

## As onze telas

**Estado** — Mapa de alvos · Carteira e qualificação · Janela de 31/12
**Município** — Território · Ranking de bairros · Saneamento · Pavimentação e
viário · Perfis socioeconômicos
**Referência** — Relatórios exportáveis · Metodologia e fontes · Fora da v1

Os 199 municípios sem bairro no Censo não são buracos: entram em **modo
sem-bairro**, com os mesmos indicadores no agregado municipal e os controles de
bairro escondidos em vez de inertes.

## Regras que o painel respeita

- método de cálculo: `docs/metodologia-iv.md` (a §6 traz os adendos da fusão);
- **nenhuma tela com dado fictício** — o que não tem fonte está em *Fora da v1*,
  com o motivo;
- todo CSV exportado sai com fonte, data de consulta e regra de cálculo no
  cabeçalho;
- ausência de dado é cinza e travessão, nunca zero: 72 municípios não entregaram
  RREO 2025 e isso não é "arrecadação zero";
- população é a do Censo 2022 (`V0001`), não a estimativa anual do CSV de
  qualificação — que fica no painel e no CSV como linha de rastreio;
- os dois temas saem dos mesmos tokens de CSS, inclusive as rampas do mapa: não
  existe paleta de JavaScript separada da de CSS.

## Outros arquivos aqui

- `conversa.html` — narrativa de cinco telas da sessão ZCode, para conversa de
  mesa. Íntegra, só Teresina, dados embutidos.
