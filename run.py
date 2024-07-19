import pandas as pd
import numpy as np
import sys
sys.path.append(".")

# Importar funciones necesarias
from analisis_de_recibo import analisis_de_recibo
from calcular_articulos_requeridos import calcular_articulos_requeridos
from calcular_costo_proyecto import calcular_costo_proyecto
from actualizar_cotizacion_excel import actualizar_cotizacion_excel

## Datos del recibo extraídos manualmente
#datos_recibo = {
#    "nombre_cliente": "ESPUMADOS DEL BAJIO SA DE CV",
#    "direccion_cliente": "CARR PANAM IRAP SIL KM 90.0, CERCA CTRO LOGISTICO BAJI, EX HACIENDA DE MARQUES, C.P. 36815, IRAPUATO, GTO",
#    "tarifa": "GDMTH",
#    "consumo_periodo_actual": 56363,  # Total kWh (sum of kWh base, kWh intermedia, kWh punta, KWh)
#    "consumos_historicos": [13580, 10365, 14768, 15204, 16172, 8240, 8365, 12589, 12658, 10812, 12095, 11183],  # Historical consumption excluding current period
#    "demanda_contratada": 297,
#    "total_a_pagar": 48250.84
#}


def run(datos_recibo):
    # Análisis del recibo
    resultado_analisis = analisis_de_recibo(
        tarifa=datos_recibo["tarifa"],
        consumo_periodo_actual=datos_recibo["consumo_periodo_actual"],
        consumos_historicos=datos_recibo["consumos_historicos"],
        nombre_cliente=datos_recibo["nombre_cliente"],
        direccion_cliente=datos_recibo["direccion_cliente"],
        demanda_contratada=datos_recibo["demanda_contratada"]
    )
    print("resultados del analisis del recibo:")
    print(resultado_analisis)
    # Calcular artículos requeridos
    articulos_requeridos = calcular_articulos_requeridos(
        numero_paneles=resultado_analisis["numero_paneles"],
        tarifa=datos_recibo["tarifa"]
    )

    print("resultados del calcular_articulos_requeridos:")
    print(articulos_requeridos)
    # Calcular costo del proyecto
    costo_proyecto = calcular_costo_proyecto(
        articulos_requeridos=articulos_requeridos,
        analisis_resultado=resultado_analisis,
        path_precios_csv="/mnt/data/precios.csv",
        tarifa=datos_recibo["tarifa"]
    )
    print("resultados del costo del proyecto:")
    print(costo_proyecto)
    # Actualizar cotización en el archivo Excel
    ruta_actualizada_excel = actualizar_cotizacion_excel(
        analisis_resultado=resultado_analisis,
        articulos_requeridos=articulos_requeridos,
        costo_total_proyecto=costo_proyecto[1],
        tarifa=datos_recibo["tarifa"],
        path_excel="/mnt/data/cotizacion.xlsx"
    )

    # Mostrar la ruta del archivo actualizado
    print(f"Archivo Excel actualizado en: {ruta_actualizada_excel}")
