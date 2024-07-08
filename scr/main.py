#%% Import das bibliotecas
import pandas as pd
import numpy as np
import os
import sqlalchemy
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
#%% Gerador de planilhas com Segmentação RFV
def main():
    # Carregamento dos dados
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, '../data/processed/olist_data.db')
    query_path = os.path.join(current_dir, 'query.sql')

    engine = sqlalchemy.create_engine(f'sqlite:///{db_path}') 

    with open(query_path, 'r') as open_file:
        query = open_file.read()
    
    rfv = pd.read_sql(query, engine)
    # Pré-processamento
    rfv.fillna({'recenciaDias': rfv['recenciaDias'].max()}, inplace = True)
    rfv.fillna({'frequenciaCompras': 0, 'valorTotal': 0, 'valorMedio': 0}, inplace = True)

    feature_cols  = ['recenciaDias', 'frequenciaCompras', 'valorTotal', 'valorMedio']
    standard_data = rfv.copy()

    scaler = StandardScaler()
    scaler.fit(standard_data[feature_cols])

    standard_features = scaler.transform(rfv[feature_cols])
    standard_data[feature_cols] = standard_features

    # Clusterização
    kmeans = KMeans(n_clusters = 4, random_state = 42)
    kmeans.fit(standard_data[feature_cols])
    rfv['cluster'] = kmeans.labels_

    # Mapeamento dos Segmentos
    def segmentacao(row):
        if row['cluster'] == 0: 
            return 'Cliente Regular'    
        elif row['cluster'] == 1:   
            return 'Cliente em Risco'   
        elif row['cluster'] == 2:   
            return 'Cliente Fiel'   
        else:   
            return 'Cliente de Alto Valor'  
    
    rfv['segmentoCliente'] = rfv.apply(segmentacao, axis = 1)

    # Resultado
    output_file = 'data/processed/segmentacao_clientes.xlsx'
    rfv.to_excel(output_file, index = False)
    print(f'Resultados salvos em {output_file}')

if __name__ == "__main__":
    main()