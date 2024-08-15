from document_procesor import *
from calcular_promedio_mensual import *
from datetime import datetime
import pytz

# Obtener la zona horaria de México, Guanajuato (León está en la misma zona horaria)
zona_horaria = pytz.timezone('America/Mexico_City')

# Obtener la fecha y hora actual en la zona horaria específica
fecha_actual = datetime.now(zona_horaria)

# Mapa de los meses en español para evitar problemas con locale
meses_espanol = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo",
    6: "junio", 7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre",
    11: "noviembre", 12: "diciembre"
}

# Formatear el día, mes y año en español sin usar locale
dia_actual = fecha_actual.day
mes_actual = meses_espanol[fecha_actual.month]
año_actual = fecha_actual.year





def extraer_codigo_cic(codigo_ine):
    if "IDMEX" in codigo_ine:
        posicion_x = codigo_ine.find('X')
        
        codigo_relevante = codigo_ine[posicion_x + 1:13]
        return codigo_relevante
    else:
        return codigo_ine

def run(variables):
    # Extraer códigos INE relevantes
    variables["No_INE"] = extraer_codigo_cic(variables["No_INE"])
    variables["NO_INE_GESTOR"] = extraer_codigo_cic(variables["NO_INE_GESTOR"])
    variables["dia"]=dia_actual
    variables["mes"]=mes_actual
    variables["año"]=año_actual
    # Calcular el promedio mensual
    promedio_mensual = round(calcular_promedio_mensual(variables["consumo_periodo_actual"], variables["consumos_historicos"]),2)
    variables["promedio_mensual"] = promedio_mensual
    
    # Rutas originales de los documentos
    doc_paths = [
        '/mnt/data/contrato_distribuidor_vars.docx',
        '/mnt/data/contrato_suministrador_vars.docx'
    ]
    
    # Rutas donde quieres guardar los documentos editados
    output_paths = [
        '/mnt/data/contrato_distribuidor_editado.docx',
        '/mnt/data/contrato_suministrador_editado.docx'
    ]
    
    # Instanciamos el procesador de documentos con las rutas originales
    processor = DocumentProcessor(doc_paths)
    processor.process_multiple_documents(variables, output_paths)
    return output_paths

if __name__ == "__main__":
    run(variables)
