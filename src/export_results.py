import os
import json
import sqlite3
import pandas as pd
import argparse

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "storage")
DB_PATH = os.path.join(DB_DIR, "experimentos.db")
ULTIMO_LOTE_PATH = os.path.join(DB_DIR, "ultimo_lote.txt")
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def obter_ultimo_lote_ativo() -> str:
    if os.path.exists(ULTIMO_LOTE_PATH):
        with open(ULTIMO_LOTE_PATH, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return "LOTE_PADRAO"

def exportar_dados(lote_selecionado=None):
    print("=" * 60)
    print("Exportador de Resultados de Testes do TCC (Versionamento por Lote)")
    print("=" * 60)
    
    if not os.path.exists(DB_PATH):
        print(f"Erro: O banco de dados em {DB_PATH} não foi encontrado.")
        return
        
    lote = lote_selecionado or obter_ultimo_lote_ativo()
    print(f"Lote Selecionado para Exportação: {lote}")
    
    conn = sqlite3.connect(DB_PATH)
    
    # 1. Carregar execuções filtrando pelo lote correspondente
    query = "SELECT * FROM execucoes WHERE lote = ?"
    df = pd.read_sql_query(query, conn, params=(lote,))
    
    if df.empty:
        print(f"Aviso: Não há registros para o lote '{lote}' no banco de dados.")
        conn.close()
        return
        
    # Definir caminhos de arquivos versionados com o ID do Lote
    csv_filename = f"output_resultados_{lote}.csv"
    markdown_filename = f"resumo_experimento_{lote}.md"
    
    csv_path = os.path.join(ROOT_DIR, csv_filename)
    report_path = os.path.join(ROOT_DIR, markdown_filename)
    
    # Salvar resultados brutos em CSV
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"Dados brutos do lote exportados para: {csv_path}")
    
    # 2. Gerar estatísticas para o relatório Markdown
    print("Gerando estatísticas para o relatório de resumo...")
    
    # Latência média por estratégia
    df_latencia = df.groupby("estrategia")["latencia_segundos"].mean().reset_index()
    df_latencia.columns = ["Estratégia", "Latência Média (s)"]
    
    # Total de tokens por estratégia
    df_tokens = df.groupby("estrategia").agg({
        "tokens_entrada": "sum",
        "tokens_saida": "sum",
        "tokens_totais": "sum",
        "chamadas_totais": "sum"
    }).reset_index()
    df_tokens.columns = ["Estratégia", "Soma Tokens Entrada", "Soma Tokens Saída", "Soma Tokens Totais", "Total Chamadas"]
    
    # Preview de uma resposta por estratégia (cenário S0, repetição 1)
    df_preview = df[(df["cenario"] == "S0") & (df["repeticao"] == 1)]
    
    # 3. Montar o relatório Markdown
    markdown_content = []
    markdown_content.append(f"# Relatório Resumido do Experimento do TCC ({lote})")
    markdown_content.append(f"Gerado em: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    markdown_content.append("Este relatório compila os dados agregados das simulações de engenharia de prompt e mitigação de vieses cognitivos no setor de serviços públicos concedidos na RMSP.\n")
    
    markdown_content.append("## 1. Desempenho e Latência por Estratégia")
    markdown_content.append("Tempo médio de execução (latência) medido para cada técnica de prompting:")
    markdown_content.append(df_latencia.to_markdown(index=False))
    markdown_content.append("")
    
    markdown_content.append("## 2. Consumo de Tokens e Custos por Estratégia")
    markdown_content.append("Volume total de tokens e chamadas de API acumulados por estratégia (todas as repetições e cenários do lote):")
    markdown_content.append(df_tokens.to_markdown(index=False))
    markdown_content.append("")
    
    markdown_content.append("## 3. Amostra de Resposta Gerada (Cenário S0 - Controle RMSP)")
    markdown_content.append("Comparação do texto gerado por cada uma das estratégias testadas para o Cenário de Controle (S0 - Saneamento):\n")
    
    for _, row in df_preview.iterrows():
        markdown_content.append(f"### Estratégia: {row['estrategia']}")
        markdown_content.append(f"**Chamadas na API**: {row['chamadas_totais']} | **Tokens Totais**: {row['tokens_totais']} | **Latência**: {row['latencia_segundos']:.2f}s")
        markdown_content.append("\n**Resposta do Modelo**:")
        markdown_content.append(f"```text\n{row['resposta_modelo']}\n```")
        
        if row['respostas_intermediarias']:
            markdown_content.append("\n**Respostas Intermediárias (Processo Cognitivo)**:")
            try:
                intermediarias = json.loads(row['respostas_intermediarias'])
                for key, val in intermediarias.items():
                    markdown_content.append(f"- *{key.upper()}*:")
                    markdown_content.append(f"```text\n{val}\n```")
            except Exception:
                markdown_content.append(f"```json\n{row['respostas_intermediarias']}\n```")
        markdown_content.append("\n" + "-"*40 + "\n")
        
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(markdown_content))
        
    print(f"Relatório Markdown detalhado gerado com sucesso em: {report_path}")
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exportador de resultados por lote.")
    parser.add_argument("--lote", type=str, default=None, help="Especifica um ID de lote de execução para exportar.")
    args = parser.parse_args()
    exportar_dados(lote_selecionado=args.lote)

