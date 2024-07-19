import pandas as pd
import numpy as np
import sys
import os
import json
import logging

# Configuración de logging
logging.basicConfig(filename='run.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s')

sys.path.append(".")

# Importar funciones necesarias
try:
    from analisis_de_recibo import analisis_de_recibo
    from calcular_articulos_requeridos import calcular_articulos_requeridos
    from calcular_costo_proyecto import calcular_costo_proyecto
    from actualizar_cotizacion_excel import actualizar_cotizacion_excel
except ImportError as e:
    logging.error("Error importando módulos: %s", e)
    raise

def validar_datos(datos_recibo):
    required_fields = ["nombre_cliente", "direccion_cliente", "tarifa", "consumo_periodo_actual", "consumos_historicos", "demanda_contratada", "total_a_pagar"]
    for field in required_fields:
        if field not in datos_recibo:
            logging.error("Campo faltante en datos del recibo: %s", field)
            raise ValueError(f"Campo faltante: {field}")
    logging.info("Todos los campos requeridos están presentes.")
    return True

def run(datos_recibo):
    try:
        # Validar datos
        validar_datos(datos_recibo)

        # Análisis del recibo
        resultado_analisis = analisis_de_recibo(
            tarifa=datos_recibo["tarifa"],
            consumo_periodo_actual=datos_recibo["consumo_periodo_actual"],
            consumos_historicos=datos_recibo["consumos_historicos"],
            nombre_cliente=datos_recibo["nombre_cliente"],
            direccion_cliente=datos_recibo["direccion_cliente"],
            demanda_contratada=datos_recibo["demanda_contratada"]
        )
        logging.info("Resultados del análisis del recibo: %s", resultado_analisis)

        # Calcular artículos requeridos
        articulos_requeridos = calcular_articulos_requeridos(
            numero_paneles=resultado_analisis["numero_paneles"],
            tarifa=datos_recibo["tarifa"]
        )
        logging.info("Resultados del cálculo de artículos requeridos: %s", articulos_requeridos)

        # Calcular costo del proyecto
        costo_proyecto = calcular_costo_proyecto(
            articulos_requeridos=articulos_requeridos,
            analisis_resultado=resultado_analisis,
            path_precios_csv="/mnt/data/precios.csv",
            tarifa=datos_recibo["tarifa"]
        )
        logging.info("Resultados del costo del proyecto: %s", costo_proyecto)

        # Actualizar cotización en el archivo Excel
        ruta_actualizada_excel = actualizar_cotizacion_excel(
            analisis_resultado=resultado_analisis,
            articulos_requeridos=articulos_requeridos,
            costo_total_proyecto=costo_proyecto[1],
            tarifa=datos_recibo["tarifa"],
            path_excel="/mnt/data/cotizacion.xlsx"
        )
        logging.info("Archivo Excel actualizado en: %s", ruta_actualizada_excel)
        
        return ruta_actualizada_excel
    except Exception as e:
        logging.error("Error durante la ejecución del script: %s", e)
        raise

if __name__ == "__main__":
    # Cargar datos del recibo desde archivo JSON
    try:
        with open("/mnt/data/datos_recibo.json", "r") as f:
            datos_recibo = json.load(f)
    except Exception as e:
        logging.error("Error cargando datos del recibo: %s", e)
        raise

    # Ejecutar la función run con los datos del recibo
    run(datos_recibo)
