import pandas as pd
from ai_analyzer import AnalisadorTesteAB

def test_anova_com_vencedor_claro():
    # Construindo um cenário onde o Grupo A é nitidamente superior (Lucro ~300 vs ~50)
    df_mock = pd.DataFrame({
        'Data': pd.date_range(start='2026-01-01', periods=10),
        'Grupos de usuários': ['Grupo A'] * 5 + ['Grupo B'] * 5,
        'Parceiro': ['Parceiro Teste'] * 10,
        'compradores': [100] * 10,
        'vendas totais': [5000] * 10,
        'comissão': [500] * 10,
        'cashback': [200] * 10,
        'Lucro': [300, 310, 290, 305, 295] + [50, 45, 55, 60, 40] 
    })
    
    analisador = AnalisadorTesteAB(df_mock)
    vencedor, resultado_lucro, df_resumo = analisador.analisar_e_resumir()
    
    # Verificações Estatísticas
    assert vencedor == 'Grupo A'
    assert resultado_lucro['eh_significativo']
    assert resultado_lucro['valor_p'] < 0.05
    
    # Verificação do Agrupamento
    lucro_total_grupo_a = df_resumo.loc[df_resumo['Grupos de usuários'] == 'Grupo A', 'Lucro'].iloc[0]
    assert lucro_total_grupo_a == 1500 # Soma de 300+310+290+305+295
