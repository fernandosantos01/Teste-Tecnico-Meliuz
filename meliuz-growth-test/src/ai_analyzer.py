import pandas as pd
import numpy as np
from scipy import stats

class ABTestAnalyzer:
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
        
    def gerar_relatorio(self):
        resultado_lucro = self.analisar_metrica('Lucro')
        
        df_resumo = self.obter_resumo()
        
        if resultado_lucro['eh_significativo']:
            recomendacao = f"**Escalar o {resultado_lucro['melhor_grupo']} para 100% do tráfego.** O teste apresentou significância estatística (p-value: {resultado_lucro['valor_p']:.4f}) indicando que este grupo gera o maior Lucro diário médio."
            vencedor = resultado_lucro['melhor_grupo']
        else:
            recomendacao = f"**Empate Estatístico.** O teste NÃO apresentou diferença significativa no Lucro entre os grupos (p-value: {resultado_lucro['valor_p']:.4f}). Sugere-se escolher o grupo com maior ROI ou estender o teste."
            vencedor = resultado_lucro['melhor_grupo']
            
        relatorio = f"# Relatório de Teste A/B - {self.parceiro}\n\n"
        relatorio += "## Decisão Acionável\n"
        relatorio += f"{recomendacao}\n\n"
        
        relatorio += "## Resumo de Performance por Grupo\n"
        
        relatorio += df_resumo.to_markdown(index=False, floatfmt=".2f")
        relatorio += "\n\n"
        
        relatorio += "## Detalhes Estatísticos (Métrica: Lucro Diário)\n"
        for grupo, valor_medio in resultado_lucro['medias'].items():
            relatorio += f"- **{grupo}**: R$ {valor_medio:.2f} médio por dia\n"
        relatorio += f"\n- **P-Value (ANOVA)**: {resultado_lucro['valor_p']:.4f}\n"
        relatorio += f"- **Significância**: {'Sim (Confiança > 95%)' if resultado_lucro['eh_significativo'] else 'Não'}\n"
        
        return relatorio, vencedor, resultado_lucro
