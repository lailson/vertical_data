# e-SIC 4 — TCE-PI · preço praticado e concorrência

> ⚠️ **PARCIALMENTE RESOLVIDO SEM PROTOCOLO, 18/09/2026.** A nota de rodapé deste
> documento dizia que valia tentar a API antes de protocolar. Valeu.
>
> - **Item 2 (IPTU de Altos) — RESPONDIDO.** A suspeita estava certa: o retorno do
>   SICONFI vinha parcial. SICONFI **R$ 245.127** contra TCE **R$ 1.310.555** (5,35×).
>   Ver `docs/metodologia-iv.md` §12.2.
> - **Item 1 (contratos e dispensas já firmados) — CONTINUA DE PÉ.** O endpoint
>   `/licitacoes` do Portal da Cidadania é **calendário do que vem**, não arquivo do que
>   passou: traz certames marcados, com objeto e valor previsto, mas não contratos
>   assinados nem fornecedor vencedor. **Este é o pedido que ainda precisa ser
>   protocolado**, e agora pode ser mais preciso — ver a versão enxuta abaixo.
>
> Ganho colateral não previsto: a API trouxe, para os **224** municípios, receitas por
> natureza e **despesas por elemento**, incluindo o 3.3.90.39 que o roteiro de
> qualificação pergunta. Os 72 municípios sem RREO 2025 deixaram de vir em branco.

**Por que existe:** é o único meio de conhecer **preço praticado e concorrência** antes de fixar a
própria faixa — e alimenta o gatilho de comoditização (concorrente vendendo integração abaixo de
R$ 8 mil). De quebra, valida o IPTU de Altos, cujo retorno no SICONFI veio com apenas 2 linhas, o que
sugere preenchimento parcial do demonstrativo.

**Órgão:** Tribunal de Contas do Estado do Piauí
**Canal:** e-SIC do TCE-PI / Portal da Cidadania — https://sistemas.tce.pi.gov.br

---

Com fundamento na Lei nº 12.527/2011, solicito as seguintes informações sobre contratações
municipais registradas neste Tribunal:

1. Relação de contratos e dispensas de licitação firmados por municípios piauienses nos exercícios
   de **2024, 2025 e 2026** cujo objeto envolva: cadastro imobiliário, cadastro técnico
   multifinalitário, geoprocessamento, planta genérica de valores, recadastramento imobiliário ou
   integração ao Sinter/CIB — com município, fornecedor, objeto, valor e data.

2. Para o município de **Altos (PI)**, os valores de arrecadação de IPTU e de ITBI nos exercícios de
   2024 e 2025, conforme prestação de contas recebida por este Tribunal.

Solicito o fornecimento em **formato aberto** (CSV ou XLSX). Todas as informações são de natureza
pública, referentes a contratações e receitas de entes públicos.

---

**Notas de uso (não enviar):**
- O item 1 é o mais estratégico de todos os quatro pedidos: mostra **quem já vende, para quem e por
  quanto** no estado. Se vier completo, redefine a faixa de preço com base em evidência, não em
  estimativa.
- O TCE-PI tem API documentada em `sistemas.tce.pi.gov.br/api/portaldacidadania/docs/` — vale tentar
  a consulta direta antes de protocolar; o pedido formal é o plano B.

---

## Versão enxuta, para protocolar agora

Com o item 2 já respondido pela API, o pedido reduz-se ao que ela não tem — e fica mais
fácil de deferir, porque pede menos:

> Com fundamento na Lei nº 12.527/2011, solicito relação de **contratos e dispensas de
> licitação já firmados** por municípios piauienses nos exercícios de **2024, 2025 e
> 2026**, cujo objeto envolva cadastro imobiliário, cadastro técnico multifinalitário,
> geoprocessamento, planta genérica de valores, recadastramento imobiliário ou integração
> ao Sinter/CIB.
>
> Para cada registro: município, fornecedor (razão social e CNPJ), objeto, modalidade,
> valor contratado e data de assinatura. Solicito em **formato aberto** (CSV ou XLSX).
>
> Registro que as informações de **receita e despesa** desses municípios já foram obtidas
> pela API pública do Portal da Cidadania deste Tribunal, de modo que este pedido se
> restringe ao que não está disponível por aquela via.

**Por que a última frase importa:** mostra que se tentou o caminho aberto antes de gerar
trabalho para o servidor. Pedido que demonstra ter feito a lição de casa é deferido com
mais frequência — e, se for indeferido, o indeferimento fica mais difícil de justificar.
