# Registro das ligações — por que a planilha importa mais que a ligação

**Origem:** sugestão da rodada 10. O índice das fichas ordena por **facilidade de
atendimento**, não por propensão de compra — porque não existe, hoje, nenhuma variável
que preveja quem compra. A RCL foi medida e não discrimina: o contrato é 0,16% dela.

**As respostas da porta 3 são o primeiro rótulo real que este projeto vai ter sobre
comportamento de compra.** Vinte ligações registradas de forma estruturada valem mais,
para a próxima decisão, do que qualquer índice que eu consiga construir com dado aberto.

É a mesma lógica que já se aplicou à ANEEL: desfecho observado vale mais que proxy
engenhoso. Lá o rótulo veio de graça na base; aqui ele vem do telefone.

---

## A planilha

`registro-ligacoes.csv`, uma linha por ligação. **Preencher na hora**, não depois — o
detalhe que vira variável é o que se perde em vinte minutos.

| coluna | valores | por que existe |
|---|---|---|
| `data` | AAAA-MM-DD | — |
| `cd_ibge` | 7 dígitos | chave para cruzar com tudo o mais |
| `municipio` | texto | conferência humana |
| `falei_com` | `contador` · `sec_financas` · `sec_admin` · `prefeito` · `ninguem` | **quem atende prevê se a conversa avança** |
| `porta1_conhece` | `sim` · `nao` · `nao_sabe` | conhecimento da obrigação do art. 266 |
| `porta2_fornecedor` | `sim` · `nao` · `nao_sabe` | há incumbente? confirma ou desmente o sinal de Certificate Transparency |
| `porta3_saldo` | `sim` · `nao` · `suplementar` · `nao_sabe` | **a variável que interessa** |
| `porta3_elemento` | texto livre | qual elemento citaram, se citaram |
| `prazo_dispensa_dias` | inteiro | quanto consome da janela |
| `porta4_assina` | `prefeito` · `secretario` · `nao_sabe` | sem isto não há proposta |
| `resultado` | `avancar` · `voltar_em_janeiro` · `nao` · `sem_contato` | desfecho |
| `proximo_passo`, `data_retorno` | texto, data | operacional |
| `observacao` | texto | onde mora o que a planilha ainda não sabe perguntar |

---

## Três regras de preenchimento

1. **`nao_sabe` é uma resposta, não um campo vazio.** "O contador não soube dizer se há
   saldo" é informação forte — pode significar que a dotação não é acompanhada, e isso
   prevê atrito.
2. **`voltar_em_janeiro` não é `nao`.** Confundir os dois apaga a diferença entre mercado
   inexistente e mercado com data. Foi explicitamente separado no roteiro §2.
3. **Não preencha o que não perguntou.** Campo em branco é ausência; `nao_sabe` é
   medição. A regra da casa vale aqui como vale no painel: **ausência não é zero.**

---

## Quando isto vira modelo

Com ~20 linhas dá para olhar tabela cruzada: `porta3_saldo` contra o que já se sabe do
município (entregou RREO, tem incumbente, volume, porte). Com ~60 dá para estimar.

**Antes disso, não modele.** Foi a lição do modelo de risco: 72 eventos sustentam sete
variáveis, e menos que isso é sobreajuste com aparência de rigor.
