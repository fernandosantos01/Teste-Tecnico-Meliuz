import os
import pytest
from unittest.mock import patch, mock_open, MagicMock
from sheets_client import ClienteRastreamento

# Simula as credenciais estando presentes para não falhar no CI/CD
@patch('sheets_client.os.path.exists', return_value=True)
@patch('sheets_client.os.getenv', side_effect=lambda k: 'fake_value' if k in ['GOOGLE_APPLICATION_CREDENTIALS', 'SPREADSHEET_URL'] else None)
@patch('sheets_client.ServiceAccountCredentials.from_json_keyfile_name')
@patch('sheets_client.gspread.authorize')
def test_sincronizacao_offline_com_sucesso(mock_gspread_auth, mock_creds, mock_getenv, mock_exists):
    # Simula a estrutura do gspread
    mock_planilha = MagicMock()
    # Finge que a planilha já tem o cabeçalho
    mock_planilha.get_all_values.return_value = [['Data da Análise', 'Nome do Teste', 'Descrição', 'Resultado', 'Decisão Tomada']]
    
    mock_cliente = MagicMock()
    mock_cliente.open_by_url.return_value.sheet1 = mock_planilha
    mock_gspread_auth.return_value = mock_cliente
    
    # Simula um CSV de cache na máquina local
    fake_csv_content = "Data da Análise,Nome do Teste,Descrição,Resultado,Decisão Tomada\n2026-07-16 10:00:00,Teste A,Desc A,Res A,Dec A\n2026-07-16 10:05:00,Teste B,Desc B,Res B,Dec B"
    
    with patch('builtins.open', mock_open(read_data=fake_csv_content)):
        with patch('sheets_client.os.path.isfile', return_value=True):
            with patch('sheets_client.os.remove') as mock_remove:
                # O __init__ da classe automaticamente tenta conectar e aciona a sincronização
                cliente = ClienteRastreamento(caminho_csv_fallback='fake.csv')
                
                # Valida se a nuvem foi ativada
                assert cliente.usar_sheets is True
                
                # Valida se subiu o lote (padrão Outbox) corretamente, pulando o cabeçalho
                mock_planilha.append_rows.assert_called_once_with([
                    ['2026-07-16 10:00:00', 'Teste A', 'Desc A', 'Res A', 'Dec A'],
                    ['2026-07-16 10:05:00', 'Teste B', 'Desc B', 'Res B', 'Dec B']
                ])
                
                # Valida se o cache local foi apagado após o upload bem-sucedido
                mock_remove.assert_called_once_with('fake.csv')
