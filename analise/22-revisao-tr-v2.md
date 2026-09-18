# Revisão do TR v2 — o que passar para a outra sessão

## BLOQUEANTES (corrigir antes de qualquer circulação)

### B1. O documento está corrompido em duas seções
A **seção 2** saiu com mojibake de renderização matemática:
> *"parcela fixa desetup [R X]∗∗+∗∗valorunit a ˊ rioporim o ˊ velanalisado[R Y]"*

E a **seção 3** idem. Além disso, a **seção 5, item (e)** traz **"версões"** — palavra em cirílico.
O TR é um documento que vai ao jurídico de uma prefeitura. **Reescrever as seções 2, 3 e 5(e) em
texto limpo**, sem notação especial, e revisar o arquivo inteiro por corrupção de caractere.

### B2. Contradição interna: o pagamento da Fase 2 depende de ato de terceiro
O item 1.3 estabelece — corretamente — que a Fase 2 **"não se sujeita a data certa"** porque depende
de atos do contratante e da RFB.

Mas o item 4 diz:
> *"[70]% na **emissão do CIB aos imóveis** ou no relatório de impedimento aceito pelo gestor"*

**A emissão do CIB é ato da Receita Federal**, não do contratado nem do contratante. Vincular 70% do
preço a ato de terceiro é exatamente o risco que o item 1.3 se esforçou para afastar — e cria a
hipótese de o contratado entregar tudo e não receber porque a RFB atrasou.

**Correção:** o gatilho dos 70% deve ser **"aceite da remessa em homologação"** (ato verificável e
sob controle do processo) ou o relatório de impedimento. A emissão do CIB pode aparecer como
*resultado esperado*, nunca como condição de pagamento.

### B3. O mini-diagnóstico gratuito NÃO pode estar no TR
Item 1.2, entre parênteses:
> *"Na pré-venda, o contratado executa mini-diagnóstico de 72h sobre o export, sem custo, como
> subsídio à estimativa de preço."*

Isso é **atividade de pré-venda descrita dentro do instrumento contratual**. Dois problemas:
1. Um órgão de controle lê como **serviço prestado antes da cobertura contratual** — irregularidade
   clássica, e que respinga no gestor, não no fornecedor.
2. Descrever no TR que o fornecedor já teve acesso ao cadastro antes da contratação levanta pergunta
   sobre **isonomia** no procedimento (ver B4).

**Correção: retirar inteiramente do TR.** O mini-diagnóstico é ação comercial; se precisar de amparo,
formaliza-se por termo de confidencialidade próprio, fora do processo de contratação.

## ALTO (afeta o cronograma e a estratégia)

### B4. O art. 75, § 3º não está no dossiê — e muda o calendário e a exposição
> **Art. 75, § 3º:** a dispensa dos incisos I e II será **"preferencialmente precedida de divulgação
> de aviso em sítio eletrônico oficial, pelo prazo mínimo de 3 (três) dias úteis, com a especificação
> do objeto e com a manifestação de interesse da Administração em obter propostas adicionais"**,
> selecionando-se a mais vantajosa.

Três consequências que o dossiê não trata:
1. **+3 dias úteis no mínimo** no cronograma — que já é apertado (20/11 → 10/12).
2. Embora a lei diga *"preferencialmente"*, **muitos municípios regulamentaram como obrigatório** e
   vários TCEs assim tratam. **Verificar o regulamento municipal de cada alvo** — e isso é item de
   qualificação de lead, não detalhe.
3. **Expõe o objeto à concorrência.** O aviso público de um objeto "conformidade CIB/CADURB" é
   exatamente o sinal que aciona o gatilho de vigilância sobre a Foxinline. Não é motivo para evitar —
   é motivo para **estar preparado**: proposta de referência pronta, diferencial técnico explícito no
   TR (metodologia, pin de versão, vocabulário oficial de falhas) e preço já fundamentado.

### B5. Faltam as duas cláusulas que o plano definiu como constitutivas do ativo
O TR trata de LGPD e devolução de arquivos, mas **não traz**:

1. **Propriedade intelectual.** O plano fixou: *"PI do software e dos modelos retida pela empresa, com
   licença de uso ao município"*. **Sem cláusula expressa, abre-se a discussão** de que o produto
   desenvolvido sob contrato administrativo pertence ao contratante. É a lacuna mais cara do TR.
2. **Uso do dado para calibração.** O plano identificou como *"a cláusula que constitui o ativo da
   empresa"* — o pool regional de dados que torna o Segmento A viável. Sem ela no primeiro contrato,
   **perde-se 100% do dado dos primeiros clientes**, e retrofit em 2027 não recupera.

Redação sugerida, compatível com a governança já declarada: *"o Contratado poderá utilizar os dados
de forma agregada e anonimizada para calibração e aprimoramento de seus modelos, vedada a
identificação de titulares e a transferência a terceiros, permanecendo o Município como controlador"*.

## MÉDIO (qualidade do instrumento)

| # | Lacuna | Correção |
|---|---|---|
| M1 | **Não define o que é "imóvel analisado"** — base do preço unitário | definir: registro único por `inscricaoImobiliaria`; duplicatas contam uma vez e entram no laudo como falha |
| M2 | **Não há prazo nem rito para o aceite do Laudo** | *"o gestor manifesta-se em até [5] dias úteis; o silêncio implica aceite tácito"* — sem isso o pagamento trava indefinidamente |
| M3 | **Vigência "prorrogável enquanto vigente o empenho"** | vigência não se prorroga por empenho; usar prazo determinado com previsão de prorrogação nos termos dos arts. 105–107 |
| M4 | **Sem sanções** (art. 156) | mesmo em dispensa, incluir cláusula sucinta de sanções — a ausência total é notada pelo parecerista |
| M5 | **Fase opcional "contratável junto ou separadamente"** | se junto, integra o objeto e o valor; se separada, entra no somatório do § 1º. Escolher uma e declarar |
| M6 | **Devolução de arquivos sem prazo/forma** | *"em até [30] dias do encerramento, com declaração de expurgo"* |

## O QUE ESTÁ BOM E NÃO SE MEXE
- **A estrutura de fases com naturezas distintas** (obrigação com prazo certo × marco com critério
  objetivo) é a melhor parte do documento e resolve o risco jurídico mais provável.
- **O critério de aceite da Fase 2** (*remessa aceita em homologação OU relatório de impedimento*) é
  redação correta de obrigação de meio.
- **A modularidade setup + unitário por imóvel** é a decisão certa: permite portes diferentes no mesmo
  instrumento e não precisa ser redesenhada para consórcio.
- **A citação do § 1º no item 3**, mandando verificar outras contratações de mesma natureza no
  exercício, está correta e é exatamente o cuidado que faltava na v1.
- **O TR alternativo (fallback) com a instrução explícita "jamais como oferta principal"** é bom
  desenho comercial dentro de um documento jurídico.
- **A distinção R$ 130.984,22 (serviços, consórcio) × R$ 130.984,20 (engenharia)** foi incorporada e
  está correta.

## ORDEM DE TRABALHO SUGERIDA
1. B1 (encoding) — 20 min, e sem isso nada circula
2. B2 (gatilho dos 70%) — 10 min
3. B3 (retirar mini-diagnóstico do TR) — 5 min
4. B5 (PI + calibração) — 30 min, e é o que protege o ativo
5. B4 (art. 75 §3º no dossiê + verificar regulamento municipal por alvo) — 1h
6. M1–M6 — 1h
