import argparse
import os
from data_processor import carregar_e_processar_dados
from ai_analyzer import ABTestAnalyzer
from sheets_client import TrackingClient

def main():
    analisador_argumentos = argparse.ArgumentParser(description="Analisador de Testes A/B AI-Native - Growth Méliuz")
    analisador_argumentos.add_argument('--file', type=str, required=True, help="Caminho para o arquivo CSV do dataset do parceiro")
    argumentos = analisador_argumentos.parse_args()
    
    caminho_arquivo = argumentos.file
    
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: O arquivo {caminho_arquivo} não foi encontrado.")
        return
        
    print(f"Iniciando análise do dataset: {caminho_arquivo}...")
    
    print("1. Processando e limpando dados...")
    df = carregar_e_processar_dados(caminho_arquivo)
    nome_parceiro = df['Parceiro'].iloc[0]
    
    print("2. Rodando testes estatísticos...")
    analisador = ABTestAnalyzer(df)
    relatorio_md, vencedor, resultado_lucro = analisador.gerar_relatorio()
    
    os.makedirs('reports', exist_ok=True)
    nome_arquivo_relatorio = f"reports/relatorio_ab_teste_{nome_parceiro.replace(' ', '_')}.md"
    with open(nome_arquivo_relatorio, 'w', encoding='utf-8') as f:
        f.write(relatorio_md)
    print(f"-> Relatório gerado com sucesso: {nome_arquivo_relatorio}")
    
    print("3. Atualizando tracking (histórico)...")
    rastreador = TrackingClient()
    nome_teste = f"Otimização de Cashback - {nome_parceiro}"
    rastreador.registrar_resultado(nome_teste, nome_parceiro, vencedor, resultado_lucro)
    
    print("\nAnálise concluída com sucesso! Verifique a pasta 'reports' para mais detalhes.")

if __name__ == "__main__":
    main()
