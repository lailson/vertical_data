/**
 * Basic auth para o Painel CERURB no Cloudflare Pages.
 *
 * Roda antes de qualquer arquivo — HTML, JSON de dados, Leaflet. Sem o
 * cabeçalho certo, nada sai. Usuário e senha vêm de variáveis de ambiente do
 * projeto (PAINEL_USUARIO / PAINEL_SENHA), nunca deste arquivo:
 *
 *   npx wrangler pages secret put PAINEL_SENHA --project-name painel-cerurb
 */

/** base64 de uma string UTF-8, sem depender de `unescape` (legado, e que
 *  quebraria silenciosamente uma senha com acento). */
function b64utf8(texto) {
  const bytes = new TextEncoder().encode(texto);
  let bin = '';
  for (const b of bytes) bin += String.fromCharCode(b);
  return btoa(bin);
}

/**
 * Compara sem vazar ONDE as strings divergem — um `===` sai no primeiro byte
 * diferente e deixa medir o prefixo correto. O COMPRIMENTO ainda separa cedo,
 * e isso é aceitável aqui: o formato do cabeçalho Basic já o entrega.
 */
function igual(a, b) {
  if (a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

const NEGADO = () =>
  new Response('Acesso restrito ao Painel CERURB.', {
    status: 401,
    headers: {
      'WWW-Authenticate': 'Basic realm="Painel CERURB", charset="UTF-8"',
      'Cache-Control': 'no-store',
      'Content-Type': 'text/plain; charset=utf-8',
    },
  });

export async function onRequest({ request, env, next }) {
  const usuario = env.PAINEL_USUARIO;
  const senha = env.PAINEL_SENHA;

  // Sem credencial configurada o site não sobe aberto por acidente.
  if (!usuario || !senha) {
    return new Response(
      'Painel sem credencial configurada. Defina PAINEL_USUARIO e PAINEL_SENHA no projeto.',
      { status: 503, headers: { 'Content-Type': 'text/plain; charset=utf-8' } },
    );
  }

  const recebido = request.headers.get('Authorization') || '';
  const esperado = 'Basic ' + b64utf8(`${usuario}:${senha}`);
  if (!igual(recebido, esperado)) return NEGADO();

  const resposta = await next();
  const r = new Response(resposta.body, resposta);
  // Conteúdo autenticado não deve ser guardado por proxy no caminho.
  r.headers.set('Cache-Control', 'private, no-store');
  r.headers.set('X-Robots-Tag', 'noindex, nofollow');
  return r;
}
