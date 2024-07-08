#%% Importação das bibliotecas
# Manipulação de dados
import pandas as pd
import numpy as np
import sqlalchemy

# Visualizações 
import matplotlib.pyplot as plt
import seaborn as sns

# Pré-processamento e Clusterização
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
# %% Criação de engine
engine = sqlalchemy.create_engine('sqlite:///../../data/processed/olist_data.db')
with open ('rfv_query.sql', 'r') as open_file:
    query = open_file.read()
# %% Carregamento dos dados
df = pd.read_sql(query, engine)
df.head()
# %% Imputações
df.fillna({'recenciaDias': df['recenciaDias'].max()}, inplace = True)
df.fillna({'frequenciaCompras': 0, 'valorTotal': 0, 'valorMedio': 0}, inplace = True)
# %% Aplicação do StandardScaler()
feature_cols  = ['recenciaDias', 'frequenciaCompras', 'valorTotal', 'valorMedio']
standard_data = df.copy()

scaler = StandardScaler()
scaler.fit(standard_data[feature_cols])

standard_features = scaler.transform(df[feature_cols])
standard_data[feature_cols] = standard_features
# %% Definição do número de Clusters com o Metodo do Cotovelo
data = standard_data.iloc[:, [2, 3, 4]].values

k_range = range(1, 16)
distortions = []
k_values = []

for k in k_range:
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(data)
    distortions.append(kmeans.inertia_)
    k_values.append(k)

fig = plt.figure(figsize = (8, 6))
ax = fig.add_axes([0, 0, 1, 1])

plt.plot(k_values, distortions)
ax.set_title("Método do Cotovelo", loc = "left", fontsize = 16, pad = 10)
ax.set_xlabel("Número de Clusters", fontsize = 10)
ax.set_ylabel("Distorção", fontsize = 10)
plt.show()
# %% Aplicação do KMeans
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans.fit(standard_data[feature_cols])

df['Cluster'] = kmeans.labels_
df.head()
# %% Agrupamento do DataFrame para nomeação dos Clusters/Segmentos
df.groupby('Cluster').agg(
    {
        'idCustomer': 'nunique',
        'recenciaDias': 'mean',
        'frequenciaCompras': 'mean',
        'valorTotal': 'mean',
        'valorMedio': 'mean'
    }
).reset_index()
# %% Função de segmentação
def segmentacao(row):
    if row['Cluster'] == 0:
        return 'Cliente Regular'
    elif row['Cluster'] == 1:
        return 'Cliente em Risco'
    elif row['Cluster'] == 2:
        return 'Cliente Fiel'
    else:
        return 'Cliente de Alto Valor'
# %% Aplicação da função
df['Segmentação'] = df.apply(segmentacao, axis = 1)
df.head()
# %% Salvando os resultados de teste
output_file = '../../data/processed/segmentacao_rfv_testfile.xlsx'
df.to_excel(output_file, index = False)