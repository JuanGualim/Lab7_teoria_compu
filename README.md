# Laboratorio 7 – Teoría de la Computación

Programa en **Python** que carga gramáticas libres de contexto desde archivos de texto,
valida cada línea con una expresión regular (usando un motor propio de regex → AFN,
basado en el Proyecto 1) y elimina las **producciones-ε**, mostrando cada paso del algoritmo.

## Video de demostración

📺 [Ver video en YouTube](https://youtu.be/CNgQhv6p3Eg)

## Estructura

```
.
├── main.py                  # Programa principal
├── src/
│   ├── regex_engine.py      # Shunting Yard + Thompson + simulación de AFN (Proyecto 1)
│   ├── grammar.py           # Carga y validación de gramáticas
│   └── epsilon.py           # Eliminación de producciones-ε
├── gramaticas/
│   ├── gramatica1.txt       # Gramática 1 del Problema 2
│   ├── gramatica2.txt       # Gramática 2 del Problema 2
│   ├── gramatica3.txt       # Gramática 3 del Problema 2
│   └── gramatica_error.txt  # Gramática con errores para la demostración
├── problema2/
│   ├── Problema2.pdf        # Problema 2: ε, unarias, inútiles y CNF (a mano)
│   └── generar_pdf.py
└── tests/test_lab7.py       # Pruebas unitarias
```

## Uso

Requiere Python 3.8+ (sin dependencias externas para el programa).

```bash
python main.py                                  # procesa las tres gramáticas
python main.py gramaticas/gramatica1.txt        # un archivo específico
python main.py gramaticas/gramatica_error.txt   # muestra la validación deteniendo la ejecución
python -m unittest -v                           # pruebas
```

## Formato de los archivos

- Una o más producciones por línea, separadas por `|`: `S -> 0A0 | 1B1 | BB`
- Mayúsculas = no-terminales; minúsculas y dígitos = terminales.
- La flecha puede ser `->` o `→`; épsilon se escribe `ε`. Los espacios se ignoran.

## Validación

Cada línea (sin espacios) debe ser aceptada por la expresión regular:

```
[A-Z](->|→)(ε|[A-Za-z0-9]+)(\|(ε|[A-Za-z0-9]+))*
```

La expresión se convierte a postfix (Shunting Yard), luego a un AFN (Thompson) y se
simula. Si alguna línea no es aceptada, el programa indica la línea y el símbolo donde
falló, y **detiene la ejecución**.

## Algoritmo de eliminación de producciones-ε

1. **Símbolos anulables**: base `X → ε`; inducción: si `A → X1…Xk` con todos los `Xi`
   anulables, `A` es anulable. Se muestra cada iteración.
2. **Producciones anulables**: se listan las que contienen ε o algún símbolo anulable.
3. **Nuevas producciones**: para cada producción con `m` símbolos anulables se generan los
   `2^m` casos (cada anulable presente o ausente), descartando los cuerpos vacíos y las
   producciones triviales `A → A`.
4. Se imprime la gramática resultante sin producciones-ε.

## Problema 2 (teórico)

La solución con todo el procedimiento (eliminación de producciones-ε, producciones unarias,
símbolos inútiles y Forma Normal de Chomsky) de las tres gramáticas está en
[`problema2/Problema2.pdf`](problema2/Problema2.pdf).

## Resultados del programa (gramáticas sin producciones-ε)

**Gramática 1**
```
S → 0A0 | 00 | 1B1 | 11 | BB | B
A → C
B → S | A
C → S
```

**Gramática 2**
```
S → aAa | aa | bBb | bb
A → C | a
B → C | b
C → CDE | CE | DE | E
D → A | B | ab
```

**Gramática 3**
```
S → ASA | AS | SA | aB | a
A → B | S
B → b
```
