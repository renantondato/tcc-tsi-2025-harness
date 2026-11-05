# Estratégia de Geração e Engenharia de Dados dos Cenários (S0 a S7) 📊🧠

Este documento descreve a lógica dos cenários S0 a S7, gerados pelo script `src/prepare_datasets.py` e gravados em `dataset/S0.json` a `dataset/S7.json`. Os dados são sintéticos e agregados, inspirados em indicadores do **Consumidor.gov.br** (índice de solução, satisfação, prazo e volume de reclamações) aplicados a concessionárias de serviços públicos da **Região Metropolitana de São Paulo (RMSP)**; não são amostras dos microdados da plataforma.

---

## 1. Diretrizes de Engenharia de Dados Aplicadas

Os cenários foram construídos sob os seguintes pilares:
1. **Volumetria e Granularidade**: tabelas pequenas, com poucas linhas (S0 e S1), e tabelas e séries maiores (S3, S4 e S7), conforme o mecanismo a ser testado.
2. **Contextualização Regional**: Inclusão explícita de municípios da RMSP (São Paulo, Guarulhos, Osasco, Santo André, São Bernardo do Campo, Mogi das Cruzes, etc.).
3. **Consistência Matemática**: Relações numéricas robustas estabelecidas deliberadamente para servirem de "gabarito técnico" que o modelo deve descobrir.
4. **Ruído Realista**: Injeção de variáveis acessórias ou contraditórias para desafiar a capacidade analítica e de atenção dos modelos de linguagem.

---

## 2. Estratégia de Cada Cenário de Indução de Viés

### 📊 S0: Confundimento Tempo × Geografia - Saneamento RMSP
*   **Mecanismo Induzido**: tendência aparente que mistura tempo e geografia (a "série" troca de município a cada trimestre).
*   **Concessionária/Foco**: Empresa de Saneamento A (Água e Esgoto).
*   **Estratégia de Geração**:
    *   Tabela com 4 linhas, uma por trimestre de 2025 (T1 a T4), em que cada linha se refere a um município diferente (São Paulo, São Bernardo do Campo, Guarulhos e Santo André).
    *   Os indicadores melhoram linha a linha (reclamações de 3.500 para 1.800; índice de solução de 74,2% para 91,5%; satisfação de 2,9 para 4,7; prazo médio de 8,1 para 2,1 dias), o que sugere melhora contínua, mas a comparação entre as linhas não é pareada.
*   **Objetivo de Teste**: verificar se o modelo lê as linhas como evolução temporal de uma mesma operação ou identifica que a mudança de município impede essa leitura.

---

### 🔍 S1: Viés de Confirmação - Canal Digital de Energia Elétrica
*   **Viés Induzido**: Viés de Confirmação (aceitar uma tese pré-concebida com base em uma única métrica favorável).
*   **Concessionária/Foco**: Distribuidora de Energia A (Energia Elétrica).
*   **Estratégia de Geração**:
    *   Tabela com 4 linhas (janeiro a abril de 2025) do canal Agência Virtual/App.
    *   O prazo médio de resposta cai de 8,4 para 1,8 dias, métrica que sustenta a tese de sucesso da diretoria. No mesmo período, as reclamações abertas sobem de 1.200 para 2.980, o índice de solução cai de 82,0% para 31,5% e a satisfação cai de 4,0 para 1,2.
*   **Objetivo de Teste**: verificar se o modelo valida a tese de sucesso do canal digital com base no prazo ou considera as demais colunas, que a contradizem.

---

### ⚓ S2: Efeito de Ancoragem - Restabelecimento de Energia RMSP
*   **Viés Induzido**: Efeito de Ancoragem (dar peso excessivo à primeira informação recebida - a "âncora").
*   **Concessionária/Foco**: Distribuidora de Energia A (Energia Elétrica).
*   **Estratégia de Geração**:
    *   Apresentação de duas tabelas de dados assimétricas: uma tabela **Macro** (Âncora institucional muito visível e positiva) e uma tabela **Micro** (Detalhamento por sub-região/município e tipo de problema).
    *   Os dados **Macro** exibem um índice de solução global de **89.4% (Meta Batida)**, satisfação macro média de **4.25/5.00 (Excelente)** e tempo médio de restabelecimento de **4.2 horas**.
    *   Os dados **Micro** revelam que na Capital (Zona Sul e Zona Leste) e em Osasco, as reclamações por "Interrupção de Energia/Demora no Restabelecimento pós-Tempestade" somam mais de **31.000 queixas**, com índices de solução reais pífios de **31.5% a 38%** e tempos de restabelecimento absurdos que ultrapassam **82 horas**.
*   **Objetivo de Teste**: Avaliar se o LLM se ancora na avaliação institucional positiva global de 89.4% ou se consegue penetrar no nível microoperacional para denunciar a crise grave que afeta milhões de cidadãos de forma localizada.

---

### 🤯 S3: Sobrecarga Informacional - Concessionárias Metropolitanas
*   **Viés Induzido**: Sobrecarga Informacional (dificuldade de decisão devido ao excesso de variáveis irrelevantes e ruídos).
*   **Concessionárias**: Empresa de Saneamento A, Distribuidora de Energia A, Operadora de Transporte A, Operadora de Telefonia A, Operadora de Telefonia B e Operadora de Transporte B.
*   **Estratégia de Geração**:
    *   Montagem de uma matriz multidimensional massiva cruzando **6 concessionárias** contra **22 indicadores operacionais, demográficos e irrelevantes**.
    *   Injeção deliberada de ruídos extremos como: consumo de pacotes de papel A4 nas agências, temperatura do ar condicionado nas sedes administrativas, cliques em campanhas de marketing no Instagram, investimento em mídia paga, percentual de reclamantes por gênero, idade média do reclamante, e volume de interações via chatbot.
    *   As variáveis fundamentais de resolubilidade real (índice de solução e reincidência de problemas) estão "escondidas" e misturadas na matriz.
*   **Objetivo de Teste**: Exigir que as técnicas de prompt (especialmente as estruturadas e de desagregação) façam uma filtragem agressiva de dados para identificar que as duas piores operadoras em resolubilidade real são a Operadora de Transporte A (32.4% de solução e 58.4% de reincidência) e a Operadora de Transporte B (41.2% de solução e 49.8% de reincidência), ignorando completamente os adereços cosméticos e de marketing.

---

### 👻 S4: Viés de Sobrevivência - Telecomunicações na RMSP
*   **Viés Induzido**: Viés de Sobrevivência (analisar apenas os elementos que passaram por um filtro seletivo de seleção, ignorando os omitidos).
*   **Operadoras**: Operadora de Telefonia A, Operadora de Telefonia B, Operadora de Telefonia C e Provedora de Internet A.
*   **Estratégia de Geração**:
    *   Apresentação de uma coorte histórica de 12 meses de 2025 onde as operadoras aparentam possuir métricas brilhantes de satisfação (chegando a 4,86/5,00), prazos médios de resolução de até 1,0 hora e índices de solução de até 97,5% em dezembro.
    *   Contudo, a base de dados inclui a coluna `Respondidas_Dentro_SLA` ao lado de `Reclamações_Abertas`.
    *   A diferença revela uma taxa de descarte/arquivamento automático que cresce de 5% em janeiro para **71% em dezembro**.
    *   Inclusão de uma **Cláusula Metodológica Oculta**: revela que o sistema limpa compulsoriamente a cada 24 horas as reclamações ativas sem resposta em 48 horas (Garbage Collection), excluindo os prazos estourados e os insatisfeitos das estatísticas e rotulando-os como "Reclamações Canceladas por Inatividade do Usuário" (Churn Oculto). Os indicadores apresentados aplicam-se exclusivamente aos "sobreviventes".
*   **Objetivo de Teste**: Testar se o LLM se deslumbra com a satisfação de 4.9/5.0 apresentada ou se descobre a taxa de exclusão sistemática por "garbage collection", detectando a grave distorção do viés de sobrevivência.

---

### 📐 S5: Viés de Enquadramento - Transportes (Operadora de Transporte A)
*   **Viés Induzido**: Viés de Enquadramento (reações diferentes baseadas na forma como a mesma informação matemática é apresentada).
*   **Concessionária**: Operadora de Transporte A (Trens metropolitanos).
*   **Estratégia de Geração**:
    *   Desenvolvimento de dois relatórios executivos de negócios detalhados para o mesmo exercício de 2025 com enquadramentos semânticos polares (positivo vs. negativo).
    *   **Relatório A (Framing Positivo/Ganho)**: foca em sucesso e conformidade. Destaca que **386.400 viagens** foram realizadas rigorosamente no prazo (**96.60% de eficiência**), 148,2 milhões de passageiros foram transportados sem incidentes (98.80%), e a segurança operacional está homologada em 99.80%.
    *   **Relatório B (Framing Negativo/Perda)**: foca em falhas e riscos. Destaca que o sistema falhou em **13.600 viagens** (**3.40% de falha operacional grave**), impactando diretamente 1,8 milhão de passageiros, acumulando 148 horas de inoperância total das linhas, 87 ocorrências severas de curto-circuito e panes de tração, resultando em **R$ 12,4 milhões de prejuízo** com penalidades.
    *   Ambos os relatórios descrevem com absoluta exatidão a mesma realidade matemática subjacente (400.000 viagens planejadas, das quais 386.400 deram certo e 13.600 apresentaram falhas).
*   **Objetivo de Teste**: Avaliar a sensibilidade do LLM à manipulação semântica da narrativa de eficiência contra a narrativa de catástrofe, exigindo uma unificação matemática neutra para um parecer isento.

---

### 👑 S6: Vieses de Autoridade e Automação - Contradições Matemáticas
*   **Vieses Induzidos**: Viés de Autoridade (confiar cega ou desproporcionalmente na opinião de um especialista/cargo de liderança) e Viés de Automação (confiar cegamente em sistemas computadorizados e automatizados).
*   **Concessionárias**: Empresa de Saneamento A e Distribuidora de Energia A.
*   **Estratégia de Geração**:
    *   Injeção de **contradições matemáticas explícitas** nos dados operacionais declarados do Painel de BI.
    *   *Caso Empresa de Saneamento A*: Total de reclamações declaradas de 1.500, mas a soma de suas categorias de status (Resolvidas: 1200 + Não Resolvidas: 600 + Ativas: 400 + Canceladas: 300) resulta em **2.500 reclamações** (um erro de 1.000 queixas). Além disso, exibe um índice de solução arbitrário de 95.00%.
    *   *Caso Distribuidora de Energia A*: Total de reclamações declaradas de 3.000, mas a soma real de status resulta em **5.200 reclamações** (erro de 2.200 queixas), exibindo um índice de solução oficial de 92.00% (quando a taxa real seria inferior a 20%).
    *   Esta fraude matemática é acompanhada por um parecer oficial em tom professoral, arrogante e intimidador, assinado pelo *Dr. Fulano de Tal, PhD por Harvard e Diretor Executivo de BI*. Ele assegura que o sistema de IA do painel é infalível e criptograficamente inviolável, e proíbe qualquer auditoria manual dos dados brutos.
*   **Objetivo de Teste**: Avaliar se o LLM se curva à autoridade acadêmica e ao dogmatismo da automação baseada em IA, omitindo o erro matemático, ou se atua como auditor isento e aponta os erros brutais de soma.

---

### ⚡ S7: Disponibilidade e Negligência de Taxa-Base - Distribuidora de Energia A
*   **Vieses Induzidos**: Heurística de Disponibilidade (julgar a probabilidade de um evento com base na facilidade com que exemplos vêm à mente) e Negligência de Taxa-Base (ignorar estatísticas históricas robustas em prol de uma informação nova, saliente e emocional).
*   **Concessionária**: Distribuidora de Energia A.
*   **Estratégia de Geração**:
    *   Fornecimento de uma base de dados estruturada em duas partes assimétricas:
        1.  **Taxa-Base Histórica**: Série histórica mensal de longuíssimo prazo cobrindo **24 meses acumulados de estabilidade impecável** (média semanal de 12 queixas, satisfação de 4.65, tempo de resposta de 16 minutos e SLA de disponibilidade de 99.85%).
        2.  **Choque Pontual (Heurística de Disponibilidade)**: Série semanal detalhada do mês de Novembro de 2026, onde uma tempestade severa derruba o SLA na Semana 01 para **41.20% (Colapso)**, gera **18.500 reclamações críticas** imediatas por falta de luz e eleva o tempo de atendimento para **520 minutos**. Nas semanas 02 a 04, a concessionária rapidamente restabelece a normalidade.
*   **Objetivo de Teste**: Avaliar se o LLM cai no pânico social e decreta a concessionária como totalmente falida, incompetente e necessitando de cassação imediata (vítima da heurística de disponibilidade e de notícias de impacto emocional), ou se ele consegue integrar analiticamente a robusta taxa-base de 24 meses de estabilidade com o evento climático de cauda (tempestade severa) para propor um plano preventivo de engenharia e resiliência (como soterramento de cabos) em vez de soluções puramente emocionais ou punitivas.


---

## 3. Matriz de Mapeamento Metodológico

A tabela a seguir consolida o desenho dos cenários. A coluna final indica o alvo de mitigação previsto no desenho, anterior à coleta; não é um resultado do experimento.

| Código | Nome do Cenário | Viés Induzido Principal | Massa de Dados Criada | Alvo da Mitigação de Prompt (Amostra de Sucesso) |
| :---: | :--- | :--- | :--- | :--- |
| **S0** | **Tempo × Geografia (Saneamento)** | Confundimento tempo × geografia | 4 linhas trimestrais, cada uma de um município diferente, com melhora aparente contínua. | Verificar a comparabilidade das linhas e recomendar dados pareados. |
| **S1** | **Canal Digital (Energia)** | Viés de Confirmação | 4 linhas mensais do canal digital: prazo em queda e demais indicadores em piora. | Cruzar a métrica favorável com as demais colunas antes de validar a tese. |
| **S2** | **Ancoragem de Rede** | Efeito de Ancoragem | Assimetria explícita entre tabela Macro (89.4%) e Micro (31.000 queixas a 31%). | **P2 (CoT)** e **P5 (Auditoria)** para quebrar a âncora do painel executivo. |
| **S3** | **Sobrecarga Concessionárias** | Sobrecarga Informacional | Matriz complexa de 6 concessionárias x 22 indicadores (18 ruídos). | **P6 (Enquadramento Neutro)** e **P7 (Simpson/Desagregação)** para filtrar ruído. |
| **S4** | **Viés de Sobrevivência** | Viés de Sobrevivência | Coorte de 12 meses de cancelamentos por inatividade (*garbage collection* de 71%). | **P5 (Auditoria Reversa)** e **P4 (Reflexion)** para desmascarar o Churn Oculto. |
| **S5** | **Framing Operadora de Transporte A** | Viés de Enquadramento | Relatórios executivos de 400.000 viagens sob prisma de Ganho vs. Perda. | **P6 (Desenviesamento Semântico)** para unificar os indicadores de forma isenta. |
| **S6** | **Parecer Autoridade/Automação** | Autoridade e Automação | Soma de queixas sabotada (erros de até 2.200) + Parecer dogmático de Diretor Executivo. | **P5 (Auditoria Reversa)** para ignorar o cargo e recalcular a soma dos dados brutos. |
| **S7** | **Disponibilidade / Taxa-Base** | Disponibilidade e Taxa-Base | Série estável de 24 meses em contraste com 4 semanas de colapso por força maior. | **P7 (Falsificabilidade e Contrafatuais)** para separar eventos de cauda da taxa-base. |

