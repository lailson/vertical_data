#!/usr/bin/env python3
"""Agrega o mural de licitações do TCE-PI por município.

**O que se pode afirmar com isto, e o que não.**

Afirma: quem tem **certame marcado agora**, em que modalidade e por quanto. Município
com processo de compra em andamento tem máquina de contratação funcionando — é o
sinal mais próximo de "há dotação" que dado aberto oferece, e complementa a porta 3
do roteiro de qualificação.

**Não afirma nada sobre o passado.** O endpoint é calendário do que vem, não arquivo
do que foi. Se nenhum certame cita cadastro imobiliário, isso significa *"ninguém tem
certame de cadastro marcado nesta janela"* — **não** significa "ninguém vende cadastro
no Piauí". Essa pergunta continua no e-SIC (`entregaveis/esic-4-TCE-pi.md`, item 1).

Entrada: dados/bruto/tce/licitacoes/*.json
Saída:   painel/dados/tce_licitacoes.json
"""
import glob, json, os, re, statistics
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
D = os.path.join(RAIZ, 'dados', 'bruto', 'tce', 'licitacoes')
arqs = sorted(glob.glob(os.path.join(D, '*.json')))
if not arqs:
    raise SystemExit(f'nada em {D} — rode `python3 dados/baixar_tce_licitacoes.py`')

LIMITE_DISPENSA_2026 = 65492.11
# termos que denunciariam concorrência direta no objeto
TERMOS = ('cadastro imobili', 'cadastro t', 'geoprocessa', 'planta gen', 'recadastr',
          'georreferenc', 'sinter', 'multifinalit')

saida = {
    'fonte': 'TCE-PI · mural de licitações (Portal da Cidadania)',
    'url': 'https://sistemas.tce.pi.gov.br/api/portaldacidadania/docs/',
    'baixado_em': date.today().isoformat(),
    'nota_escopo': ('calendário de certames MARCADOS, não arquivo de contratos firmados. '
                    'Ausência de objeto sobre cadastro significa "nada marcado nesta janela", '
                    'nunca "ninguém vende"'),
    'limite_dispensa_2026': LIMITE_DISPENSA_2026,
    'municipios': {},
}
todos, negativos = [], 0
for f in arqs:
    d = json.load(open(f, encoding='utf-8'))
    p = d['prefeitura']
    cs = d.get('certames') or []
    for c in cs:
        c['_cd'] = p['codIBGE']
        todos.append(c)
    disp = [c for c in cs if 'dispensa' in (c.get('modalidade') or '').lower()]
    # previsto negativo existe na origem; é sujeira, não valor — sai da estatística
    vd = [c['previsto'] for c in disp if (c.get('previsto') or 0) > 0]
    negativos += sum(1 for c in cs if (c.get('previsto') or 0) < 0)
    casa = [c for c in cs if any(t in (c.get('objeto') or '').lower() for t in TERMOS)]
    saida['municipios'][p['codIBGE']] = {
        'nome': p['nome'], 'certames': len(cs), 'datas': len(d.get('datas') or []),
        'dispensas': len(disp),
        'dispensa_mediana': round(statistics.median(vd), 2) if vd else None,
        'dispensa_max': round(max(vd), 2) if vd else None,
        'modalidades': sorted({c.get('modalidade') for c in cs if c.get('modalidade')}),
        'previsto_total': round(sum(c['previsto'] for c in cs if (c.get('previsto') or 0) > 0), 2),
        'objeto_do_ramo': [{'objeto': c.get('objeto'), 'previsto': c.get('previsto'),
                            'modalidade': c.get('modalidade'), 'mural': c.get('mural')} for c in casa],
    }

disp_all = [c for c in todos if 'dispensa' in (c.get('modalidade') or '').lower()]
vals = sorted(c['previsto'] for c in disp_all if (c.get('previsto') or 0) > 0)
saida['uf'] = {
    'certames': len(todos),
    'municipios_com_certame': sum(1 for v in saida['municipios'].values() if v['certames']),
    'dispensas': len(disp_all),
    'dispensa_mediana': round(statistics.median(vals), 2) if vals else None,
    'dispensa_dentro_do_limite': sum(1 for v in vals if v <= LIMITE_DISPENSA_2026),
    'dispensa_total_validas': len(vals),
    'previsto_negativo_descartado': negativos,
    'certames_do_ramo': sum(len(v['objeto_do_ramo']) for v in saida['municipios'].values()),
}
cam = os.path.join(AQUI, 'dados', 'tce_licitacoes.json')
with open(cam, 'w', encoding='utf-8') as fh:
    json.dump(saida, fh, ensure_ascii=False, separators=(',', ':'))
u = saida['uf']
print(f"ok: {cam} · {os.path.getsize(cam)//1024} KB")
print(f"  {u['certames']} certames · {u['municipios_com_certame']} municípios com certame")
print(f"  {u['dispensas']} avisos de dispensa · mediana R$ {u['dispensa_mediana']:,.0f}".replace(',', '.'))
print(f"  dentro do limite de 2026: {u['dispensa_dentro_do_limite']} de {u['dispensa_total_validas']}")
print(f"  certames do ramo (cadastro/geo/PGV): {u['certames_do_ramo']}")
print(f"  previsto negativo descartado: {u['previsto_negativo_descartado']}")
