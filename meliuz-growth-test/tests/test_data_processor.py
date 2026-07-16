import pandas as pd
from data_processor import limpar_coluna_financeira, calcular_metricas_derivadas

def test_limpar_coluna_financeira():
    # Simulando dados sujos que a Méliuz poderia receber (padrão BR)
    dados_sujos = pd.Series(["R$ 1.000,50", " 1.000,50 ", "500", "invalido", None])
    dados_limpos = limpar_coluna_financeira(dados_sujos)
    
    assert dados_limpos.iloc[0] == 1000.50
    assert dados_limpos.iloc[1] == 1000.50
    assert dados_limpos.iloc[2] == 500.0
    assert pd.isna(dados_limpos.iloc[3])
    assert pd.isna(dados_limpos.iloc[4])

def test_calcular_metricas_derivadas():
    # Dataset mínimo para garantir que a matemática de negócios está correta
    df_mock = pd.DataFrame({
        'compradores': [100, 0],
        'vendas totais': [10000.0, 0.0],
        'comissão': [500.0, 0.0],
        'cashback': [200.0, 0.0]
    })
    
    df_resultado = calcular_metricas_derivadas(df_mock)
    
    # Linha 1 (dados normais)
    assert df_resultado.loc[0, 'Lucro'] == 300.0 # 500 - 200
    assert df_resultado.loc[0, 'Ticket Médio'] == 100.0 # 10000 / 100
    assert df_resultado.loc[0, 'ROI'] == 1.5 # 300 / 200
    
    # Linha 2 (prevenindo divisão por zero)
    assert df_resultado.loc[1, 'Ticket Médio'] == 0.0
    assert df_resultado.loc[1, 'ROI'] == 0.0
