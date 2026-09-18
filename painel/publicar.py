#!/usr/bin/env python3
"""Gera a versão do painel para publicação como página compartilhável.

A plataforma embrulha o arquivo num esqueleto próprio (<!doctype>, <html>,
<head>, <body>), então o que se envia é só o conteúdo: título, estilo, corpo e
script. O index.html local continua sendo um documento completo — que é o que
`python3 -m http.server` precisa servir.

Uso: python3 painel/publicar.py [saida.html]
"""
import io, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(AQUI, 'index.html')
SAIDA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, 'publicar.html')

s = io.open(ORIG, encoding='utf-8').read()
cabeca = re.search(r'<head>(.*?)</head>', s, re.S).group(1)
corpo = re.search(r'<body>(.*?)</body>', s, re.S).group(1)
# remove só o que a plataforma injeta por conta própria — qualquer outra meta
# que venha a existir no arquivo local continua indo junto
cabeca = re.sub(r'<meta[^>]*(charset|name="viewport")[^>]*>\s*', '', cabeca)

io.open(SAIDA, 'w', encoding='utf-8').write(cabeca.strip() + '\n' + corpo.strip() + '\n')
print(SAIDA, os.path.getsize(SAIDA) // 1024, 'KB')
