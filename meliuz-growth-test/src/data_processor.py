import pandas as pd
import numpy as np

def limpar_coluna_financeira(serie):
    if hasattr(serie, 'str'):
        serie = serie.str.replace(r'[^\d.,]', '', regex=True)
        serie = serie.str.replace('.', '', regex=False)
        serie = serie.str.replace(',', '.', regex=False)
        
    return pd.to_numeric(serie, errors='coerce')

def carregar_csv(caminho_arquivo):
    try:
        df = pd.read_csv(caminho_arquivo)
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo {caminho_arquivo}: {e}")
        
    colunas_obrigatorias = ['Data', 'Grupos de usuários', 'Parceiro', 'compradores', 'comissão', 'cashback', 'vendas totais']
    for coluna in colunas_obrigatorias:
        if coluna not in df.columns:
            raise ValueError(f"Coluna obrigatória ausente: {coluna}")
            
    return df

def limpar_dataframe(df):
    df_limpo = df.copy()
    df_limpo['Data'] = pd.to_datetime(df_limpo['Data'], errors='coerce')
    
    for coluna in ['comissão', 'cashback', 'vendas totais']:
        df_limpo[coluna] = limpar_coluna_financeira(df_limpo[coluna])
        
    df_limpo = df_limpo.dropna(subset=['compradores', 'comissão', 'cashback', 'vendas totais'])
    df_limpo['compradores'] = df_limpo['compradores'].astype(int)
    
    return df_limpo

def calcular_metricas_derivadas(df):
    df_metricas = df.copy()
    
    df_metricas['Lucro'] = df_metricas['comissão'] - df_metricas['cashback']
    
    df_metricas['Ticket Médio'] = np.where(df_metricas['compradores'] > 0, 
                                           df_metricas['vendas totais'] / df_metricas['compradores'], 
                                           0)
    
    df_metricas['Lucro por Comprador'] = np.where(df_metricas['compradores'] > 0, 
                                                  df_metricas['Lucro'] / df_metricas['compradores'], 
                                                  0)
                                         
    df_metricas['ROI'] = np.where(df_metricas['cashback'] > 0, 
                                  df_metricas['Lucro'] / df_metricas['cashback'], 
                                  0)
                                  
    return df_metricas

def carregar_e_processar_dados(caminho_arquivo):
    df_bruto = carregar_csv(caminho_arquivo)
    df_limpo = limpar_dataframe(df_bruto)
    df_final = calcular_metricas_derivadas(df_limpo)
    
    return df_final

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        arquivo_teste = sys.argv[1]
        print(f"Testando processador de dados no arquivo: {arquivo_teste}")
        df_processado = carregar_e_processar_dados(arquivo_teste)
        print(df_processado.head())
        print(df_processado.info())
    else:
        print("Por favor, forneça o caminho de um dataset para testar.")
