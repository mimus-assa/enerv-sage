from fpdf import FPDF
from text_contrato import *
from bs4 import BeautifulSoup

# Definir las variables
variables = {
    "nombre_cliente": "Juan Pérez",
    "nombre_gestor": "María Gómez",
    "No_INE": "1234567890123",
    "promedio_mensual": "500 kWh",
    "voltaje_tension": "220V",
    "RPU": "RPU-12345",
    "RMU": "RMU-67890",
    "cuenta": "987654321",
    "direccion_cliente": "Calle Falsa 123, Colonia Centro, Municipio Ejemplo, Estado Ejemplo, 12345",
    "tarifa": "Tarifa 1",
    "numero_hilos": "3",
    "numero_medidor": "MED-45678",
    "demanda_contratada": "20 kW",
    "demanda_instalada": "25 kW",
    "telefono_cliente": "555-1234",
    "correo_cliente": "juan.perez@example.com",
    "lugar_fecha": "Ciudad Ejemplo, 28 de Julio de 2024",
    "No_INE_gestor": "9876543210987"
}

# Leer las líneas del archivo de texto y reemplazar los marcadores de posición con los valores de las variables
with open('mnt/data/contrato_variables.txt', 'r', encoding='utf-8') as file:
    lines = [line.strip().format(**variables) for line in file]

# Crear clase PDF personalizada
class CustomPDF(FPDF):
    def header(self):
        pass  # No queremos encabezados en este caso

    def footer(self):
        pass  # No queremos pies de página en este caso

# Crear instancia de PDF
pdf = CustomPDF()
pdf.add_page()
pdf.set_font("Arial", size=8)

# Función para agregar texto con estilos
def add_styled_text(pdf, x, y, text, size=8, style='', align='J', line_height=5, border=0):
    pdf.set_xy(x, y)
    pdf.set_font("Arial", size=size, style=style)

    soup = BeautifulSoup(text, "html.parser")

    # Configuración de estilos predeterminados
    default_font_style = style
    default_font_size = size
    default_text_color = (0, 0, 0)  # Negro

    def set_style(element):
        # Aplicar estilos según las etiquetas HTML
        if element.name == 'b':
            pdf.set_font("Arial", size=default_font_size, style='B')
        elif element.name == 'span' and 'style' in element.attrs and 'color:blue' in element.attrs['style']:
            pdf.set_text_color(0, 0, 255)  # Azul
            pdf.set_font("Arial", size=default_font_size, style='B')
        else:
            pdf.set_font("Arial", size=default_font_size, style=default_font_style)
            pdf.set_text_color(*default_text_color)

    for element in soup:
        if isinstance(element, str):
            pdf.write(line_height, element.encode('latin-1', 'replace').decode('latin-1').replace('?', '"'))
        else:
            set_style(element)
            pdf.write(line_height, element.get_text().encode('latin-1', 'replace').decode('latin-1').replace('?', '"'))
            # Restablecer al estilo predeterminado después de cada elemento
            pdf.set_font("Arial", size=default_font_size, style=default_font_style)
            pdf.set_text_color(*default_text_color)

# Obtener todas las configuraciones de texto para cada página
text_pages = [text_page_1(lines), text_page_2(lines), text_page_3(lines), text_page_4(lines), text_page_5(lines), text_page_6(lines)]

# Añadir el texto a cada página
for page_index, text_settings in enumerate(text_pages):
    if page_index > 0:
        pdf.add_page()
    for setting in text_settings:
        add_styled_text(pdf, setting['x'], setting['y'], setting['text'], setting.get('size', 8), setting.get('style', ''), setting.get('align', 'J'), setting.get('line_height', 5), setting.get('border', 0))

# Añadir la decimoctava línea del archivo justificada en una nueva página
pdf.add_page()
pdf.set_xy(30, 10)
pdf.multi_cell(0, 4, lines[17].encode('latin-1', 'replace').decode('latin-1').replace('?', '"'), align="J")

# Guardar el archivo PDF
output_path = "mnt/data/Contrato_Interconexion.pdf"
pdf.output(output_path)

output_path
