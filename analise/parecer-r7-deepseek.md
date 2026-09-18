Concordo com o Anexo 1 §5 (k-means não elimina arbitrariedade).

1. **k-means** (Anexo 2 §3) afirma “reproduzível” com sementes fixas, mas a normalização min–max usa min/max da amostra; incluir um município muda o intervalo e pode remapear grupos de todos os bairros. Consequência: índice oficial deve usar cortes fixos e pesos declarados; k-means fica só como camada exploratória.

2. **V05000** (Anexo 1 §3): adicionar `cobertura_entorno` é necessário, mas insuficiente. Consequência: o pipeline deve tratar `cobertura < 90%` como dado ausente e excluir o bairro do ranking, não apenas exibir selo; senão o painel de Altos/Guaribas apresenta amostra como censo.

3. **Spec `0.0.1-SNAPSHOT`** (Anexo 1 §7) sem teste de divergência pode gerar laudo contra contrato obsoleto. Consequência: bloqueante para vender diagnóstico; exigir hash pinado da spec e falha explícita no CI antes de qualquer laudo.

4. **Validação apenas sintática** (Anexo 1 §7 item 3) entrega um relatório de `required` que qualquer um extrai do Swagger. Consequência: bloqueante para justificar R$ 3–5 mil; sem CEP, logradouro/município, inscrição única e área/tipologia, o diagnóstico não vale o preço.

5. **Fluxo de geometria** (Anexo 1 §7 item 2; Anexo 4 §4) só é bloqueante se o pitch prometer geometria/REURB. Consequência: ou descope explícito “diagnóstico alfanumérico apenas” no M0, ou a promessa exige implementar lote + vinculação antes de vender.

6. **Erro factual na metodologia** (Anexo 1 §4): Tabajaras tem razão média/mediana 1,11, não “muito inferior”. Consequência: trocar o exemplo por Brasilar/Mocambinho antes de publicar; manter Tabajaras dá munição a qualquer parecer contrário.
