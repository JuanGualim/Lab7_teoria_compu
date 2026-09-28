"""
Carga y validación de gramáticas libres de contexto desde archivos de texto.

Convenciones:
  - Una letra mayúscula es un no-terminal; minúsculas y dígitos son terminales.
  - La flecha puede escribirse como '->' o '→'.
  - Épsilon se escribe como 'ε'.
  - Varias producciones de una línea se separan con '|'.
  - Los espacios se ignoran; las líneas vacías o que inician con '#' se omiten.
"""

from .regex_engine import Regex

EPSILON = "ε"

# Expresión regular que acepta una línea de producciones (sin espacios):
#   [A-Z] (->|→) cuerpo (\| cuerpo)*     con cuerpo = ε | [A-Za-z0-9]+
CUERPO = "(ε|[A-Za-z0-9]+)"
REGEX_PRODUCCION = "[A-Z](->|→)" + CUERPO + "(\\|" + CUERPO + ")*"

_validador = Regex(REGEX_PRODUCCION)


class ErrorGramatica(Exception):
    pass


class Gramatica:
    def __init__(self, inicial=None):
        self.inicial = inicial
        self.producciones = {}  # no-terminal -> lista de tuplas de símbolos

    def agregar(self, cabeza, cuerpo):
        if self.inicial is None:
            self.inicial = cabeza
        lista = self.producciones.setdefault(cabeza, [])
        if cuerpo not in lista:
            lista.append(cuerpo)

    def no_terminales(self):
        return list(self.producciones)

    def copiar(self):
        g = Gramatica(self.inicial)
        for cabeza, cuerpos in self.producciones.items():
            g.producciones[cabeza] = list(cuerpos)
        return g

    @staticmethod
    def cuerpo_a_str(cuerpo):
        return "".join(cuerpo) if cuerpo else EPSILON

    def __str__(self):
        lineas = []
        for cabeza, cuerpos in self.producciones.items():
            if cuerpos:
                lineas.append(f"{cabeza} → " + " | ".join(self.cuerpo_a_str(c) for c in cuerpos))
        return "\n".join(lineas)


def validar_linea(linea):
    """Devuelve (True, None) si la línea es válida, o (False, mensaje) si no."""
    compacta = "".join(linea.split())
    if _validador.acepta(compacta):
        return True, None
    pos = _validador.fallo_en(compacta)
    if pos >= len(compacta):
        return False, "la línea termina de forma incompleta"
    return False, f"símbolo inesperado '{compacta[pos]}' en la posición {pos + 1} de '{compacta}'"


def parsear_linea(linea):
    compacta = "".join(linea.split()).replace("→", "->")
    cabeza, cuerpos = compacta.split("->", 1)
    resultado = []
    for alt in cuerpos.split("|"):
        resultado.append(tuple() if alt == EPSILON else tuple(alt))
    return cabeza, resultado


def cargar_gramatica(ruta, verbose=True):
    """Lee y valida un archivo. Lanza ErrorGramatica ante la primera línea inválida."""
    with open(ruta, encoding="utf-8") as f:
        lineas = f.read().splitlines()

    if verbose:
        print(f"Expresión regular de validación: {REGEX_PRODUCCION}\n")

    g = Gramatica()
    for num, linea in enumerate(lineas, start=1):
        if not linea.strip() or linea.strip().startswith("#"):
            continue
        ok, error = validar_linea(linea)
        if not ok:
            if verbose:
                print(f"  Línea {num}: {linea!r:30} -> INVÁLIDA")
            raise ErrorGramatica(f"Error en la línea {num} ({linea.strip()!r}): {error}")
        if verbose:
            print(f"  Línea {num}: {linea!r:30} -> válida")
        cabeza, cuerpos = parsear_linea(linea)
        for c in cuerpos:
            g.agregar(cabeza, c)

    if not g.producciones:
        raise ErrorGramatica("El archivo no contiene producciones")

    sin_definir = sorted({s for cuerpos in g.producciones.values() for c in cuerpos
                          for s in c if s.isupper() and s not in g.producciones})
    if sin_definir and verbose:
        print(f"\n  Advertencia: no-terminales sin producciones: {', '.join(sin_definir)}")
    return g
