# Harness de Testes de Engenharia de Prompt e Mitigação de Vieses Cognitivos 🎓

Harness de testes automatizado, resiliente e versionado por lotes para o TCC em Engenharia de Prompt focado na mitigação de vieses cognitivos em Grandes Modelos de Linguagem (LLMs) usando a API da **Google Cloud Vertex AI** (Gemini 3.6 Flash) em um projeto GCP próprio (configurado por variável de ambiente) na região `global`.

---

## 1. Arquitetura do Sistema 🏗️

O harness é focado no universo de **"Desempenho de Serviços Públicos Concedidos e Concessionárias na Região Metropolitana de São Paulo (RMSP)"** (empresas fictícias de saneamento, energia, telefonia e transporte) mapeando dados do Consumidor.gov.br.

```text
tcc-tsi-2025/
├── .env                              # Variáveis locais (GCP_PROJECT, GCP_LOCATION); não versionado
├── requirements.txt                  # Dependências Python (google-genai, pandas, python-dotenv, tabulate)
├── runner.py                         # Orquestrador: percorre cenário x estratégia x repetição, com retomada por lote
├── dataset/                          # Cenários S0 a S7 (JSON) lidos pelo runner
│   └── nucleo_original/              # Versões de S0 a S3 enviadas a P0-P4 (apenas documentação/conferência)
├── prompts/                          # Templates das estratégias (P0 a P7 e etapas intermediárias)
├── storage/                          # Banco SQLite (experimentos.db) com todas as execuções, por lote
└── src/
    ├── database.py                   # Modelagem SQL, persistência e isolamento por lote
    ├── llm_client.py                 # Cliente da Vertex AI (Google GenAI SDK) com retentativas e métricas de uso
    ├── prepare_datasets.py           # Gera os cenários sintéticos em dataset/
    ├── strategies.py                 # Implementação de P0 a P7 (chamadas únicas, paralelas e encadeadas)
    ├── export_results.py             # Exporta um lote para CSV e relatório Markdown
    └── reproduce_metrics.py          # Recalcula tokens, chamadas, latência e médias ordinais a partir do CSV
```

### Fluxo de uma execução

1. `runner.py` monta a lista de unidades (cenário, estratégia, repetição) e ignora as já concluídas no lote ativo.
2. Para cada unidade, `strategies.py` carrega o cenário (`dataset/Sx.json`) e o template (`prompts/`), e executa o pipeline da estratégia (1 a 4 chamadas ao modelo).
3. `llm_client.py` chama o Gemini na Vertex AI e devolve texto, tokens de entrada/saída e latência.
4. `database.py` grava o registro (prompt enviado, resposta final, respostas intermediárias, tokens, chamadas, latência, data/hora) no SQLite.
5. Ao final, os resultados são exportados em `output_resultados_LOTE_*.csv` e `resumo_experimento_LOTE_*.md`.

---

## 2. Estratégia Funcional (Matriz Metodológica) 🧠

O experimento cruza **8 cenários de dados (vieses na RMSP)** com **8 estratégias de prompt (mitigações)** executados em **3 repetições independentes com temperatura controlada**, totalizando 192 simulações de controle por lote (ou o delta incremental).

### A. Cenários Metropolitanos de Negócio (Indução de Viés)
* **S0 (Controle - Saneamento RMSP)**: Desempenho convergente de melhora nas concessionárias de esgoto (queda de reclamações, alta resolubilidade e excelente satisfação).
* **S1 (Viés de Confirmação - Canais Digitais)**: Uma diretoria defende que o App de energia foi um sucesso devido ao prazo de resposta curto, ocultando que a resolubilidade despencou para 31% e os conflitos dispararam.
* **S2 (Efeito de Ancoragem - Restabelecimento de Energia)**: Apresenta satisfação macro de 88.2% na RMSP (âncora), mas omite o caos operacional de interrupções longas especificamente na Capital.
* **S3 (Sobrecarga Informacional - Multi-serviços)**: Tabela complexa cruzando 12 métricas heterogêneas e ruidosas (gêneros, idades, custos operacionais e bots) sobre concessionárias de SP.
* **S4 (Viés de Sobrevivência - Telecomunicações)**: Dados com satisfação e tempos de resposta excelentes, omitindo uma nota metodológica oculta que avisa que o sistema exclui e arquiva automaticamente reclamações com prazos estourados (churn oculto).
* **S5 (Viés de Enquadramento - Operadora de Transporte A)**: Apresenta exatamente a mesma base matemática em dois formatos textuais com enquadramentos opostos: ganho/sucesso (96,6% de viagens no prazo) e perda/falha (3,4% de viagens com atrasos graves e prejuízo financeiro de R$ 12,4 milhões).
* **S6 (Vieses de Autoridade e Automação - Contradições)**: Dados com contradições matemáticas brutas explícitas de somatório e percentuais declarados, acompanhados de uma declaração oficial e opinativa incorreta de um Diretor de BI endossando o sistema automatizado sem auditar os dados brutos.
* **S7 (Disponibilidade e Negligência de Taxa-Base - Distribuidora de Energia A)**: Série histórica perfeitamente estável e positiva ao longo de 24 meses (taxa-base robusta), mas confrontada com um pico extremo de reclamações críticas textuais e tempo de espera de 8 horas decorrente de um colapso na última semana (heurística da disponibilidade).

### B. Estratégias de Prompt (Técnicas de Mitigação)
* **P0 (Prompt Simples)**: Baseline. Instrução de resposta direta de negócio. (1 chamada).
* **P1 (Estruturado)**: Exige divisão analítica estrita na resposta (limitações) e proíbe reativamente a invenção de informações. (1 chamada).
* **P2 (Decomposição Analítica)**: Instrução de raciocínio encadeado (Chain of Thought), demandando ponderação de evidências antes da conclusão. (1 chamada).
* **P3 (Self-Consistency)**: Dispara **3 chamadas independentes e paralelas** (usando `ThreadPoolExecutor` para otimizar latência na Vertex AI) com temperatura de variação racional (`temperature=0.3`) usando o template analítico (P2). Pega as 3 visões concorrentes, insere-as em um template de consolidação e executa uma 4ª chamada determinística para gerar a síntese. (4 chamadas).
* **P4 (Reflexion)**: Executa um ciclo de autoavaliação. Roda uma análise inicial (P2), envia essa resposta para um agente crítico focado em identificar vieses cognitivos e realiza uma 3ª chamada corretiva que reescreve a análise calibrando o julgamento final. (3 chamadas).
* **P5 (Auditoria Reversa)**: Instruções que transformam o LLM em um auditor de dados independente, orientando-o a confrontar diretamente todas as asserções qualitativas contra as tabelas de dados brutos e ignorar explicitamente títulos ou cargos de autoridade. (1 chamada, `temperature=0.0`).
* **P6 (Enquadramento Neutro)**: Abordagem de desenviesamento semântico em duas etapas em uma única execução. O modelo primeiro extrai e remove todos os adjetivos e termos indutivos da pergunta original do usuário para reconstruí-la em formato puramente neutro, e depois responde com base estritamente na nova pergunta formulada. (1 chamada, `temperature=0.0`).
* **P7 (Desagregação Contrafatual)**: Pipeline avançado de duas chamadas encadeadas. A primeira chamada (`temperature=0.2`) isola variáveis latentes e fatores de confundimento nos dados brutos. A segunda chamada (`temperature=0.0`) consolida os resultados aplicando desagregação (teste de Simpson), simulação de cenários contrafatuais ("e se...") e uma matriz técnica de falsificabilidade de hipóteses. (2 chamadas).

---

## 3. Fontes de Dados e Bases Utilizadas 📊

As simulações do diretório `/dataset` foram estruturadas de forma a emular diretamente a volumetria, os tipos e os indicadores disponibilizados pela plataforma nacional de intermediação de conflitos de consumo:

* **Plataforma Fonte**: **[Consumidor.gov.br](https://www.consumidor.gov.br/)** (SENACON / MJSP).
* **Filtros Aplicados**: Geográfico (`UF == 'SP'` e RMSP) e setorial (Energia, Saneamento, Telecomunicações e Transportes).

### Versões dos cenários (importante para reprodutibilidade)

Os dados são **sintéticos e fictícios**: todos os valores, as narrativas e o "diretor" do S6 foram inventados para induzir vieses e **não descrevem desempenho real** de nenhuma empresa ou pessoa. As empresas aparecem com rótulos genéricos (por exemplo, "Empresa de Saneamento A", "Distribuidora de Energia A", "Operadora de Telefonia A/B/C", "Operadora de Transporte A/B"), os mesmos usados na dissertação.

O experimento teve duas fases, e os cenários S1–S3 mudaram entre elas:

| Estratégias | Cenários usados | Origem dos JSONs |
|---|---|---|
| P0–P4 (núcleo original de 60 respostas, S0–S3) | S2 e S3 **originais** (S2 com consolidado de 88,2% e 5 recortes; S3 com 4 prestadores e 12 métricas). S0 e S1 idênticos aos atuais (S1 difere só em espaços em branco). | `dataset/nucleo_original/` |
| P5–P7 e S4–S7 (matriz ampliada) | S2 e S3 **ampliados** (S2 com 89,4% e 10 recortes; S3 com 6 prestadores), mais S4–S7 | `dataset/` (lido por `runner.py`) |

`runner.py` lê apenas `dataset/`. Os arquivos de `dataset/nucleo_original/` existem para documentar e reconferir o que foi enviado a P0–P4 (os prompts gravados no CSV contêm exatamente esses textos). Rodar `python src/prepare_datasets.py` regenera `dataset/` (versão ampliada).

### Seleção das 192 respostas finais e reprodução das métricas

O CSV do lote é cumulativo: 343 linhas, das quais 192 são as respostas finais e 151 foram substituídas por reexecuções. Regra de seleção: para cada combinação cenário–estratégia–repetição vale o **último registro gravado**; em empate no mesmo segundo, vale a **última linha do arquivo**.

```bash
python src/reproduce_metrics.py
```

Imprime, sem usar API, as unidades finais, as chamadas (336), os tokens (1.824.555 no total), a latência média por estratégia, as razões em relação a P0, a sensibilidade "primeiro x último registro" e as médias da codificação ordinal (`codificacao_ordinal_LOTE_20260811_104318.csv`, 60 respostas, avaliador único, descritiva).

### Observações sobre o lote

* **Anonimização:** a execução original usou nomes reais de concessionárias nos cenários. Nesta versão pública, esses nomes foram substituídos por rótulos genéricos em `dataset/`, `src/prepare_datasets.py`, na documentação e nos textos gravados nos CSVs e resumos (`prompt_enviado`, respostas e respostas intermediárias). Os valores numéricos, os tokens, as latências e os tamanhos registrados são os da execução original e não foram recalculados após a substituição. As métricas de `src/reproduce_metrics.py` não dependem dos nomes. O alinhamento por espaços das tabelas em texto (`to_string`) dentro dos JSONs e dos prompts gravados mantém a largura original das colunas; rodar `python src/prepare_datasets.py` regenera os JSONs com rótulos genéricos e larguras ajustadas, com o mesmo conteúdo.
* O identificador `LOTE_20260811_104318` foi mantido, embora a execução tenha sido ampliada em 12/08/2026.
* `LOTE_20260811_103700` é um lote-piloto de 2 registros (S0, P0) que não integra a análise.
* Em `strategies.py`, o `prompt_enviado` gravado para P3 é o da síntese e para P4 é o da etapa inicial; a terceira chamada de P4 (reescrita) usa o texto definido na função `executar_P4`.
* `P1_estruturado.txt` contém "resposta in" (erro de digitação preservado porque foi o instrumento executado).

---

## 4. Como Executar o Harness 🚀

### Passo 1: Autenticar no GCP (Vertex AI)
Certifique-se de estar autenticado com suas credenciais do GCP via CLI (o projeto e a região são definidos pelas variáveis `GCP_PROJECT` e `GCP_LOCATION` no arquivo `.env`, que não é versionado):
```bash
gcloud auth application-default login
```

### Passo 2: Instalar as Dependências e Preparar Dataset
```bash
pip install -r requirements.txt
python src/prepare_datasets.py
```

### Passo 3: Executar o Loop do Experimento
* **Executar/Retomar os Testes (Retomada síncrona no Lote ativo)**:
  ```bash
  python runner.py
  ```
* **Executar um cenário específico (ex: S1)**:
  ```bash
  python runner.py --scenario S1
  ```
* **Forçar reexecução completa (Cria novo Lote com Timestamp)**:
  ```bash
  python runner.py --full
  ```
* **Forçar reexecução completa de um único cenário**:
  ```bash
  python runner.py --scenario S1 --full
  ```

### Passo 4: Visualizar Resultados Versionados por Lote
O runner exporta e gera automaticamente no final de cada simulação os resultados brutos e relatórios Markdown com nomes dinâmicos baseados no timestamp do lote:
* `output_resultados_LOTE_YYYYMMDD_HHMMSS.csv`
* `resumo_experimento_LOTE_YYYYMMDD_HHMMSS.md`

Para reexportar qualquer lote do passado manualmente, execute:
```bash
python src/export_results.py --lote LOTE_20261108_154500
```

---

## 5. Alinhamento com as Melhores Práticas de Engenharia de Prompt (Prompt Guide) 📚

Este harness foi desenhado em conformidade com as descobertas científicas dos principais pesquisadores da área (Jason Wei, Xuezhi Wang, Noah Shinn, Sander Schulhoff) e guias de engenharia de prompt de referência (Chip Huyen, documentação do Google/Vertex AI). 

Abaixo está o mapeamento detalhado de como as diretrizes do **Prompt Guide** foram implementadas de forma prática e sistemática nas técnicas de prompt do harness:

### A. Diretrizes de Arquitetura e Engenharia de Contexto
*   **Definição Estrita de Papel (Role-Prompting):** 
    *   *Na prática:* Os prompts avançados utilizam personas técnicas altamente especializadas e com escopo limitado de atuação para mitigar alucinações e direcionar a atenção do modelo.
        *   **P5 (Auditoria):** *"Você é um Auditor de Dados Independente especializado em Analytics e detecção de vieses analíticos."*
        *   **P6 (Enquadramento):** *"Você é um Engenheiro de Analytics Sênior."*
        *   **P7 (Desagregação):** *"Você é um Cientista de Dados Sênior."*
*   **Separação por Delimitadores Semânticos:**
    *   *Na prática:* Todos os templates de prompt utilizam estruturação rica em Markdown (`#`, `##`, `###`), delimitadores claros (`---`) e seções isoladas (como `## DADOS DE ENTRADA`, `### Tabela de Dados (Contexto):`, `### Parecer ou Pergunta de Negócio:`). Isso previne a injeção de prompts por parte de dados externos.
*   **Guardrails Textuais e Instruções Negativas:**
    *   *Na prática:* Uso de instruções de exclusão e mandatos explícitos em caixa alta para travar comportamentos erráticos.
        *   **P1:** *"Não invente valores, fatos ou relações causais."*
        *   **P3:** *"Não selecione uma conclusão apenas por aparecer com maior frequência."*
        *   **P6:** *"Você deve seguir OBRIGATORIAMENTE um processo rigoroso de duas etapas..."* e *"Ignore qualquer pressão linguística ou emocional..."*.

### B. Técnicas Avançadas de Raciocínio (O Paradoxo do Sistema 2)
*   **Cadeia de Pensamento (Chain-of-Thought - CoT):**
    *   *Na prática:* Implementada de forma direta no **P2 (Analítico)** (*"Execute uma análise em etapas verificáveis. Primeiro, defina... Em seguida, confira... Liste evidências..."*) e no **P6** (que exige o cumprimento da Etapa 1 de reformulação antes da resposta final na Etapa 2).
*   **Consistência Própria (Self-Consistency):**
    *   *Na prática:* Implementada no pipeline de execução do **P3**. O script `src/strategies.py` executa 3 chamadas paralelas com temperatura `0.3` usando o template analítico (P2) e depois alimenta essas respostas no prompt de síntese consolidado (**P3**) com temperatura `0.0`.
*   **Auto-Reflexão Verbal (Reflexion):**
    *   *Na prática:* Implementada no fluxo cíclico do **P4**. O harness gera uma análise preliminar, a submete ao prompt de crítica estruturada (**P4_critica.txt**) para auditar vieses e omissões, e usa esse parecer para reescrever de forma limpa e calibrada a resposta final.

### C. Blindagem contra Armadilhas de Negócios (BI & Analytics)
*   **Desenviesamento de Enquadramento por Meta-Perguntas:**
    *   *Na prática:* O **P6 (Enquadramento Neutro)** obriga o modelo a realizar a conversão na Etapa 1, identificando adjetivos e termos carregados (ex: "sucesso", "colapso") e reescrevendo a pergunta de negócio original em uma hipótese neutra de duas vias antes de consultar os dados.
*   **Falsificabilidade Ativa de Hipóteses:**
    *   *Na prática:* O **P7 (Desagregação Contrafatual)** exige que o modelo produza uma *"Matriz de Falsificabilidade de Hipóteses"* contendo a coluna obrigatória *"Condição de Falsificação (O que provaria que esta hipótese está errada?)"*.
*   **Desagregação de Simpson Mandatória:**
    *   *Na prática:* O pipeline do **P7** (unindo `P7_analise_intermediaria.txt` e `P7.txt`) exige explicitamente o fatiamento dos dados agregados para revelar as tendências micro reais ocultas em subgrupos (ex: municípios específicos na RMSP).

### D. Controle de Parâmetros e Engenharia de Software
*   **Casamento de Temperatura:**
    *   *Na prática:* Rigorosamente configurado no `src/strategies.py`:
        *   `temperature=0.0`: Para tarefas de auditoria e extração que exigem reprodutibilidade acadêmica rigorosa e determinismo (**P0, P1, P2, P4, P5, P6**).
        *   `temperature=0.2 / 0.3`: Para estimular a diversidade de caminhos e pensamento em subchamadas e análises intermediárias de Self-Consistency (**P3**) e detecção de variáveis latentes contrafatuais (**P7_analise_intermediaria**).
*   **Controle de Formato Nativo (Structured Outputs):**
    *   *Na prática:* Os prompts impõem estruturas Markdown fixas e bem-definidas (seções numeradas, tabelas Markdown para a matriz de incongruências e falsificabilidade), garantindo que as respostas analíticas e notas ordinais venham em formatos consistentes e facilmente processáveis pelas camadas de extração.

