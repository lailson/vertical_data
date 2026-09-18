"""
Regras semânticas do Laudo de Completude — CADURB/Sinter.

Complementa a validação sintática derivada da spec OpenAPI. Estas são as regras que a spec NÃO
expressa e que justificam o preço do diagnóstico: sem elas o produto é um `required`-checker.

Sem dependências externas. Python 3.9+.

Vocabulário de falha: os rótulos são os do enum `TipoFalhaDTO` da API oficial, para que o laudo
offline fale a mesma língua da resposta do CADURB. O typo em PRRENCHIMENTO é do SERPRO — mantido
de propósito.

Uso:
    from regras_semanticas import validar_registro, validar_base, DOMINIOS
    falhas = validar_base(lista_de_dicts, codigo_ibge="2200400")
"""
from __future__ import annotations
import json, re, unicodedata
from datetime import date
from pathlib import Path
from collections import Counter, defaultdict

# ---------------------------------------------------------------- vocabulário oficial
NAO_INFORMADO   = "CAMPO_NAO_INFORMADO_OU_NULO"
FORMATO_INVALIDO= "CAMPO_COM_FORMATACAO_INVALIDA"
TAMANHO_INVALIDO= "CAMPO_COM_TAMANHO_INVALIDO"
DATA_INVALIDA   = "DATA_COM_FORMATO_INVALIDO"
VALOR_INVALIDO  = "CAMPO_COM_VALOR_INVALIDO"
INCOMPATIVEL    = "CAMPO_COM_PRRENCHIMENTO_INCOMPATIVEL"   # typo é do SERPRO
DV_INVALIDO     = "CAMPO_COM_DV_INVALIDO"

_DOM_PATH = Path(__file__).with_name("dominios_cadurb.json")
DOMINIOS = json.loads(_DOM_PATH.read_text(encoding="utf-8")) if _DOM_PATH.exists() else {}

def _cods(secao: str) -> set:
    return set(DOMINIOS.get(secao, {}).get("codigos", {}))

TIPO_IMOVEL      = _cods("9.1")   # 01 territorial · 02 predial · 03 características especiais
TIPO_ARQUIT      = _cods("9.2")
BICE             = _cods("9.3")
DESTINACAO       = _cods("9.4")
PADRAO_CONSTR    = _cods("9.5")
TIPO_LOGRADOURO  = _cods("9.6")
TIPO_TITULARIDADE= _cods("9.7")
DOC_TITULARIDADE = _cods("9.8")
TIPO_TRANSACAO   = _cods("9.13")


class Falha:
    __slots__ = ("linha", "campo", "tipo", "detalhe", "impeditiva")
    def __init__(self, linha, campo, tipo, detalhe, impeditiva=True):
        self.linha, self.campo, self.tipo = linha, campo, tipo
        self.detalhe, self.impeditiva = detalhe, impeditiva
    def __repr__(self):
        marca = "IMPEDITIVA" if self.impeditiva else "atenção"
        return f"[{marca}] linha {self.linha} · {self.campo} · {self.tipo} · {self.detalhe}"
    def as_dict(self):
        return {"linha": self.linha, "campo": self.campo, "tipo": self.tipo,
                "detalhe": self.detalhe, "impeditiva": self.impeditiva}


# ---------------------------------------------------------------- utilitários
def _norm(s) -> str:
    s = "" if s is None else str(s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return " ".join(s.lower().split())

def _num(v):
    if v is None or str(v).strip() == "": return None
    t = str(v).strip().replace(".", "").replace(",", ".") if str(v).count(",") == 1 else str(v).strip()
    try: return float(t)
    except ValueError: return None

def _cod(v) -> str:
    """Normaliza código de domínio para o formato do manual (2 dígitos, zero à esquerda)."""
    if v is None: return ""
    t = str(v).strip()
    return t.zfill(2) if t.isdigit() and len(t) < 2 else t


def dv_cpf(cpf: str) -> bool:
    n = re.sub(r"\D", "", cpf or "")
    if len(n) != 11 or n == n[0] * 11: return False
    for pos in (9, 10):
        s = sum(int(n[i]) * ((pos + 1) - i) for i in range(pos))
        d = (s * 10) % 11 % 10
        if d != int(n[pos]): return False
    return True

def dv_cnpj(cnpj: str) -> bool:
    n = re.sub(r"\D", "", cnpj or "")
    if len(n) != 14 or n == n[0] * 14: return False
    for pos, pesos in ((12, [5,4,3,2,9,8,7,6,5,4,3,2]), (13, [6,5,4,3,2,9,8,7,6,5,4,3,2])):
        s = sum(int(n[i]) * pesos[i] for i in range(pos))
        d = 11 - (s % 11); d = 0 if d > 9 else d
        if d != int(n[pos]): return False
    return True

def dv_documento(doc: str) -> bool:
    n = re.sub(r"\D", "", doc or "")
    if len(n) == 11: return dv_cpf(n)
    if len(n) == 14: return dv_cnpj(n)
    return False

def cep_do_municipio(cep: str, faixas) -> bool:
    """faixas: lista de (inicio, fim) em int, obtida dos Correios/IBGE para o município."""
    n = re.sub(r"\D", "", cep or "")
    if len(n) != 8: return False
    v = int(n)
    return any(a <= v <= b for a, b in faixas)


# ---------------------------------------------------------------- regras por registro
def validar_registro(r: dict, linha: int, ctx: dict | None = None) -> list:
    """ctx aceita: {"faixas_cep": [(inicio,fim)], "ano_corrente": int}"""
    ctx = ctx or {}
    ano_corr = ctx.get("ano_corrente") or date.today().year
    f = []
    g = lambda k: r.get(k)

    # R1 — obrigatórios do schema (DadosGeraisImovel + EnderecoImovel)
    for campo in ("inscricaoImobiliaria", "tipoImovel", "areaTerreno", "temBairro"):
        if g(campo) in (None, ""):
            f.append(Falha(linha, campo, NAO_INFORMADO, "obrigatório no leiaute CADURB"))
    for campo in ("cep", "nomeLogradouro", "tipoLogradouro"):
        if g(campo) in (None, ""):
            f.append(Falha(linha, campo, NAO_INFORMADO, "obrigatório em EnderecoImovel"))

    # R2 — tamanhos declarados na spec
    for campo, lim in (("inscricaoImobiliaria", 45), ("nomeLogradouro", 150), ("bairro", 30),
                       ("numeroImovel", 8), ("complEndereco", 30), ("nomeTitular", 300)):
        v = g(campo)
        if v not in (None, "") and len(str(v)) > lim:
            f.append(Falha(linha, campo, TAMANHO_INVALIDO, f"{len(str(v))} caracteres; máximo {lim}"))

    # R3 — CEP: formato e pertinência ao município
    cep = re.sub(r"\D", "", str(g("cep") or ""))
    if cep and len(cep) != 8:
        f.append(Falha(linha, "cep", FORMATO_INVALIDO, "deve ter 8 dígitos"))
    elif cep and ctx.get("faixas_cep") and not cep_do_municipio(cep, ctx["faixas_cep"]):
        f.append(Falha(linha, "cep", VALOR_INVALIDO, "CEP fora da faixa do município"))

    # R4 — domínios (tabelas da seção 9 do manual; a spec declara só int32)
    for campo, dominio, sec in (("tipoImovel", TIPO_IMOVEL, "9.1"),
                                ("tpArquitetonico", TIPO_ARQUIT, "9.2"),
                                ("bice", BICE, "9.3"),
                                ("destinacaoImovel", DESTINACAO, "9.4"),
                                ("padraoConstrutivo", PADRAO_CONSTR, "9.5"),
                                ("tipoLogradouro", TIPO_LOGRADOURO, "9.6"),
                                ("tipoTitularidade", TIPO_TITULARIDADE, "9.7"),
                                ("docTitularidade", DOC_TITULARIDADE, "9.8"),
                                ("tpTransacaoITBI", TIPO_TRANSACAO, "9.13")):
        v = g(campo)
        if v not in (None, "") and dominio and _cod(v) not in dominio:
            f.append(Falha(linha, campo, VALOR_INVALIDO, f"valor '{v}' fora da tabela {sec} do manual"))

    # R5 — coerência tipoImovel × área/arquitetônico (regra explícita do manual)
    ti = _cod(g("tipoImovel"))
    area_c, area_t = _num(g("areaConstruida")), _num(g("areaTerreno"))
    if ti == "01":
        if area_c not in (None, 0):
            f.append(Falha(linha, "areaConstruida", INCOMPATIVEL,
                           "territorial (01) com área construída NÃO recebe CIB"))
        if g("tpArquitetonico") not in (None, ""):
            f.append(Falha(linha, "tpArquitetonico", INCOMPATIVEL,
                           "territorial (01) com tipo arquitetônico NÃO recebe CIB"))
    if ti == "02":
        if area_c in (None, 0):
            f.append(Falha(linha, "areaConstruida", NAO_INFORMADO, "obrigatório quando predial (02)"))
        if g("tpArquitetonico") in (None, ""):
            f.append(Falha(linha, "tpArquitetonico", NAO_INFORMADO, "obrigatório quando predial (02)"))

    # R6 — faixas numéricas
    if area_t is not None and area_t <= 0:
        f.append(Falha(linha, "areaTerreno", VALOR_INVALIDO, "deve ser maior que zero"))
    ac = _num(g("anoConstrutivo"))
    if ac is not None:
        if not (1900 <= ac <= 2100):
            f.append(Falha(linha, "anoConstrutivo", VALOR_INVALIDO, "fora da faixa 1900–2100 da spec"))
        elif ac > ano_corr:
            f.append(Falha(linha, "anoConstrutivo", VALOR_INVALIDO,
                           f"posterior ao ano corrente ({ano_corr})", impeditiva=False))

    # R7 — dígito verificador de documentos
    # `niTitular` é o nome do CPF/CNPJ do titular no TitularDTO da spec — e é para
    # ele que o validador mapeia a coluna do CSV. Sem ele nesta lista a R7 nunca
    # rodava sobre dado real: o laudo dizia "apto" sem ter conferido um só DV.
    for campo in ("niTitular", "docTitular", "cpfCnpjTitular",
                  "idTransmitenteITBI", "idAdquirenteITBI"):
        v = g(campo)
        if v not in (None, "") and not dv_documento(str(v)):
            f.append(Falha(linha, campo, DV_INVALIDO, "CPF/CNPJ com dígito verificador inválido"))

    # R8 — somas de percentual (cada campo é 0..1 na spec; a soma não é validada por ela)
    for campo, alvo in (("percTitularidade", "titularidade"), ("percTransacionadoITBI", "ITBI")):
        v = _num(g(campo))
        if v is not None and not (0 <= v <= 1):
            f.append(Falha(linha, campo, VALOR_INVALIDO, "deve estar entre 0 e 1"))
    return f


# ---------------------------------------------------------------- regras de base inteira
def validar_base(registros, codigo_ibge: str | None = None, ctx: dict | None = None) -> dict:
    falhas, por_inscricao = [], defaultdict(list)
    for i, r in enumerate(registros, start=1):
        falhas.extend(validar_registro(r, i, ctx))
        insc = str(r.get("inscricaoImobiliaria") or "").strip()
        if insc: por_inscricao[insc].append(i)

    # R9 — unicidade da inscrição imobiliária (o erro mais comum em cadastro de planilha)
    for insc, linhas in por_inscricao.items():
        if len(linhas) > 1:
            falhas.append(Falha(linhas[0], "inscricaoImobiliaria", VALOR_INVALIDO,
                                f"duplicada em {len(linhas)} registros (linhas {linhas[:6]})"))

    # R10 — somas de percentual por imóvel
    somas = defaultdict(float)
    for r in registros:
        insc = str(r.get("inscricaoImobiliaria") or "").strip()
        p = _num(r.get("percTitularidade"))
        if insc and p is not None: somas[insc] += p
    for insc, s in somas.items():
        if abs(s - 1.0) > 0.01:
            falhas.append(Falha(por_inscricao[insc][0], "percTitularidade", INCOMPATIVEL,
                                f"soma de titularidade do imóvel = {s:.3f}; esperado 1,000"))

    total = len(registros)
    impeditivas = [x for x in falhas if x.impeditiva]
    linhas_com_impeditiva = {x.linha for x in impeditivas}
    aptos = total - len(linhas_com_impeditiva)

    return {
        "codigo_ibge": codigo_ibge,
        "imoveis_analisados": total,
        "aptos_a_transmissao": aptos,
        "percentual_apto": round(aptos / total * 100, 1) if total else 0.0,
        "falhas": [x.as_dict() for x in falhas],
        "por_tipo": dict(Counter(x.tipo for x in falhas)),
        "por_campo": dict(Counter(x.campo for x in falhas).most_common()),
        "top_impeditivas": [c for c, _ in Counter(
            x.campo for x in impeditivas).most_common(10)],
        "cobertura_por_campo": _cobertura(registros),
    }


def _cobertura(registros) -> dict:
    """% de registros com cada campo preenchido — a métrica-título do laudo."""
    if not registros: return {}
    campos = set()
    for r in registros: campos.update(r.keys())
    tot = len(registros)
    return {c: round(sum(1 for r in registros if r.get(c) not in (None, "")) / tot * 100, 1)
            for c in sorted(campos)}


if __name__ == "__main__":
    exemplo = [
        {"inscricaoImobiliaria": "001", "tipoImovel": "1", "areaTerreno": "250",
         "temBairro": True, "cep": "64000000", "nomeLogradouro": "Rua A",
         "tipoLogradouro": "250", "areaConstruida": "120"},              # territorial com área
        {"inscricaoImobiliaria": "001", "tipoImovel": "02", "areaTerreno": "300",
         "temBairro": True, "cep": "6400", "nomeLogradouro": "Rua B",
         "tipoLogradouro": "999", "anoConstrutivo": "2035"},             # duplicada, CEP, domínio, ano
    ]
    import pprint
    r = validar_base(exemplo, codigo_ibge="2200400")
    print(f"analisados={r['imoveis_analisados']} aptos={r['aptos_a_transmissao']} "
          f"({r['percentual_apto']}%)\n")
    for x in r["falhas"]: print(" ", Falha(**x))
