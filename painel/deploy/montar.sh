#!/usr/bin/env bash
# Monta a pasta que vai ao ar. Tudo aqui é cópia do que já existe na árvore —
# a pasta é descartável e pode ser apagada sem perder nada.
set -euo pipefail

raiz="$(cd "$(dirname "$0")/../.." && pwd)"
saida="$raiz/painel/deploy/publico"

rm -rf "$saida"
mkdir -p "$saida/m0-conector"

# O painel vai como documento completo — aqui não há plataforma embrulhando nada.
cp "$raiz/painel/index.html"                 "$saida/index.html"
cp -r "$raiz/painel/dados"                   "$saida/dados"
cp -r "$raiz/painel/vendor"                  "$saida/vendor"
cp "$raiz/m0-conector/LAUDO-completude.html" "$saida/m0-conector/"

# modelo do coletor de campo — mesma porta, mesma senha
mkdir -p "$saida/coletor"
cp "$raiz/coletor/index.html" "$saida/coletor/"

# Nada de indexação, nem que a senha falhe.
printf 'User-agent: *\nDisallow: /\n' > "$saida/robots.txt"

echo "pronto: $saida"
du -sh "$saida"
find "$saida" -type f | wc -l | xargs echo "arquivos:"
