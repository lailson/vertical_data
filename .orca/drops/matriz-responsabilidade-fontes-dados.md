# Matriz de Responsabilidade — Fontes de Dados do Painel de Gestão Territorial

Documento de apoio para orientar os contatos institucionais necessários à viabilização
do aplicativo. Organizado por domínio de dado, com o órgão/entidade responsável, o tipo
de informação a solicitar e o grau de prioridade para o início do projeto.

---

## 1. Regularização fundiária e cadastro de imóveis

| Item | Detalhe |
|---|---|
| **Dados** | Localização, tipo de posse, status de regularização, tempo de ocupação, material construtivo, composição familiar |
| **Responsável** | Foxinline Technologies (fornecedora do CERURB) |
| **Contato sugerido** | Canal comercial/suporte já usado pelo escritório junto à Foxinline |
| **O que solicitar** | (1) Lista completa de campos coletados no formulário de campo atual; (2) possibilidade de API/webhook de integração; (3) alternativa de exportação periódica (CSV/relatório) |
| **Prioridade** | Alta — é a base do projeto e você já tem relação comercial ativa |
| **Observação** | Verificar no contrato com a prefeitura/CERURB a quem pertence a titularidade dos dados coletados, para respaldar o pedido de acesso |

---

## 2. Saneamento básico (água e esgoto)

| Item | Detalhe |
|---|---|
| **Dados** | Cobertura de rede de água tratada e esgoto por bairro/setor |
| **Responsável** | Concessionária de saneamento local (ex.: Águas de Teresina) e/ou Secretaria Municipal de Meio Ambiente e Recursos Hídricos |
| **Contato sugerido** | Diretoria técnica ou setor de planejamento da concessionária; gabinete da secretaria |
| **O que solicitar** | Mapas de cobertura de rede por bairro/setor censitário, ou dados brutos de domicílios atendidos |
| **Prioridade** | Alta — indicador central do painel |
| **Observação** | Concessionárias privadas podem exigir ofício formal da prefeitura para liberar dados agregados |

---

## 3. Pavimentação e infraestrutura viária

| Item | Detalhe |
|---|---|
| **Dados** | Extensão de vias pavimentadas e não pavimentadas por bairro |
| **Responsável** | Secretaria Municipal de Obras e Infraestrutura (ou equivalente local) |
| **Contato sugerido** | Setor de cadastro técnico/engenharia da secretaria |
| **O que solicitar** | Malha viária georreferenciada (shapefile ou KML), com status de pavimentação por trecho |
| **Prioridade** | Média-alta |
| **Observação** | Se não houver base georreferenciada pronta, a secretaria pode ter apenas planilhas de obras executadas — útil como ponto de partida |

---

## 4. Educação (evasão, matrículas, distância escolar)

| Item | Detalhe |
|---|---|
| **Dados** | Número de escolas, matrículas ativas, taxa de evasão, localização das unidades |
| **Responsável** | Secretaria Municipal de Educação (SEMEDUC) |
| **Contato sugerido** | Setor de planejamento educacional ou núcleo de estatísticas educacionais |
| **O que solicitar** | Extrato do Censo Escolar (INEP) por unidade, se a secretaria não tiver base própria consolidada |
| **Prioridade** | Média |
| **Observação** | O Censo Escolar do INEP é público e pode servir de fonte inicial independente da secretaria, o que acelera essa frente |

---

## 5. Iluminação pública

| Item | Detalhe |
|---|---|
| **Dados** | Cobertura de iluminação pública por bairro |
| **Responsável** | Secretaria de Serviços Urbanos (ou equivalente) e/ou concessionária de energia elétrica |
| **Contato sugerido** | Setor de manutenção/contratos de iluminação pública |
| **O que solicitar** | Mapa de pontos de iluminação instalados e relatório de chamados/manutenção por região |
| **Prioridade** | Baixa-média — pode entrar em uma segunda fase do projeto |

---

## 6. Dados demográficos e socioeconômicos de base

| Item | Detalhe |
|---|---|
| **Dados** | População, densidade, renda média por setor censitário |
| **Responsável** | IBGE (fonte pública, não exige contato institucional) |
| **Contato sugerido** | Não aplicável — dados abertos |
| **O que solicitar** | Malha de setores censitários e indicadores do Censo (SIDRA/IBGE), para uso como camada-base enquanto as integrações municipais amadurecem |
| **Prioridade** | Alta — é a fonte mais rápida de viabilizar, por ser pública |
| **Observação** | Recomendado como primeiro passo prático: permite montar uma versão inicial do painel sem depender de nenhuma negociação institucional |

---

## Ordem de ação recomendada

1. **Já viável agora**: iniciar com dados públicos do IBGE (item 6) para validar a arquitetura do painel sem depender de terceiros.
2. **Contato prioritário**: Foxinline (item 1), por já haver relação comercial — define o que realmente está disponível do lado do CERURB.
3. **Contato institucional**: um ofício único da Prefeitura, coordenado por um gabinete central (ex.: Secretaria de Planejamento), solicitando os dados dos itens 2, 3 e 4 às respectivas secretarias — mais eficiente do que contatos avulsos.
4. **Segunda fase**: iluminação pública (item 5), quando o núcleo do painel já estiver validado.
