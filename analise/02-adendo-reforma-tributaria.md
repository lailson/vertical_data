# Adendo 2 — a reforma tributária transforma a PGV em obrigação anual recorrente

Fonte: **Nota Técnica CTAT nº 05/2025 da CNM** ("Orientações aos Municípios sobre Sinter e CIB",
texto extraído do PDF oficial), **LC 214/2025**, **IN RFB 2.275/2025**, página oficial do CIB na
Receita Federal.

## 1. O CIB é obrigação legal com prazo, não recomendação

**LC 214/2025, art. 265:** todos os bens imóveis urbanos e rurais **deverão ser inscritos no CIB**.
O CIB **deve constar obrigatoriamente de todos os documentos relativos a obra de construção civil
expedidos pelo Município** (§2º).

**Art. 266 — prazos de inscrição:**
- **12 meses** → órgãos federais, serviços notariais e registrais, **capitais e DF** incluem o CIB
  em seus sistemas → **a partir de 01/01/2026**.
- **24 meses** → órgãos estaduais e **os demais Municípios** → **a partir de 01/01/2027**.

Formato do CIB: alfanumérico, 7 caracteres + dígito verificador (`ABC1234-5`).

## 2. O achado central: o art. 256 torna a avaliação de imóveis uma obrigação ANUAL

**LC 214/2025, art. 256** — os entes devem **divulgar e disponibilizar no SINTER o VALOR DE
REFERÊNCIA** dos imóveis, **estimado para TODOS os bens imóveis que integram o CIB** e
**ATUALIZADO ANUALMENTE**. Esse valor de referência **será utilizado no cálculo do IBS** nas
operações com bens imóveis.

A metodologia prevista no art. 256 considera: preços praticados no mercado imobiliário; informações
enviadas pelas administrações tributárias de Municípios, DF, Estados e União; informações dos
serviços registrais e notariais; e **localização, tipologia, destinação, data, padrão e área de
construção** do imóvel.

### Por que isso reposiciona o projeto inteiro

1. **A PGV deixa de ser módulo opcional e vira obrigação recorrente.** Na proposta original, a
   Planta Genérica de Valores era o módulo 3, vendável como melhoria de justiça fiscal. Com o
   art. 256, avaliar todos os imóveis e atualizar **todo ano** passa a ser dever legal ligado à
   arrecadação do IBS. "Atualizado anualmente" é a definição de assinatura recorrente.
2. **A metodologia do art. 256 é literalmente um problema de modelo estatístico** — estimar valor
   de mercado a partir de localização, tipologia, padrão e área construída, calibrado por preços
   observados. É **avaliação em massa (CAMA / mass appraisal)**. Aqui, e só aqui, machine learning
   deixa de ser enfeite de proposta e vira o método tecnicamente indicado — com a ressalva de que
   exige cadastro robusto e amostra de transações (ITBI, cartórios) para calibrar.
3. **Muda o comprador dentro da prefeitura**: sai o planejamento urbano (compra por vontade) e entra
   a Secretaria de Fazenda/Finanças (compra por prazo legal e por receita).
4. **Muda o argumento**: não é "painel bonito", é "sem isso o município perde base de cálculo do IBS
   e fica inadimplente com a LC 214".

## 3. Existe especificação técnica pública para a integração

A RFB publicou o **Roteiro Técnico de Integração ao SINTER** — especificamente o *"Roteiro
Operacional para envio de Remessa com Informações Georreferenciadas e Alfanuméricas das Unidades
Imobiliárias das Prefeituras ao Módulo Cadastro Urbano — CADURB do SINTER"* (RFB, 2023), disponível
no sítio do ENAT. O módulo aceita **envio alfanumérico puro ou alfanumérico + georreferenciado**.

Ou seja: **o formato de saída do produto já está especificado por norma federal.** Isso é raro e é
bom — elimina ambiguidade de requisito e cria um critério de aceite objetivo ("a remessa foi aceita
pelo CADURB").

## 4. Existe dinheiro carimbado para o município pagar por isso

A NT da CNM (seção 6.4, "Municípios que necessitam de recursos financeiros para implantação")
aponta o **PROFISCO III — Programa de Apoio à Gestão dos Fiscos do Brasil**, do **Ministério da
Fazenda em parceria com o BID**, linha de crédito disponível para **municípios**, desenhada em
grande parte para apoiar a operacionalização da Reforma Tributária.

**Consequência:** a objeção "a prefeitura não tem orçamento" tem resposta pronta e oficial. Ajudar o
município a acessar o PROFISCO III é, em si, parte da venda.

## 5. O caminho de adesão é burocrático e conhecido — e isso é oportunidade de serviço

A NT descreve **16 passos** de adesão: Termo de Adesão ao Convênio SINTER assinado com certificado
digital ICP-Brasil → processo digital no e-CAC da RFB → "Celebração de Acordos Nacionais" → "Aderir
ao Convênio Sinter de 15/12/2022" → juntada de documentos → **publicação do Termo no DOU** → só
então o município pode enviar suas bases conforme o Roteiro Técnico. Normativo de referência:
**Portaria ASCIF nº 6, de 15/12/2022**.

Nenhuma prefeitura pequena tem equipe para conduzir isso. **A condução da adesão é um produto de
entrada barato, de ciclo curto, que cria o relacionamento e a dependência técnica antes da venda
grande.**

---

## 6. RESSALVA IMPORTANTE — uma ambiguidade que precisa ser confirmada antes de virar tese de venda

A leitura da seção 2 acima ("a PGV vira obrigação anual do município") **é a interpretação otimista,
e ela tem um contraponto sério que não pode ser ignorado.**

O art. 256 da LC 214/2025 diz que o valor de referência é apurado **"pelas administrações
tributárias"** — no plural e sem especificar qual ente —, considerando preços de mercado,
informações enviadas pelas administrações tributárias **dos Municípios, do DF, dos Estados e da
União**, e informações **dos serviços registrais e notariais**.

E a **IN RFB nº 2.275, de 15/08/2025**, obriga os **serviços notariais e de registro a compartilhar
as informações das operações imobiliárias via SINTER**.

**O contraponto:** se a RFB passa a receber de cartório o preço de todas as transações imobiliárias
do país, ela tem, centralizadamente, a melhor amostra de calibração que existe — e pode apurar o
valor de referência **ela mesma**, sem que cada município precise contratar avaliação em massa.
Nesse cenário, a obrigação municipal é **enviar dados cadastrais**, não **produzir avaliação**, e a
tese de "PGV anual como assinatura recorrente" enfraquece bastante.

### Como isso muda o que se pode afirmar

- **Não afirmar, ainda, que o município é obrigado a contratar avaliação em massa anual.** Isso
  precisa ser confirmado na IN e no Roteiro Técnico antes de entrar em qualquer proposta.
- **O que se pode afirmar com segurança**, independentemente de quem apura:
  1. O município é obrigado a **inscrever todos os imóveis no CIB** e a **enviar seus dados
     cadastrais** ao SINTER (art. 265/266) — isso não é ambíguo.
  2. Se a RFB publicar um valor de referência **acima do valor venal da PGV municipal**, a defasagem
     fica **visível e auditável** — pelo TCE, pelo Ministério Público e pela imprensa. A pressão
     política e jurídica para o município atualizar a PGV vira consequência quase automática.
     **O efeito é indireto, mas é forte, e talvez mais forte que a obrigação direta:** o município
     não vai poder mais alegar que não sabia da defasagem.
  3. A PGV continua sendo competência municipal para fins de **IPTU e ITBI**, independentemente do
     IBS.

**Conclusão prática:** a recorrência do negócio provavelmente existe, mas por um mecanismo diferente
do que a seção 2 sugere — não por obrigação direta de avaliar, e sim por **exposição da defasagem**.
Isso é uma tese de venda melhor (o município reage a um número publicado pela Receita), mas é uma
tese diferente, e o time precisa saber qual das duas está usando.

**Item obrigatório de due diligence antes de qualquer proposta:** ler a íntegra da IN RFB 2.275/2025
e obter o Roteiro Técnico do CADURB. Registro relevante: **o Roteiro Técnico NÃO é público** — a
tentativa de baixá-lo do sítio do ENAT retorna conteúdo restrito, e a NT da CNM confirma que ele é
"enviado aos Gestores (do Convênio e de TI) indicados no requerimento", isto é, **só após a adesão
do município ao convênio**. Isso reforça o valor de entrar pelo serviço de condução da adesão: é o
que dá acesso à especificação.
