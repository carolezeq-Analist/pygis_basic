import geopandas as gpd # Biblioteca para manipulação de dados geoespaciais
import pandas as pd

#  Um Dash com Geopandas

caminho_es = r"C:\Users\carol\OneDrive\Imagens\PROJETOS\pygis\es_area\es_area.shp"
es = gpd.read_file(caminho_es)
df = es[['NM_MUN', 'area_km2_1', 'geometry']]
df = df.rename(columns={'NM_MUN': 'Municipio', 'area_km2_1': 'Area_km2'})
df = df.sort_values("Area_km2", ascending=False)
print(df.head())


# Criando os graficos por municipio
import plotly.express as px
fig = px.bar(df,
             x='Municipio',
             y='Area_km2',
             title='Área dos Municípios do Espírito Santo km2')
fig.show()

