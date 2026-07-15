import pandas as pd
import numpy as np
from scipy import stats

class AnalisadorTesteAB:
    def __init__(self, df):
        self.df = df
        self.grupos = self.df['Grupos de usuários'].unique()
        self.parceiro = self.df['Parceiro'].iloc[0]
        self.resultados = {}
        
    def analisar_metrica(self, metrica='Lucro'):
        dados_grupo = []
        for grupo in self.grupos:
            dados = self.df[self.df['Grupos de usuários'] == grupo][metrica].values
            dados_grupo.append(dados)
            
        estatistica_f, valor_p = stats.f_oneway(*dados_grupo)
        
        medias = {grupo: self.df[self.df['Grupos de usuários'] == grupo][metrica].mean() for grupo in self.grupos}
        
        melhor_grupo = max(medias, key=medias.get)
        
        self.resultados[metrica] = {
            'valor_p': valor_p,
            'eh_significativo': valor_p < 0.05,
            'medias': medias,
            'melhor_grupo': melhor_grupo
        }
        return self.resultados[metrica]
        
    def obter_resumo(self):
        resumo = self.df.groupby('Grupos de usuários').agg({
            'compradores': 'sum',
            'vendas totais': 'sum',
            'comissão': 'sum',
            'cashback': 'sum',
            'Lucro': 'sum'
        }).reset_index()
        
        resumo['ROI'] = np.where(resumo['cashback'] > 0, resumo['Lucro'] / resumo['cashback'], 0)
        return resumo
        
    def analisar_e_resumir(self):
        resultado_lucro = self.analisar_metrica('Lucro')
        df_resumo = self.obter_resumo()
        vencedor = resultado_lucro['melhor_grupo']
        
        return vencedor, resultado_lucro, df_resumo
