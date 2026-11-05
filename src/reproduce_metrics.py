"""Reproduz as métricas operacionais e ordinais citadas na dissertação.

Uso (a partir da raiz do repositório):
    python src/reproduce_metrics.py
    python src/reproduce_metrics.py --csv output_resultados_LOTE_20260811_104318.csv

Regra de seleção (dissertação, seção 3.5.3 e Apêndice C): para cada combinação
cenário–estrategia–repetição vale o ÚLTIMO registro gravado; em empate no mesmo
segundo, vale a última linha do arquivo. Não depende de API nem de credenciais.
"""
import argparse

import pandas as pd

CHAVE = ["cenario", "estrategia", "repeticao"]
CRITERIOS = [
    "uso_evidencias", "identificacao_inconsistencias", "hipoteses_alternativas",
    "resistencia_interpretacao_induzida", "calibracao", "ausencia_alucinacoes",
    "coerencia_analitica",
]


def selecionar(df: pd.DataFrame, manter: str = "last") -> pd.DataFrame:
    """Ordena por horário preservando a ordem do arquivo (sort estável) e deduplica."""
    df = df.reset_index().sort_values(["data_hora", "index"], kind="stable")
    return df.drop_duplicates(CHAVE, keep=manter).drop(columns="index")


def resumo(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("estrategia").agg(
        respostas=("id", "size"),
        chamadas=("chamadas_totais", "sum"),
        tokens_entrada=("tokens_entrada", "sum"),
        tokens_saida=("tokens_saida", "sum"),
        tokens_totais=("tokens_totais", "sum"),
        latencia_media_s=("latencia_segundos", "mean"),
    )
    g["razao_tokens_P0"] = g.tokens_totais / g.tokens_totais["P0"]
    g["aumento_tokens_%"] = (g.razao_tokens_P0 - 1) * 100
    g["razao_latencia_P0"] = g.latencia_media_s / g.latencia_media_s["P0"]
    return g


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="output_resultados_LOTE_20260811_104318.csv")
    ap.add_argument("--ordinal", default="codificacao_ordinal_LOTE_20260811_104318.csv")
    a = ap.parse_args()

    bruto = pd.read_csv(a.csv)
    final = selecionar(bruto, "last")
    primeiro = selecionar(bruto, "first")

    print(f"Linhas no CSV: {len(bruto)} | IDs únicos: {bruto.id.nunique()}")
    print(f"Unidades finais: {len(final)} | substituídas: {len(bruto) - len(final)}")
    print(f"Chamadas (finais): {int(final.chamadas_totais.sum())} | "
          f"tokens totais: {int(final.tokens_totais.sum()):,}".replace(",", "."))
    print(f"Intervalo: {final.data_hora.min()} a {final.data_hora.max()}")
    sem_inter = final[final.estrategia.isin(["P3", "P4", "P7"])].respostas_intermediarias.isna().sum()
    print(f"P3/P4/P7 sem resposta intermediária: {sem_inter}\n")

    pd.set_option("display.width", 200)
    print("== Tabelas 13-16 (regra: último registro) ==")
    print(resumo(final).round(3).to_string(), "\n")

    print("== Tabela 37 (razão de tokens: último x primeiro registro) ==")
    r = pd.DataFrame({
        "ultimo": resumo(final).razao_tokens_P0,
        "primeiro": resumo(primeiro).razao_tokens_P0,
    }).round(2)
    print(r.drop(index="P0").to_string(), "\n")

    try:
        o = pd.read_csv(a.ordinal)
    except FileNotFoundError:
        return
    assert (o[CRITERIOS].sum(axis=1) == o["total"]).all(), "total != soma dos critérios"
    ids_ok = o.id.isin(final.id).all()
    print(f"== Codificação ordinal (n={len(o)}; IDs presentes na matriz final: {ids_ok}) ==")
    print(o.groupby("estrategia").total.mean().round(2).to_string())
    print("S0:", o[o.cenario == "S0"].groupby("estrategia").total.mean().round(2).to_dict())


if __name__ == "__main__":
    main()
