#analisis_de_recibo.py

import math

def analisis_de_recibo(tarifa, consumo_periodo_actual, consumos_historicos, nombre_cliente, direccion_cliente, demanda_contratada, numero_de_periodos=0):
    resultado = {
        'numero_paneles': 0,
        'promedio_mensual': 0,
        'KWp': 0,
        'KWh': 0,
        'tipo_de_periodo': ''
    }

    print("tarifa: ", tarifa, "tamaño de consumos_historicos: ", len(consumos_historicos))
    
    if tarifa in ['PDBT', '01', '02', 'DAC']:
        suma_consumos_historicos = sorted(consumos_historicos, reverse=True)
        if numero_de_periodos == 0:
            suma_consumos_historicos = suma_consumos_historicos[:5]
        else:
            suma_consumos_historicos = suma_consumos_historicos[:numero_de_periodos]
        
        print("suma_consumos_historicos: ", suma_consumos_historicos)
        
        promedio_mensual = (consumo_periodo_actual + sum(suma_consumos_historicos)) / (len(suma_consumos_historicos) + 1)
        print("promedio_mensual: ", promedio_mensual)
        
        numero_paneles = math.ceil(promedio_mensual / (585 * 0.3057))
        print("numero_paneles (PDBT, 01, 02, DAC): ", numero_paneles)
        
        KWp = numero_paneles *585 / 1000
        KWh = numero_paneles * 585 * 0.3057
        tipo_de_periodo = 'Bimestral'
        se_necesita_medidor = False
        
    elif tarifa in ['GDMTO', 'GDMTH']:
        suma_consumos_historicos = sorted(consumos_historicos, reverse=True)
        if numero_de_periodos == 0:
            suma_consumos_historicos = suma_consumos_historicos[:11]
        else:
            suma_consumos_historicos = suma_consumos_historicos[:numero_de_periodos]
        
        print("suma_consumos_historicos: ", suma_consumos_historicos)
        
        promedio_mensual = (consumo_periodo_actual + sum(suma_consumos_historicos)) / (len(suma_consumos_historicos) + 1)
        print("promedio_mensual: ", promedio_mensual)
        
        numero_paneles = math.ceil(2 * promedio_mensual / (585 * 0.3057))
        print("numero_paneles (GDMTO, GDMTH): ", numero_paneles)
        
        KWp = numero_paneles * 585 / 1000
        KWh = numero_paneles * 585 * 0.3057 / 2
        tipo_de_periodo = 'Mensual'
        
        se_necesita_medidor = KWp > demanda_contratada
    
    else:
        print('Tarifa no encontrada')
        return {}

    resultado['numero_paneles'] = numero_paneles
    resultado['promedio_mensual'] = promedio_mensual
    resultado['KWp'] = KWp
    resultado['KWh'] = KWh
    resultado['tipo_de_periodo'] = tipo_de_periodo
    resultado['nombre_cliente'] = nombre_cliente
    resultado['direccion_cliente'] = direccion_cliente
    resultado['se_necesita_medidor'] = se_necesita_medidor
    
    print('Numero de paneles:', numero_paneles, 'Promedio mensual:', promedio_mensual, 'KWp:', KWp, 'KWh:', KWh, 'Tipo de periodo:', tipo_de_periodo)
    
    return resultado