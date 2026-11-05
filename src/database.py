import os
import sqlite3
import uuid
from datetime import datetime

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "storage")
DB_PATH = os.path.join(DB_DIR, "experimentos.db")
ULTIMO_LOTE_PATH = os.path.join(DB_DIR, "ultimo_lote.txt")

def obter_ou_criar_lote(novo_lote=False) -> str:
    """Retorna o lote atual ou gera um novo lote com timestamp."""
    os.makedirs(DB_DIR, exist_ok=True)
    if novo_lote or not os.path.exists(ULTIMO_LOTE_PATH):
        lote_id = f"LOTE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        with open(ULTIMO_LOTE_PATH, 'w', encoding='utf-8') as f:
            f.write(lote_id)
        return lote_id
    with open(ULTIMO_LOTE_PATH, 'r', encoding='utf-8') as f:
        return f.read().strip()

def inicializar_banco():
    """Cria o diretório storage e inicializa as tabelas do banco de dados SQLite."""
    os.makedirs(DB_DIR, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Criar tabela execucoes incluindo a coluna lote
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS execucoes (
        id TEXT PRIMARY KEY,
        lote TEXT NOT NULL,
        cenario TEXT NOT NULL,
        estrategia TEXT NOT NULL,
        repeticao INTEGER NOT NULL,
        modelo TEXT NOT NULL,
        versao_api TEXT NOT NULL,
        prompt_enviado TEXT NOT NULL,
        resposta_modelo TEXT NOT NULL,
        respostas_intermediarias TEXT, -- JSON formatado
        chamadas_totais INTEGER NOT NULL,
        tokens_entrada INTEGER NOT NULL,
        tokens_saida INTEGER NOT NULL,
        tokens_totais INTEGER NOT NULL,
        latencia_segundos REAL NOT NULL,
        data_hora TEXT NOT NULL
    );
    """)
    
    # Tentar adicionar a coluna lote de forma incremental caso o banco já existisse sem ela
    try:
        cursor.execute("ALTER TABLE execucoes ADD COLUMN lote TEXT DEFAULT 'LOTE_PADRAO';")
    except sqlite3.OperationalError:
        pass # Coluna já existe
        
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS avaliacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        execucao_id TEXT NOT NULL,
        uso_evidencias INTEGER NOT NULL CHECK (uso_evidencias IN (0, 1, 2)),
        identificacao_inconsistencias INTEGER NOT NULL CHECK (identificacao_inconsistencias IN (0, 1, 2)),
        hipoteses_alternativas INTEGER NOT NULL CHECK (hipoteses_alternativas IN (0, 1, 2)),
        resistencia_inducao INTEGER NOT NULL CHECK (resistencia_inducao IN (0, 1, 2)),
        calibracao INTEGER NOT NULL CHECK (calibracao IN (0, 1, 2)),
        ausencia_alucinacoes INTEGER NOT NULL CHECK (ausencia_alucinacoes IN (0, 1, 2)),
        coerencia_analitica INTEGER NOT NULL CHECK (coerencia_analitica IN (0, 1, 2)),
        observacoes_pesquisador TEXT,
        FOREIGN KEY (execucao_id) REFERENCES execucoes(id) ON DELETE CASCADE
    );
    """)
    
    conn.commit()
    conn.close()

def salvar_execucao(
    id_execucao,
    lote,
    cenario,
    estrategia,
    repeticao,
    modelo,
    versao_api,
    prompt_enviado,
    resposta_modelo,
    respostas_intermediarias,
    chamadas_totais,
    tokens_entrada,
    tokens_saida,
    tokens_totais,
    latencia_segundos
):
    """Insere um novo registro de execução no banco de dados."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    data_hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
    INSERT INTO execucoes (
        id, lote, cenario, estrategia, repeticao, modelo, versao_api,
        prompt_enviado, resposta_modelo, respostas_intermediarias,
        chamadas_totais, tokens_entrada, tokens_saida, tokens_totais,
        latencia_segundos, data_hora
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        id_execucao, lote, cenario, estrategia, repeticao, modelo, versao_api,
        prompt_enviado, resposta_modelo, respostas_intermediarias,
        chamadas_totais, tokens_entrada, tokens_saida, tokens_totais,
        latencia_segundos, data_hora_atual
    ))
    
    conn.commit()
    conn.close()

def checar_execucao_existente(cenario, estrategia, repeticao, modelo, lote) -> bool:
    """Verifica se já existe uma execução gravada com os mesmos parâmetros chave para o lote."""
    if not os.path.exists(DB_PATH):
        return False
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(1) FROM execucoes 
        WHERE cenario = ? AND estrategia = ? AND repeticao = ? AND modelo = ? AND lote = ?;
    """, (cenario, estrategia, repeticao, modelo, lote))
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado > 0

def limpar_execucoes_modelo(modelo, lote):
    """Remove registros de execuções do modelo e lote especificados."""
    if not os.path.exists(DB_PATH):
        return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM execucoes WHERE modelo = ? AND lote = ?;", (modelo, lote))
    conn.commit()
    conn.close()

def limpar_execucoes_cenario(modelo, cenario, lote):
    """Remove registros de execuções do cenário, modelo e lote especificados."""
    if not os.path.exists(DB_PATH):
        return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM execucoes WHERE modelo = ? AND cenario = ? AND lote = ?;", (modelo, cenario, lote))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    inicializar_banco()
    print(f"Banco de dados inicializado com sucesso em: {DB_PATH}")

