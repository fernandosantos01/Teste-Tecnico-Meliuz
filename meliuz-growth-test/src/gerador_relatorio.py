from formatador import FormatadorApresentacao

class GeradorRelatorio:
    @staticmethod
    def gerar_markdown(nome_parceiro, resultado_lucro, df_resumo):
        df_resumo_formatado = FormatadorApresentacao.formatar_tabela_resumo(df_resumo)
        
        if resultado_lucro['eh_significativo']:
            recomendacao = f"**Escalar o {resultado_lucro['melhor_grupo']} para 100% do tráfego.** O teste apresentou significância estatística (p-value: {resultado_lucro['valor_p']:.4f}) indicando que este grupo gera o maior Lucro diário médio."
        else:
            recomendacao = f"**Empate Estatístico.** O teste NÃO apresentou diferença significativa no Lucro entre os grupos (p-value: {resultado_lucro['valor_p']:.4f}). Sugere-se escolher o grupo com maior ROI ou estender o teste."
            
        relatorio = f"# Relatório de Teste A/B - {nome_parceiro}\n\n"
        relatorio += "## Decisão Acionável\n"
        relatorio += f"{recomendacao}\n\n"
        
        relatorio += "## Resumo de Performance por Grupo\n"
        
        relatorio += df_resumo_formatado.to_markdown(index=False)
        relatorio += "\n\n"
        
        relatorio += "## Detalhes Estatísticos (Métrica: Lucro Diário)\n"
        for grupo, valor_medio in resultado_lucro['medias'].items():
            relatorio += f"- **{grupo}**: {FormatadorApresentacao.moeda(valor_medio)} médio por dia\n"
        relatorio += f"\n- **P-Value (ANOVA)**: {resultado_lucro['valor_p']:.4f}\n"
        relatorio += f"- **Significância**: {'Sim (Confiança > 95%)' if resultado_lucro['eh_significativo'] else 'Não'}\n"
        
        return relatorio
