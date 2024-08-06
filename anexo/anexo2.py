import PyPDF2
from fpdf import FPDF
from text_anexo2 import *

# Definir las variables
variables = {
    "fecha": "28/07/2024",
    "nombre_cliente": "Juan Pérez",
    "domicilio_calle": "Calle Falsa",
    "domicilio_no_exterior": "123",
    "domicilio_no_interior": "4B",
    "domicilio_zip": "12345",
    "domicilio_colonia": "Colonia Centro",
    "domicilio_municipio": "Municipio Ejemplo",
    "domicilio_estado": "Estado Ejemplo",
    "telefono_cliente": "555-1234",
    "correo_cliente": "juan.perez@example.com",
    "nombre_gestor": "María Gómez",
    "puesto_gestor": "Gestor de Proyecto",
    "domicilio_gestor_calle": "Otra Calle",
    "domicilio_gestor_no_exterior": "456",
    "domicilio_gestor_no_interior": "7A",
    "domicilio_gestor_zip": "67890",
    "domicilio_gestor_colonia": "Colonia Ejemplo",
    "domicilio_gestor_municipio": "Municipio Ejemplo",
    "domicilio_gestor_estado": "Estado Ejemplo",
    "telefono_gestor": "555-6789",
    "correo_gestor": "maria.gomez@example.com",
    "baja_tencion": "Sí",
    "media_tension": "No",
    "consumo_centro_carga": "500 kWh",
    "consumo_centro_carga_venta_excedentes": "100 kWh",
    "venta_total": "600 kWh",
    "RPU": "RPU-12345",
    "voltaje_tension": "220V",
    "fecha_estimada": "01/08/2024",
    "capacidad_bruta_instalada": "50 kW",
    "generacion_promedio_mensual_estimada": "2000 kWh",
    "cantidad_de_paneles": "20",
    "latitud": "19.432608",
    "longitud": "-99.133209"
}

# Leer las líneas del archivo de texto y reemplazar los marcadores de posición con los valores de las variables
with open('/home/mimus/enerf/chatgpt agent/mnt/data/anexo2_variables.txt', 'r', encoding='utf-8') as file:
    lines = [line.strip().format(**variables) for line in file]

# Crear clase PDF personalizada
class CustomPDF(FPDF):
    def header(self):
        pass  # No queremos encabezados en este caso

    def footer(self):
        pass  # No queremos pies de página en este caso

# Función para agregar texto
def add_text(pdf, x, y, text, size=8, style='', align='J', cell_height=10, line_height=5, border=0):
    pdf.set_xy(x, y)
    pdf.set_font("Arial", size=size, style=style)
    if align == 'C':
        pdf.cell(0, cell_height, text.encode('latin-1', 'replace').decode('latin-1').replace('?', '"'), ln=1, align=align)
    else:
        pdf.multi_cell(0, line_height, text.encode('latin-1', 'replace').decode('latin-1').replace('?', '"'), align=align, border=border)

# Crear el contenido adicional en un PDF temporal
temp_pdf = CustomPDF()
temp_pdf.set_auto_page_break(auto=False, margin=0)

# Añadir texto a la primera página
temp_pdf.add_page()
text_settings_page1 = text_page_1(lines)
for setting in text_settings_page1:
    add_text(temp_pdf, **setting)

# Añadir texto a la segunda página
temp_pdf.add_page()
text_settings_page2 = text_page_2(lines)
for setting in text_settings_page2:
    add_text(temp_pdf, **setting)

# Guardar el PDF temporal
temp_pdf_output_path = "/home/mimus/enerf/chatgpt agent/mnt/data/temp_output.pdf"
temp_pdf.output(temp_pdf_output_path)

# Leer el PDF existente y el temporal
existing_pdf_path = "/home/mimus/enerf/chatgpt agent/mnt/data/ANEXO_2_empty.pdf"
output_pdf_path = "/home/mimus/enerf/chatgpt agent/mnt/data/ANEXO_2.pdf"

with open(existing_pdf_path, "rb") as existing_file, open(temp_pdf_output_path, "rb") as temp_file:
    existing_pdf = PyPDF2.PdfReader(existing_file)
    temp_pdf = PyPDF2.PdfReader(temp_file)

    # Crear un nuevo PDF que combinará ambos
    output_pdf = PyPDF2.PdfWriter()

    # Superponer el contenido del temporal sobre la primera página del existente
    existing_page = existing_pdf.pages[0]
    temp_page = temp_pdf.pages[0]
    existing_page.merge_page(temp_page)
    output_pdf.add_page(existing_page)

    # Superponer el contenido del temporal sobre la segunda página del existente
    existing_page = existing_pdf.pages[1]
    temp_page = temp_pdf.pages[1]
    existing_page.merge_page(temp_page)
    output_pdf.add_page(existing_page)

    # Añadir las páginas restantes del PDF existente
    for i in range(2, len(existing_pdf.pages)):
        output_pdf.add_page(existing_pdf.pages[i])

    # Guardar el PDF final
    with open(output_pdf_path, "wb") as output_file:
        output_pdf.write(output_file)

output_pdf_path
