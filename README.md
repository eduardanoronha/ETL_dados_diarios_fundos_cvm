# 📊 Análises dos dados diários de Fundos de Investimento - CVM

## 📌 Descrição
Este projeto coleta, trata, armazena e analisa dados diários de fundos de investimento divulgados pela CVM, permitindo análises exploratórias em SQL, Python e Power BI.  

---

## 🎯 Motivação
Fundos de investimentos são um produto de grande interesse tanto para empresas do o mercado financeiro quanto para investidores em geral.  
Além disso, os dados da CVM são públicos e acessíveis, o que torna o projeto replicável e útil como portfólio de análise de dados.  
Tenho background profissional com dados qualitativos de fundos, e esse projeto me permitiu aprofundar no lado quantitativo.  

---

## 🛠️ Tecnologias Utilizadas
- **Python** (Pandas, matplotlib, urllib, requests, pyodbc, zipfile)  
- **SQL** (PostgreSQL)  
- **Power BI**  
- **Git/GitHub**  

---

## 🔄 Arquitetura do Projeto
1. **Coleta** → Download do CSV da CVM via script em Python, usando as bibliotecas **urllib** para download e **zipfile** para extração dos documentos do arquivo zip.  
2. **Transformações** → Ajuste de tipos de dados, tratamento de nulos e criação da medida `flag_subclasse` para diferenciar **classe x subclasse** de fundos.  
   - 📌 *Por que isso é importante?*  
     A CVM publica os dados a nível de classe ou subclasse, a depender de como é a estrutura do fundo e em qual nível suas cotas são negociadas.
     Essa flag permite identificar se os dados analisados para um determinado fundo são a nível de classe ou subclasse.  
3. **Armazenamento** → Criação de tabela no **PostgreSQL** para centralizar os dados.  
   - Código SQL de criação incluído em [`arquivos_sql/create_table.sql`].  
4. **Análises** →  
   - Queries em **SQL** (Captação líquida, número de cotistas, patrimônio líquido, Retorno).  
   - Funções em **Python** para replicar análises e gerar gráficos.  (resultados das análises na pasta [`\visualizacao_resultados`])
5. **Dashboards** → Exploração visual no **Power BI**, com foco em:  
   - Evolução do patrimônio líquido.  
   - Retorno diário e mensal.  
   - Captação líquida (diária e mensal).  
   - Top 10 fundos em diferentes métricas.  

---

## 📊 Detalhamento do dashboard em Power BI
1. **Importação dos Dados** → Conexão direta com o banco PostgreSQL criado na etapa anterior e carregamento através de uma consulta à tabela.
2. **Transformações no Power Query** → Ajustes de tipos de dados e nomes das colunas.
3. **Criação de Medidas DAX**
   Exemplos de medidas implementadas:
   - Captação Líquida = Entradas – Saídas de recursos
   - Retorno Diário e Mensal com base na variação do patrimônio
4. **Construção dos Visuais**
  - Visuais de segmentação de dados para filtrar os demais visuais da página por fundo e data
  - Evolução temporal: linha/área mostrando crescimento do patrimônio e retornos
  - Ranking Top 10: gráfico de barras comparando fundos com maior captação e maior patrimônio líquido
  - Indicadores principais: cartões com valores de patrimônio total, nº de fundos ativos e captação líquida acumulada.

---

## 🖼️ Exemplos dos Visuais
<img width="1215" height="667" alt="image" src="https://github.com/user-attachments/assets/91af3130-410f-4f06-9744-fc8e825b6799" />
<img width="1227" height="687" alt="image" src="https://github.com/user-attachments/assets/fcb55722-0ad3-44eb-8cb8-30e138d8b156" />

---

## 📊 Resultados Principais
- Ranking dos **Top 10 fundos por captação líquida**
- Ranking dos **Top 10 fundos por patrimônio líquido**
- Ranking dos **Top 10 fundos por número de cotitstas**.
- Evolução do **Patrimônio Líquido** de fundos específicos
- Evolução do **captação líquida** de fundos específicos
- **Retorno diário** e **retorno em 30 dias** por fundo
- Dashboards interativos no Power BI para análise dinâmica 

---
