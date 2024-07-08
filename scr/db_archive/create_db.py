# %% Importação das bibliotecas
import pandas as pd
import sqlalchemy
import os
# %% Função para criar o arquivo .db 
def csv_to_sqlite(db_name, directory):
    engine = sqlalchemy.create_engine(f'sqlite:///{db_name}')
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

    for csv_file in csv_files:
        csv_path = os.path.join(directory, csv_file)
        table_name = os.path.splitext(csv_file)[0]

        df = pd.read_csv(csv_path)
        df.to_sql(table_name, engine, if_exists = 'replace', index = False)
# %% Definição de diretórios
directory = '../../data/raw'
db_name = '../../data/processed/olist_data.db'
# %% Aplicação da função
csv_to_sqlite(db_name, directory)