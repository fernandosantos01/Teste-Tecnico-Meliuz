# Méliuz Growth AI-Native — Analisador de Testes A/B

Solução automatizada, parametrizada e robusta para análise de testes A/B de cashback, desenvolvida para o Teste Técnico da vaga de Estágio de Operações Integradas.

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
├── data/                    # Datasets CSV brutos dos parceiros
│   └── historico_testes.csv # Registro local de fallback (gerado automaticamente)
├── reports/                 # Relatórios Markdown gerados após cada análise
├── src/
│   ├── main.py              # Orquestrador principal (ponto de entrada)
│   ├── data_processor.py    # Limpeza de dados e cálculo de métricas derivadas
│   ├── ai_analyzer.py       # Motor estatístico (ANOVA) e geração de relatório
│   └── sheets_client.py     # Integração com a Google Sheets API
├── .env                     # Variáveis de ambiente (não versionado)
└── requirements.txt         # Dependências do projeto
```

---

## Setup do Ambiente Local

Clone o repositório e instale as dependências dentro de um ambiente virtual:

```bash
git clone <url-do-repositorio>
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

O script é parametrizado e funciona para qualquer parceiro sem alteração de código. Basta trocar o arquivo:

```bash
PYTHONPATH=src python src/main.py --file data/dataset_02_parceiroB.csv
PYTHONPATH=src python src/main.py --file data/dataset_03_parceiroC.csv
```

---

## Workflow AI-Native

A arquitetura foi projetada para ser operada por uma Inteligência Artificial. Um analista não-técnico pode usar o seguinte prompt no Cursor, Claude ou Gemini para executar toda a pipeline:

> "Analise o novo dataset anexado utilizando a solução de testes A/B da pasta `src/`. Mova o arquivo recebido para a pasta `data/` e em seguida rode o comando `PYTHONPATH=src python src/main.py --file data/[NOME_DO_ARQUIVO].csv`. Ao finalizar, me retorne um resumo do arquivo `.md` gerado na pasta `reports/`, focando exclusivamente em qual variante devemos escalar para 100% do tráfego."
