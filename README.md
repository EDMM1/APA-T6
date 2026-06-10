# Expresiones Regulares

## Nom i cognoms

> [!Important]
> Introduzca a continuación su nombre y apellidos:
>
> Edgar Milián Marín

## Aviso Importante

> [!Caution]
> 
> El objetivo de esta tarea es aprender a usar las expresiones regulares. En concreto, su
> implementación en Python. A los profesores de la asignatura les importa un pimiento si
> usted conoce alguna biblioteca que hace el mismo trabajo de manera más sencilla y/o
> eficiente; su uso está prohibido.
>
> ¿Quiere saber más?, consulte con el profesorado.
 
## Fecha de entrega: 7 de junio a medianoche

## Tratamiento de ficheros de notas

Con el final de curso llega la ardua tarea de evaluar las tareas realizadas por los alumnos durante el
mismo. Para facilitar esta tarea, se dispone de la clase `Alumno` que proporciona los datos
fundamentales de cada alumno: su número de identificación (`numIden`), su nombre completo 
(`nombre`) y la lista de notas obtenidas a lo largo del curso (`notas`). La clase también
proporciona métodos para añadir una nota al expediente del alumno (`__add__()`), para obtener
la representación *oficial* del mismo (`__repr__()`) y para obtener la representación
*bonita* (`__str__()`).

La definición de la clase `Alumno`, disponible en `alumno.py`, es:

```python
class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'
```

A menudo, las notas de los alumnos se almacenan en ficheros de texto en los que los datos de cada alumno
ocupan una línea con los distintos valores separados por espacios y/o tabuladores.

El ejemplo siguiente muestra un fichero típico con las notas de tres alumnos:

```text
171 Blanca Agirrebarrenetse 10  	9 	  9.5
23  Carles Balcell de Lara  5 	    5 	  4.5  	5.2
68  David Garcia Fuster 	7.75    5.25  8   
```

Añada al fichero `alumno.py` la función `leeAlumnos(ficAlum)` que lea un fichero de texto con los datos de 
todos los alumnos y devuelva un diccionario en el que la clave sea el nombre de cada alumno y su contenido 
el objeto `Alumno` correspondiente.

La función deberá cumplir los requisitos siguientes:

- Sólo debe realizar lo que se indica; es decir, debe leer el fichero de texto que se le pasa como único
  argumento y devolver un diccionario con los datos de los alumnos.
- El análisis de cada línea de texto se realizará usando expresiones regulares.
- La función `leeAlumnos()` debe incluir, en su cadena de documentación, la prueba unitaria siguiente según
  el formato de la biblioteca `doctest`, donde el fichero `'alumnos.txt'` es el fichero mostrado como ejemplo
  al principio de este enunciado:

  ```python
  >>> alumnos = leeAlumnos('alumnos.txt')
  >>> for alumno in alumnos:
  ...     print(alumnos[alumno])
  ...
  171     Blanca Agirrebarrenetse 9.5
  23      Carles Balcells de Lara 4.9
  68      David Garcia Fuster     7.0
  ```

  - Evidentemente, es responsabilidad del autor comprobar que la prueba unitaria se pasa satisfactoriamente
    antes de la entrega de la tarea.

  - Para evitar que diferencias debidas a espacios en blanco o tabuladores den lugar a error, se recomienda
    efectuar las pruebas unitarias con la opción `doctest.NORMALIZE_WHITESPACE`. Por ejemplo,
    `doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)`.


## Análisis de expresiones horarias

En casi todos los idiomas más habituales, cualquier hora puede reducirse al formato estándar HH:MM, donde HH es 
un número de dos dígitos, que representa la hora y está comprendido entre 00 y 23, y MM es otro número de dos 
dígitos, que representa el minuto y está comprendido entre 00 y 59.

No obstante, en el lenguaje hablado, es raro usar este formato estándar. En el caso del castellano, existe una
gran variedad de formatos. La lista siguiente alguna de las posibilidades más frecuentes, aunque existen bastantes
más:

- **08:27**

  Es el formato estándar. Cuando la hora es menor que 10, es posible representarla con
  dos dígitos (08:27), o sólo uno (8:27). Los minutos se representan siempre con dos (8:05).

- **8h27m**

  Las horas o minutos menores que 10 pueden representarse usando uno o dos dígitos. Las horas
  *en punto* pueden indicarse sin minutos (8h).

- **8 en punto**

  Las horas exactas suelen indicarse con la partícula *'en punto'*. En ese caso, es
  habitual omitir la letra *h* después de la cifra.

  Otras alternativas semejantes son las *'8 y cuarto'*, las *'8 y media'* o las *'8 menos cuarto'*.

  En todos estos casos, el reloj empleado será de 12 horas y empezando en 1 (de 1 a 12). El
  resultado será ambiguo, ya que no sabremos si una cierta hora es AM o PM, pero así es cómo
  se suele hablar (la gente queda a *'las 11 en punto'* para ir a una fiesta, no a las
  *'las 23 en punto'*). El resultado se devolverá siempre en el rango de 00:00 a 11:59.

- **... de la mañana**

  Las expresiones horarias entre las 4 y las 12 pueden ir seguidas de la partícula *'de la mañana'*.

  Análogamente, las horas entre las 12 y las 3 pueden ir seguidas de *'del mediodía'*, las horas entre
  las 3 y las 8 pueden serlo de *'de la tarde'*, entre 8 y 4 de *'de la noche'* y entre 1 y
  6 de *'de la madrugada'*.

  En estos casos, el reloj empleado es siempre de 12 horas (nunca se dice *'las 18 de la tarde'*, sino
  *'las 6 de la tarde'*). Además la hora no puede ser cero, sino que, en ese caso, se usaría 12.

### Tarea: normalización de las expresiones horarias de un texto

Escriba el fichero `horas.py` con la función `normalizaHoras(ficText, ficNorm)`, que lee el fichero de
texto `ficText`, lo analiza en busca de expresiones horarias y escribe el fichero `ficNorm` en el que
éstas se expresan según el formato normalizado, con las horas y los minutos indicados por dos dígitos
y separados por dos puntos (08:27).

Cada línea del fichero puede contener, o no, una o más expresiones horarias, pero éstas nunca aparecerán
partidas en más de una línea.

Las horas con expresión incorrecta, por ejemplo, *'17:5'* (en la expresión normalizada deben usarse dos
dígitos para expresar los minutos) u *'11 de la tarde'* (la tarde nunca llega hasta esa hora), deben
dejarse tal cual.

Para la evaluación de la tarea se usará un texto con unas cien expresiones horarias, que incluirán tanto
expresiones correctas como incorrectas. Una parte de la nota dependerá de la precisión en su normalización.

Se recomienda empezar normalizando textos que sólo contengan expresiones correctas del tipo más sencillo;
es decir, con la forma *'18h45m'*. La consecución de este objetivo garantiza una nota mínima de notable
bajo (7). La extensión al resto de formatos indicados y la detección de expresiones incorrectas serán
necesarias para alcanzar la nota máxima (10).

La tabla siguiente muestra un ejemplo de texto antes y después de su normalización, incluyendo tanto
expresiones horarias **correctas** como <span style="color:red">**incorrectas**</span>.

### Ejemplo de normalización de las expresiones horarias de un texto

Las líneas siguientes muestran ejemplos de expresiones horarias, tanto correctas como incorrectas. Las
mismas expresiones se encuentran en el fichero `horas.txt`, que puede usar para comprobar el correcto
funcionamiento de su función.

#### Expresiones válidas

> - La llegada del tren está prevista a las **18:30**
> - La llegada del tren está prevista a las **18:30**

> - Tenía su clase entre las **8h** y las **10h30m**
> - Tenía su clase entre las **08:00** y las **10:30**

> - Se acaba a las **4 y media de la tarde**
> - Se acaba a las **16:30**

> - Empieza a trabajar a las **7h de la mañana**
> - Empieza a trabajar a las **07:00**

> - Es lo mismo **5 menos cuarto** que **4:45**
> - Es lo mismo **04:45** que **04:45**

> - Tenemos descanso hasta las **17h5m**
> - Tenemos descanso hasta las **17:05**

> - Las campanadas son a las **12 de la noche**
> - Las campanadas son a las **00:00**

#### Expresiones incorrectas

> - Son exactamente las $\textbf{\color{red}17:5}$
> - Son exactamente las $\textbf{\color{red}17:5}$

> - Cuando llegó, ya eran las $\textbf{\color{red}11 de la tarde}$
> - Cuando llegó, ya eran las $\textbf{\color{red}11 de la tarde}$

> - El examen es a las $\textbf{\color{red}17 de la tarde}$
> - El examen es a las $\textbf{\color{red}17 de la tarde}$

> - Cenamos en las $\textbf{\color{red}7}$ puertas
> - Cenamos en las $\textbf{\color{red}7}$ puertas

> - No llegará antes de las $\textbf{\color{red}1h78m}$
> - No llegará antes de las $\textbf{\color{red}1h78m}$

> - *Corrió* la maratón en $\textbf{\color{red}32h31m}$, pero no ganó
> - *Corrió* la maratón en $\textbf{\color{red}32h31m}$, pero no ganó

> - Quedamos a las $\textbf{\color{red}23 en punto}$
> - Quedamos a las $\textbf{\color{red}23 en punto}$


#### Entrega

##### Ficheros `alumno.py` y `horas.py`

- Ambos ficheros deben incluir una cadena de documentación con el nombre del alumno o alumnos
  y una descripción de su contenido.

- Se valorará lo pythónico de la solución; en concreto, su claridad y sencillez, y el
  uso de los estándares marcados por PEP-ocho.

##### Ejecución de los tests unitarios de `alumno.py`

Inserte a continuación una captura de pantalla que muestre el resultado de ejecutar el
fichero `alumno.py` con la opción *verbosa*, de manera que se muestre el
resultado de la ejecución de los tests unitarios.

<img src="img/test.PNG" alt="Test unitario alumno.py">

##### Código desarrollado

Inserte a continuación los códigos fuente desarrollados en esta tarea, usando los
comandos necesarios para que se realice el realce sintáctico en Python del mismo (no
vale insertar una imagen o una captura de pantalla, debe hacerse en formato *markdown*).<br><br>
<strong>Código alumno.py</strong>
```python
class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'


import re

def leeAlumnos(ficAlum):
    """
    Lee un fichero de texto con los datos de los alumnos y devuelve un
    diccionario donde la clave es el nombre del alumno y el valor es
    el objeto 'Alumno' correspondiente.

    La función analiza cada línea mediante expresiones regulares.

    Prueba unitaria (doctest):
    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171\tBlanca Agirrebarrenetse\t9.5
    23\tCarles Balcell de Lara\t4.9
    68\tDavid Garcia Fuster\t7.0
    """
    dicc_alumnos = {}
    
    # Expresión regular:
    # ^(\\d+): Captura el ID al inicio
    # \\s+(.+?): Captura el nombre de forma no codiciosa hasta las notas
    # \\s+([\\d\\s.]+?)$: Captura la secuencia de notas al final de la línea
    patron = re.compile(r"^(\d+)\s+(.+?)\s+([\d\s.]+?)$")

    try:
        with open(ficAlum, 'r', encoding='utf-8') as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                
                match = patron.match(linea)
                if match:
                    id_str, nombre, notas_str = match.groups()
                    num_id = int(id_str)
                    
                    # Extraemos todas las notas individuales de la subcadena
                    notas = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", notas_str)]
                    
                    # Creamos el objeto Alumno y lo guardamos
                    dicc_alumnos[nombre] = Alumno(nombre, num_id, notas)
    except FileNotFoundError:
        print(f"Error: El fichero '{ficAlum}' no existe.")
        
    return dicc_alumnos

if __name__ == "__main__":
    import doctest
    # Se ejecuta el doctest con normalización de espacios en blanco
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE, verbose=True)
```
<br><br>
<strong>Código horas.py </strong>
```python
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
```

##### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y
visualizarse correctamente en el repositorio, incluyendo la imagen con la ejecución de
los tests unitarios y el realce sintáctico del código fuente insertado.

##### Y NADA MÁS

Sólo se corregirá el contenido de este fichero `README.md` y los códigos fuente `alumno.py`
y `horas.py`. No incluya otros ficheros con código fuente, notebooks de Jupyter o explicaciones
adicionales; simplemente, no se tendrán en cuenta para la evaluación de la tarea. Evidentemente,
sí puede añadir ficheros con las imágenes solicitadas en el enunciado, pero éstas deberán ser
visualizadas correctamente desde este mismo fichero al acceder al repositorio de la tarea.