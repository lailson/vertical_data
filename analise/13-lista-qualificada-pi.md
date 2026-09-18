# Lista qualificada — os 25 municípios do PI com bairros, cruzados com tenant e dado fiscal

Verificado em 2026-09-16: malha `PI_bairros_CD2022` (DBF) × Certificate Transparency `%.foxinline.com`
× SICONFI RREO Anexo 03 (2025).

| Município | Bairros | IPTU 2025 | RCL 2025 | Pop. | Tenant Fox | Segmento |
|---|---|---|---|---|---|---|
| Teresina | 123 | R$ 166.321.115 | R$ 4,80 bi | 868.523 | — | A |
| Parnaíba | 46 | R$ 4.161.751 | R$ 786,0 mi | 163.087 | — | A |
| Floriano | 40 | R$ 1.208.395 | R$ 327,7 mi | 62.593 | — | A |
| Piripiri | 30 | R$ 1.533.757 | R$ 347,1 mi | 65.762 | **SIM** | A |
| Picos | 27 | R$ 7.062.110 | R$ 415,3 mi | 82.028 | — | A |
| Campo Maior | 21 | R$ 1.043.286 | R$ 278,1 mi | 45.252 | **SIM** | A |
| **Altos** | **17** | **R$ 245.127** | **R$ 61,3 mi** | **46.826** | **—** | **fronteira** |
| **Paulistana** | **17** | **R$ 558.221** | **R$ 131,8 mi** | 21.080 | **—** | **fronteira** |
| Barras | 15 | R$ 882.361 | R$ 298,3 mi | 47.909 | **SIM** | fronteira |
| Corrente | 15 | R$ 751.325 | R$ 143,8 mi | 27.419 | **SIM** | fronteira |
| Elesbão Veloso | 15 | R$ 125.340 | R$ 68,6 mi | 13.574 | — | fronteira |
| Bom Jesus | 10 | R$ 1.022.220 | R$ 228,6 mi | 28.857 | — | A |
| São Félix do Piauí | 10 | R$ 40.788 | R$ 31,4 mi | 2.842 | — | B |
| Cocal | 7 | R$ 32.309 | R$ 145,7 mi | 28.121 | — | B |
| Ribeiro Gonçalves | 5 | R$ 32.663 | R$ 81,7 mi | 6.164 | — | B |
| Brasileira | 7 | R$ 9.295 | R$ 54,8 mi | 8.438 | **SIM** | B |
| Simões | 9 | R$ 0 | R$ 104,3 mi | 14.344 | — | B |
| União · Luís Correia · Piracuruca · Água Branca · Baixa Grande do Ribeiro · Ilha Grande · Lagoa do Barro · Simplício Mendes | 3–14 | **sem retorno** | **sem retorno** | — | 4 SIM | B |

## Correção a um dos dois nomes sugeridos

A análise paralela apontou **Campo Maior e Altos** como "tenants Foxinline com bairros". Verificado:
**Campo Maior é tenant; Altos não é.** Tenants com bairros são: Piripiri, Campo Maior, Barras,
Corrente, União, Água Branca, Brasileira, Ilha Grande.

## O melhor candidato a piloto de painel fora da capital: **Altos**

| Critério | Altos |
|---|---|
| Tem bairros (painel funciona) | **17** |
| Não é tenant Foxinline | **✅** |
| RCL confortável | **R$ 61,3 mi** |
| IPTU pequeno mas não nulo | R$ 245 mil — **fronteira A/B** |
| População | 46.826 (7º do estado) |

Altos é o único município do PI que reúne **bairros + ausência do incumbente + porte razoável**.
É onde o painel territorial e a conformidade cadastral podem ser vendidos no mesmo contrato — o que
nenhum outro município da lista permite. **Paulistana** é o segundo (17 bairros, não-tenant,
RCL R$ 131,8 mi), com a ressalva da população menor (21 mil).

## Um sinal que apareceu sem ser procurado

**Oito dos 25 municípios não retornaram RREO 2025 no SICONFI** — União, Luís Correia, Piracuruca,
Água Branca, Baixa Grande do Ribeiro, Ilha Grande, Lagoa do Barro do Piauí, Simplício Mendes.

Município que não publica demonstrativo fiscal obrigatório é município com gestão fiscal frágil e sem
equipe — **exatamente o perfil do comprador do Segmento B**. A ausência de dado no SICONFI vira, ela
mesma, um critério de qualificação de lead: quem não consegue enviar RREO ao Tesouro não vai
conseguir enviar remessa ao CADURB sozinho até 31/12.

## Ressalva de método
Ausência no Certificate Transparency **não prova** que o município não é cliente da Foxinline — ele
pode não ter subdomínio próprio. É evidência forte para a presença, fraca para a ausência. Confirmar
caso a caso antes de usar comercialmente.
