"""
Laboratorio 7 - Teoría de la Computación
Simplificación de gramáticas: eliminación de producciones-ε.

Uso:
    python main.py                      # procesa gramaticas/gramatica1.txt y gramatica2.txt
    python main.py archivo1.txt [...]   # procesa los archivos indicados
"""

import sys

from src.epsilon import eliminar_epsilon
from src.grammar import ErrorGramatica, cargar_gramatica

ARCHIVOS_POR_DEFECTO = ["gramaticas/gramatica1.txt", "gramaticas/gramatica2.txt"]


def procesar(ruta):
    print("=" * 70)
    print(f"Archivo: {ruta}")
    print("=" * 70)
    print("Validación de las líneas del archivo")
    g = cargar_gramatica(ruta)

    print("\nGramática original:")
    print(g)
    print()

    resultado, _ = eliminar_epsilon(g)

    print("Gramática sin producciones-ε:")
    print(resultado)
    print()


def main():
    archivos = sys.argv[1:] or ARCHIVOS_POR_DEFECTO
    for ruta in archivos:
        try:
            procesar(ruta)
        except FileNotFoundError:
            print(f"ERROR: no se encontró el archivo {ruta}")
            sys.exit(1)
        except ErrorGramatica as e:
            print(f"\nERROR: {e}")
            print("La gramática está mal escrita. Se detiene la ejecución.")
            sys.exit(1)


if __name__ == "__main__":
    main()
