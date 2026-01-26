from qgis.processing import alg
from qgis.core import (QgsProject, 
                       QgsProcessingFeatureSourceDefinition)
import processing

@alg(name="buffer_automacao", label="02 - Criar Buffer Automático", group="meus_scripts", group_label="Meus Scripts")
@alg.input(type=alg.VECTOR_LAYER, name="INPUT_LAYER", label="Camada para aplicar o Buffer")
@alg.input(type=alg.DISTANCE, name="DISTANCIA", label="Distancia do Buffer (metros/graus)", default=1000)
@alg.output(type=alg.VECTOR_LAYER, name="OUTPUT", label="Camada com Buffer")
def buffer_municipio_alg(instance, parameters, context, feedback, inputs):
    """
    Cria automaticamente uma area de influencia (buffer) ao redor 
    das feicoes da camada selecionada.
    """
    # 1. Obter parametros
    camada_entrada = instance.parameterAsVectorLayer(parameters, "INPUT_LAYER", context)
    distancia = instance.parameterAsDouble(parameters, "DISTANCIA", context)

    feedback.pushInfo(f"Calculando buffer de {distancia} unidades...")

    # 2. Executar o Buffer
    # 'SEGMENTS' define o quão redonda fica a borda (5 é o padrão)
    params_buffer = {
        'INPUT': camada_entrada,
        'DISTANCE': distancia,
        'SEGMENTS': 5,
        'END_CAP_STYLE': 0, # Round
        'JOIN_STYLE': 0,    # Round
        'MITER_LIMIT': 2,
        'DISSOLVE': False,  # Mude para True se quiser que os buffers se unam
        'OUTPUT': 'TEMPORARY_OUTPUT'
    }
    
    resultado = processing.run("native:buffer", params_buffer, context=context, feedback=feedback)

    # 3. Adicionar ao mapa
    final = resultado['OUTPUT']
    final.setName(f"Buffer_{distancia}m_{camada_entrada.name()}")
    QgsProject.instance().addMapLayer(final)
    
    return {"OUTPUT": final}