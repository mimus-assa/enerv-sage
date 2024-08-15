from document_procesor import *
from calcular_promedio_mensual import *
from datetime import datetime
import pytz

import locale


# Configurar la localización en español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# Obtener la zona horaria de México, Guanajuato
zona_horaria = pytz.timezone('America/Mexico_City')

# Obtener la fecha y hora actual en la zona horaria específica
fecha_actual = datetime.now(zona_horaria)

# Formatear el día, mes y año en español
dia_actual = fecha_actual.day
mes_actual = fecha_actual.strftime('%B').lower()  # mes en formato completo y en minúsculas
año_actual = fecha_actual.year
variables = {
    # referente al recibo
    "nombre_cliente": "John Doe",
    "RPU": "987654321",
    "RMU": "567890123",
    "cuenta": "1234567890",
    "direccion_cliente": "123 Main Street, City, Country",
    "tarifa": "1C",
    "numero_hilos": "3",
    "numero_medidor": "5432109876",
    "consumo_periodo_actual": 300,
    "consumos_historicos": [350, 400, 500, 600, 300, 280, 240, 550, 600],
    "demanda_contratada": "50 kW",
    "demanda_instalada": "60 kW",
    "ciudad": "irapuato",

    # calculado
    "promedio_mensual": "",  # Esto se actualizará después

    # fecha
    "dia": dia_actual,
    "mes": mes_actual,
    "año": año_actual,

    # datos específicos
    "voltaje_tension": "220V",
    "telefono_cliente": "555-1234",
    "correo_cliente": "cliente@example.com",

    # ine cliente
    "No_INE": "1234567890123",

    # ine gestor
    "No_INE_gestor": "0987654321098",
    "nombre_gestor": "Jane Smith",
}

# Calcular el promedio mensual
promedio_mensual = calcular_promedio_mensual(variables["consumo_periodo_actual"], variables["consumos_historicos"])
variables["promedio_mensual"] = promedio_mensual


# Rutas originales de los documentos
doc_paths = [
    'mnt/data/contrato_distribuidor_vars.docx',
    'mnt/data/contrato_suministrador_vars.docx'
]

# Rutas donde quieres guardar los documentos editados
output_paths = [
    'mnt/data/contrato_distribuidor_editado.docx',
    'mnt/data/contrato_suministrador_editado.docx'
]

# Instanciamos el procesador de documentos con las rutas originales
processor = DocumentProcessor(doc_paths)
processor.process_multiple_documents(variables, output_paths)
