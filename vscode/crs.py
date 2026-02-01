# Verificando Crs do shapefile de municípios do Espírito Santo e mudando para o de sua area

import geopandas as gpd 

caminho_es = r"C:\Users\carol\OneDrive\Imagens\PROJETOS\pygis\municipios_es.shp"
es = gpd.read_file(caminho_es)
print("CRS ORIGINAL ES:", es.crs)
es_utm = es.to_crs(epsg=32724)
print("CRS UTM ES:", es_utm.crs)

saida_shp = r"C:\Users\carol\OneDrive\Imagens\PROJETOS\pygis\es_utm.shp"
es_utm.to_file(saida_shp)