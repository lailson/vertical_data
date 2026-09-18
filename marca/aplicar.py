#!/usr/bin/env python3
"""Injeta os tokens de marca nas páginas, a partir de marca/vertical-data.css.

As páginas são aplicações de arquivo único de propósito — abrem por file:// numa
prefeitura sem wifi —, então não podem depender de um <link> para um CSS irmão.
A cópia embutida entre VD:INICIO e VD:FIM resolve isso sem criar uma segunda
fonte de verdade: este script reescreve o bloco, e o diff mostra o que mudou.

Uso:  python3 marca/aplicar.py [--conferir]
      --conferir sai com código 1 se alguma página estiver fora de sincronia,
      sem escrever nada. É o que se roda antes de publicar.
"""
import io, os, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTE = os.path.join(RAIZ, 'marca', 'vertical-data.css')
ALVOS = [os.path.join(RAIZ, 'painel', 'index.html'),
         os.path.join(RAIZ, 'coletor', 'index.html')]
INI, FIM = '/* VD:INICIO */', '/* VD:FIM */'

css = io.open(FONTE, encoding='utf-8').read().strip()
bloco = f'{INI}\n{css}\n{FIM}'
conferir = '--conferir' in sys.argv
fora = []

for alvo in ALVOS:
    s = io.open(alvo, encoding='utf-8').read()
    a, b = s.find(INI), s.find(FIM)
    if a < 0 or b < 0:
        raise SystemExit(f'{alvo}: marcadores {INI} / {FIM} ausentes — '
                         'a página ainda não foi migrada para os tokens de marca')
    novo = s[:a] + bloco + s[b + len(FIM):]
    if novo == s:
        print(f'  ok        {os.path.relpath(alvo, RAIZ)}')
        continue
    fora.append(os.path.relpath(alvo, RAIZ))
    if conferir:
        print(f'  DIVERGE   {os.path.relpath(alvo, RAIZ)}')
    else:
        io.open(alvo, 'w', encoding='utf-8').write(novo)
        print(f'  atualizado {os.path.relpath(alvo, RAIZ)}')

if conferir and fora:
    raise SystemExit(f'\n{len(fora)} página(s) fora de sincronia com marca/vertical-data.css — '
                     'rode `python3 marca/aplicar.py`')
