from openpyxl import load_workbook
from openpyxl.styles import Font
from datetime import datetime
import pytz

def actualizar_cotizacion_excel(analisis_resultado, articulos_requeridos, costo_total_proyecto, path_excel='/mnt/data/cotizacion.xlsx', new_path_excel='/mnt/data/cotizacion_actualizada.xlsx'):
    """
    Actualiza el archivo Excel de cotización con los resultados del análisis y los artículos requeridos.

    Parámetros:
    - analisis_resultado (dict): Resultados del análisis de consumo y requerimientos de paneles.
    - articulos_requeridos (dict): Diccionario con la cantidad de artículos requeridos.
    - costo_total_proyecto (float): Costo total del proyecto.
    - path_excel (str): Ruta al archivo Excel original.
    - new_path_excel (str): Ruta donde se guardará el archivo Excel actualizado.

    Retorna:
    - str: La ruta del archivo Excel actualizado.
    """
    # Cargar el archivo Excel para su edición
    wb = load_workbook(filename=path_excel)
    sheet = wb['SFV']

    # Actualizar datos del cliente y del proyecto
    sheet['E4'] = analisis_resultado['nombre_cliente']  # Asegúrate de que esta clave existe en analisis_resultado
    sheet['E5'] = analisis_resultado['direccion_cliente']  # Asegúrate de que esta clave existe en analisis_resultado
    sheet['D34'] = analisis_resultado['numero_paneles']
    sheet['F19'] = f"Instalación de sistema fotovoltaico interconectado a la red de C.F.E. incluye: Suministro e instalación de SFVI de {round(analisis_resultado['KWp'],2)} KWp ó {round(analisis_resultado['KWh'],2)} KWh {analisis_resultado['tipo_de_periodo']}. Instalación a nivel de piso y Gestión de interconexión a red de C.F.E."

    # Actualizar componentes específicos y sus cantidades
    estructura_unirac = ", ".join([f"{v} ESTRUCTURA UNIRAC SM ASCENDER {k}" for k, v in articulos_requeridos['Kits de Montaje Unirac'].items()])
    sheet['F26'] = estructura_unirac

    # Extraer el calibre del cable desde el nombre del artículo y actualizarlo en la hoja de Excel
    
    # Actualizar cables y sus cantidades
    descripciones_cables = []
    for articulo, cantidad in articulos_requeridos.items():
        if articulo.startswith("CABLE CALIBRE"):
            descripcion_cable = f"{cantidad}x {articulo}"
            descripciones_cables.append(descripcion_cable)
    descripcion_cables_texto = ", ".join(descripciones_cables)
    sheet['F27'] = descripcion_cables_texto  # Asume que F27 es la celda correcta para los cables

    # Actualizar detalles de los artículos requeridos
    sheet['D28'] = articulos_requeridos['Supresores de Picos 600VDC']
    sheet['D30'] = articulos_requeridos['ITM en DC 25 AMP']
    sheet['D32'] = articulos_requeridos['Pares de Conectores MC4 (10 pares)']
    sheet['D31'] = articulos_requeridos['Gabinetes de Protecciones ABB 12/18 espacios']
    
    # Actualizar inversores y sus cantidades
    descripciones_inversores = []
    for inversor in articulos_requeridos['Inversores']:
        nombre_inversor = inversor['inversor']
        cantidad_inversor = inversor['cantidad']
        # Si necesitas incluir el calibre, asegúrate de ajustar esta parte para que se añada solo cuando sea necesario
        descripcion_inversor = f"{cantidad_inversor}x {nombre_inversor}"
        descripciones_inversores.append(descripcion_inversor)
    descripcion_inversores_texto = ", ".join(descripciones_inversores)
    sheet['F33'] = descripcion_inversores_texto  # Asume que F33 es la celda correcta para los inversores

    sheet['D29'] = articulos_requeridos['Pastillas Termomagnéticas en AC']
    
    # ahora añadimos a la D13 la fecha de hoy
    # Establecer la zona horaria de México (Ciudad de México como ejemplo)
    tz_mexico = pytz.timezone('America/Mexico_City')
    # Obtener la fecha actual en la zona horaria de México
    fecha_actual_mexico = datetime.now(tz_mexico).strftime("%d/%m/%Y")
    # Asignar la fecha obtenida a la celda deseada en tu hoja de Excel
    sheet['D13'] = fecha_actual_mexico
    
    # Actualizar costo del proyecto
    sheet['J19'] = round(costo_total_proyecto, 2)
    
    # Cambiar el estilo de las celdas E25 al E40 para que estén en negrita
    bold_font = Font(bold=True)
    for row in range(25, 41):
        cell = sheet[f'E{row}']
        cell.font = bold_font
        print(f"Updated cell E{row} to bold.")  # Mensaje de depuración para verificar que las celdas se actualizan

    # Guardar los cambios realizados en el archivo Excel
    wb.save(filename=new_path_excel)

    return new_path_excel