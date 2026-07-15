# Méliuz Growth AI-Native A/B Test Analyzer

Solução automatizada, parametrizada e robusta para análise de testes A/B de cashback, desenvolvida para o Teste Técnico da vaga de Estágio de Operações Integradas.

## O que essa solução faz?

1. Robustez na Limpeza: Lê nativamente dados CSV "sujos" de testes A/B financeiros, com tratamento avançado por Regex para não quebrar independente da formatação do valor monetário (R$, pontos, espaços extras).
2. Decisão Acionável e Estatística: Calcula o Lucro (Comissão - Cashback), Ticket Médio e ROI, aplicando um teste estatístico de variância (ANOVA) entre os grupos do teste.
3. Escalabilidade AI-Native: Foi desenvolvida sob a ótica de um Workflow Agêntico, projetada para ser facilmente invocada em linguagem natural por analistas não-técnicos através de LLMs (Claude, Cursor, Gemini).
4. Integração em Nuvem: Conecta e registra a decisão final de negócio diretamente em uma planilha do Google Sheets via API, com um fallback inteligente para arquivo CSV caso haja indisponibilidade nas credenciais.

## Estrutura do Projeto

```bash
meliuz-growth-test/
│
├── data/                  # Pasta para os Datasets CSV brutos
│   └── historico_testes.csv # Fallback de acompanhamento local
├── reports/               # Relatórios Markdown de decisão gerados pela análise
├── src/
│   ├── main.py            # Orquestrador da esteira AI-Native
│   ├── data_processor.py  # Lógica de limpeza robusta e métricas derivadas
│   ├── ai_analyzer.py     # Motor estatístico (ANOVA) e recomendações
│   └── sheets_client.py   # Conexão com Google Sheets API
├── .env                   # Variáveis de ambiente e credenciais
└── requirements.txt       # Dependências da aplicação
```

## Como rodar (Setup)

1. Clone este repositório.
2. Ative um ambiente virtual e instale as dependências:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Coloque os datasets de parceiros (.csv) na pasta data/.

(Opcional) Configurando o Google Sheets:
Abra o arquivo .env e aponte para o caminho absoluto da sua chave JSON do Google Service Account, junto com a URL da sua planilha com permissão de edição.

## Como usar (Workflow AI-Native)

Essa arquitetura brilhará nas mãos de uma Inteligência Artificial. Basta o usuário jogar este Prompt Padrão no Cursor, Claude ou ChatGPT (com Code Interpreter) junto ao arquivo .csv que deseja analisar:

> "Analise o novo dataset anexado utilizando a solução de testes A/B da pasta src/. Mova o arquivo recebido para a pasta data/ e em seguida rode o comando python src/main.py --file data/[NOME_DO_ARQUIVO].csv. Ao finalizar, me retorne um resumo do arquivo .md que foi gerado na pasta de reports, focando exclusivamente em qual variante devemos escalar para 100% do tráfego."
