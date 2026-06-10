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