#!/usr/bin/env bash
# Cria (se preciso) e publica o projeto no Cloudflare Pages.
#
# Autentica por API token, não por OAuth: o `wrangler login` abre um servidor
# em localhost esperando o callback do navegador, e neste ambiente o navegador
# não alcança esse localhost — o login expira sempre.
#
# Espera um arquivo com o token, fora do repositório:
#   ~/.vertical-data.env   (chmod 600)
#     CLOUDFLARE_API_TOKEN=...
#     CLOUDFLARE_ACCOUNT_ID=...
#
# O nome antigo (~/.cerurb-cf.env) continua valendo: o projeto mudou de nome,
# a credencial é a mesma, e obrigar a renomear um arquivo de segredo só para
# alinhar nomenclatura é trocar risco por estética.
set -euo pipefail

projeto="${1:-vertical-data}"
aqui="$(cd "$(dirname "$0")" && pwd)"
env_file="${VERTICAL_DATA_ENV:-}"
if [[ -z $env_file ]]; then
	for c in "$HOME/.vertical-data.env" "$HOME/.cerurb-cf.env"; do
		[[ -f $c ]] && { env_file="$c"; break; }
	done
	env_file="${env_file:-$HOME/.vertical-data.env}"
fi

[[ -f $env_file ]] || { echo "faltando $env_file — veja painel/deploy/LEIAME.md" >&2; exit 1; }
echo "· credencial $env_file"
set -a; # shellcheck disable=SC1090
source "$env_file"; set +a
[[ -n ${CLOUDFLARE_API_TOKEN:-} ]] || { echo "CLOUDFLARE_API_TOKEN vazio em $env_file" >&2; exit 1; }
# Token restrito a Pages não enxerga a lista de contas, e é dela que o wrangler
# deduziria o ID. Sem o ID, ele falha com "Failed to automatically retrieve
# account IDs" — erro que não diz o que fazer.
[[ -n ${CLOUDFLARE_ACCOUNT_ID:-} ]] || {
	echo "CLOUDFLARE_ACCOUNT_ID vazio em $env_file." >&2
	echo "Um token só de Pages não deduz o ID sozinho. Ele está na URL do painel" >&2
	echo "(dash.cloudflare.com/<ID>/...) ou em Workers & Pages → Overview." >&2
	exit 1
}

cd "$aqui"
[[ -d publico ]] || ./montar.sh

# O wrangler procura `functions/` no diretório CORRENTE, não no publicado. Rodar
# o deploy de outro lugar sobe os arquivos sem o basic auth, e sem avisar — o
# painel inteiro ficaria aberto. Daí o cd acima e esta conferência.
[[ -f functions/_middleware.js ]] || {
	echo "ERRO: functions/_middleware.js não está em $aqui — o deploy subiria SEM senha." >&2
	exit 1
}

# O token mínimo (só Pages · Edit) não tem permissão de ler o usuário: o whoami
# falha, e sob `pipefail` isso abortaria o deploy inteiro. É informativo, não
# condição — daí o `|| true`.
echo "· conta"
npx --yes wrangler@latest whoami 2>/dev/null | sed -n '1,6p' || true

echo "· projeto $projeto"
# `\b` trata hífen como fronteira, então "painel-cerurb" casaria dentro de
# "x-painel-cerurb-y"; e uma falha passageira do `list` não pode virar abortar o
# deploy — se o projeto já existir, o `create` falha e seguimos assim mesmo.
lista=$(npx --yes wrangler@latest pages project list 2>/dev/null || true)
if printf '%s\n' "$lista" | grep -qE "(^|[[:space:]|])${projeto}([[:space:]|]|\$)"; then
	echo "  já existe"
else
	npx --yes wrangler@latest pages project create "$projeto" --production-branch main \
		|| echo "  criação não concluída — se o projeto já existe, o deploy segue"
fi

echo "· publicando"
npx --yes wrangler@latest pages deploy publico --project-name "$projeto" --commit-dirty=true

# O middleware devolve 503 quando PAINEL_USUARIO/PAINEL_SENHA não existem — falha
# fechada, nunca aberta. Num projeto recém-criado elas AINDA NÃO EXISTEM, e não
# saem daqui: segredo se digita no painel da Cloudflare, não em script.
cat <<'FIM'

Se este é um projeto novo, ele está no ar SEM credencial cadastrada — e o
middleware responde 503 a tudo até que ela exista. Para liberar:

  Workers & Pages → <projeto> → Settings → Variables and Secrets
  PAINEL_USUARIO e PAINEL_SENHA (tipo Secret), ambiente Production

Variável nova só vale no PRÓXIMO deploy. Depois de salvar, rode este script
outra vez.
FIM
