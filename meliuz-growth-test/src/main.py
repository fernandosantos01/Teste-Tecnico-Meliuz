import argparse
import os
from data_processor import carregar_e_processar_dados
from ai_analyzer import AnalisadorTesteAB
from gerador_relatorio import GeradorRelatorio
from sheets_client import ClienteRastreamento
from logger_config import get_logger

logger = get_logger(__name__)

def main():
    analisador_argumentos = argparse.ArgumentParser(description="Analisador de Testes A/B AI-Native - Growth Méliuz")
    analisador_argumentos.add_argument('--file', type=str, required=True, help="Caminho para o arquivo CSV do dataset do parceiro")
    argumentos = analisador_argumentos.parse_args()
    
    caminho_arquivo = argumentos.file
    
    if not os.path.exists(caminho_arquivo):
        logger.error(f"Erro: O arquivo {caminho_arquivo} não foi encontrado.")
        return
        
    logger.info(f"Iniciando análise do dataset: {caminho_arquivo}...")
    
    logger.info("1. Processando e limpando dados...")
    df = carregar_e_processar_dados(caminho_arquivo)
    nome_parceiro = df['Parceiro'].iloc[0]
    
    logger.info("2. Rodando testes estatísticos...")
    analisador = AnalisadorTesteAB(df)
    vencedor, resultado_lucro, df_resumo = analisador.analisar_e_resumir()
    
    logger.info("3. Gerando relatório Markdown...")
    relatorio_md = GeradorRelatorio.gerar_markdown(nome_parceiro, resultado_lucro, df_resumo)
    
    os.makedirs('reports', exist_ok=True)
    nome_arquivo_relatorio = f"reports/relatorio_ab_teste_{nome_parceiro.replace(' ', '_')}.md"
    with open(nome_arquivo_relatorio, 'w', encoding='utf-8') as f:
        f.write(relatorio_md)
    logger.info(f"-> Relatório gerado com sucesso: {nome_arquivo_relatorio}")
    
    logger.info("4. Atualizando tracking (histórico)...")
    rastreador = ClienteRastreamento()
    nome_teste = f"Otimização de Cashback - {nome_parceiro}"
    rastreador.registrar_resultado(nome_teste, nome_parceiro, vencedor, resultado_lucro)
    
    logger.info("Análise concluída com sucesso! Verifique a pasta 'reports' para mais detalhes.")

if __name__ == "__main__":
    main()
