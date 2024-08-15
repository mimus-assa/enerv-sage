        
def calcular_promedio_mensual(consumo_periodo_actual,suma_consumos_historicos):
        return (consumo_periodo_actual + sum(suma_consumos_historicos)) / (len(suma_consumos_historicos) + 1)
