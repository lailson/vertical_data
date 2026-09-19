#!/usr/bin/env python3
"""Coleta o mural de licitações do TCE-PI, por município.

**O que esta fonte é — e o que ela não é.** É um **calendário do que vem**, não um
arquivo do que passou: `/licitacoes/:id` devolve as datas com certame marcado, e
`/licitacoes/:id/:esfera/:data` devolve os certames daquele dia, com `objeto` em
texto completo, `modalidade`, valor previsto e link para o mural.

Logo ela **não** responde o item 1 do `esic-4-TCE-pi.md` — quem já vendeu cadastro
imobiliário no estado e por quanto. Esse pedido continua de pé.

**Mas responde algo mais útil para uma janela de 60 dias:** quem está contratando
**agora**. Município com certame marcado tem processo de compra vivo — e
`modalidade = "Aviso de Dispensa"` mostra como cada um conduz dispensa e em que
faixa de valor, que é exatamente o que a porta 3 do roteiro tenta descobrir.

Entrada: API do Portal da Cidadania (sem chave)
Saída:   dados/bruto/tce/licitacoes/<idUnidadeGestora>.json
Uso:     python3 dados/baixar_tce_licitacoes.py [--refazer]
"""
import json, os, sys, time, urllib.error, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://sistemas.tce.pi.gov.br/api/portaldacidadania'
DEST = os.path.join(AQUI, 'bruto', 'tce', 'licitacoes')
os.makedirs(DEST, exist_ok=True)
REFAZER = '--refazer' in sys.argv


def get(path, tentativas=3):
    for i in range(tentativas):
        try:
            req = urllib.request.Request(BASE + path, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            if i == tentativas - 1:
                return None
            time.sleep(2 ** i)
    return None


prefs = get('/prefeituras')
if not prefs:
    raise SystemExit('não consegui listar /prefeituras')
print(f'{len(prefs)} prefeituras')

novos = pulados = com_certame = 0
total_certames = 0
for i, p in enumerate(prefs, 1):
    cam = os.path.join(DEST, f"{p['id']}.json")
    if os.path.exists(cam) and not REFAZER:
        pulados += 1
        continue
    datas = get(f"/licitacoes/{p['id']}") or []
    time.sleep(0.3)
    certames = []
    for d in datas:
        # esfera 1 = Municipal. qtdePorPagina é aceito aqui, ao contrário de /receitas
        lote = get(f"/licitacoes/{p['id']}/1/{d['link']}?qtdePorPagina=200") or []
        certames += lote
        time.sleep(0.3)
    if datas:
        com_certame += 1
        total_certames += len(certames)
    with open(cam, 'w', encoding='utf-8') as fh:
        json.dump({'prefeitura': p, 'datas': datas, 'certames': certames}, fh, ensure_ascii=False)
    novos += 1
    if i % 25 == 0 or i == len(prefs):
        print(f"  [{i:>3}/{len(prefs)}] {p['nome'][:24]:26} · com certame {com_certame} · certames {total_certames}")

print(f'\nok: {DEST} · {novos} novos · {pulados} já existentes')
print(f'  {com_certame} municípios com certame marcado · {total_certames} certames')
