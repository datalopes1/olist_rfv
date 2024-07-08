# Gerando Planilhas de Análise RFV com Python 🏪

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) contém dados de transações realizadas por dirversos pequenos negócios brasileiros cadastrados na plataforma de vendas para marketplace. Estes pequenos negócios conseguem através do [Olist Store](https://olist.com/) vender seus produtos diretamente e os enviar através dos parceiros logísticos da Olist. 

![olist](https://i.imgur.com/EoWCjR8.jpeg)

### Objetivos e resultados
A análise RFV (recencia, frequência e valor) é uma forma de fazer segmentação de clientes utilizada por setores de Marketing e CRM. Existem diversas maneiras de realizar este tipo de análise e para este projeto foi escolhida a Clusterização utilizando o algoritmo KMeans. 

O objetivo portanto é usar as linguagens Python e SQL (com SQLite), para criar um código capaz de gerar uma planilha (.xlsx) com a segmentação dos clientes. 

### 🛠️ Ferramentas utilizadas
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white) ![Microsoft Excel](https://img.shields.io/badge/Microsoft_Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)

## Estrutura dos Dados
![schema](https://i.imgur.com/HRhd2Y0.png)

## Bibliotecas Python utilizadas
#### Manipulação de dados
- Pandas, Numpy, OS, sqlalchemy
#### Visualizações
- Seaborn, Matplotlib
#### Machine Learning e Feature Engineering
- sklearn
# Criação do arquivo .db do SQLite
O primeiro passo no projeto foi transformar os arquivos .csv que foram disponibilizados no Kaggle.
```python
import pandas as pd
import sqlalchemy
import os

def csv_to_sqlite(db_name, directory):
    engine = sqlalchemy.create_engine(f'sqlite:///{db_name}')
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

    for csv_file in csv_files:
        csv_path = os.path.join(directory, csv_file)
        table_name = os.path.splitext(csv_file)[0]

        df = pd.read_csv(csv_path)
        df.to_sql(table_name, engine, if_exists = 'replace', index = False)

directory = '../../data/raw'
db_name = '../../data/processed/olist_data.db'

csv_to_sqlite(db_name, directory)
```
**Porque criar este database do SQLite?** A linguagem SQL é uma base sólida da carreira do Analista ou Cientista de Dados. O mais rotineiro em projetos reais será ter contato com bancos de dados e não .csv prontos para manipulação.
# Gerando a tabela de análise RFV
O passo seguinte é a criação de uma tabela que classifique os clientes por sua Recencia, Frequência e Valor Monetários gerados a empresa. 
```sql
WITH tb_rf AS(
SELECT 
    t1.customer_unique_id AS idCustomer,
    CAST(julianday('2018-10-31') - MAX(julianday(DATE(t2.order_approved_at))) AS INTEGER) AS recenciaDias,
    COUNT(t2.customer_id) AS frequenciaCompras
FROM olist_customers_dataset AS t1
LEFT JOIN 
    olist_orders_dataset AS t2
    ON t1.customer_id = t2.customer_id
GROUP BY idCustomer),

tb_val AS(
SELECT 
    t3.customer_unique_id AS idCustomer,
    SUM(t1.payment_value) AS valorTotal,
    AVG(t1.payment_value) AS valorMedio

FROM olist_order_payments_dataset AS t1
LEFT JOIN olist_orders_dataset AS t2
ON t1.order_id = t2.order_id

LEFT JOIN olist_customers_dataset AS t3
ON t2.customer_id = t3.customer_id

GROUP BY idCustomer)

SELECT 
    '2018-10-31' AS dtRef,
    t1.*,
    t2.valorTotal,
    t2.valorMedio
FROM tb_rf AS t1
LEFT JOIN tb_val AS t2
ON t1.idCustomer = t2.idCustomer
```
# Definindo a segmentação
A definição do número de clusters foi realizada através do metodo do cotovelo, e teve como resultado 4 clusters.
![cotov](https://i.imgur.com/e9YBlny.png)

Após a aplicação do algoritmo e análise dos resultados a segmentação foi definida em:
- Cliente Regular: Tem a maior recencia, frequência e valores médios.
- Cliente em Risco: Tem baixa recencia, frequência e valor.
- Cliente Fiel: Tem alta recencia, maior frequência e alto valor.
- Cliente de Alto Valor: Tem recencia média, alta frequêncai e maior valor. 

E com isso ao final do processo será gerado um arquivo .xlsx com os valores de Data de Referência, ID Único do Cliente, Recencia, Frequencia, Valor e Segmento. 