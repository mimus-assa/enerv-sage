import pandas as pd

def calcular_precio(kwp):
    slope = 849.5104895104896
    intercept = 992.153846153842
    precio = slope * kwp + intercept
    return precio  # hay que ajustar esto con ()

def calcular_costo_proyecto(articulos_requeridos, analisis_resultado, path_precios_csv, tarifa):
    # Cargando los precios desde el archivo CSV
    precios_df = pd.read_csv(path_precios_csv)
    
    # Asegurarse de que el DataFrame tiene un índice de artículo para poder buscar
    precios_df.set_index('Articulo', inplace=True)
    
    # Preparando los datos de los artículos requeridos para el cálculo
    articulos_cantidad = {}
    
    # Inversores
    for inversor in articulos_requeridos['Inversores']:
        # Utiliza directamente el nombre del inversor sin añadir calibre
        nombre_inversor = inversor['inversor']
        articulos_cantidad[nombre_inversor] = inversor['cantidad']
    
    # El resto del código permanece igual
    
    # Cables
    for key, value in articulos_requeridos.items():
        if key.startswith('CABLE CALIBRE'):
            articulos_cantidad[key] = value
    
    # Otros artículos
    for articulo, cantidad in articulos_requeridos.items():
        if articulo not in ['Inversores', 'Kits de Montaje Unirac']:
            articulos_cantidad[articulo] = cantidad
    
    # Kits de Montaje Unirac
    for tipo_estructura, cantidad_estructura in articulos_requeridos.get('Kits de Montaje Unirac', {}).items():
        if tipo_estructura == '2x1':
            tipo_estructura = '2x2'  # Reemplazar 2x1 por 2x2
        nombre_completo_articulo = f'ESTRUCTURA UNIRAC SM ASCENDER {tipo_estructura}'
        articulos_cantidad[nombre_completo_articulo] = cantidad_estructura
    
    # Calculando el costo por artículo
    costo_articulos = {}
    for articulo, cantidad in articulos_cantidad.items():
        try:
            precio_articulo = precios_df.loc[articulo, 'Precio']
            costo_articulos[articulo] = precio_articulo * cantidad
        except KeyError:
            print(f"Advertencia: '{articulo}' no encontrado en la lista de precios.")
    
    # Calculando el costo total del proyecto
    costo_total_proyecto = sum(costo_articulos.values()) * 2
    if tarifa in ["GDMTO", "GDMTH"]:
        costo_total_proyecto += calcular_precio(analisis_resultado["KWp"])
    
    if analisis_resultado.get("se_necesita_medidor", False):
        costo_total_proyecto += 25000
    
    return costo_articulos, costo_total_proyecto

