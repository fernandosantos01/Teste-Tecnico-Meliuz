class FormatadorApresentacao:
    @staticmethod
    def moeda(valor):
        texto = f"{valor:,.2f}"
        texto = texto.replace(',', 'X').replace('.', ',').replace('X', '.')
        return f"R$ {texto}"

    @staticmethod
    def porcentagem(valor):
        texto = f"{valor * 100:,.2f}"
        texto = texto.replace(',', 'X').replace('.', ',').replace('X', '.')
        return f"{texto}%"

    @classmethod
    def formatar_tabela_resumo(cls, df):
        df_formatado = df.copy()
        
        colunas_financeiras = ['vendas totais', 'comissão', 'cashback', 'Lucro']
        for col in colunas_financeiras:
            if col in df_formatado.columns:
                df_formatado[col] = df_formatado[col].apply(cls.moeda)
                
        if 'ROI' in df_formatado.columns:
            df_formatado['ROI'] = df_formatado['ROI'].apply(cls.porcentagem)
            
        return df_formatado
