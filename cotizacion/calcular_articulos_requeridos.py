#calcular_articulos_requeridos.py

import math

def calcular_articulos_requeridos(numero_paneles, tarifa):
    if tarifa in ['PDBT', '01', '02', 'DAC']:
        # Para pdbt o similar: un supresor de picos por cada 10 paneles, máximo 12
        supresores_de_picos = min(math.ceil(numero_paneles / 10), 12)
    elif tarifa in ['GDMTO', 'GDMTH']:
        # Para gdmto o gdmth: un supresor de picos por cada 18 paneles, máximo 20
        supresores_de_picos = min(math.ceil(numero_paneles / 18), 20)
    else:
        # Por defecto, se aplica el modo 'pdbt'
        print("error on tarifa")

    itm_en_dc = pares_conectores_mc4 = math.ceil(numero_paneles / 10)
    gabinetes_protecciones_abb = math.ceil(numero_paneles / 30)
    pastillas_termomagneticas = 1

    # Determinar inversores y calibres necesarios
    inversores, cables = determinar_inversores_y_calibres(numero_paneles)

    kits_unirac = calcular_kits_unirac_correctamente(numero_paneles)

    # Construir el diccionario de artículos requeridos
    articulos_requeridos = {
        'Supresores de Picos 600VDC': supresores_de_picos,
        'ITM en DC 25 AMP': itm_en_dc,
        'Pares de Conectores MC4 (10 pares)': pares_conectores_mc4,
        'Gabinetes de Protecciones ABB 12/18 espacios': gabinetes_protecciones_abb,
        'Inversores': inversores,
        **cables,
        'Kits de Montaje Unirac': kits_unirac,
        'Pastillas Termomagnéticas en AC': pastillas_termomagneticas,
        'PANEL FOTOVOLTAICO 585 W MARCA CANADIAN SOLAR O SIMILAR': numero_paneles
    }

    return articulos_requeridos

# Redefiniendo la función con los ajustes necesarios
def determinar_inversores_y_calibres(numero_paneles):
    rangos_inversores = [
        (1, 5, ('inversor mic 2500tl-x growatt', '12')),
        (6, 8, ('inversor min 3600tl-x growatt', '12')),
        (9, 11, ('inversor min 6000tl-x growatt', '10')),
        (12, 18, ('inversor min 8000tl-x(e) growatt', '10')),
        (19, 24, ('inversor min 10000tl-x growatt', '8')),
        (25, 37, ('inversor mac 15ktl3-xl growatt', '6')),
        (38, 50, ('inversor mac 20ktl3-xl growatt', '4')),
        (51, 74, ('inversor mac 30ktl3-xl growatt', '2')),
        (75, 150, ('inversor max 60ktl3-xl2 growatt', '00'))
    ]

    inversores = []
    cables = {}
    paneles_restantes = numero_paneles
    
    while paneles_restantes > 0:
        encontrado = False
        for rango_inferior, rango_superior, (inversor, calibre) in reversed(rangos_inversores):
            if paneles_restantes >= rango_inferior:
                if paneles_restantes >= rango_superior:
                    cantidad_inversores = paneles_restantes // rango_superior
                    paneles_que_cubre = cantidad_inversores * rango_superior
                else:
                    cantidad_inversores = 1
                    paneles_que_cubre = rango_superior
                inversores.append({'inversor': inversor, 'calibre': calibre, 'cantidad': cantidad_inversores})
                cable_key = f'CABLE CALIBRE {calibre} AWG THW-LS 100% COBRE(incluye tuberia conduit)'
                cables[cable_key] = cables.get(cable_key, 0) + cantidad_inversores
                paneles_restantes -= paneles_que_cubre
                encontrado = True
                break

    return inversores, cables


def calcular_kits_unirac_correctamente(numero_paneles):
    kits_unirac = {}
    kits_de_2x10 = numero_paneles // 20
    paneles_restantes = numero_paneles % 20

    if kits_de_2x10 > 0:
        kits_unirac['2x10'] = kits_de_2x10

    if paneles_restantes > 0:
        kits_unirac[f'2x{math.ceil(paneles_restantes / 2)}'] = 1

    return kits_unirac
