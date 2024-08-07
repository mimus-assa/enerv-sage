from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from formato_contratos import formato_distribuidor
from roman import convertir_a_romano
from configurador_documento import *

class ProcesadorTexto:
    def __init__(self, documento):
        self.documento = documento

    def agregar_texto_con_formato(self, parrafo, texto, tamano_fuente, color=None, negrita=False):
        run = parrafo.add_run(texto)
        run.font.size = Pt(tamano_fuente)
        run.font.name = "Arial"
        r = run._element
        r.rPr.rFonts.set(qn('w:eastAsia'), "Arial")
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
                
                if tag.startswith('<b>'):
                    end_bold_tag_pos = texto.find('</b>', i) + len('</b>')
                    bold_text = texto[i + len('<b>'):end_bold_tag_pos - len('</b>')]
                    self.agregar_texto_con_formato(parrafo, bold_text, tamano_fuente, negrita=True)
                    i = end_bold_tag_pos
                
                elif tag.startswith('<color='):
                    end_color_tag_pos = texto.find('</color>', i) + len('</color>')
                    color_code = tag[len('<color='):tag.find('>')]
                    color_value = tuple(map(int, color_code.split(',')))
                    color_text_start = end_tag_pos
                    color_text_end = texto.find('</color>', color_text_start)
                    color_text = texto[color_text_start:color_text_end]

                    if '<b>' in color_text:
                        start_bold_in_color = color_text.find('<b>') + len('<b>')
                        end_bold_in_color = color_text.find('</b>')
                        self.agregar_texto_con_formato(parrafo, color_text[:start_bold_in_color - len('<b>')], tamano_fuente, color=color_value)
                        self.agregar_texto_con_formato(parrafo, color_text[start_bold_in_color:end_bold_in_color], tamano_fuente, color=color_value, negrita=True)
                        self.agregar_texto_con_formato(parrafo, color_text[end_bold_in_color + len('</b>'):], tamano_fuente, color=color_value)
                    else:
                        self.agregar_texto_con_formato(parrafo, color_text, tamano_fuente, color=color_value)
                    
                    i = end_color_tag_pos
                
                else:
                    i = end_tag_pos
            else:
                next_tag_pos = texto.find('<', i)
                if next_tag_pos == -1:
                    self.agregar_texto_con_formato(parrafo, texto[i:], tamano_fuente)
                    break
                else:
                    self.agregar_texto_con_formato(parrafo, texto[i:next_tag_pos], tamano_fuente)
                    i = next_tag_pos

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from formato_contratos import formato_distribuidor
from roman import convertir_a_romano

class DocumentoContrato:
    def __init__(self):
        self.documento = Document()
        self.documento._body.clear_content()
        self.configurador = ConfiguradorDocumento(self.documento)
        self.procesador = ProcesadorTexto(self.documento)
        self.configurador.configurar_pagina()

    def agregar_parrafo(self, texto, tamano_fuente=12, alineacion='left', justificado=False, indentacion=0):
        p = self.documento.add_paragraph()
        p_format = p.paragraph_format
        
        if indentacion > 0:
            p_format.left_indent = Pt(indentacion)
        
        p_format.space_before = Pt(0)
        p_format.space_after = Pt(0)
        p_format.line_spacing = Pt(12)

        lineas = texto.split('\n')
        for i, linea in enumerate(lineas):
            if i > 0:
                p.add_run().add_break()
            self.procesador.procesar_etiquetas(p, linea, tamano_fuente)

        self.configurador.configurar_fuente(p)

        if justificado:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        else:
            if alineacion == 'center':
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif alineacion == 'right':
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT

    def agregar_lista(self, items, tamano_fuente=12, alineacion='left', justificado=False, indentacion=0):
        for i, item in enumerate(items):
            if item.strip():
                n = i + 1
                numero_romano = convertir_a_romano(n)
                p = self.documento.add_paragraph()

                # Agregar el número romano y un tab
                run = p.add_run(f"{numero_romano}. \t")
                run.font.size = Pt(tamano_fuente)
                run.font.name = "Arial"

                # Agregar el texto del item después del tab
                self.procesador.procesar_etiquetas(p, item, tamano_fuente)
                self.configurador.configurar_fuente(p)

                # Configurar el formato del párrafo
                p_format = p.paragraph_format
                p_format.left_indent = Inches(0.5)  # Sangría de todo el párrafo
                p_format.first_line_indent = Inches(-0.5)  # Sangría negativa para la primera línea
                p_format.space_before = Pt(0)
                p_format.space_after = Pt(0)
                p_format.line_spacing = Pt(12)

                if justificado:
                    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                else:
                    if alineacion == 'center':
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    elif alineacion == 'right':
                        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    else:
                        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p = self.documento.add_paragraph()
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)

    def procesar_linea(self, linea, configuracion, i, lineas):
        config = configuracion.get(i, {'tamano_fuente': 12, 'alineacion': 'left', 'justificado': False, 'indentacion': 0})
        tamano_fuente = config['tamano_fuente']
        alineacion = config['alineacion']
        justificado = config['justificado']
        indentacion = config['indentacion']

        if linea.startswith('<list>'):
            items = []
            i += 1
            while i < len(lineas) and not lineas[i].startswith('</list>'):
                item = lineas[i].strip().replace('<item>', '').replace('</item>', '')
                if item:
                    items.append(item)
                i += 1
            self.agregar_lista(items, tamano_fuente, alineacion, justificado, indentacion)
        elif linea.startswith('</list>'):
            return i + 1
        else:
            self.agregar_parrafo(linea, tamano_fuente, alineacion, justificado, indentacion)
        return i + 1

    def generar_documento(self, lineas, variables, configuracion):
        i = 0
        while i < len(lineas):
            linea = lineas[i].rstrip()
            if linea:
                for clave, valor in variables.items():
                    linea = linea.replace(f"{{{clave}}}", valor)
                i = self.procesar_linea(linea, configuracion, i, lineas)
            else:
                p = self.documento.add_paragraph()
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                i += 1

    def guardar_documento(self, nombre_archivo):
        self.documento.save(nombre_archivo)

def cargar_lineas_archivo(ruta_archivo):
    with open(ruta_archivo, "r", encoding="utf-8") as file:
        return file.readlines()

# Ejemplo de uso
if __name__ == "__main__":
    ruta_lineas = "mnt/data/contrato_distribuidor.txt"
    lineas = cargar_lineas_archivo(ruta_lineas)

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

    doc_contrato = DocumentoContrato()
    doc_contrato.generar_documento(lineas, variables, formato_distribuidor)
    doc_contrato.guardar_documento("mnt/data/contrato_generado.docx")
