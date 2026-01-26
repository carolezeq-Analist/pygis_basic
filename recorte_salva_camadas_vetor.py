from qgis.processing import alg
from qgis.core import QgsProject, QgsProcessingFeatureSourceDefinition
import processing
import os

@alg(name="exportar_recortes_v3", label="08 - Recortar e SALVAR (Versão Final)", group="meus_scripts", group_label="Meus Scripts")
@alg.input(type=alg.VECTOR_LAYER, name="MUNICIPIOS", label="Camada BR_Municipios_2024")
@alg.input(type=alg.STRING, name="NOME_MUN", label="Nome do Municipio", default="Nova Olinda")
@alg.input(type=alg.STRING, name="CAMINHO_PASTA", label="Cole o caminho da pasta aqui (Ex: C:/Mapas)")
@alg.output(type=alg.NUMBER, name="TOTAL", label="Total de arquivos salvos")
def exportar_recortes_alg(instance, parameters, context, feedback, inputs):
    """
    Recorta e salva arquivos permanentemente na pasta indicada.
    """
    camada_mun = instance.parameterAsVectorLayer(parameters, "MUNICIPIOS", context)
    nome_mun = instance.parameterAsString(parameters, "NOME_MUN", context)
    # Pegamos o caminho como texto para evitar erros de compatibilidade
    pasta_raiz = instance.parameterAsString(parameters, "CAMINHO_PASTA", context).replace('\\', '/')
    
    # 1. Selecionar Municipio
    camada_mun.selectByExpression(f"\"NM_MUN\" = '{nome_mun}'")
    
    if camada_mun.selectedFeatureCount() == 0:
        feedback.reportError(f"Municipio {nome_mun} nao encontrado!")
        return {"TOTAL": 0}

    contador = 0
    # 2. Percorrer camadas do projeto
    for camada in QgsProject.instance().mapLayers().values():
        if camada.id() == camada_mun.id(): continue
        
        nome_limpo = f"{nome_mun}_{camada.name()}".replace(" ", "_")
        caminho_completo = os.path.join(pasta_raiz, nome_limpo)

        # Se for VETOR -> Salvar como Shapefile
        if camada.type() == 0:
            processing.run("native:clip", {
                'INPUT': camada,
                'OVERLAY': QgsProcessingFeatureSourceDefinition(camada_mun.id(), selectedFeaturesOnly=True),
                'OUTPUT': caminho_completo + ".shp"
            }, context=context, feedback=feedback)
            contador += 1
            
        # Se for RASTER -> Salvar como GeoTIFF
        elif camada.type() == 1:
            processing.run("gdal:cliprasterbymasklayer", {
                'INPUT': camada,
                'MASK': QgsProcessingFeatureSourceDefinition(camada_mun.id(), selectedFeaturesOnly=True),
                'CROP_TO_CUTLINE': True,
                'OUTPUT': caminho_completo + ".tif"
            }, context=context, feedback=feedback)
            contador += 1

    camada_mun.removeSelection()
    feedback.pushInfo(f"✅ Sucesso! {contador} arquivos exportados para {pasta_raiz}")
    return {"TOTAL": contador}

