from document_procesor import *

# Diccionario de variables y sus valores
variables = {
    "nombre_cliente": "John Doe",
    "nombre_gestor": "Jane Smith",
    "No_INE": "1234567890123",
    "promedio_mensual": "5000",
    "voltaje_tension": "220V",
    "RPU": "987654321",
    "RMU": "567890123",
    "cuenta": "1234567890",
    "direccion_cliente": "123 Main Street, City, Country",
    "tarifa": "1C",
    "numero_hilos": "3",
    "numero_medidor": "5432109876",
    "demanda_contratada": "50 kW",
    "demanda_instalada": "60 kW",
    "telefono_cliente": "555-1234",
    "correo_cliente": "cliente@example.com",
    "ciudad": "Irapuato",
    "dia": "16",
    "mes":"julio",
    "año":"2024",
    "No_INE_gestor": "0987654321098"
}

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
