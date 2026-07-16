from formatador import FormatadorApresentacao

def test_formata_moeda_padrao_br():
    valor = 1543.5
    resultado = FormatadorApresentacao.moeda(valor)
    assert resultado == "R$ 1.543,50"

def test_formata_porcentagem():
    valor = 1.23
    resultado = FormatadorApresentacao.porcentagem(valor)
    assert resultado == "123,00%"
