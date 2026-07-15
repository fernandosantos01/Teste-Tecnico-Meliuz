import pandas as pd
import numpy as np

def limpar_coluna_financeira(serie):
    if hasattr(serie, 'str'):
        serie = serie.str.replace(r'[^\d.,]', '', regex=True)
        serie = serie.str.replace('.', '', regex=False)
        serie = serie.str.replace(',', '.', regex=False)
        
    return pd.to_numeric(serie, errors='coerce')

def carregar_e_processar_dados(caminho_arquivo):
    try:
        df = pd.read_csv(caminho_arquivo)
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo {caminho_arquivo}: {e}")
        
    colunas_obrigatorias = ['Data', 'Grupos de usuários', 'Parceiro', 'compradores', 'comissão', 'cashback', 'vendas totais']
    for coluna in colunas_obrigatorias:
        if coluna not in df.columns:
            raise ValueError(f"Coluna obrigatória ausente: {coluna}")

    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    
    for coluna in ['comissão', 'cashback', 'vendas totais']:
        df[coluna] = limpar_coluna_financeira(df[coluna])
        
    df = df.dropna(subset=['compradores', 'comissão', 'cashback', 'vendas totais'])
    
    df['compradores'] = df['compradores'].astype(int)
    
    df['Lucro'] = df['comissão'] - df['cashback']
    
    df['Ticket Médio'] = np.where(df['compradores'] > 0, 
                                  df['vendas totais'] / df['compradores'], 
                                  0)
    
    df['Lucro por Comprador'] = np.where(df['compradores'] > 0, 
                                         df['Lucro'] / df['compradores'], 
                                         0)
                                         
    df['ROI'] = np.where(df['cashback'] > 0, 
                         df['Lucro'] / df['cashback'], 
                         0)
                         
    return df

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
