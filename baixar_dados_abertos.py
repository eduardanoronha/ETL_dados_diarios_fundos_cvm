import os
import time
import pyodbc
import zipfile
import datetime
import pandas as pd
import urllib.request
import platform
print(platform.architecture())

inicio = time.time()

# Antes de iniciar o código é preciso criar algumas variáveis de data:

# Data atual e mês anterior
data_atual = datetime.date.today()
data_mes = data_atual.strftime("%Y%m")

print('Programa iniciado...')

# Estabelecer a conexão com o banco de dados do SQL
print(pyodbc.drivers())
conn = pyodbc.connect(
    "DRIVER={PostgreSQL ODBC Driver(UNICODE)};"
    "SERVER=localhost;"
    "PORT=5432;"
    "DATABASE=projeto1;"
    "UID=eduardan;"
    "PWD=coutinho;"
)
cursor = conn.cursor()
print(cursor)

## Baixar os arquivos da CVM ##

# URL do arquivo zip
url = f"https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{data_mes}.zip"

# Pasta de destino para salvar o arquivo
diretorio = r"C:\Users\Duda\PycharmProjects\ETL_dados_diarios_fundos_cvm/arquivos_zip"

# Nome do arquivo zip
zip_name = os.path.join(diretorio, f"inf_diario_fi_{data_mes}.zip")

# Nome dos arquivos CSV dentro do zip
csv = fr"inf_diario_fi_{data_mes}.csv"

# Baixar o arquivo zip
urllib.request.urlretrieve(url, zip_name)
print("Arquivo ZIP baixado com sucesso!")
# Extrair os arquivos CSV do zip
with zipfile.ZipFile(zip_name, "r") as zip_ref:
    zip_ref.extract(csv, diretorio)
os.remove(zip_name)
print("Arquivos CSV extraídos do ZIP com sucesso!")


final = time.time()
tempo_execucao = final-inicio
print("Programa finalizado!")
print(f"Tempo de execução: {tempo_execucao} segundos.")