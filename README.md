# Méliuz Growth AI-Native — Analisador de Testes A/B

[![Repositório GitHub](https://img.shields.io/badge/GitHub-Repositório_Oficial-181717?style=for-the-badge&logo=github)](https://github.com/fernandosantos01/Teste-Tecnico-Meliuz)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![Google Sheets API](https://img.shields.io/badge/Google_Sheets-API-34A853?style=for-the-badge&logo=google-sheets&logoColor=white)]()

Solução automatizada, parametrizada e robusta para análise de testes A/B de cashback, desenvolvida para o Teste Técnico da vaga de Estágio de Operações Integradas.

---

## Acesso aos Resultados (Planilha de Acompanhamento)

A planilha do Google Sheets integrada a esta aplicação, onde as decisões finais estatísticas são registradas em tempo real, pode ser acessada (modo leitura) pelo recrutador através do link abaixo:

**[Acessar Planilha de Acompanhamento (Google Sheets)](https://docs.google.com/spreadsheets/d/1upEL0kFe6n_0Bo4HQJMIYijBJ9J3PBLX1OXRtt-sh6s/edit?usp=sharing)**

---

## O que essa solução faz?

1. **Robustez na Limpeza:** Lê nativamente dados CSV "sujos" de testes A/B financeiros, com tratamento avançado por Regex para não quebrar independente da formatação do valor monetário (R$, pontos, espaços extras). Valores nulos e datas corrompidas são descartados silenciosamente sem interromper a execução.
2. **Decisão Acionável e Estatística:** Calcula o Lucro (Comissão - Cashback), Ticket Médio e ROI por grupo, aplicando um teste estatístico de variância (ANOVA) para garantir que a decisão de escalar tráfego seja matematicamente fundamentada — e não uma "achologia".
3. **Escalabilidade AI-Native:** Foi desenvolvida sob a ótica de um Workflow Agêntico, projetada para ser facilmente invocada em linguagem natural por analistas não-técnicos através de LLMs (Claude, Cursor, Gemini).
4. **Integração em Nuvem:** Conecta e registra a decisão final de negócio diretamente em uma planilha do Google Sheets via API, com um fallback inteligente para arquivo CSV local caso as credenciais não estejam configuradas.

---

## Pré-requisitos

- Python 3.10 ou superior
- `pip` instalado
- Uma conta no [Google Cloud](https://console.cloud.google.com/) (para a integração com Google Sheets)
- Uma planilha criada no [Google Sheets](https://sheets.google.com/)

---

## Estrutura do Projeto

```
meliuz-growth-test/
│
├── data/                      # Datasets CSV brutos (Parceiros A, B, C)
│   └── historico_testes.csv   # Cache local para a Sincronização Offline
├── reports/                   # Relatórios finais em Markdown (Decisões Acionáveis)
├── src/
│   ├── main.py                # Orquestrador
│   ├── data_processor.py      # Tratamento de dados "sujos" e matemática de negócio
│   ├── ai_analyzer.py         # Motor de inteligência estatística
│   ├── gerador_relatorio.py   # Motor de Apresentação
│   ├── formatador.py          # Micro-utilitário de máscaras financeiras (R$ e %)
│   ├── logger_config.py       # Logs padronizados para Monitoramento
│   └── sheets_client.py       # Integração Sheets
├── tests/                     # Suíte de Qualidade (QA) utilizando Pytest
│   ├── test_formatador.py     
│   ├── test_data_processor.py 
│   ├── test_ai_analyzer.py    
│   └── test_sheets_client.py  # Cobertura de Testes com Mocks
├── .env.example               # Template de variáveis
├── .env                       # Chaves reais (Omitido por segurança)
└── requirements.txt           # Lista exata de dependências do projeto
```

---

## Setup do Ambiente Local

Clone o repositório e instale as dependências dentro de um ambiente virtual:

```bash
git clone https://github.com/fernandosantos01/Teste-Tecnico-Meliuz.git
cd meliuz-growth-test
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Coloque os datasets dos parceiros (arquivos `.csv`) dentro da pasta `data/`.

---

## Configurando a Integração com Google Sheets

Esta é a etapa mais importante do setup. Siga os passos com atenção, pois existe uma distinção crítica entre os tipos de credenciais do Google Cloud que determina se a planilha será atualizada ou não.

### Passo 1 — Criar o projeto e ativar as APIs

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/) e crie um novo projeto.
2. No menu lateral, vá em **APIs e Serviços > Biblioteca**.
3. Ative as seguintes APIs:
   - **Google Sheets API**
   - **Google Drive API**

### Passo 2 — Criar a Conta de Serviço (o tipo correto de credencial)

> **Atenção — O erro mais comum:** Na tela de "Credenciais" do Google Cloud, existem dois tipos de chave disponíveis: o *OAuth 2.0 Client ID* e a *Conta de Serviço*. Se você baixar o *OAuth 2.0 Client ID* (um arquivo JSON que começa com `client_secret_...`), o código vai executar normalmente, **mas a planilha nunca será atualizada**. A biblioteca `gspread` vai detectar que o tipo de credencial é incorreto, lançar um aviso silencioso e usar apenas o fallback local em CSV. A integração com o Sheets exige obrigatoriamente uma chave de **Conta de Serviço**.

Para criar a credencial correta:

1. No menu lateral, vá em **IAM e Administrador > Contas de Serviço**.
2. Clique em **Criar conta de serviço**, dê um nome e confirme.
3. Dentro da conta criada, acesse a aba **Chaves**.
4. Clique em **Adicionar chave > Criar nova chave > JSON**.
5. O arquivo `.json` será baixado automaticamente. Guarde-o em um local seguro (nunca versionado no Git).

### Passo 3 — Compartilhar a planilha com a Conta de Serviço

1. Abra o arquivo JSON baixado e copie o valor do campo `client_email`. Ele terá o formato: `nome@projeto.iam.gserviceaccount.com`.
2. Abra a sua planilha no Google Sheets.
3. Clique em **Compartilhar** e adicione esse e-mail com permissão de **Editor**.

### Passo 4 — Configurar o arquivo `.env`

Na raiz do projeto (`meliuz-growth-test/`), preencha o arquivo `.env` com os dois valores abaixo:

```env
GOOGLE_APPLICATION_CREDENTIALS=/caminho/absoluto/para/sua/chave-service-account.json
SPREADSHEET_URL=https://docs.google.com/spreadsheets/d/SEU_ID_AQUI/edit
```

---

## Como Executar

Com o ambiente virtual ativo e o `.env` configurado, execute o script passando o caminho do dataset como argumento:

```bash
PYTHONPATH=src python src/main.py --file data/dataset_01_parceiroA.csv
```

O output esperado no terminal será:

```
Iniciando análise do dataset: data/dataset_01_parceiroA.csv...
1. Processando e limpando dados...
2. Rodando testes estatísticos...
-> Relatório gerado com sucesso: reports/relatorio_ab_teste_Parceiro_A.md
3. Atualizando tracking (histórico)...
Conectado ao Google Sheets com sucesso.
Resultado registrado no Google Sheets: <url-da-sua-planilha>

Análise concluída com sucesso! Verifique a pasta 'reports' para mais detalhes.
```

O script é flexível e parametrizado. Isso significa que, se a Méliuz expandir a operação e novos parceiros ou datasets surgirem no futuro, basta passá-los como argumento (`--file`) sem precisar alterar nenhuma linha de código da aplicação!

### Processamento em Lote (Batch Processing)

Se houverem dezenas de datasets na pasta `data/` e você desejar executar as análises e subir todas elas para o Sheets de uma única vez, você pode utilizar o seguinte laço de repetição (`for`) no seu terminal:

```bash
for arquivo in data/dataset_*.csv; do PYTHONPATH=src python src/main.py --file "$arquivo"; done
```

Esse comando garante que todos os arquivos com o padrão `dataset_*.csv` serão processados sequencialmente, populando todos os relatórios e a planilha em poucos segundos.

---

## Workflow AI-Native

A arquitetura foi projetada para ser operada por uma Inteligência Artificial. Um analista não-técnico pode usar os seguintes prompts no Cursor, Claude ou Gemini para executar toda a pipeline sem tocar em código:

**Para um único teste:**
> "Analise o novo dataset anexado utilizando a solução de testes A/B da pasta `src/`. Mova o arquivo recebido para a pasta `data/` e em seguida rode o comando `PYTHONPATH=src python src/main.py --file data/[NOME_DO_ARQUIVO].csv`. Ao finalizar, me retorne um resumo do arquivo `.md` gerado na pasta `reports/`, focando exclusivamente em qual variante devemos escalar para 100% do tráfego."

**Para processamento em lote (Múltiplos testes):**
> "Mova os 3 novos arquivos CSV anexados para a pasta `data/`. Em seguida, rode o comando `for arquivo in data/dataset_*.csv; do PYTHONPATH=src python src/main.py --file "$arquivo"; done` no terminal. Após a execução, leia todos os relatórios gerados na pasta `reports/` e construa uma tabela comparativa me informando qual foi a decisão acionável tomada para cada um dos parceiros."
