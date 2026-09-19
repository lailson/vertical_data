# Carta à Equatorial Piauí — teste de uma hora

**Status:** rascunho para revisão. **Não enviado.**
**Origem:** rodada 10 (`analise/28` §13.2) — o revisor observou que a lista do BDGD vale
para a distribuidora, não para a prefeitura. Isto é o teste barato dessa hipótese.

**O que se quer descobrir, e é só isto:** se existe interesse comercial. Não é proposta,
não tem preço, não promete entrega. Uma hora de trabalho para responder uma pergunta de
modelo de negócio que nenhuma discussão interna resolve.

---

## Antes de enviar — três conferências

1. **O dado é ODbL e é deles.** O BDGD é declarado pela própria distribuidora à ANEEL.
   Oferecer a eles um recorte do que eles mesmos enviaram só faz sentido pelo **trabalho
   de cruzamento**, não pelo dado. O texto abaixo diz isso explicitamente — retirar essa
   frase transformaria a carta em algo constrangedor na primeira resposta técnica.
2. **Destinatário.** Diretoria comercial ou de mercado livre / geração distribuída. Não
   ouvidoria, não SAC.
3. **A amostra vai anexa, com 10 linhas e sem identificação de titular.** O BDGD publicado
   não traz nome de titular nas tabelas usadas, e nada de pessoa física entra.

---

## Texto

> **Assunto:** Cruzamento de dados públicos — unidades consumidoras de média tensão sem
> geração distribuída no Piauí
>
> Prezados,
>
> Sou responsável pela Vertical Data, que trabalha com dados públicos territoriais do
> Piauí. Cruzamos três bases abertas da própria ANEEL — a relação de empreendimentos de
> micro e minigeração, a Base de Dados Geográfica da Distribuidora e as tarifas
> homologadas — com o Cadastro Nacional de Endereços do IBGE.
>
> Do cruzamento saiu um recorte que talvez lhes seja útil: **3.284 unidades consumidoras
> de pessoa jurídica em média e alta tensão no Piauí que ainda não têm geração própria**,
> com bairro, CEP, CNAE e carga instalada. Outras 944 já têm.
>
> Os dados são públicos e vieram, em boa parte, da própria companhia — o que oferecemos
> não é a informação, é o **trabalho de cruzamento e a atualização recorrente**. Segue em
> anexo uma amostra de dez linhas para que avaliem se o recorte tem valor prático.
>
> Duas observações de método, para que saibam o que estão vendo:
>
> - o recorte cobre **apenas média e alta tensão de pessoa jurídica**, que é o que a base
>   pública publica. Baixa tensão residencial não entra;
> - a base é declarada pela distribuidora e tem a defasagem dela — não afirmamos
>   atualidade que o dado não tem.
>
> Se houver interesse, podemos conversar sobre recorte, periodicidade e formato. Se não
> houver, agradeço a leitura e não voltarei ao assunto.
>
> Atenciosamente,
> Lailson Henrique — Vertical Data

---

## O anexo

Gerado por `entregaveis/gerar_amostra_bdgd.py`: dez linhas, ordenadas por carga
instalada, colunas município, bairro, CEP, CNAE, carga em kW, tensão. Sem titular, sem
coordenada exata — a coordenada é o ativo, e amostra não entrega ativo.

## Como ler a resposta

| resposta | o que significa |
|---|---|
| pedem a base completa | há produto; a conversa passa a ser preço e periodicidade |
| pedem para conversar | há interesse; descubra se é comercial ou regulatório antes de precificar |
| respondem que já têm | esperado, e é informação: a pergunta vira **por que não usam** |
| silêncio em duas semanas | hipótese fechada por um custo de uma hora. Não insista |
