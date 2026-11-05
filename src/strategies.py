import os
import json
from src.llm_client import gerar_resposta

PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prompts")

def carregar_prompt(nome_arquivo):
    caminho = os.path.join(PROMPTS_DIR, nome_arquivo)
    with open(caminho, 'r', encoding='utf-8') as f:
        return f.read()

def executar_P0(contexto, pergunta, model="gemini-3.6-flash"):
    template = carregar_prompt("P0_simples.txt")
    prompt_final = template.format(contexto=contexto, pergunta=pergunta)
    resposta_texto, t_in, t_out, t_tot = gerar_resposta(prompt_final, model=model)
    return {
        "resposta_final": resposta_texto,
        "respostas_intermediarias": None,
        "prompt_enviado": prompt_final,
        "chamadas_totais": 1,
        "tokens_entrada": t_in,
        "tokens_saida": t_out,
        "tokens_totais": t_tot
    }

def executar_P1(contexto, pergunta, model="gemini-3.6-flash"):
    template = carregar_prompt("P1_estruturado.txt")
    prompt_final = template.format(contexto=contexto, pergunta=pergunta)
    resposta_texto, t_in, t_out, t_tot = gerar_resposta(prompt_final, model=model)
    return {
        "resposta_final": resposta_texto,
        "respostas_intermediarias": None,
        "prompt_enviado": prompt_final,
        "chamadas_totais": 1,
        "tokens_entrada": t_in,
        "tokens_saida": t_out,
        "tokens_totais": t_tot
    }

def executar_P2(contexto, pergunta, model="gemini-3.6-flash"):
    template = carregar_prompt("P2_analitico.txt")
    prompt_final = template.format(contexto=contexto, pergunta=pergunta)
    resposta_texto, t_in, t_out, t_tot = gerar_resposta(prompt_final, model=model)
    return {
        "resposta_final": resposta_texto,
        "respostas_intermediarias": None,
        "prompt_enviado": prompt_final,
        "chamadas_totais": 1,
        "tokens_entrada": t_in,
        "tokens_saida": t_out,
        "tokens_totais": t_tot
    }


from concurrent.futures import ThreadPoolExecutor

def executar_P3(contexto, pergunta, model="gemini-3.6-flash"):
    template_p2 = carregar_prompt("P2_analitico.txt")
    prompt_p2 = template_p2.format(contexto=contexto, pergunta=pergunta)
    
    # Executar as 3 chamadas em paralelo usando ThreadPoolExecutor
    # Isso otimiza o uso do Vertex AI reduzindo o tempo de espera sequencial.
    def fazer_chamada_p3(_):
        return gerar_resposta(prompt_p2, model=model, temperature=0.3)
        
    with ThreadPoolExecutor(max_workers=3) as executor:
        resultados_paralelos = list(executor.map(fazer_chamada_p3, range(3)))
        
    respostas_intermediarias = [r[0] for r in resultados_paralelos]
    tot_in = sum(r[1] for r in resultados_paralelos)
    tot_out = sum(r[2] for r in resultados_paralelos)
    tot_tot = sum(r[3] for r in resultados_paralelos)
        
    template_sintese = carregar_prompt("P3_sintese.txt")
    prompt_sintese = template_sintese.format(
        analise_1=respostas_intermediarias[0],
        analise_2=respostas_intermediarias[1],
        analise_3=respostas_intermediarias[2]
    )
    
    resposta_final, t_in_f, t_out_f, t_tot_f = gerar_resposta(prompt_sintese, model=model, temperature=0.0)
    tot_in += t_in_f
    tot_out += t_out_f
    tot_tot += t_tot_f
    
    intermediarias_json = json.dumps({
        "analise_1": respostas_intermediarias[0],
        "analise_2": respostas_intermediarias[1],
        "analise_3": respostas_intermediarias[2]
    }, ensure_ascii=False)
    
    return {
        "resposta_final": resposta_final,
        "respostas_intermediarias": intermediarias_json,
        "prompt_enviado": prompt_sintese,
        "chamadas_totais": 4,
        "tokens_entrada": tot_in,
        "tokens_saida": tot_out,
        "tokens_totais": tot_tot
    }

def executar_P4(contexto, pergunta, model="gemini-3.6-flash"):
    template_p2 = carregar_prompt("P2_analitico.txt")
    prompt_inicial = template_p2.format(contexto=contexto, pergunta=pergunta)
    resp_inicial, t_in_1, t_out_1, t_tot_1 = gerar_resposta(prompt_inicial, model=model, temperature=0.0)
    
    template_critica = carregar_prompt("P4_critica.txt")
    prompt_critica = template_critica.format(resposta_inicial=resp_inicial)
    critica, t_in_2, t_out_2, t_tot_2 = gerar_resposta(prompt_critica, model=model, temperature=0.0)
    
    prompt_revisao = (
        "Com base na análise original e na crítica estruturada abaixo, "
        "elabore uma resposta final revisada e corrigida, mitigando todos os vieses apontados.\n\n"
        f"Análise Original:\n{resp_inicial}\n\n"
        f"Crítica:\n{critica}\n\n"
        "Resposta Final Corrigida:"
    )
    resposta_final, t_in_3, t_out_3, t_tot_3 = gerar_resposta(prompt_revisao, model=model, temperature=0.0)
    
    tot_in = t_in_1 + t_in_2 + t_in_3
    tot_out = t_out_1 + t_out_2 + t_out_3
    tot_tot = t_tot_1 + t_tot_2 + t_tot_3
    
    intermediarias_json = json.dumps({
        "resposta_inicial": resp_inicial,
        "critica": critica
    }, ensure_ascii=False)
    
    return {
        "resposta_final": resposta_final,
        "respostas_intermediarias": intermediarias_json,
        "prompt_enviado": prompt_inicial,
        "chamadas_totais": 3,
        "tokens_entrada": tot_in,
        "tokens_saida": tot_out,
        "tokens_totais": tot_tot
    }

def executar_P5(contexto, pergunta, model="gemini-3.6-flash"):
    template = carregar_prompt("P5.txt")
    prompt_final = template.format(contexto=contexto, pergunta=pergunta)
    resposta_texto, t_in, t_out, t_tot = gerar_resposta(prompt_final, model=model, temperature=0.0)
    return {
        "resposta_final": resposta_texto,
        "respostas_intermediarias": None,
        "prompt_enviado": prompt_final,
        "chamadas_totais": 1,
        "tokens_entrada": t_in,
        "tokens_saida": t_out,
        "tokens_totais": t_tot
    }

def executar_P6(contexto, pergunta, model="gemini-3.6-flash"):
    template = carregar_prompt("P6.txt")
    prompt_final = template.format(contexto=contexto, pergunta=pergunta)
    resposta_texto, t_in, t_out, t_tot = gerar_resposta(prompt_final, model=model, temperature=0.0)
    return {
        "resposta_final": resposta_texto,
        "respostas_intermediarias": None,
        "prompt_enviado": prompt_final,
        "chamadas_totais": 1,
        "tokens_entrada": t_in,
        "tokens_saida": t_out,
        "tokens_totais": t_tot
    }

def executar_P7(contexto, pergunta, model="gemini-3.6-flash"):
    # Chamada 1: Isola variáveis latentes (temperature = 0.2)
    template_analise = carregar_prompt("P7_analise_intermediaria.txt")
    prompt_analise = template_analise.format(contexto=contexto, pergunta=pergunta)
    analise_intermediaria, t_in_1, t_out_1, t_tot_1 = gerar_resposta(prompt_analise, model=model, temperature=0.2)
    
    # Chamada 2: Consolida o relatório final usando o template do P7 (temperature = 0.0)
    template_p7 = carregar_prompt("P7.txt")
    prompt_final = template_p7.format(
        contexto=contexto,
        pergunta=pergunta,
        analise_intermediaria=analise_intermediaria
    )
    resposta_final, t_in_2, t_out_2, t_tot_2 = gerar_resposta(prompt_final, model=model, temperature=0.0)
    
    tot_in = t_in_1 + t_in_2
    tot_out = t_out_1 + t_out_2
    tot_tot = t_tot_1 + t_tot_2
    
    intermediarias_json = json.dumps({
        "analise_intermediaria_latente": analise_intermediaria
    }, ensure_ascii=False)
    
    return {
        "resposta_final": resposta_final,
        "respostas_intermediarias": intermediarias_json,
        "prompt_enviado": prompt_final,
        "chamadas_totais": 2,
        "tokens_entrada": tot_in,
        "tokens_saida": tot_out,
        "tokens_totais": tot_tot
    }


