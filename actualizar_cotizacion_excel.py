#actualizar_cotizacion_excel.py
from openpyxl import load_workbook
from openpyxl.styles import Font
from datetime import datetime
import pytz
from openpyxl.styles import NamedStyle
import time


from openpyxl import load_workbook
from openpyxl.styles import Font, NamedStyle
from datetime import datetime
import pytz
import time

# Función para calcular el nuevo folio basado en timestamp
def calcular_nuevo_folio():
    timestamp = int(time.time())
    nuevo_folio = f"GPT-{timestamp}"
    print(f"Nuevo folio basado en timestamp: {nuevo_folio}")
    return nuevo_folio

def actualizar_cotizacion_excel(analisis_resultado, articulos_requeridos, costo_total_proyecto, tarifa, path_excel='/mnt/data/cotizacion.xlsx', new_path_excel='/mnt/data/cotizacion_actualizada.xlsx'):
    nuevo_folio = calcular_nuevo_folio()

    # Cargar el archivo Excel para su edición
    wb = load_workbook(filename=path_excel)
    sheet = wb['SFV']

    # Actualizar el folio en la celda E3
    sheet['E3'].value = nuevo_folio

    # Actualizar datos del cliente y del proyecto
    sheet['E4'] = analisis_resultado['nombre_cliente']
    sheet['E5'] = analisis_resultado['direccion_cliente']
    sheet['D34'] = analisis_resultado['numero_paneles']
    sheet['F19'] = f"Instalación de sistema fotovoltaico interconectado a la red de C.F.E. incluye: Suministro e instalación de SFVI de {round(analisis_resultado['KWp'],2)} KWp ó {round(analisis_resultado['KWh'],2)} KWh {analisis_resultado['tipo_de_periodo']}. Instalación a nivel de piso y Gestión de interconexión a red de C.F.E."

    # Actualizar componentes específicos y sus cantidades
    estructura_unirac = ", ".join([f"{v} ESTRUCTURA UNIRAC SM ASCENDER {k}" for k, v in articulos_requeridos['Kits de Montaje Unirac'].items()])
    sheet['F26'] = estructura_unirac

    # Actualizar cables y sus cantidades
    descripciones_cables = []
    for articulo, cantidad in articulos_requeridos.items():
        if articulo.startswith("CABLE CALIBRE"):
            descripcion_cable = f"{cantidad}x {articulo}"
            descripciones_cables.append(descripcion_cable)
    descripcion_cables_texto = ", ".join(descripciones_cables)
    sheet['F27'] = descripcion_cables_texto

    # Actualizar detalles de los artículos requeridos
    sheet['D28'] = articulos_requeridos['Supresores de Picos 600VDC']
    sheet['D30'] = articulos_requeridos['ITM en DC 25 AMP']
    sheet['D32'] = articulos_requeridos['Pares de Conectores MC4 (10 pares)']
    sheet['D31'] = articulos_requeridos['Gabinetes de Protecciones ABB 12/18 espacios']
    sheet['D29'] = articulos_requeridos['Pastillas Termomagnéticas en AC']
    
    # Actualizar inversores y sus cantidades
    descripciones_inversores = []
    for inversor in articulos_requeridos['Inversores']:
        nombre_inversor = inversor['inversor']
        cantidad_inversor = inversor['cantidad']
        descripcion_inversor = f"{cantidad_inversor}x {nombre_inversor}"
        descripciones_inversores.append(descripcion_inversor)
    descripcion_inversores_texto = ", ".join(descripciones_inversores)
    sheet['F33'] = descripcion_inversores_texto

    # Añadir la fecha de hoy
    tz_mexico = pytz.timezone('America/Mexico_City')
    fecha_actual_mexico = datetime.now(tz_mexico).strftime("%d/%m/%Y")
    sheet['D13'] = fecha_actual_mexico
    
    # Actualizar costo del proyecto
    sheet['J19'] = round(costo_total_proyecto, 2)
    
    # Crear un estilo nombrado para el texto en negrita
    bold_style = NamedStyle(name="bold_style")
    bold_style.font = Font(bold=True)
    
    if 'bold_style' not in wb.named_styles:
        wb.add_named_style(bold_style)

    # Cambiar el estilo de las celdas E25 al E40 para que estén en negrita
    for row in range(25, 41):
        cell = sheet[f'E{row}']
        if cell.value is not None and isinstance(cell.value, str):
            cell.style = 'bold_style'

    # Aplicar fuente Arial y tamaño 11 a las celdas F19 a F40
    arial_font = Font(name='Arial', size=11)
    
    for row in range(19, 41):
        cell = sheet[f'F{row}']
        if cell.value is not None:
            cell.font = arial_font

    # Limpiar las celdas D38 a F40 si la tarifa es "PDBT", "01", "02", "DAC"
    if tarifa in ['PDBT', '01', '02', 'DAC']:
        for row in range(38, 41):
            for col in ['D', 'E', 'F']:
                sheet[f'{col}{row}'] = ""

    # Guardar los cambios realizados en el archivo Excel
    wb.save(filename=new_path_excel)

    return new_path_excel
