import os
import time
import pyodbc
import zipfile
import datetime
import pandas as pd
import urllib.request

inicio = time.time()

# Antes de iniciar o código é preciso criar algumas variáveis de data:

# Data atual e mês anterior
data_atual = datetime.date.today()
data_mes = data_atual.strftime("%Y%m")

print('Programa iniciado...')

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

## Baixar os arquivos da CVM ##

# URL do arquivo zip
url = f"https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{data_mes}.zip"

# Pasta de destino para salvar o arquivo
diretorio = r"C:\Users\Duda\PycharmProjects\ETL_dados_diarios_fundos_cvm/arquivos_zip"

#Nome do arquivo zip
zip_name = os.path.join(diretorio, f"inf_diario_fi_{data_mes}.zip")
#Nome do arquivo CSV dentro do zip
csv = fr"inf_diario_fi_{data_mes}.csv"
#caminho completo do csv
caminho_csv = os.path.join(diretorio, csv)

# Baixar o arquivo zip
urllib.request.urlretrieve(url, zip_name)
print("Arquivo ZIP baixado com sucesso!")
# Extrair os arquivos CSV do zip
with zipfile.ZipFile(zip_name, "r") as zip_ref:
    zip_ref.extract(csv, diretorio)
os.remove(zip_name)
print("Arquivos CSV extraído do ZIP com sucesso!")


#Transforma o CSV em um dataframe pandas
df_fundo = pd.read_csv(caminho_csv, encoding="cp1252", delimiter=";")
df_fundo = df_fundo.fillna("")
df_fundo.columns = [
    "TP_FUNDO_CLASSE"
    ,"CNPJ_FUNDO_CLASSE"
    ,"ID_SUBCLASSE"
    ,"DT_COMPTC"
    ,"VL_TOTAL"
    ,"VL_QUOTA"
    ,"VL_PATRIM_LIQ"
    ,"CAPTC_DIA"
    ,"RESG_DIA"
    ,"NR_COTST"
]
print("Total de linhas do CSV: ", len(df_fundo))
print('Arquivo acessado: ', caminho_csv)
print(f"Os dados do arquvo registro_fundo.csv serão inseridos na tabela dados_abertos_cvm.informe_diario_fundos...")

count_linhas_insert = 0

#Itera sobre os valores do dataframe para inserir os dados na tabela
for index, row in df_fundo.iterrows():
    TP_FUNDO_CLASSE = row["TP_FUNDO_CLASSE"] if pd.notna(row["TP_FUNDO_CLASSE"]) else None
    CNPJ_FUNDO_CLASSE = row["CNPJ_FUNDO_CLASSE"] if pd.notna(row["CNPJ_FUNDO_CLASSE"]) else None
    ID_SUBCLASSE = row["ID_SUBCLASSE"] if pd.notna(row["ID_SUBCLASSE"]) else None
    DT_COMPTC =  row["DT_COMPTC"]
    VL_TOTAL = pd.to_numeric(row["VL_TOTAL"], errors="coerce")
    VL_QUOTA = pd.to_numeric(row["VL_QUOTA"], errors="coerce")
    VL_PATRIM_LIQ = pd.to_numeric(row["VL_PATRIM_LIQ"], errors="coerce")
    CAPTC_DIA = pd.to_numeric(row["CAPTC_DIA"], errors="coerce")
    RESG_DIA = pd.to_numeric(row["RESG_DIA"], errors="coerce")
    NR_COTST = pd.to_numeric(row["NR_COTST"], errors="coerce")
    FLAG_SUBCLASSE = 0 if ID_SUBCLASSE == 'Não se aplica' else 1 #flag = a 1: fundo é uma subclasse

    #Insere os dados na tabela
    query_insert = f"""
    INSERT INTO dados_abertos_cvm.informe_diario_fundos
    VALUES (
    '{TP_FUNDO_CLASSE}'
    ,'{CNPJ_FUNDO_CLASSE}'
    ,case when '{ID_SUBCLASSE}' = '' THEN 'Não se aplica' else '{ID_SUBCLASSE}' END
    ,'{DT_COMPTC}'
    ,'{VL_TOTAL}'
    ,'{VL_QUOTA}'
    ,'{VL_PATRIM_LIQ}'
    ,'{CAPTC_DIA}'
    ,'{RESG_DIA}'
    ,{NR_COTST}
    ,{FLAG_SUBCLASSE}
    )
    ON CONFLICT (CNPJ_FUNDO_CLASSE, ID_SUBCLASSE, DT_COMPTC) DO NOTHING
    """
    try:
        #print(query_insert)
        cursor.execute(query_insert)
        conn.commit()
        count_linhas_insert += cursor.rowcount

        #print("Dados inseridos na tabela dados_abertos_cvm.informe_diario_fundos com sucesso!")

    except Exception as e:
        print(e)


print(f"Total de linhas inseridas: {count_linhas_insert}")
final = time.time()
tempo_execucao = final-inicio
tempo_minutoss = tempo_execucao/60
print("Programa finalizado!")
print(f"Tempo de execução: {tempo_execucao} segundos.")
print(f"Tempo de execução: {tempo_minutoss} minutos.")