"""
Módulo horas.py
Autor: Edgar Milián Marín
Descripción: Contiene la función normalizaHoras para buscar y estandarizar
             expresiones horarias dentro de un texto a formato HH:MM.
"""

import re
import os

def validar_periodo(hora, periodo):
    """
    Valida y ajusta la hora según la franja horaria especificada.
    Devuelve la hora en formato de 24h (0-23) o None si es inválida por rango.
    """
    if hora < 1 or hora > 12:
        return None
        
    hora_base = 0 if hora == 12 else hora

    if periodo == "de la mañana" and (4 <= hora <= 12):
        return hora_base
    elif periodo == "del mediodía" and (hora == 12 or 1 <= hora <= 3):
        return hora_base if hora == 12 else hora + 12
    elif periodo == "de la tarde" and (3 <= hora <= 8):
        return hora + 12
    elif periodo == "de la noche" and ((8 <= hora <= 12) or (1 <= hora <= 4)):
        return hora_base if hora == 12 else (hora + 12 if hora >= 8 else hora)
    elif periodo == "de la madrugada" and (1 <= hora <= 6):
        return hora
        
    return None

def procesar_match(match):
    """
    Analiza los grupos capturados por la regex y devuelve
    la cadena normalizada 'HH:MM' o la cadena original si es inválida.
    """
    texto_original = match.group(0)
    d = match.groupdict()

    # --- FORMATO 1: HH:MM estándar ---
    if d['h1'] is not None:
        h, m = int(d['h1']), int(d['m1'])
        if 0 <= h <= 23 and 0 <= m <= 59:
            return f"{h:02d}:{m:02d}"
        return texto_original

    # --- FORMATO 2: XhYm o Xh ---
    if d['h2'] is not None:
        h = int(d['h2'])
        m = int(d['m2']) if d['m2'] is not None else 0
        periodo = d['p2']
        
        if periodo:
            h_ajustada = validar_periodo(h, periodo)
            if h_ajustada is None or not (0 <= m <= 59):
                return texto_original
            h = h_ajustada
        else:
            if not (0 <= h <= 23) or not (0 <= m <= 59):
                return texto_original
            if d['m2'] is None and h > 12:
                return texto_original
            if h == 12 and d['m2'] is None:
                h = 0
            
        return f"{h:02d}:{m:02d}"

    # --- FORMATO 3: Expresiones conversacionales ---
    if d['h3'] is not None:
        h = int(d['h3'])
        mod = d['mod3']
        periodo = d['p3']
        
        m = 0
        if mod == "y cuarto": m = 15
        elif mod == "y media": m = 30
        elif mod == "menos cuarto":
            m = 45
            h = h - 1
            if h == 0: h = 12
            
        if periodo:
            h_ajustada = validar_periodo(h, periodo)
            if h_ajustada is None:
                return texto_original
            h = h_ajustada
        else:
            if not (1 <= h <= 12):
                return texto_original
            h = 0 if h == 12 else h
            
        return f"{h:02d}:{m:02d}"

    return texto_original

def normalizaHoras(ficText, ficNorm):
    """
    Busca expresiones horarias en ficText, las normaliza al formato HH:MM
    y guarda el resultado final en el archivo ficNorm.

    Prueba unitaria (doctest):
    >>> texto_prueba = '''La llegada del tren está prevista a las 18:30
    ... Tenía su clase entre las 8h y las 10h30m
    ... Se acaba a las 4 y media de la tarde
    ... Empieza a trabajar a las 7h de la mañana
    ... Es lo mismo 5 menos cuarto que 4:45
    ... Tenemos descanso hasta las 17h5m
    ... Las campanadas son a las 12 de la noche'''
    
    >>> with open('horas_test.txt', 'w', encoding='utf-8') as f:
    ...     _ = f.write(texto_prueba)
    
    >>> normalizaHoras('horas_test.txt', 'horas_norm.txt')
    
    >>> with open('horas_norm.txt', 'r', encoding='utf-8') as f:
    ...     for linea in f:
    ...         print(linea.strip())
    La llegada del tren está prevista a las 18:30
    Tenía su clase entre las 08:00 y las 10:30
    Se acaba a las 16:30
    Empieza a trabajar a las 07:00
    Es lo mismo 04:45 que 04:45
    Tenemos descanso hasta las 17:05
    Las campanadas son a las 00:00
    """
    periodos = r"(?:de la mañana|del mediodía|de la tarde|de la noche|de la madrugada)"
    
    # f1: HH:MM estándar
    f1 = r"(?P<h1>\d{1,2}):(?P<m1>\d{2})"
    
    # f2: Formato compacto con 'h' y 'm' (Buscamos f2 antes para blindar el '17h5m' y '8h')
    f2 = r"(?P<h2>\d{1,2})h(?:(?P<m2>\d{1,2})m)?(?:\s+(?P<p2>" + periodos + r"))?"
    
    # f3: Modificado con lógica booleana OR interna (A o B) en la regex para que NUNCA capture un número solo.
    # Exige estrictamente: (Modificador + Periodo opcional) O (Periodo obligatorio sin modificador)
    f3 = r"(?P<h3>\d{1,2})(?:\s+(?P<mod3>en punto|y cuarto|y media|menos cuarto)(?:\s+(?P<p3>" + periodos + r"))?|\s+(?P<p3_solo>" + periodos + r"))"
    
    # Orden óptimo: f1 (dos puntos), f2 (con 'h' explícita), f3 (frases conversacionales blindadas)
    patron_completo = re.compile(f"{f1}|{f2}|{f3}")

    def wrapper_match(m):
        d = m.groupdict()
        # Si cayó en 'p3_solo' (como '12 de la noche'), lo movemos a 'p3' para procesar_match
        if d.get('p3_solo') is not None:
            m.groupdict()['p3'] = d['p3_solo']
            m.groupdict()['mod3'] = None
        return procesar_match(m)

    try:
        with open(ficText, 'r', encoding='utf-8') as entrada, \
             open(ficNorm, 'w', encoding='utf-8') as salida:
             
            for linea in entrada:
                linea_normalizada = patron_completo.sub(wrapper_match, linea)
                salida.write(linea_normalizada)
                
    except FileNotFoundError:
        print(f"Error: No se pudo abrir el archivo de entrada.")

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE, verbose=True)
    
    for fichero in ['horas_test.txt', 'horas_norm.txt']:
        if os.path.exists(fichero):
            os.remove(fichero)