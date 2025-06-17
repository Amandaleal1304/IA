import pandas as pd
from datetime import datetime, timedelta

# Parâmetros
inicio = datetime(2025, 5, 5)
horas_por_dia = 6
horas_totais = 300
dias_uteis_por_semana = 5
horas_por_semana = horas_por_dia * dias_uteis_por_semana
dias_uteis_necessarios = horas_totais // horas_por_dia

# Criar lista com datas e horas
datas = []
horas = []

data_atual = inicio
dias_contados = 0

while dias_contados < dias_uteis_necessarios:
    if data_atual.weekday() < 5:  # 0-4 são dias úteis (segunda a sexta)
        datas.append(data_atual.strftime('%d/%m/%Y'))
        horas.append(horas_por_dia)
        dias_contados += 1
    else:
        datas.append(data_atual.strftime('%d/%m/%Y'))
        horas.append(0)
    data_atual += timedelta(days=1)

# Adicionar os últimos dias do período com 0 horas até o final do mês de julho (31/07/2025)
fim = datetime(2025, 7, 31)
while data_atual <= fim:
    datas.append(data_atual.strftime('%d/%m/%Y'))
    horas.append(0)
    data_atual += timedelta(days=1)

# Criar DataFrame
df = pd.DataFrame({
    'Data': datas,
    'Horas Estágio': horas
})

# Salvar em arquivo Excel
arquivo = '/mnt/data/tabela_acompanhamento_estagio.xlsx'
df.to_excel(arquivo, index=False)

arquivo
