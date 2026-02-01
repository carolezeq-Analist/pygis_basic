# Juntando CRS e cálculo de área em um pipeline

import geopandas as gpd


def pipeline_processamento(caminho_entrada, epsg_destino=31984):
    gdf = gpd.read_file(caminho_entrada)
    print(f"arquivo carregado. CRS original: {gdf.crs}")
    gdf = gdf.to_crs(epsg=epsg_destino)
    print(f"CRS convertido para EPSG: {epsg_destino}")
    gdf['area_m2'] = gdf.geometry.area
    gdf['area_km2'] = gdf['area_m2'] / 1_000_000
    print("Área calculada com sucesso")
    return gdf 

# Opicional se eu quiser de um municipio especifico
# gdf = gdf[gdf['SIGLA_UF'] == 'ES']
# print("Filtro do Espirito Santo aplicado!")

caminho_br = r"C:\Users\carol\OneDrive\Imagens\PROJETOS\pygis\BR_Municipios_2024\BR_Municipios_2024.shp"
    
municipios_processados = pipeline_processamento(caminho_br)
municipios_processados.to_file("municipios_final_com_area.shp")
print("Arquivo salvo e pronto")