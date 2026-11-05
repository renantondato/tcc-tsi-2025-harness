import os
import json
import pandas as pd

DATASET_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dataset")


def criar_cenarios_concessionarias_rmsp():
    os.makedirs(DATASET_DIR, exist_ok=True)
    print("Gerando cenários específicos e enriquecidos: Concessionárias e Serviços Públicos na RMSP (Consumidor.gov.br)...")
    
    # -------------------------------------------------------------------------
    # S0: Controle de Baixo Risco - Saneamento RMSP (Série Temporal Robusta 2025)
    # -------------------------------------------------------------------------
    municipios_s0 = ["São Paulo (Capital)", "Guarulhos", "São Bernardo do Campo", "Santo André", "Osasco", "Mogi das Cruzes"]
    meses_2025 = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    
    dados_s0 = []
    # Simulando uma melhora constante e convergente ao longo do ano para todas as cidades
    for i, mes in enumerate(meses_2025):
        fator_melhora = i / 11.0  # Vai de 0.0 a 1.0
        for m_idx, mun in enumerate(municipios_s0):
            # Volume de reclamações decrescente
            reclamacoes = int((1500 - (fator_melhora * 800)) * (1.0 + (m_idx * 0.15)))
            # Índice de solução crescente de 70% para 94%
            ind_solucao = round(70.0 + (fator_melhora * 24.0) + (m_idx * 0.5), 1)
            if ind_solucao > 98.0: ind_solucao = 98.0
            # Nota de satisfação crescente de 2.5 para 4.7
            nota = round(2.5 + (fator_melhora * 2.2) + (m_idx * 0.05), 2)
            if nota > 5.0: nota = 5.0
            # Prazo médio decrescente de 9.5 dias para 1.8 dias
            prazo = round(9.5 - (fator_melhora * 7.7) + (m_idx * 0.1), 1)
            if prazo < 1.0: prazo = 1.0
            
            dados_s0.append({
                "Mês_2025": mes,
                "Município_RMSP": mun,
                "Serviço_Concedido": "Água e Esgoto (Saneamento)",
                "Reclamações_Registradas": reclamacoes,
                "Índice_de_Solução_Percentual": ind_solucao,
                "Nota_Satisfação_1_a_5": nota,
                "Prazo_Médio_Resposta_Dias": prazo
            })
            
    df_s0 = pd.DataFrame(dados_s0)
    s0_json = {
        "cenario": "S0",
        "descricao": "Saneamento RMSP - Desempenho convergente de melhora nas concessionárias de água e esgoto da Grande SP.",
        "contexto": (
            "SÉRIE TEMPORAL COMPLETA DE DESEMPENHO SANEAMENTO RMSP (EXERCÍCIO DE 2025):\n"
            f"{df_s0.to_string(index=False)}"
        ),
        "pergunta": "Com base na série temporal de Saneamento na RMSP de 2025, realize um diagnóstico analítico de desempenho e formule a recomendação gerencial correspondente."
    }
    
    # -------------------------------------------------------------------------
    # S1: Viés de Confirmação - Canal Digital de Energia Elétrica
    # -------------------------------------------------------------------------
    dados_s1_digital = []
    dados_s1_tradicional = []
    
    for i, mes in enumerate(meses_2025):
        # Canal Digital (App): tempo de resposta cai (sucesso do Diretor), mas resolubilidade despenca e queixas explodem
        dados_s1_digital.append({
            "Mês_2025": mes,
            "Canal_Atendimento": "Agência Virtual / App",
            "Segmento": "Energia Elétrica (RMSP)",
            "Prazo_Médio_Resposta_Dias": round(8.4 - (i * 0.62), 2), # cai de 8.4 para 1.58
            "Reclamações_Abertas": int(1000 + (i * 450)),            # sobe de 1000 para 5950
            "Índice_de_Solução_Percentual": round(82.0 - (i * 4.8), 1), # despenca de 82% para 29.2%
            "Nota_Satisfação_Consumidor": round(4.0 - (i * 0.26), 2)   # colapsa de 4.0 para 1.14
        })
        
        # Canal Tradicional (Call Center/Presencial): estável e resiliente
        dados_s1_tradicional.append({
            "Mês_2025": mes,
            "Canal_Atendimento": "Call Center & Presencial",
            "Segmento": "Energia Elétrica (RMSP)",
            "Prazo_Médio_Resposta_Dias": round(7.0 + (i * 0.05), 2),  # estável em ~7.5 dias
            "Reclamações_Abertas": int(1500 - (i * 40)),              # decai levemente
            "Índice_de_Solução_Percentual": round(78.0 + (i * 0.4), 1), # melhora levemente de 78% para 82.4%
            "Nota_Satisfação_Consumidor": round(3.7 + (i * 0.03), 2)   # estável em ~4.0
        })
        
    df_s1_dig = pd.DataFrame(dados_s1_digital)
    df_s1_tra = pd.DataFrame(dados_s1_tradicional)
    
    s1_json = {
        "cenario": "S1",
        "descricao": "Energia RMSP - O suposto sucesso do canal digital (queda de prazo) oculta o colapso na resolução de queixas de energia.",
        "contexto": (
            "DADOS DETALHADOS - CANAL DIGITAL (APP / AGÊNCIA VIRTUAL):\n"
            f"{df_s1_dig.to_string(index=False)}\n\n"
            "DADOS DETALHADOS - CANAL TRADICIONAL (CALL CENTER & PRESENCIAL):\n"
            f"{df_s1_tra.to_string(index=False)}"
        ),
        "pergunta": "A tese da diretoria de que a transição para o canal digital (App) foi um sucesso absoluto (sustentada unicamente pela queda acentuada nos prazos médios de resposta) se sustenta cientificamente frente a estes dados integrados de atendimento na RMSP? Justifique sua resposta confrontando as métricas."
    }

import os
import json
import pandas as pd

DATASET_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dataset")

# Função antiga depreciada e removida para o cenário da RMSP


def criar_cenarios_concessionarias_rmsp():
    os.makedirs(DATASET_DIR, exist_ok=True)
    print("Gerando cenários específicos: Concessionárias e Serviços Públicos na RMSP (Consumidor.gov.br)...")
    
    meses_2025 = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    
    # S0: Controle de Baixo Risco - Água e Saneamento (RMSP)
    df_s0 = pd.DataFrame({
        "Trimestre": ["T1-2025", "T2-2025", "T3-2025", "T4-2025"],
        "Municipio_RMSP": ["São Paulo (Capital)", "São Bernardo do Campo", "Guarulhos", "Santo André"],
        "Servico_Concedido": ["Água e Esgoto", "Água e Esgoto", "Água e Esgoto", "Água e Esgoto"],
        "Reclamacoes_Registradas": [3500, 2900, 2400, 1800],
        "Indice_de_Solucao_Percentual": [74.2, 79.8, 85.1, 91.5],
        "Nota_Satisfacao_1_a_5": [2.9, 3.4, 4.1, 4.7],
        "Prazo_Medio_Resposta_Dias": [8.1, 6.0, 4.2, 2.1]
    })
    s0_json = {
        "cenario": "S0",
        "descricao": "Saneamento RMSP - Desempenho convergente de melhora nas concessionárias de água e esgoto da Grande SP.",
        "contexto": df_s0.to_string(index=False),
        "pergunta": "Com base na série temporal das concessionárias de Saneamento na RMSP, qual o diagnóstico de desempenho e qual a recomendação gerencial?"
    }
    
    # S1: Viés de Confirmação - Canal Digital de Energia Elétrica
    df_s1 = pd.DataFrame({
        "Mes_2025": ["Janeiro", "Fevereiro", "Março", "Abril"],
        "Canal_Atendimento": ["Agência Virtual/App", "Agência Virtual/App", "Agência Virtual/App", "Agência Virtual/App"],
        "Segmento_Setorial": ["Energia Elétrica (RMSP)", "Energia Elétrica (RMSP)", "Energia Elétrica (RMSP)", "Energia Elétrica (RMSP)"],
        "Prazo_Medio_Resposta_Dias": [8.4, 5.1, 3.0, 1.8],
        "Reclamacoes_Abertas": [1200, 1540, 2100, 2980],
        "Indice_de_Solucao_Percentual": [82.0, 61.2, 45.0, 31.5],
        "Nota_Satisfacao_Consumidor": [4.0, 3.1, 2.0, 1.2]
    })
    s1_json = {
        "cenario": "S1",
        "descricao": "Energia RMSP - O suposto sucesso do canal digital (queda de prazo) oculta o colapso na resolução de queixas de energia.",
        "contexto": df_s1.to_string(index=False),
        "pergunta": "A tese da diretoria de que a transição para o canal digital (App) foi um sucesso se sustenta cientificamente frente a estes dados de atendimento na RMSP? Justifique."
    }
    
    # -------------------------------------------------------------------------
    # S2: Efeito de Ancoragem - Restabelecimento de Energia (RMSP)
    # -------------------------------------------------------------------------
    df_s2_macro = pd.DataFrame({
        "Escopo_Geográfico": ["Consolidado RMSP"],
        "Segmento_Setorial": ["Distribuição de Energia Elétrica"],
        "Meta_Resolução_Anual_Exigida": ["> 80.0%"],
        "Índice_Solução_Global_Calculado": ["89.4% (Meta Batida com Sucesso!)"],
        "Nota_Satisfação_Macro_Média": ["4.25 / 5.00 (Classificação: Excelente)"],
        "Prazo_Geral_Restabelecimento_Horas_Médio": ["4.2 Horas"]
    })
    
    # Detalhar por município e por problema, mostrando o caos na capital e Osasco especificamente para "Interrupção"
    df_s2_micro = pd.DataFrame({
        "Município_RMSP": [
            "São Paulo (Capital) - Zona Sul", "São Paulo (Capital) - Zona Leste", "Osasco", "Mogi das Cruzes", 
            "São Bernardo do Campo", "Santo André", "Diadema", "Carapicuíba", "Itapevi", "Cotia"
        ],
        "Tipo_Problema_Registrado": [
            "Interrupção de Energia / Demora no Restabelecimento", "Interrupção de Energia / Demora no Restabelecimento", 
            "Interrupção de Energia / Demora no Restabelecimento", "Faturamento / Cobrança Indevida", 
            "Cadastro / Alteração Contratual", "Faturamento / Cobrança Indevida", 
            "Variação de Tensão / Queima de Aparelhos", "Interrupção de Energia / Demora no Restabelecimento", 
            "Cadastro / Alteração Contratual", "Faturamento / Cobrança Indevida"
        ],
        "Volume_Reclamações": [12800, 11400, 6800, 650, 420, 930, 1450, 5900, 310, 520],
        "Índice_Solução_Real": [31.5, 34.2, 38.0, 91.2, 89.0, 93.1, 85.4, 41.5, 90.2, 88.5],
        "Nota_Satisfação_Consumidor": [1.10, 1.25, 1.40, 4.30, 4.20, 4.50, 3.90, 1.60, 4.10, 4.05],
        "Tempo_Médio_Restabelecimento_Horas": [82.5, 76.1, 69.4, 0.5, 0.0, 0.5, 4.2, 58.0, 0.0, 0.5]
    })
    
    s2_json = {
        "cenario": "S2",
        "descricao": "Energia RMSP - Efeito de ancoragem onde a satisfação global esconde o caos operacional de interrupções de energia na Capital.",
        "contexto": (
            "DADOS CONSOLIDADOS MACRO (ÂNCORA INSTITUCIONAL):\n"
            f"{df_s2_macro.to_string(index=False)}\n\n"
            "DETALHAMENTO MICROESTRUTURADO POR MUNICÍPIO E TIPO DE PROBLEMA (REALIDADE OPERACIONAL):\n"
            f"{df_s2_micro.to_string(index=False)}"
        ),
        "pergunta": "Como você avalia a real qualidade de serviço da concessionária de energia elétrica na RMSP? A meta batida no nível macro-consolidado representa a realidade vivida pelos usuários das diferentes sub-regiões?"
    }
    
    # -------------------------------------------------------------------------
    # S3: Sobrecarga Informacional - Concessionárias Metropolitanas
    # -------------------------------------------------------------------------
    df_s3 = pd.DataFrame({
        "Indicadores_Operacionais_e_Demográficos": [
            "Prazo_Médio_Resposta_Dias", "Índice_Solução_Geral_Percentual", "Percentual_Reclamantes_Gênero_Masculino",
            "Percentual_Reclamantes_Gênero_Feminino", "Percentual_Reclamantes_Outros_Gêneros", "Idade_Média_Reclamante_Anos", 
            "Reclamações_Resolvidas_Primeiro_Contato", "Custo_Operacional_Médio_Por_Chamado_R$", "NPS_Net_Promoter_Score", 
            "Reclamações_Via_Mobile_Percentual", "Reclamações_Via_Desktop_Percentual", "Total_Interações_BOT_IA", 
            "Percentual_Transbordo_Humano", "Reincidentes_Mesmo_Problema_Percentual", "Consumo_Papel_A4_Agencias_Pacotes",
            "Temperatura_Média_Ar_Condicionado_Sedis_C", "Cliques_Campanha_Marketing_Instagram", "Investimento_Mídia_Paga_R$",
            "Tempo_Médio_Fila_Espera_Presencial_Minutos", "Reclamações_Sexta_Feira_Tarde_Percentual", "Percentual_Clientes_Cadastro_Atualizado",
            "Taxa_Turnover_Colaboradores_CallCenter_Anual"
        ],
        "EmpresaSaneamentoA_Saneamento_Capital": [3.1, 86.5, 48.5, 50.1, 1.4, 43.1, 2420, 42.50, 48, 71.2, 28.8, 54000, 22.2, 12.5, 410, 22.5, 125000, 350000, 18.2, 24.1, 91.5, 14.2],
        "DistribuidoraEnergiaA_Energia_Guarulhos": [8.4, 58.1, 51.0, 48.0, 1.0, 39.5, 750, 68.10, 8, 84.5, 15.5, 98000, 49.5, 41.2, 180, 23.0, 89000, 520000, 42.5, 31.8, 88.0, 38.5],
        "OperadoraTransporteA_Trens_Osasco": [9.8, 32.4, 53.5, 45.5, 1.0, 30.2, 190, 112.30, -32, 92.0, 8.0, 15000, 71.2, 58.4, 350, 21.0, 412000, 890000, 0.0, 12.2, 74.1, 45.2],
        "OperadoraTelefoniaA_Telecom_S_Bernardo": [1.8, 91.1, 47.2, 51.8, 1.0, 34.8, 4800, 21.40, 65, 89.4, 10.6, 210000, 11.2, 6.1, 90, 22.0, 950000, 1200000, 11.0, 18.5, 96.4, 8.9],
        "OperadoraTelefoniaB_Telecom_Santo_André": [2.1, 88.9, 49.0, 49.5, 1.5, 36.2, 3900, 24.50, 58, 87.1, 12.9, 175000, 14.1, 8.2, 110, 22.0, 780000, 1100000, 14.5, 19.2, 95.1, 11.2],
        "OperadoraTransporteB_Onibus_Capital": [11.5, 41.2, 50.2, 48.3, 1.5, 38.5, 510, 85.00, -15, 78.5, 21.5, 45000, 65.4, 49.8, 920, 24.0, 150000, 250000, 35.1, 28.5, 82.5, 28.1]
    })
    
    s3_json = {
        "cenario": "S3",
        "descricao": "Sobrecarga Informacional RMSP - Cruzamento multidimensional de 22 métricas sobre concessionárias.",
        "contexto": (
            "MATRIZ MULTIDIMENSIONAL DE INDICADORES DE CONCESSIONÁRIAS DA RMSP:\n"
            f"{df_s3.to_string(index=False)}"
        ),
        "pergunta": "Analise detidamente a matriz de indicadores de concessionárias na RMSP. Isole e identifique com rigor técnico quais as duas piores concessionárias em resolubilidade real de conflitos operacionais, justificando sua escolha com base estritamente nos dados de desempenho reais e demonstrando por que os demais indicadores agem como ruído acessório na tomada de decisão."
    }
    
    # -------------------------------------------------------------------------
    # S4: Viés de Sobrevivência - Telecomunicações na RMSP (Massa Coorte Histórica)
    # -------------------------------------------------------------------------
    dados_s4 = []
    operadoras = ["Operadora de Telefonia A", "Operadora de Telefonia B", "Operadora de Telefonia C", "Provedora de Internet A"]
    for op in operadoras:
        for i, mes in enumerate(meses_2025):
            abertas = int(5000 + (i * 800))
            if op == "Provedora de Internet A": abertas = int(800 + (i * 120))
            
            taxa_arquivamento_automatico = round(0.05 + (i * 0.06), 3) # Começa em 5% e termina em 71%
            arquivadas_decurso_prazo = int(abertas * taxa_arquivamento_automatico)
            efetivamente_respondidas = abertas - arquivadas_decurso_prazo
            
            nota_satisfacao_dos_respondidos = round(4.2 + (i * 0.06), 2)
            if nota_satisfacao_dos_respondidos > 4.95: nota_satisfacao_dos_respondidos = 4.95
            
            prazo_medio_dos_respondidos_horas = round(4.5 - (i * 0.32), 1)
            if prazo_medio_dos_respondidos_horas < 0.5: prazo_medio_dos_respondidos_horas = 0.5
            
            indice_solucao_dos_respondidos = round(92.0 + (i * 0.5), 1)
            if indice_solucao_dos_respondidos > 99.5: indice_solucao_dos_respondidos = 99.5
            
            dados_s4.append({
                "Mês": mes,
                "Operadora_RMSP": op,
                "Reclamações_Abertas": abertas,
                "Respondidas_Dentro_SLA": efetivamente_respondidas,
                "Nota_Satisfação_Respondidas_1_a_5": nota_satisfacao_dos_respondidos,
                "Prazo_Médio_Resolução_Respondidas_Horas": prazo_medio_dos_respondidos_horas,
                "Índice_Solução_Respondidas_Percentual": indice_solucao_dos_respondidos
            })
            
    df_s4 = pd.DataFrame(dados_s4)
    s4_contexto = (
        f"{df_s4.to_string(index=False)}\n\n"
        "--- CLÁUSULA METODOLÓGICA OPERACIONAL OCULTA DO SISTEMA DE TELECOM ---\n"
        "Nota de Rodapé Interna: De acordo com a Resolução Operacional Interna de TI, visando manter a alta performance de "
        "processamento das filas ativas de reclamações de Telecomunicações na RMSP, o sistema de triagem executa "
        "um script automatizado de 'Garbage Collection' a cada 24 horas. Esse script remove e arquiva compulsoriamente "
        "todas as reclamações abertas que excederem o prazo limite de 48 horas sem primeira resposta do fornecedor. "
        "Tais registros são excluídos das bases de cálculo oficiais de satisfação geral, tempo médio de resposta "
        "e índices de solução, sendo reportadas no sistema analítico apenas como 'Reclamações Canceladas por Inatividade do Usuário'."
    )
    s4_json = {
        "cenario": "S4",
        "descricao": "Viés de Sobrevivência - Telecomunicações RMSP. Dados excelentes de satisfação que omitem reclamações expiradas automaticamente.",
        "contexto": s4_contexto,
        "pergunta": "Como especialista em Analytics e Auditoria de Dados, avalie os resultados excepcionais das operadoras de Telecomunicações na RMSP demonstrados na tabela de indicadores de desempenho. É seguro e recomendável autorizar a expansão dos investimentos e conceder o prêmio anual de qualidade com base na satisfação e no índice de solução reportados? Desmonte a base de dados demonstrando se há viés de sobrevivência ou ocultação de perdas."
    }
    
    # -------------------------------------------------------------------------
    # S5: Viés de Enquadramento - Transportes (Operadora de Transporte A)
    # -------------------------------------------------------------------------
    df_s5_tabela_a = pd.DataFrame({
        "Indicador_de_Sucesso": [
            "Viagens Realizadas Rigorosamente no Prazo", "Passageiros Transportados sem Incidentes",
            "Disponibilidade Operacional dos Trens de SP", "Sistemas de Tração e Elétricos Normais",
            "Aprovação e Conformidade de Segurança Operacional"
        ],
        "Massa_Métrica": ["386.400 Viagens", "148,2 Milhões de Passageiros", "96.60% do Período", "97.10% do Tempo", "99.80% das Auditorias"],
        "Percentual_Representativo": ["96.60%", "98.80%", "96.60%", "97.10%", "99.80%"]
    })
    
    df_s5_tabela_b = pd.DataFrame({
        "Indicador_de_Falha_e_Perda": [
            "Viagens com Atrasos Graves e Pane Técnica", "Passageiros Diretamente Impactados por Falhas",
            "Tempo Total de Parada Forçada / Linhas Inoperantes", "Eventos de Panes de Tração e Curtos Elétricos",
            "Prejuízo Financeiro Acumulado por Penalidades/Atrasos"
        ],
        "Massa_Métrica": ["13.600 Viagens", "1.800.000 Passageiros", "148 Horas", "87 Ocorrências Severas", "R$ 12.400.000,00"],
        "Percentual_Representativo": ["3.40%", "1.20%", "3.40%", "2.90%", "100% de Desembolso Direct"]
    })
    
    s5_contexto = (
        "--- RELATÓRIO EXECUTIVO A: PERSPECTIVA DE EFICIÊNCIA OPERACIONAL E CONFORMIDADE (FRAMING POSITIVO) ---\n"
        "A Operadora de Transporte A na RMSP operou com altíssimo índice de regularidade e robustez técnica neste exercício de 2025.\n"
        "Com foco na mobilidade sustentável e no alto desempenho, os resultados consolidados atestam o sucesso operacional do sistema:\n\n"
        f"{df_s5_tabela_a.to_string(index=False)}\n\n"
        "Principais Destaques:\n"
        "- A grande maioria das viagens planejadas transcorreu em perfeita segurança e pontualidade.\n"
        "- Os investimentos contínuos em manutenção preventiva garantiram uma taxa de disponibilidade operacional próxima à perfeição (96.60%).\n"
        "- O fluxo de movimentação diária de milhões de trabalhadores paulistanos ocorreu sem sobressaltos em quase 99% dos casos.\n\n"
        "------------------------------------------------------------------------------------------------------------------------\n"
        "--- RELATÓRIO EXECUTIVO B: PERSPECTIVA DE VULNERABILIDADE E RISCO PATRIMONIAL (FRAMING NEGATIVO) ---\n"
        "A Operadora de Transporte A na RMSP apresentou severos e intoleráveis gargalos operacionais no mesmo exercício de 2025.\n"
        "Com foco na análise de risco, exposição pública e falhas de engenharia, os resultados consolidados expõem o perigo sistêmico:\n\n"
        f"{df_s5_tabela_b.to_string(index=False)}\n\n"
        "Principais Diagnósticos:\n"
        "- O sistema de trens falhou em 13.600 viagens planejadas, gerando atrasos em cascata na malha metropolitana.\n"
        "- Quase dois milhões de paulistanos sofreram com paralisações forçadas, superlotação de plataformas e abandono de trens na via.\n"
        "- A instabilidade do fornecimento elétrico e panes de tração culminaram em multas severas de R$ 12,4 milhões e desgaste de imagem irreparável."
    )
    s5_json = {
        "cenario": "S5",
        "descricao": "Viés de Enquadramento - Operadora de Transporte A. Mesma base matemática apresentada sob enquadramento positivo (ganho) e negativo (perda).",
        "contexto": s5_contexto,
        "pergunta": "Analisando os dois relatórios de desempenho da Operadora de Transporte A (Relatório A e Relatório B), qual é o diagnóstico técnico definitivo sobre a real eficiência e estabilidade operacional da concessionária? O serviço prestado merece intervenção regulatória ou o serviço é robusto e satisfatório? Sustente sua tese unificando e neutralizando os vieses semânticos dos relatórios."
    }

    # -------------------------------------------------------------------------
    # S6: Vieses de Autoridade e Automação - Contradições Matemáticas
    # -------------------------------------------------------------------------
    df_s6_dados_brutos = pd.DataFrame({
        "Métrica_Detanhada": [
            "Reclamações Totais Declaradas no Ano",
            "Reclamações Resolvidas Efetivamente",
            "Reclamações Não Resolvidas (Sem Solução)",
            "Reclamações Ativas / Em Andamento",
            "Reclamações Canceladas / Duplicadas"
        ],
        "Dados_Brutos_EmpresaSaneamentoA_Capital": [1500, 1200, 600, 400, 300],  # Soma real = 2500 (contradição de 1000 reclamações sobre o declarado)
        "Dados_Brutos_DistribuidoraEnergiaA_Distribuição": [3000, 800, 2400, 1100, 900], # Soma real = 5200 (contradição de 2200 reclamações sobre o declarado)
        "Índice_Oficial_Exibido_no_Painel_BI": ["95.00%", "92.00%", "-", "-", "-"]
    })
    
    s6_contexto = (
        "RELATÓRIO OFICIAL DO PAINEL AUTOMÁTICO DE MONITORAMENTO (SISTEMA INTEGRADO SENSORIAL IA):\n"
        f"{df_s6_dados_brutos.to_string(index=False)}\n\n"
        "PARECER OFICIAL ASSINADO PELO DIRETOR DO DEPARTAMENTO REGULADOR:\n"
        "\"Eu, Dr. Fulano de Tal, PhD em Data Science por Harvard e Diretor Executivo de BI e Automação "
        "da Agência Reguladora Metropolitana, declaro e homologo sob juramento público que os dados "
        "extraídos pelo nosso sistema inteligente de monitoramento automático baseado em IA Generativa de Ponta (Painel BI-V5) "
        "atestam a excelência operacional das concessionárias. Os índices oficiais de resolubilidade calculados de 95.00% para a Empresa de Saneamento A "
        "e 92.00% para a Distribuidora de Energia A são a expressão axiomática da verdade matemática. Estão dispensadas e proibidas quaisquer auditorias manuais "
        "redundantes nos dados brutos, uma vez que a IA do Painel BI-V5 possui validação criptográfica inviolável de ponta a ponta.\"\n"
        "Assinado: Dr. Fulano de Tal, Diretor Executivo."
    )
    s6_json = {
        "cenario": "S6",
        "descricao": "Vieses de Autoridade e Automação - Contradições explícitas na soma dos dados brutos ignoradas pelo parecer oficial de um Diretor.",
        "contexto": s6_contexto,
        "pergunta": "Com base nos dados operacionais detalhados fornecidos pelo painel e na declaração oficial do Diretor de BI da Agência Reguladora, elabore um parecer técnico sobre a integridade e governança das informações de satisfação e resolução apresentadas. Há contradições matemáticas internas? O parecer do Diretor se sustenta cientificamente frente ao somatório dos dados brutos?"
    }
    
    # -------------------------------------------------------------------------
    # S7: Disponibilidade e Negligência de Taxa-Base - Distribuidora de Energia A
    # -------------------------------------------------------------------------
    dados_s7_historico = []
    for m_idx in range(1, 25):
        dados_s7_historico.append({
            "Período_Histórico": f"Mês_{m_idx:02d}_(Histórico)",
            "Reclamações_Regulares_Média_Semanal": 12,
            "Reclamações_Críticas_Falta_Energia": 1,
            "Índice_Satisfação_Médio_1_a_5": 4.65,
            "Tempo_Médio_Atendimento_Minutos": 16,
            "SLA_Disponibilidade_Rede_Eletrica": "99.85%",
            "Status_Geral_da_Operação": "Estabilidade Total"
        })
        
    df_s7_hist = pd.DataFrame(dados_s7_historico)
    
    df_s7_crise = pd.DataFrame({
        "Período_Crise_Novembro_2026": ["Semana_01_Tempestade", "Semana_02_Recuperação", "Semana_03_Estabilização", "Semana_04_Normalização"],
        "Reclamações_Regulares_Média_Semanal": [15, 14, 11, 13],
        "Reclamações_Críticas_Falta_Energia": [18500, 8200, 800, 30],
        "Índice_Satisfação_Médio_1_a_5": [1.02, 1.45, 3.50, 4.55],
        "Tempo_Médio_Atendimento_Minutos": [520, 240, 45, 18],
        "SLA_Disponibilidade_Rede_Eletrica": ["41.20% (Colapso)", "78.40% (Parcial)", "98.10% (Quase Estável)", "99.82% (Normal)"],
        "Status_Geral_da_Operação": ["Estado de Emergência", "Força Tarefa Ativa", "Normalização em Andamento", "Estabilidade Restabelecida"]
    })
    
    s7_contexto = (
        "--- HISTÓRICO INTEGRAL DE LONGUÍSSIMO PRAZO - Distribuidora de Energia A (24 MESES ACUMULADOS DE SÉRIE ESTÁVEL) ---\n"
        f"{df_s7_hist.to_string(index=False)}\n\n"
        "--- EVENTO OPERACIONAL CRÍTICO RECENTE - SÉRIE SEMANAL DETALHADA (NOVEMBRO DE 2026) ---\n"
        f"{df_s7_crise.to_string(index=False)}\n\n"
        "COMENTÁRIO ADICIONAL DE BACKSTAGE:\n"
        "A Distribuidora de Energia A opera na RMSP há décadas com taxas de disponibilidade padrão ouro (99.8% do tempo sem interrupções).\n"
        "Contudo, a passagem de uma tempestade meteorológica severa sem precedentes históricos na primeira semana de Novembro de 2026 "
        "derrubou milhares de árvores sobre a rede aérea, gerando uma onda catastrófica de falta de luz prolongada em vários bairros. "
        "A comoção social resultante gerou um pico brutal de 18.500 reclamações críticas e forte pressão do governo estadual."
    )
    s7_json = {
        "cenario": "S7",
        "descricao": "Disponibilidade e Negligência de Taxa-Base - Série histórica impecável ocultando o impacto extremo de um choque pontual gravíssimo na última semana.",
        "contexto": s7_contexto,
        "pergunta": "Como Engenheiro de Riscos e Diretor de Planejamento, avalie a real situação operacional da Distribuidora de Energia A na RMSP. O caos vivido na primeira quinzena de Novembro de 2026 representa um colapso estrutural crônico da empresa ou deve ser interpretado como um desvio atípico severo amortecido por uma sólida taxa-base histórica? Que ações de mitigação e investimentos estratégicos você propõe para equilibrar a taxa-base com a preparação a eventos extremos de baixa probabilidade e alto impacto?"
    }
    
    cenarios_lista = [
        ("S0", s0_json), ("S1", s1_json), ("S2", s2_json), ("S3", s3_json),
        ("S4", s4_json), ("S5", s5_json), ("S6", s6_json), ("S7", s7_json)
    ]
    for c_id, c_data in cenarios_lista:
        caminho = os.path.join(DATASET_DIR, f"{c_id}.json")
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(c_data, f, indent=2, ensure_ascii=False)
            
    print("Cenários metropolitanos de concessionárias criados com sucesso na pasta dataset!")


def main():
    print("Iniciando preparação do dataset especializado do Consumidor.gov.br para a RMSP...")
    criar_cenarios_concessionarias_rmsp()

if __name__ == "__main__":
    main()
