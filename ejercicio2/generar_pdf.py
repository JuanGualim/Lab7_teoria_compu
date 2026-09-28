"""Genera ejercicio2/Ejercicio2.pdf con la solución a mano del Ejercicio 2."""

import os

from fpdf import FPDF

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTES = "/usr/share/fonts/truetype/dejavu"

CONTENIDO = [
    ("h1", "Laboratorio 7 – Teoría de la Computación"),
    ("p", "Ejercicio 2: eliminación de producciones-ε"),
    ("p", "Procedimiento: (1) encontrar los símbolos anulables (A es anulable si A ⇒* ε); "
          "(2) por cada producción con m símbolos anulables en su cuerpo, formar los 2^m casos "
          "posibles, conservando u omitiendo cada anulable; (3) eliminar todas las producciones "
          "A → ε y las producciones triviales A → A."),

    ("h2", "Gramática 1"),
    ("code", "S → 0A0 | 1B1 | BB\nA → C\nB → S | A\nC → S | ε"),
    ("h3", "Paso 1: símbolos anulables"),
    ("p", "• Base: C → ε, por lo tanto C es anulable.\n"
          "• A → C y C es anulable, por lo tanto A es anulable.\n"
          "• B → A y A es anulable, por lo tanto B es anulable.\n"
          "• S → BB y B es anulable, por lo tanto S es anulable.\n"
          "Anulables = { S, A, B, C }"),
    ("h3", "Paso 2: nuevas producciones"),
    ("code", "S → 0A0   m=1 (A)    → 0A0, 00\n"
             "S → 1B1   m=1 (B)    → 1B1, 11\n"
             "S → BB    m=2 (B,B)  → BB, B, B, ε  (ε se descarta)\n"
             "A → C     m=1 (C)    → C, ε         (ε se descarta)\n"
             "B → S     m=1 (S)    → S, ε         (ε se descarta)\n"
             "B → A     m=1 (A)    → A, ε         (ε se descarta)\n"
             "C → S     m=1 (S)    → S, ε         (ε se descarta)\n"
             "C → ε                → se elimina"),
    ("h3", "Resultado"),
    ("code", "S → 0A0 | 00 | 1B1 | 11 | BB | B\nA → C\nB → S | A\nC → S"),
    ("p", "Como S es anulable, ε ∈ L(G); la nueva gramática genera L(G) − {ε}."),

    ("h2", "Gramática 2"),
    ("code", "S → aAa | bBb | ε\nA → C | a\nB → C | b\nC → CDE | ε\nD → A | B | ab"),
    ("h3", "Paso 1: símbolos anulables"),
    ("p", "• Base: S → ε y C → ε, por lo tanto S y C son anulables.\n"
          "• A → C y B → C, por lo tanto A y B son anulables.\n"
          "• D → A (o D → B), por lo tanto D es anulable.\n"
          "• E no tiene producciones, así que no es anulable (C → CDE no hace a C anulable por esta vía).\n"
          "Anulables = { S, A, B, C, D }"),
    ("h3", "Paso 2: nuevas producciones"),
    ("code", "S → aAa   m=1 (A)    → aAa, aa\n"
             "S → bBb   m=1 (B)    → bBb, bb\n"
             "S → ε                → se elimina\n"
             "A → C     m=1 (C)    → C, ε         (ε se descarta)\n"
             "A → a     m=0        → a\n"
             "B → C     m=1 (C)    → C, ε         (ε se descarta)\n"
             "B → b     m=0        → b\n"
             "C → CDE   m=2 (C,D)  → CDE, CE, DE, E\n"
             "C → ε                → se elimina\n"
             "D → A     m=1 (A)    → A, ε         (ε se descarta)\n"
             "D → B     m=1 (B)    → B, ε         (ε se descarta)\n"
             "D → ab    m=0        → ab"),
    ("h3", "Resultado"),
    ("code", "S → aAa | aa | bBb | bb\nA → C | a\nB → C | b\nC → CDE | CE | DE | E\nD → A | B | ab"),
    ("p", "Como S es anulable, ε ∈ L(G); la nueva gramática genera L(G) − {ε}. "
          "Observación: E no tiene producciones, por lo que es un símbolo inútil; en una "
          "simplificación posterior (eliminación de símbolos inútiles) desaparecerían E y "
          "todas las producciones de C, y con ellas las producciones A → C y B → C."),
]


def main():
    pdf = FPDF()
    pdf.add_font("DejaVu", "", os.path.join(FUENTES, "DejaVuSans.ttf"))
    pdf.add_font("DejaVu", "B", os.path.join(FUENTES, "DejaVuSans-Bold.ttf"))
    pdf.add_font("Mono", "", os.path.join(FUENTES, "DejaVuSansMono.ttf"))
    pdf.set_margins(20, 20, 20)
    pdf.add_page()
    for tipo, texto in CONTENIDO:
        if tipo == "h1":
            pdf.set_font("DejaVu", "B", 16)
            pdf.multi_cell(0, 9, texto, new_x="LMARGIN", new_y="NEXT")
        elif tipo == "h2":
            pdf.ln(4)
            pdf.set_font("DejaVu", "B", 13)
            pdf.multi_cell(0, 8, texto, new_x="LMARGIN", new_y="NEXT")
        elif tipo == "h3":
            pdf.set_font("DejaVu", "B", 11)
            pdf.multi_cell(0, 7, texto, new_x="LMARGIN", new_y="NEXT")
        elif tipo == "code":
            pdf.set_font("Mono", "", 10)
            pdf.set_fill_color(242, 242, 242)
            pdf.multi_cell(0, 5.5, texto, fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
        else:
            pdf.set_font("DejaVu", "", 10.5)
            pdf.multi_cell(0, 6, texto, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
    pdf.output(os.path.join(AQUI, "Ejercicio2.pdf"))


if __name__ == "__main__":
    main()
