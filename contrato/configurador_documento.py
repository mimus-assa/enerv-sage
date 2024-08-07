
from docx.shared import Pt, RGBColor, Inches
from docx.oxml.ns import qn

class ConfiguradorDocumento:
    def __init__(self, documento):
        self.documento = documento

    def configurar_pagina(self):
        sections = self.documento.sections
        for section in sections:
            section.page_width = Inches(8.5)
            section.page_height = Inches(11)
            section.left_margin = Inches(1.18)
            section.right_margin = Inches(1.18)
            section.top_margin = Inches(0.49)
            section.bottom_margin = Inches(0.49)

    def configurar_fuente(self, parrafo, fuente="Arial"):
        for run in parrafo.runs:
            run.font.name = fuente
            r = run._element
            r.rPr.rFonts.set(qn('w:eastAsia'), fuente)
