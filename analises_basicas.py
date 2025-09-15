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
#print(df.head(10))

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
    plt.ylabel("Captação líquida em milhões")
    plt.grid(True)
    # formatação do eixo X para MM/YYYY
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
    plt.xticks(rotation=45)  # deixa mais legível
    plt.show()

    return result

#captacao_liquida_mensal(df, "44.703.508/0001-21")

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

#print(top10_captacao_mensal(df, "2025-08"))

##################################################
# 3. Top 10 fundos por patrimônio líquido no mês #
##################################################

def top10_patrimonio_liquido(df, mes_ref):
    # converte dt_comptc para datetime
    df = df.copy()
    df['dt_comptc'] = pd.to_datetime(df['dt_comptc'], errors='coerce')

    # converte mes_ref para datetime
    mes_ref = pd.to_datetime(mes_ref)

    df["id_fundo"] = df.apply(
        lambda x: x["id_subclasse"] if x["flag_subclasse"] == 1 else x["cnpj_fundo_classe"], axis=1
    )

    aux = df[df['dt_comptc'] == mes_ref]
    result= (
        aux.groupby('id_fundo', as_index=False)
        .agg(patrimonio_liquido=('vl_total', 'max'))
        .sort_values('patrimonio_liquido', ascending=False)
        .head(10)
    )
    # adiciona a data de referência
    result['data_ref'] = mes_ref
    # formata como moeda BRL
    result['patrimonio_liquido'] = result['patrimonio_liquido'].map(
        lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

    return result

#print(top10_patrimonio_liquido(df, "2025-08-29")) #sempre o úlltimo dia útil do mês para ter o resultado do mês.

#######################################################
# 4. Top 10 fundos por número de cotistas em uma data #
#######################################################
def top10_num_cotistas(df, data_ref):
    df = df.copy()
    df['dt_comptc'] = pd.to_datetime(df['dt_comptc'], errors='coerce')
    data_ref = pd.to_datetime(data_ref)

    df['id_fundo'] = df.apply(lambda x: x['id_subclasse'] if x['flag_subclasse'] == 1 else x['cnpj_fundo_classe'], axis=1)

    aux = df[df['dt_comptc'] == data_ref]
    result = (
        aux.groupby('id_fundo', as_index=False)
        .agg(num_cotistas=('nr_cotst', 'max'))
        .sort_values('num_cotistas', ascending=False)
        .head(10)
    )
    # adiciona a data de referência
    result['data_ref'] = data_ref

    return result

#print(top10_num_cotistas(df, '2025-09-01'))

#################################################
# 5. Evolução do Patrimônio Líquido de um fundo #
#################################################

def evolucao_patrimonio_liquido(df, id_fundo):
    df = df.copy()
    df['dt_comptc'] = pd.to_datetime(df['dt_comptc'], errors='coerce')

    df['id_fundo'] = df.apply(lambda x: x['id_subclasse'] if x['flag_subclasse'] == 1 else x['cnpj_fundo_classe'], axis=1)
    aux = df[df['id_fundo'] == id_fundo][['id_fundo', 'dt_comptc', 'vl_total']].rename(columns={'vl_total': 'patrimonio_liquido'})
    aux = aux.sort_values('dt_comptc')

    # gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(aux['dt_comptc'], aux['patrimonio_liquido'], marker='o')
    plt.title(f"Evolução Patrimônio Líquido: {id_fundo}")
    plt.xlabel("Data")
    plt.ylabel("Patrimônio Líquido")
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    plt.xticks(rotation=45)
    plt.show()

    return aux

print(evolucao_patrimonio_liquido(df,'07.593.972/0001-86'))



final = time.time()
tempo_execucao = final-inicio
tempo_minutoss = tempo_execucao/60
print("Programa finalizado!")
print(f"Tempo de execução: {tempo_execucao} segundos.")
print(f"Tempo de execução: {tempo_minutoss} minutos.")