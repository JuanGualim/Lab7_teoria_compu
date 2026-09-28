"""Genera problema2/Problema2.pdf con la solución del Problema 2."""

import os

from fpdf import FPDF

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTES = "/usr/share/fonts/truetype/dejavu"

INTRO = [
    ("h1", "Laboratorio 7 – Teoría de la Computación"),
    ("p", "Problema 2: para cada CFG se realiza (a) eliminación de producciones-ε, "
          "(b) eliminación de producciones unarias, (c) eliminación de símbolos inútiles "
          "y (d) conversión a la Forma Normal de Chomsky (CNF)."),
    ("h3", "Procedimientos utilizados"),
    ("p", "a) Producciones-ε: se calculan los símbolos anulables (base: X → ε; inducción: "
          "si A → X1…Xk y todos los Xi son anulables, A es anulable). Para cada producción con "
          "m símbolos anulables se forman los 2^m casos (cada anulable presente o ausente), y "
          "se descartan los cuerpos vacíos y las producciones triviales A → A. Si S es anulable, "
          "la gramática resultante genera L(G) − {ε}."),
    ("p", "b) Producciones unarias: se calculan los pares unarios (A, B) tales que A ⇒* B usando "
          "solo producciones unarias. Para cada par (A, B) se agrega A → α por cada producción "
          "no unaria B → α, y se eliminan todas las producciones unarias."),
    ("p", "c) Símbolos inútiles: (1) se eliminan los símbolos que no producen (no derivan "
          "ninguna cadena de terminales) junto con toda producción que los contenga; "
          "(2) se eliminan los símbolos no alcanzables desde S. El orden (primero no "
          "productores, luego no alcanzables) es importante."),
    ("p", "d) CNF: toda producción debe ser A → BC o A → a. (1) En cuerpos de longitud ≥ 2 "
          "cada terminal t se reemplaza por una variable nueva Xt → t; (2) los cuerpos de "
          "longitud ≥ 3 se dividen en cadenas de producciones binarias con variables nuevas."),
]

G1 = [
    ("h2", "Gramática 1"),
    ("code", "S → 0A0 | 1B1 | BB\nA → C\nB → S | A\nC → S | ε"),

    ("h3", "a) Eliminación de producciones-ε"),
    ("p", "Anulables:\n"
          "• Base: C → ε, entonces C es anulable.\n"
          "• A → C con C anulable, entonces A es anulable.\n"
          "• B → A con A anulable, entonces B es anulable.\n"
          "• S → BB con B anulable, entonces S es anulable.\n"
          "Anulables = { S, A, B, C }"),
    ("code", "S → 0A0   m=1 (A)    → 0A0, 00\n"
             "S → 1B1   m=1 (B)    → 1B1, 11\n"
             "S → BB    m=2 (B,B)  → BB, B, B, ε   (ε se descarta)\n"
             "A → C     m=1 (C)    → C, ε          (ε se descarta)\n"
             "B → S     m=1 (S)    → S, ε          (ε se descarta)\n"
             "B → A     m=1 (A)    → A, ε          (ε se descarta)\n"
             "C → S     m=1 (S)    → S, ε          (ε se descarta)\n"
             "C → ε                → se elimina"),
    ("p", "Resultado (genera L(G) − {ε}, ya que S es anulable):"),
    ("code", "S → 0A0 | 00 | 1B1 | 11 | BB | B\nA → C\nB → S | A\nC → S"),

    ("h3", "b) Eliminación de producciones unarias"),
    ("p", "Producciones unarias: S → B, A → C, B → S, B → A, C → S. Todas las variables "
          "quedan en un ciclo S → B → A → C → S, por lo que:"),
    ("code", "Pares unarios:\n"
             "  S: (S,S) (S,B) (S,A) (S,C)\n"
             "  A: (A,A) (A,C) (A,S) (A,B)\n"
             "  B: (B,B) (B,S) (B,A) (B,C)\n"
             "  C: (C,C) (C,S) (C,B) (C,A)\n"
             "Producciones no unarias: S → 0A0 | 00 | 1B1 | 11 | BB  (A, B y C no tienen)"),
    ("p", "Cada variable recibe las producciones no unarias de S:"),
    ("code", "S → 0A0 | 00 | 1B1 | 11 | BB\n"
             "A → 0A0 | 00 | 1B1 | 11 | BB\n"
             "B → 0A0 | 00 | 1B1 | 11 | BB\n"
             "C → 0A0 | 00 | 1B1 | 11 | BB"),

    ("h3", "c) Eliminación de símbolos inútiles"),
    ("p", "c.a) Símbolos que no producen: S, A, B y C producen la cadena 00, por lo que "
          "todos son productores. No se elimina nada.\n"
          "c.b) Símbolos no alcanzables: desde S se alcanzan A (0A0), B (1B1, BB), 0 y 1. "
          "C no aparece en ningún cuerpo alcanzable, por lo tanto se elimina."),
    ("code", "S → 0A0 | 00 | 1B1 | 11 | BB\n"
             "A → 0A0 | 00 | 1B1 | 11 | BB\n"
             "B → 0A0 | 00 | 1B1 | 11 | BB"),

    ("h3", "d) Forma Normal de Chomsky"),
    ("p", "Terminales en cuerpos largos: X0 → 0, X1 → 1. Cuerpos de longitud 3: "
          "0A0 = X0 A X0 → X0 D1 con D1 → A X0; 1B1 = X1 B X1 → X1 D2 con D2 → B X1."),
    ("code", "S  → X0 D1 | X0 X0 | X1 D2 | X1 X1 | B B\n"
             "A  → X0 D1 | X0 X0 | X1 D2 | X1 X1 | B B\n"
             "B  → X0 D1 | X0 X0 | X1 D2 | X1 X1 | B B\n"
             "D1 → A X0\n"
             "D2 → B X1\n"
             "X0 → 0\n"
             "X1 → 1"),
]

G2 = [
    ("h2", "Gramática 2"),
    ("code", "S → aAa | bBb | ε\nA → C | a\nB → C | b\nC → CDE | ε\nD → A | B | ab"),

    ("h3", "a) Eliminación de producciones-ε"),
    ("p", "Anulables:\n"
          "• Base: S → ε y C → ε, entonces S y C son anulables.\n"
          "• A → C y B → C, entonces A y B son anulables.\n"
          "• D → A, entonces D es anulable.\n"
          "• E no tiene producciones, por lo que no es anulable.\n"
          "Anulables = { S, A, B, C, D }"),
    ("code", "S → aAa   m=1 (A)    → aAa, aa\n"
             "S → bBb   m=1 (B)    → bBb, bb\n"
             "S → ε                → se elimina\n"
             "A → C     m=1 (C)    → C, ε          (ε se descarta)\n"
             "A → a     m=0        → a\n"
             "B → C     m=1 (C)    → C, ε          (ε se descarta)\n"
             "B → b     m=0        → b\n"
             "C → CDE   m=2 (C,D)  → CDE, CE, DE, E\n"
             "C → ε                → se elimina\n"
             "D → A     m=1 (A)    → A, ε          (ε se descarta)\n"
             "D → B     m=1 (B)    → B, ε          (ε se descarta)\n"
             "D → ab    m=0        → ab"),
    ("p", "Resultado (genera L(G) − {ε}, ya que S es anulable):"),
    ("code", "S → aAa | aa | bBb | bb\nA → C | a\nB → C | b\nC → CDE | CE | DE | E\nD → A | B | ab"),

    ("h3", "b) Eliminación de producciones unarias"),
    ("p", "Producciones unarias: A → C, B → C, C → E, D → A, D → B."),
    ("code", "Pares unarios:\n"
             "  S: (S,S)\n"
             "  A: (A,A) (A,C) (A,E)\n"
             "  B: (B,B) (B,C) (B,E)\n"
             "  C: (C,C) (C,E)\n"
             "  D: (D,D) (D,A) (D,B) (D,C) (D,E)\n"
             "  E: (E,E)\n"
             "Producciones no unarias:\n"
             "  S → aAa | aa | bBb | bb     A → a     B → b\n"
             "  C → CDE | CE | DE           D → ab    E: ninguna"),
    ("code", "S → aAa | aa | bBb | bb\n"
             "A → a | CDE | CE | DE\n"
             "B → b | CDE | CE | DE\n"
             "C → CDE | CE | DE\n"
             "D → ab | a | b | CDE | CE | DE"),

    ("h3", "c) Eliminación de símbolos inútiles"),
    ("p", "c.a) Símbolos que no producen: A produce a, B produce b, D produce ab y S produce aa. "
          "E no tiene producciones, así que no produce; todas las producciones de C contienen E, "
          "así que C tampoco produce. Se eliminan C, E y toda producción que los contenga:"),
    ("code", "S → aAa | aa | bBb | bb\nA → a\nB → b\nD → ab | a | b"),
    ("p", "c.b) Símbolos no alcanzables: desde S se alcanzan A, B, a y b. D no es alcanzable, "
          "por lo tanto se elimina."),
    ("code", "S → aAa | aa | bBb | bb\nA → a\nB → b"),

    ("h3", "d) Forma Normal de Chomsky"),
    ("p", "Terminales en cuerpos largos: Xa → a, Xb → b. Cuerpos de longitud 3: "
          "aAa = Xa A Xa → Xa D1 con D1 → A Xa; bBb = Xb B Xb → Xb D2 con D2 → B Xb."),
    ("code", "S  → Xa D1 | Xa Xa | Xb D2 | Xb Xb\n"
             "D1 → A Xa\n"
             "D2 → B Xb\n"
             "A  → a\n"
             "B  → b\n"
             "Xa → a\n"
             "Xb → b"),
]

G3 = [
    ("h2", "Gramática 3"),
    ("code", "S → ASA | aB\nA → B | S\nB → b | ε"),

    ("h3", "a) Eliminación de producciones-ε"),
    ("p", "Anulables:\n"
          "• Base: B → ε, entonces B es anulable.\n"
          "• A → B con B anulable, entonces A es anulable.\n"
          "• S no es anulable: S → aB contiene el terminal a y S → ASA necesitaría que S "
          "ya fuera anulable.\n"
          "Anulables = { A, B }"),
    ("code", "S → ASA   m=2 (A,A)  → ASA, SA, AS, S   (S → S es trivial, se descarta)\n"
             "S → aB    m=1 (B)    → aB, a\n"
             "A → B     m=1 (B)    → B, ε             (ε se descarta)\n"
             "A → S     m=0        → S\n"
             "B → b     m=0        → b\n"
             "B → ε                → se elimina"),
    ("p", "Resultado (S no es anulable, así que el lenguaje no cambia):"),
    ("code", "S → ASA | SA | AS | aB | a\nA → B | S\nB → b"),

    ("h3", "b) Eliminación de producciones unarias"),
    ("p", "Producciones unarias: A → B, A → S."),
    ("code", "Pares unarios:\n"
             "  S: (S,S)\n"
             "  A: (A,A) (A,B) (A,S)\n"
             "  B: (B,B)\n"
             "Producciones no unarias:\n"
             "  S → ASA | SA | AS | aB | a     B → b     A: ninguna"),
    ("code", "S → ASA | SA | AS | aB | a\n"
             "A → b | ASA | SA | AS | aB | a\n"
             "B → b"),

    ("h3", "c) Eliminación de símbolos inútiles"),
    ("p", "c.a) Símbolos que no producen: B produce b, S produce a y A produce b. Todos producen.\n"
          "c.b) Símbolos no alcanzables: desde S se alcanzan A (ASA), B (aB), a y b. Todos son "
          "alcanzables. La gramática no cambia:"),
    ("code", "S → ASA | SA | AS | aB | a\n"
             "A → b | ASA | SA | AS | aB | a\n"
             "B → b"),

    ("h3", "d) Forma Normal de Chomsky"),
    ("p", "Terminal en cuerpo largo: Xa → a (aB → Xa B). Cuerpo de longitud 3: "
          "ASA → A D1 con D1 → S A."),
    ("code", "S  → A D1 | S A | A S | Xa B | a\n"
             "A  → b | A D1 | S A | A S | Xa B | a\n"
             "B  → b\n"
             "D1 → S A\n"
             "Xa → a"),
]


def main():
    pdf = FPDF()
    pdf.add_font("DejaVu", "", os.path.join(FUENTES, "DejaVuSans.ttf"))
    pdf.add_font("DejaVu", "B", os.path.join(FUENTES, "DejaVuSans-Bold.ttf"))
    pdf.add_font("Mono", "", os.path.join(FUENTES, "DejaVuSansMono.ttf"))
    pdf.set_margins(20, 20, 20)
    pdf.set_auto_page_break(True, 18)
    pdf.add_page()
    for i, seccion in enumerate([INTRO, G1, G2, G3]):
        if i > 0:
            pdf.add_page()
        for tipo, texto in seccion:
            if tipo == "h1":
                pdf.set_font("DejaVu", "B", 16)
                pdf.multi_cell(0, 9, texto, new_x="LMARGIN", new_y="NEXT")
                pdf.ln(1)
            elif tipo == "h2":
                pdf.set_font("DejaVu", "B", 14)
                pdf.multi_cell(0, 9, texto, new_x="LMARGIN", new_y="NEXT")
            elif tipo == "h3":
                pdf.ln(2)
                pdf.set_font("DejaVu", "B", 11)
                pdf.multi_cell(0, 7, texto, new_x="LMARGIN", new_y="NEXT")
            elif tipo == "code":
                alto = 5.2 * (texto.count("\n") + 1)
                if pdf.get_y() + alto > pdf.h - 18:
                    pdf.add_page()
                pdf.set_font("Mono", "", 9.5)
                pdf.set_fill_color(242, 242, 242)
                pdf.multi_cell(0, 5.2, texto, fill=True, new_x="LMARGIN", new_y="NEXT")
                pdf.ln(2)
            else:
                pdf.set_font("DejaVu", "", 10)
                pdf.multi_cell(0, 5.6, texto, new_x="LMARGIN", new_y="NEXT")
                pdf.ln(1)
    pdf.output(os.path.join(AQUI, "Problema2.pdf"))


if __name__ == "__main__":
    main()
