import time
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

inicio = time.time()

print('Programa iniciado...')
print("")

# Estabelecer a conexão com o banco de dados do SQL
conn = pyodbc.connect(
    "DRIVER={PostgreSQL ODBC Driver(UNICODE)};"
    "SERVER=localhost;"
    "PORT=5432;"
    "DATABASE=projeto1;"
    "UID=eduardan;"
    "PWD=coutinho;"
)
cursor = conn.cursor()
print("Conexão com o SQL realizada com sucesso.")

query = """
SELECT * FROM dados_abertos_cvm.informe_diario_fundos
"""
df = pd.read_sql(query, conn)
print(df.head(10))

########################################
# 1. Captação líquida mensal por fundo #
########################################

def captacao_liquida_mensal(df, id_fundo):
    # converte dt_comptc para datetime
    df = df.copy()
    df['dt_comptc'] = pd.to_datetime(df['dt_comptc'], errors='coerce')

    df['mes'] = df['dt_comptc'].dt.to_period('M').dt.to_timestamp()
    df['id_fundo'] = df.apply(lambda x: x['id_subclasse'] if x['flag_subclasse'] == 1 else x['cnpj_fundo_classe'],axis=1)
    aux = df[df['id_fundo'] == id_fundo].copy()
    result = aux.groupby(['mes', 'id_fundo']).apply(lambda x: (x['captc_dia'] - x['resg_dia']).sum()).reset_index(
        name='captacao_liquida_mensal')

    # gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(result['mes'], result['captacao_liquida_mensal'], marker='o')
    plt.title(f"Captação líquida mensal: {id_fundo}")
    plt.xlabel("Mês")
    plt.ylabel("Captação líquida")
    plt.grid(True)
    # formatação do eixo X para MM/YYYY
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
    plt.xticks(rotation=45)  # deixa mais legível
    plt.show()

    return result

#captacao_liquida_mensal(df, "11.233.045/0001-22")

#####################################
# 2. Top 10 Captação líquida no mês #
#####################################

def top10_captacao_mensal(df, mes_ref):
    # converte dt_comptc para datetime
    df = df.copy()
    df['dt_comptc'] = pd.to_datetime(df['dt_comptc'], errors='coerce')

    # converte mes_ref para datetime
    mes_ref = pd.to_datetime(mes_ref)

    df['mes'] = df['dt_comptc'].dt.to_period('M').dt.to_timestamp()
    df['id_fundo'] = df.apply(lambda x: x['id_subclasse'] if x['flag_subclasse'] == 1 else x['cnpj_fundo_classe'], axis=1)
    aux = df[df['mes'] == mes_ref]
    result = (
        aux.assign(captacao_liquida=(aux['captc_dia'] - aux['resg_dia']))
        .groupby(['mes', 'id_fundo'], as_index=False)
        .agg(captacao_liquida_mensal=('captacao_liquida', 'sum'))
        .sort_values('captacao_liquida_mensal', ascending=False)
        .head(10)
    )

    # formata a coluna como moeda BRL
    result['captacao_liquida_mensal'] = result['captacao_liquida_mensal'].map(
        lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

    return result

print(top10_captacao_mensal(df, "2025-08-01"))