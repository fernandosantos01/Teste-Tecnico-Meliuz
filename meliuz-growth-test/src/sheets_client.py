import os
import csv
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

CABECALHO = ['Data da Análise', 'Nome do Teste', 'Parceiro', 'Variante Vencedora', 'Significância Estatística', 'P-Value']

class TrackingClient:
    def __init__(self, caminho_csv_fallback='data/historico_testes.csv'):
        self.caminho_csv_fallback = caminho_csv_fallback
        self.usar_sheets = False
        
        self.caminho_credenciais = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        self.url_planilha = os.getenv('SPREADSHEET_URL')
        
        if self.caminho_credenciais and self.url_planilha and os.path.exists(self.caminho_credenciais):
            try:
                escopo = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
                credenciais = ServiceAccountCredentials.from_json_keyfile_name(self.caminho_credenciais, escopo)
                cliente = gspread.authorize(credenciais)
                self.planilha = cliente.open_by_url(self.url_planilha).sheet1
                self.usar_sheets = True
                
                dados = self.planilha.get_all_values()
                if not dados or dados[0][0] != 'Data da Análise':
                    self.planilha.insert_row(CABECALHO, index=1)
                    
                print("Conectado ao Google Sheets com sucesso.")
            except Exception as e:
                print(f"Aviso: Falha ao conectar no Google Sheets: {e}. Usando fallback para CSV.")
                self.usar_sheets = False
                
    def registrar_resultado(self, nome_teste, parceiro, vencedor, resultado_lucro):
        str_data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        eh_significativo = 'Sim' if resultado_lucro['eh_significativo'] else 'Não'
        valor_p = f"{resultado_lucro['valor_p']:.4f}"
        
        linha = [str_data, nome_teste, parceiro, vencedor, eh_significativo, valor_p]
        
        if self.usar_sheets:
            try:
                self.planilha.append_row(linha)
                print(f"Resultado registrado no Google Sheets: {self.url_planilha}")
                return
            except Exception as e:
                print(f"Erro ao salvar no Sheets: {e}. Salvando no CSV.")
        
        arquivo_existe = os.path.isfile(self.caminho_csv_fallback)
        
        with open(self.caminho_csv_fallback, mode='a', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            if not arquivo_existe:
                escritor.writerow(CABECALHO)
            escritor.writerow(linha)
            
        print(f"Resultado registrado localmente em: {self.caminho_csv_fallback}")
