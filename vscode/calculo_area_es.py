# Calcular a área de Espírito Santo em km²

import geopandas as gpd

def calcular_area_km2(dados_geograficos):
    dados_geograficos ["area_m2"] = dados_geograficos.geometry.area
    dados_geograficos ["area_km2"] = dados_geograficos ["area_m2"] / 1000000
    if dados_geograficos.crs.is_geographic:
        raise ValueError("Reprojete antes de calcular área")
    return dados_geograficos


caminho_es_utm = r"C:\Users\carol\OneDrive\Imagens\PROJETOS\pygis\es_utm\es_utm.shp"
gdf_original = gpd.read_file(caminho_es_utm)

gdf_com_area = calcular_area_km2(gdf_original)
gdf_com_area.to_file(r"C:\Users\carol\OneDrive\Imagens\PROJETOS\pygis\es_area\es_area.shp")

