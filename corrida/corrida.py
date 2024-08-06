
from datetime import datetime
import pandas as pd
from werkzeug.utils import secure_filename
import openpyxl  # Importa la biblioteca para manejar archivos Excel
import os
from flask import send_from_directory


def calcular_amortizacion(capital, tasa_anual, plazo, gracia, fecha_alta):
    # Convertir la tasa anual a tasa mensual
    tasa_mensual = tasa_anual / 12 / 100
    num_pagos = plazo

    # Calcular el pago mensual de la amortización
    if plazo > gracia:
        factor_amortizacion = (tasa_mensual * (1 + tasa_mensual) ** (plazo - gracia)) / (((1 + tasa_mensual) ** (plazo - gracia)) - 1)
        pago_mensual = capital * factor_amortizacion
    else:
        pago_mensual = 0

    # Lista para almacenar la información de la tabla de amortización
    amortizacion = []

    # Saldo inicial del préstamo
    saldo = capital
    fecha_pago = fecha_alta

    for pago_num in range(1, num_pagos + 1):
        if pago_num <= gracia:
            # Durante el periodo de gracia se pagan solo intereses
            pago_capital = 0
            pago_intereses = saldo * tasa_mensual
        else:
            # Después del periodo de gracia se paga tanto el capital como los intereses
            pago_intereses = saldo * tasa_mensual
            pago_capital = pago_mensual - pago_intereses
            saldo -= pago_capital

        # Se asegura que el saldo no sea negativo
        saldo = max(0, saldo)

        # Agrega el pago actual a la lista
        amortizacion.append({
            'Fecha Pago': fecha_pago.strftime('%d/%m/%Y'),
            'Saldo Inicial': round(capital, 2),
            'Pago Capital': round(pago_capital, 2),
            'Pago Intereses': round(pago_intereses, 2),
            'Saldo Insoluto': round(saldo, 2),
            'Pago Mensual': round(pago_intereses + pago_capital, 2)
        })

        # Calcula la fecha del próximo pago
        mes = (fecha_pago.month % 12) + 1
        año = fecha_pago.year + ((fecha_pago.month + 1) // 13)
        fecha_pago = datetime(año, mes, fecha_pago.day)

        # Actualiza el saldo inicial para el siguiente período
        capital = saldo

    # Convertir la lista en un DataFrame de Pandas
    df_amortizacion = pd.DataFrame(amortizacion)
    return df_amortizacion



def validar_entradas(form):
    required_fields = ['cliente', 'capital', 'tasa_anual', 'plazo', 'gracia', 'fecha_alta']
    return all(field in form for field in required_fields)

def obtener_datos(form):
    cliente = form['cliente']
    capital = float(form['capital'])
    tasa_anual = float(form['tasa_anual'])
    plazo = int(form['plazo'])
    gracia = int(form['gracia'])
    fecha_alta = datetime.strptime(form['fecha_alta'], '%d/%m/%Y')
    return cliente, capital, tasa_anual, plazo, gracia, fecha_alta

def escribir_excel(cliente, capital,tasa_anual, plazo,gracia, fecha_alta, df_amortizacion):
    filename = secure_filename("pagos.xlsx")
    filepath = os.path.join('docs', filename)
    workbook = openpyxl.load_workbook(filepath)

    sheet = workbook.active
    
    sheet['C8'] = cliente
    sheet['G10'] = capital
    sheet['G11'] = tasa_anual
    sheet['G12'] = plazo
    sheet['G13'] = gracia
    sheet['D10'] = fecha_alta.strftime('%d/%m/%Y')
    escribir_datos_en_hoja(sheet, df_amortizacion)
    workbook.save(filepath)

    return filepath

def escribir_datos_en_hoja(sheet, df_amortizacion):
    columns = {
        'B': 'Saldo Inicial',
        'C': 'Pago Capital',
        'D': 'Pago Intereses',
        'F': 'Saldo Insoluto',
        'G': 'Pago Mensual'
    }
    for col, key in columns.items():
        for index, value in enumerate(df_amortizacion[key], start=18):
            sheet[f'{col}{index}'].value = value

def descargar_archivo(filepath):
    return send_from_directory(directory='docs', path=os.path.basename(filepath), as_attachment=True)