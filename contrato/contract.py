from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from text_contrato import configuracion_lineas

class DocumentoContrato:
    def __init__(self):
        self.documento = Document()
        self.documento._body.clear_content()

    def agregar_texto_con_formato(self, parrafo, texto, tamano_fuente, color=None, negrita=False):
        run = parrafo.add_run(texto)
        run.font.size = Pt(tamano_fuente)
        if negrita:
            run.bold = True
        if color:
            run.font.color.rgb = RGBColor(color[0], color[1], color[2])

    def procesar_etiquetas(self, parrafo, texto, tamano_fuente):
        i = 0
        while i < len(texto):
            if texto[i] == '<':
                end_tag_pos = texto.find('>', i) + 1
                tag = texto[i:end_tag_pos]
                
                # Procesar etiqueta de negritas
                if tag.startswith('<b>'):
                    end_bold_tag_pos = texto.find('</b>', i) + len('</b>')
                    bold_text = texto[i + len('<b>'):end_bold_tag_pos - len('</b>')]
                    self.agregar_texto_con_formato(parrafo, bold_text, tamano_fuente, negrita=True)
                    i = end_bold_tag_pos
                
                # Procesar etiqueta de color
                elif tag.startswith('<color='):
                    end_color_tag_pos = texto.find('</color>', i) + len('</color>')
                    color_code = tag[len('<color='):tag.find('>')]  # Obtener el código de color
                    color_value = tuple(map(int, color_code.split(',')))
                    color_text_start = end_tag_pos
                    color_text_end = texto.find('</color>', color_text_start)
                    color_text = texto[color_text_start:color_text_end]

                    # Manejar texto con negritas dentro de color
                    if '<b>' in color_text:
                        start_bold_in_color = color_text.find('<b>') + len('<b>')
                        end_bold_in_color = color_text.find('</b>')
                        self.agregar_texto_con_formato(parrafo, color_text[:start_bold_in_color - len('<b>')], tamano_fuente, color=color_value)
                        self.agregar_texto_con_formato(parrafo, color_text[start_bold_in_color:end_bold_in_color], tamano_fuente, color=color_value, negrita=True)
                        self.agregar_texto_con_formato(parrafo, color_text[end_bold_in_color + len('</b>'):], tamano_fuente, color=color_value)
                    else:
                        self.agregar_texto_con_formato(parrafo, color_text, tamano_fuente, color=color_value)
                    
                    i = end_color_tag_pos
                
                # Saltar cualquier otra etiqueta desconocida
                else:
                    i = end_tag_pos
            else:
                # Procesar texto sin etiquetas
                next_tag_pos = texto.find('<', i)
                if next_tag_pos == -1:
                    self.agregar_texto_con_formato(parrafo, texto[i:], tamano_fuente)
                    break
                else:
                    self.agregar_texto_con_formato(parrafo, texto[i:next_tag_pos], tamano_fuente)
                    i = next_tag_pos

    def agregar_parrafo(self, texto, tamano_fuente=12, alineacion='left', justificado=False, indentacion=0):
        p = self.documento.add_paragraph()
        
        # Aplicar indentación
        p_format = p.paragraph_format
        if indentacion > 0:
            p_format.left_indent = Pt(indentacion)
        
        # Aplicar espaciado antes y después del párrafo
        p_format.space_before = Pt(0)
        p_format.space_after = Pt(0)  # Asegurar que no haya espacio después del párrafo

        # Establecer espaciado entre líneas en 1.0
        p_format.line_spacing = Pt(12)  # Ajustar según sea necesario

        self.procesar_etiquetas(p, texto, tamano_fuente)

        if justificado:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        else:
            if alineacion == 'center':
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif alineacion == 'right':
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT

    def generar_documento(self, lineas, variables, configuracion):
        # Reemplazar variables en el texto
        for indice, linea in enumerate(lineas):
            for clave, valor in variables.items():
                linea = linea.replace(f"{{{clave}}}", valor)
            
            # Obtener configuración específica para la línea o usar valores por defecto
            config = configuracion.get(indice, {'tamano_fuente': 12, 'alineacion': 'left', 'justificado': False, 'indentacion': 0})
            tamano_fuente = config['tamano_fuente']
            alineacion = config['alineacion']
            justificado = config['justificado']
            indentacion = config['indentacion']

            # Agregar párrafo al documento
            self.agregar_parrafo(linea, tamano_fuente, alineacion, justificado, indentacion)

    def guardar_documento(self, nombre_archivo):
        self.documento.save(nombre_archivo)

# Leer el archivo de texto
with open("mnt/data/contrato_variables.txt", "r", encoding="utf-8") as file:
    lineas = file.readlines()

# Variables a reemplazar
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
    "lugar_fecha": "Ciudad, Fecha",
    "No_INE_gestor": "0987654321098"
}


# Crear y generar el documento
doc_contrato = DocumentoContrato()
doc_contrato.generar_documento(lineas, variables, configuracion_lineas)
doc_contrato.guardar_documento("mnt/data/contrato_generado.docx")
