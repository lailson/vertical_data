# Publicar o painel com usuário e senha

Pasta de deploy para **Cloudflare Pages**, em conta própria — este projeto não
depende de nenhuma infraestrutura de terceiros. O plano gratuito serve o site e
roda a função de autenticação; não há servidor para manter nem certificado para
renovar.

```
painel/deploy/
  functions/_middleware.js   ← basic auth: roda antes de todo arquivo
  publico/                   ← gerado por montar.sh, descartável
  montar.sh
```

## Por que Cloudflare Pages, e não Vercel

A Vercel faz isso — mas **proteção por senha é recurso do plano Pro** (US$ 20/mês
por usuário); no gratuito seria preciso escrever o basic auth num middleware, e o
plano Hobby é declaradamente **para uso não comercial**. Este painel é ferramenta
de venda, então o Hobby não serve.

A Cloudflare Pages é gratuita **para uso comercial**, entrega 100 mil requisições
por dia e o basic auth cabe numa função de 40 linhas. Uma conta nova, criada só
para este projeto, resolve — não precisa de domínio nem de cartão.

Alternativas equivalentes, se preferir: **Netlify** (gratuito comercial, basic
auth por Edge Function — mesma ideia, outro painel) ou uma VPS mínima com Caddy
(`basic_auth` nativo), que passa a custar e a exigir manutenção.

## Autenticação: token, não `wrangler login`

O `wrangler login` sobe um servidor em `localhost:8976` e espera o navegador
devolver o código. **Neste ambiente o navegador não enxerga esse localhost** — a
mesma separação de rede que impede o `http.server` local de ser aberto pelo
Chrome. O login expira sempre. Use API token, que é offline:

1. Em <https://dash.cloudflare.com/profile/api-tokens> → *Create Token* →
   *Create Custom Token*. Permissão mínima:
   **Account · Cloudflare Pages · Edit** (adicione *Account Settings · Read* se
   quiser que o `whoami` liste a conta). Em *Account Resources*, escolha a conta.
2. O ID da conta está na barra lateral de *Workers & Pages* (ou na URL do painel).
3. Salve os dois **fora do repositório**, num arquivo só seu:

```bash
# crie no editor, não pelo histórico do shell
$EDITOR ~/.cerurb-cf.env
chmod 600 ~/.cerurb-cf.env
```

```
CLOUDFLARE_API_TOKEN=...
CLOUDFLARE_ACCOUNT_ID=...
```

## Primeira publicação

```bash
cd ~/projetos/projeto-cerurb
./painel/deploy/montar.sh            # copia painel + dados + laudo
./painel/deploy/publicar-cf.sh       # cria o projeto e publica
```

Sem as variáveis de senha, o site responde **503** — ele não abre desprotegido.
Defina as duas no painel da Cloudflare, em *Workers & Pages → painel-cerurb →
Settings → Variables and secrets*, tipo **Secret**:

| Nome | Valor |
|---|---|
| `PAINEL_USUARIO` | o usuário que você escolher |
| `PAINEL_SENHA` | a senha que você escolher |

Depois de salvar, republique (`./painel/deploy/publicar-cf.sh`) para a função
enxergar os valores. Pela linha de comando o equivalente é
`npx wrangler pages secret put PAINEL_SENHA --project-name painel-cerurb`, que
pede o valor no terminal — use se preferir não abrir o navegador.

Sai uma URL `https://painel-cerurb.pages.dev`, já com HTTPS e já pedindo senha.
Domínio próprio é opcional — *Custom domains* no projeto, se um dia houver um.

Guarde usuário e senha no seu gerenciador de senhas. **Não há credencial neste
repositório**, e não deve haver.

## Atualizar depois de mexer no painel

```bash
./painel/deploy/montar.sh
cd painel/deploy && npx wrangler pages deploy publico --project-name painel-cerurb
```

Regerar os dados antes, se o ETL mudou: `.venv/bin/python painel/build_dados.py`.

## ⚠️ O comando tem de rodar de `painel/deploy`

O `wrangler` procura a pasta `functions/` no **diretório corrente**, não no
diretório publicado. Rodar `npx wrangler pages deploy painel/deploy/publico` da
raiz do repositório publica os arquivos **sem o basic auth, e sem avisar** — o
painel inteiro fica aberto, e a guarda de 503 não socorre, porque sem middleware
não há quem responda 503. Use `publicar-cf.sh`, que entra no diretório certo e
recusa rodar se a função não estiver lá.

## O que a função faz

Sem `Authorization` correto, **nada** sai — nem o HTML, nem os JSON de dados, nem
o Leaflet. Além disso:

- comparação em **tempo constante** (um `===` vaza o tamanho do prefixo certo);
- `Cache-Control: private, no-store` e `X-Robots-Tag: noindex` na resposta;
- `robots.txt` com `Disallow: /`;
- sem as duas variáveis configuradas o site responde **503**, não abre sozinho.

Basic auth é **credencial compartilhada**: quem recebe, repassa, e trocar exige
novo `secret put`. Se o painel passar a circular entre prefeituras e parceiros, o
caminho é o Cloudflare Access (gratuito até 50 pessoas): cada um entra com o
próprio e-mail, você revoga individualmente e fica registro de quem abriu. A
função aqui continua valendo como segunda porta.
