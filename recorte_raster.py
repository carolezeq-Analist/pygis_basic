from qgis.processing import alg
from qgis.core import (QgsProject, 
                       QgsProcessingFeatureSourceDefinition)
import processing

@alg(name="recorte_raster_mun", label="03 - Recortar RASTER por Municipio", group="meus_scripts", group_label="Meus Scripts")
@alg.input(type=alg.VECTOR_LAYER, name="MUNICIPIOS", label="Camada de Municipios (Vetor)")
@alg.input(type=alg.RASTER_LAYER, name="RASTER_ALVO", label="Imagem/Raster para Recortar")
@alg.input(type=alg.STRING, name="NOME_MUN", label="Nome do Municipio (NM_MUN)", default="Nova Olinda")
@alg.output(type=alg.RASTER_LAYER, name="OUTPUT", label="Raster Recortado")
def recorte_raster_alg(instance, parameters, context, feedback, inputs):
    """
    Recorta uma camada RASTER usando o limite de um municipio (Vetor) 
    extraido da coluna NM_MUN.
    """
    camada_mun = instance.parameterAsVectorLayer(parameters, "MUNICIPIOS", context)
    raster_alvo = instance.parameterAsRasterLayer(parameters, "RASTER_ALVO", context)
    nome = instance.parameterAsString(parameters, "NOME_MUN", context)

    # 1. Selecionar o municipio (Vetor)
    expressao = f"\"NM_MUN\" = '{nome}'"
    camada_mun.selectByExpression(expressao)

    if camada_mun.selectedFeatureCount() == 0:
        feedback.reportError(f"Municipio {nome} nao encontrado!")
        return {}

    # 2. Executar o Clip do RASTER (GDAL)
    feedback.pushInfo(f"Recortando Raster para: {nome}...")
    
    params_raster = {
        'INPUT': raster_alvo,
        'MASK': QgsProcessingFeatureSourceDefinition(camada_mun.id(), selectedFeaturesOnly=True),
        'NODATA': None,
        'ALPHA_BAND': False,
        'CROP_TO_CUTLINE': True, # Isso faz a imagem ficar do tamanho exato do recorte
        'KEEP_RESOLUTION': True,
        'OPTIONS': '',
        'DATA_TYPE': 0, # Use o tipo original
        'OUTPUT': 'TEMPORARY_OUTPUT'
    }
    
    res = processing.run("gdal:cliprasterbymasklayer", params_raster, context=context, feedback=feedback)

    # 3. Adicionar ao mapa
    final = res['OUTPUT']
    final_layer = QgsProject.instance().addMapLayer(QgsProject.instance().createLayerFromFile(final))
    final_layer.setName(f"Raster_{nome}")
    
    camada_mun.removeSelection()
    return {"OUTPUT": final}