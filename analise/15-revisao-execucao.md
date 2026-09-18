# Revisão do plano de execução + validação do painel construído

## 1. O painel existe e é bom

`index.html` (494 KB) + `teresina_full.geojson` (458 KB, **123 features com geometria Polygon**).

Propriedades por bairro: `name, cd, dom, mor, mor_por_dom, agua, esgoto, pav, ilum, calcada, rampa,
bueiro, onibus, arbor_sem, renda, renda_med, idosos_pct, criancas_pct`.

11 telas, fontes tipográficas próprias, **botão de exportar CSV** e — o detalhe que mais importa —
um botão **"Aguardando fonte"**, ou seja, o painel declara o que ainda não tem dado em vez de
inventar. É a correção direta do defeito fatal do protótipo anterior.

## 2. ERRO MEU, encontrado na validação cruzada: usei a métrica errada

Ao confrontar os valores do GeoJSON com os que extraí, a divergência era sistemática:

| Bairro | pav — meu | pav — painel |
|---|---|---|
| Tabajaras | 36,8% | **95,2%** |
| Morros | 46,0% | 81,7% |
| Olarias | 48,6% | 74,7% |
| Brasilar | 44,8% | 70,4% |
| Chapadinha | 36,7% | 46,6% |
| Centro | 100,0% | 100,0% |

Causa: **existem dois arquivos de entorno por bairro, com métricas diferentes**, e eu usei o errado.

| Arquivo | Variáveis | Unidade |
|---|---|---|
| `Agregados_por_bairros_entorno_faces_BR` | V05400+ (pav = **V05406**) | **faces de quadra** |
| `Agregados_por_bairros_entorno_domicílios_BR` | V05000+ (pav = **V05006**) | **domicílios** |

Isto também resolve a discrepância de códigos das rodadas anteriores: a análise paralela citou
V05006/V05012 e eu citei V05406/V05412 — **os dois estavam certos, sobre arquivos diferentes.**

### Por que a métrica por domicílio é a correta

Por face, um segmento de quadra com um terreno baldio pesa igual a um com 50 casas. Por domicílio,
o indicador responde à pergunta que interessa à política pública: **quantas pessoas moram em rua sem
pavimento**.

Tabajaras é a prova: **19 faces (36,8% pavimentadas) mas 293 domicílios (95,2% em face pavimentada)**
— as casas estão concentradas nas poucas faces pavimentadas; o resto são faces de terreno vazio.

**Consequência: o "achado da armadilha de Tabajaras" que registrei na rodada 6 era artefato da minha
escolha de métrica, não uma armadilha do dado.** A regra de corte mínimo de faces que propus — e que
o parecer técnico endossou — **perde a maior parte da sua razão de ser**. O painel já está certo.

O corte continua fazendo sentido, mas **em domicílios, não em faces**, e com limiar muito menor
(bairros com poucas dezenas de domicílios seguem instáveis).

## 3. O plano de execução proposto — avaliação

### Faz sentido, e o sequenciamento está certo
Duas pistas em paralelo (decisões humanas × trabalho técnico sem dependência) é o desenho correto
para uma janela curta. O ponto mais forte: **disparar os e-SIC primeiro**, porque o prazo de 30 dias
é o único item do plano que não se comprime com esforço.

### O que eu mudaria

**a) A prioridade do conector CADURB está certa, mas o pedido de credencial precisa vir antes.**
A adesão ao convênio é ato do **município**, não nosso — e depende de Termo assinado com certificado
ICP-Brasil e publicação no DOU. Construir contra o Swagger de homologação não exige credencial, mas
**testar de verdade exige**. Se a credencial depende de um município conveniado, e nenhum piloto está
definido, o conector fica sem ambiente de teste real. **Isso precisa ser verificado na primeira
semana, não descoberto na quarta.**

**b) O INEP (537 MB, geocodificação) é o item de pior relação valor/esforço do M0.** Educação é uma
tela entre onze, e o painel já tem dez funcionando. Geocodificar escolas e cruzar com polígonos é
meio a um dia de trabalho se tudo der certo, e três se não der. **Sugiro rebaixar para depois do
conector e da verificação fiscal.**

**c) Falta um item que não está em nenhuma das duas pistas: a metodologia publicada do `iv`.**
O painel tem "Vulnerabilidade por bairro" na tela principal. Se o índice não vier com pesos, fontes e
fórmula num documento anexo, ele reproduz — com dado real, o que é pior — o passivo do protótipo
antigo. **É meio dia de trabalho e é bloqueante para apresentar a terceiros.**

**d) O calendário de venda tem um otimismo:** "16/10–15/11: vender o diagnóstico em 5–10 municípios".
São 30 dias corridos para 5–10 contratos com prefeituras, sem referência anterior, em municípios onde
ninguém conhece a empresa. **Com dispensa é rápido de assinar, mas não de decidir.** Sugiro meta de
**2–3 no período**, e tratar 5–10 como cenário otimista — errar a meta para baixo no primeiro mês
contamina a leitura de todo o resto.

**e) A reunião com a Foxinline como "parceria fundiária" é a jogada certa, mas o timing é ruim
agora.** Chegar antes de ter uma remessa aceita é chegar sem ativo de troca. Depois de 2–3 remessas
aceitas em municípios que não são tenants dela, a conversa muda de "queremos seus dados" para "temos
um produto que seus 236 municípios vão precisar até 31/12". **Sugiro adiar para depois do primeiro
aceite no CADURB.**

### O que está certo e não deve mudar
- e-SIC imediato, com a SEAD (lista PROUrbe) como o mais estratégico
- revalidar o método dos RREO antes de uso comercial
- conversa de escopo com o proponente como decisão nº 1
- Altos como piloto, Paulistana como reserva
- o dossiê de dispensa reutilizável — "preencher o caminho orçamentário é parte do produto"
