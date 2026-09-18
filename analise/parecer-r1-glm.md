# Parecer R1 — eixo Negócio, Risco e Estratégia de Entrada (dossiê CERURB)

Consultor: GLM. Data: 2026-09-15. Eixo: negócio/risco. Regra da rodada respeitada: 6 achados, adversarial, sem resumo final.

---

## Achado 1 — O risco Foxinline é de mercado, não de integração (seção 2)

**Diagnóstico:** A Foxinline concentra três papéis incompatíveis — fornecedora do dado, único canal de acesso (sem API, exportação como via realista) e concorrente adjacente com ecossistema fim-a-fim — e, como fornecedora pequena com infraestrutura pública fora do ar hoje, pode bloquear, atrasar ou simplesmente descontinuar o acesso sem qualquer obrigação contratual para com quem depende dela.

**Consequência:** Toda receita que depender do dado CERURB carrega risco de interrupção de 100% e sem remédio, e o módulo de coleta (seção 5) será replicado como módulo do CERURB Pro em 1–2 ciclos de venda — a única neutralização é estrutural: CERURB expressamente fora do escopo contratual da v1, dado CERURB tratado como bônus se exportado, e zero dia-homem de engenharia em integração/scraping que não se pague no primeiro trimestre.

## Achado 2 — A janela CIB/SINTER reescreve produto, comprador e preço — e a proposta ignora (seções 1 e 3)

**Diagnóstico:** A proposta vende "painel de gestão" ao comprador errado (planejamento urbano, compra por vontade) quando a obrigação CIB de jan/2027 para os ~5.540 municípios fora das capitais cria um comprador novo (Fazenda/Controloria, comprando por prazo federal) para um produto diferente — cadastro imobiliário conformante e integrável ao SINTER — que o documento de 4 módulos (seção 1) não menciona uma única vez.

**Consequência:** Reposicionar como "conformidade CIB" encurta o ciclo de venda de 12–18 para 3–9 meses, sustenta licenciamento recorrente por município em vez de projeto único e dá ~15 meses para acumular referências antes de o mercado de sistemas de IPTU despertar — e o custo de entrar sem essa tese é competir em estética de dashboard contra BI gratuito e gratuito de brinde pelos incumbentes.

## Achado 3 — Propriedade do dado é o único ativo defensável, e as armadilhas são LGPD + 14.133 (seções 2 e 5)

**Diagnóstico:** O cadastro a ser originado (seção 5) é dado pessoal em volume (CPF, renda, família, geolocalização — seção 2) com o município como controlador, e na Lei 14.133 a contratação direta por dispensa cobre serviços comuns só até ~R$ 59 mil — acima disso o caminho é pregão com dotação orçamentária, e cláusulas omissas deixam tanto a base quanto a propriedade intelectual do software migrarem para o contrato administrativo.

**Consequência:** O contrato exige quatro cláusulas inegociáveis — (i) empresa como operadora LGPD com termo próprio, multa de até 2% do faturamento limitada a R$ 50 mi por infração se omitido; (ii) base exportável pelo município em formato aberto a qualquer momento; (iii) PI do software e dos modelos retida pela empresa, com licença de uso ao município; e (iv) vedação de repasse da nossa base a terceiros concorrentes, inclusive à Foxinline — porque sem (iv) a prefeitura pode presentear o CERURB com o cadastro que nós financiaramos, e o diferencial evapora no ato da assinatura.

## Achado 4 — Como posto, o modelo de receita é projeto único disfarçado (seções 1 e 4)

**Diagnóstico:** Dos 4 módulos da proposta (seção 1), o item mais caro não é software (aerolevantamento na casa de centenas de milhares de reais por município médio — seção 4), o que converte qualquer contrato "completo" em projeto de engenharia com margem desconhecida, enquanto ML/preditivo/chat na v1 (seção 1) só infla custo fixo sem gerar uma linha de receita adicional.

**Consequência:** Entrar pela estrutura de licenciamento — software como SaaS por município (implantação + anuidade), coleta de campo e aerolevantamento como serviço repassado a parceiro especializado fora do nosso balanço, e a posição de originador do dado (seção 5) monetizada como upgrades de conformidade e PGV — porque na forma atual cada contrato reinicia o CAC do zero e a empresa vira consultoria que termina; régua objetiva: se no primeiro contrato a receita recorrente for menor que 30% do valor total, o modelo nasceu errado.

## Achado 5 — Menor escopo que fecha contrato: diagnóstico de conformidade CIB sobre dado aberto (seções 1, 3 e 4)

**Diagnóstico:** O protótipo promete granularidade por bairro que só existe via cadastro próprio (seção 4) e não tem uma tela de imóvel nem métrica de arrecadação (seção 1), então o menor contrato honesto e imediatamente pagável é: um município, diagnóstico de aderência ao CIB/SINTER (seção 3), cruzamento do cadastro imobiliário existente da Fazenda com setor censitário do IBGE e IPTU do SICONFI, e entrega de um índice de conformidade com plano de fechamento de lacunas.

**Consequência:** Esse escopo sai em 60–90 dias com custo marginal baixo (fontes gratuitas — seção 4), entrega ao prefeito um número de campanha (potencial de IPTU não arrecadado em R$) e deixa ao time uma referência replicável para os ~5.540 municípios da janela — qualquer coisa maior que isso (cartografia, PGV, ML, chat) é dívida com juros antes da primeira receita.

## Achado 6 — Sinais de não entrar, com critério de saída (seções 2, 3, 4 e 5)

**Diagnóstico:** Não entrar se dois destes sinais coexistirem: o cliente-parceiro condicionar o projeto à integração com CERURB (seção 2); a prefeitura não emitir os ofícios de acesso às secretarias antes da assinatura (seção 4 — todo dado fino depende disso); não houver dotação orçamentária identificada na 14.133; o pagamento depender de aerolevantamento entregue por terceiros (seção 4); ou a REURB do parceiro tratar o painel como brinde sem orçamento próprio (seção 5).

**Consequência:** O cenário mediano com esses sinais não é "projeto difícil", é um piloto gratuito de 6 meses que queima a equipe dentro da janela de ~15 meses (seção 3) sem gerar contrato replicável — logo o critério de saída deve ser fixado agora: sem contrato assinado com dotação e acordo de operação de dados em até 45 dias de esforço comercial, abortar e realocar para o mercado CIB, cujo custo de oportunidade é todo o resto do país e não este município.
