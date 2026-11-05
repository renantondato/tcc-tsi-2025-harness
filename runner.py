import os, json, time, uuid, argparse
from src.database import (
    inicializar_banco, salvar_execucao, 
    checar_execucao_existente, limpar_execucoes_modelo,
    limpar_execucoes_cenario, obter_ou_criar_lote
)
import src.strategies as strats

DATASET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")

def carregar_cenario(id_cenario):
    caminho = os.path.join(DATASET_DIR, f"{id_cenario}.json")
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)

def executar_com_resiliencia(func, contexto, pergunta, model, max_tentativas=5):
    tentativa, espera_base = 0, 15.0
    while tentativa < max_tentativas:
        try:
            return func(contexto, pergunta, model=model)
        except Exception as e:
            msg = str(e)
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                tentativa += 1
                tempo = espera_base * (2 ** (tentativa - 1))
                print(f" -> [429 Quota] Tentativa {tentativa}/{max_tentativas}. Aguardando {tempo:.1f}s...")
                time.sleep(tempo)
            else:
                raise e
    raise Exception(f"Máximo de tentativas ({max_tentativas}) excedido.")

def executar_experimento(model="gemini-3.6-flash", full_reset=False, cenario_especifico=None):
    print("=" * 60)
    print("Iniciando Harness de Testes do TCC...")
    print("=" * 60)
    inicializar_banco()
    
    lote_id = obter_ou_criar_lote(novo_lote=full_reset)
    print(f"LOTE ATIVO: {lote_id}")
    
    todos_cenarios = ["S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7"]
    if cenario_especifico:
        if cenario_especifico not in todos_cenarios:
            print(f"Erro: Cenário '{cenario_especifico}' inválido.")
            return
        cenarios = [cenario_especifico]
        print(f"Apenas o cenário '{cenario_especifico}'...")
    else:
        cenarios = todos_cenarios
    
    if full_reset:
        if cenario_especifico:
            print(f"Limpando cenário '{cenario_especifico}' no {lote_id}...")
            limpar_execucoes_cenario(model, cenario_especifico, lote_id)
        else:
            print(f"Limpando lote {lote_id}...")
            limpar_execucoes_modelo(model, lote_id)
    
    estrategias = ["P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7"]
    repeticoes = [1, 2, 3]
    mapa_estrategias = {
        "P0": strats.executar_P0, "P1": strats.executar_P1,
        "P2": strats.executar_P2, "P3": strats.executar_P3,
        "P4": strats.executar_P4, "P5": strats.executar_P5,
        "P6": strats.executar_P6, "P7": strats.executar_P7
    }
    
    total_execs = len(cenarios) * len(estrategias) * len(repeticoes)
    exec_atual, delay = 0, 0.1  
    
    for c_id in cenarios:
        try:
            dados = carregar_cenario(c_id)
            contexto, pergunta = dados["contexto"], dados["pergunta"]
        except Exception as e:
            print(f"Erro ao carregar cenário {c_id}: {e}")
            continue
            
        for est_id in estrategias:
            func_est = mapa_estrategias[est_id]
            for rep in repeticoes:
                exec_atual += 1
                
                if not full_reset and checar_execucao_existente(c_id, est_id, rep, model, lote_id):
                    print(f"[{exec_atual}/{total_execs}] Cache: Cenário {c_id} | {est_id} | Repetição {rep} já executada. Pulando...")
                    continue
                
                print(f"[{exec_atual}/{total_execs}] Executando: Cenário {c_id} | Estratégia {est_id} | Repetição {rep}...")
                id_execucao = str(uuid.uuid4())
                tempo_inicio = time.perf_counter()
                
                try:
                    resultado = executar_com_resiliencia(func_est, contexto, pergunta, model=model)
                    latencia = time.perf_counter() - tempo_inicio
                    
                    salvar_execucao(
                        id_execucao=id_execucao, lote=lote_id, cenario=c_id, estrategia=est_id,
                        repeticao=rep, modelo=model, versao_api="google-genai v1",
                        prompt_enviado=resultado["prompt_enviado"],
                        resposta_modelo=resultado["resposta_final"],
                        respostas_intermediarias=resultado["respostas_intermediarias"],
                        chamadas_totais=resultado["chamadas_totais"],
                        tokens_entrada=resultado["tokens_entrada"],
                        tokens_saida=resultado["tokens_saida"],
                        tokens_totais=resultado["tokens_totais"],
                        latencia_segundos=latencia
                    )
                    print(f" -> Sucesso! Latência: {latencia:.2f}s | Tokens: {resultado['tokens_totais']}")
                    time.sleep(delay)
                except Exception as e:
                    print(f" -> Erro crítico: {e}")
                    if "API_KEY" in str(e) or "API key" in str(e) or "not found" in str(e).lower():
                        return

    print("=" * 60)
    print("Experimento concluído com sucesso!")
    print(f"Todos os dados foram consolidados no lote: {lote_id}")
    print("=" * 60)
    
    try:
        print("Disparando exportador de resultados automático para o lote atual...")
        from src.export_results import exportar_dados
        exportar_dados(lote_selecionado=lote_id)
    except Exception as exc:
        print(f"Erro ao exportar resultados automaticamente: {exc}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Harness de testes de Engenharia de Prompt do TCC.")
    parser.add_argument("--full", action="store_true", help="Gera um novo lote com timestamp e força reexecução completa.")
    parser.add_argument("--scenario", type=str, default=None, help="Especifica um cenário único para rodar (S0 a S7).")
    args = parser.parse_args()
    executar_experimento(full_reset=args.full, cenario_especifico=args.scenario)




