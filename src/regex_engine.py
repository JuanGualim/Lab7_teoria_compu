"""
Motor de expresiones regulares (basado en el Proyecto 1).

Pasos:
  1. Tokenizar la expresión regular (literales, clases [A-Z], escapes, operadores).
  2. Insertar el operador de concatenación explícito ('.').
  3. Convertir de infix a postfix con el algoritmo Shunting Yard.
  4. Construir un AFN con el algoritmo de Thompson.
  5. Simular el AFN (cerradura-ε + mover) para aceptar o rechazar una cadena.

Operadores soportados: | (unión), * (Kleene), + (una o más), ? (opcional),
paréntesis, clases de caracteres [a-z0-9], y escapes con '\\'.
"""

UNION, CONCAT, STAR, PLUS, OPTIONAL, LPAREN, RPAREN = "|", ".", "*", "+", "?", "(", ")"
PRECEDENCIA = {UNION: 1, CONCAT: 2, STAR: 3, PLUS: 3, OPTIONAL: 3}


class Token:
    """Un token es un operador o un literal (conjunto de caracteres aceptados)."""

    def __init__(self, tipo, valor):
        self.tipo = tipo  # "OP" o "LIT"
        self.valor = valor  # str para operadores, frozenset para literales

    def es_op(self, op=None):
        return self.tipo == "OP" and (op is None or self.valor == op)

    def __repr__(self):
        if self.tipo == "OP":
            return self.valor
        chars = sorted(self.valor)
        return chars[0] if len(chars) == 1 else "[" + "".join(chars[:3]) + "..]"


def _leer_clase(regex, i):
    """Lee una clase de caracteres [..] a partir de regex[i] == '['."""
    chars = set()
    i += 1
    while i < len(regex) and regex[i] != "]":
        c = regex[i]
        if c == "\\":
            i += 1
            c = regex[i]
        if i + 2 < len(regex) and regex[i + 1] == "-" and regex[i + 2] != "]":
            fin = regex[i + 2]
            for code in range(ord(c), ord(fin) + 1):
                chars.add(chr(code))
            i += 3
        else:
            chars.add(c)
            i += 1
    if i >= len(regex):
        raise ValueError("Clase de caracteres sin cerrar en la expresión regular")
    return frozenset(chars), i + 1


def tokenizar(regex):
    tokens = []
    i = 0
    while i < len(regex):
        c = regex[i]
        if c == "\\":
            if i + 1 >= len(regex):
                raise ValueError("Escape incompleto al final de la expresión regular")
            tokens.append(Token("LIT", frozenset(regex[i + 1])))
            i += 2
        elif c == "[":
            chars, i = _leer_clase(regex, i)
            tokens.append(Token("LIT", chars))
        elif c in (UNION, STAR, PLUS, OPTIONAL, LPAREN, RPAREN):
            tokens.append(Token("OP", c))
            i += 1
        else:
            tokens.append(Token("LIT", frozenset(c)))
            i += 1
    return tokens


def insertar_concatenacion(tokens):
    """Agrega el operador '.' donde hay concatenación implícita."""
    resultado = []
    for i, t in enumerate(tokens):
        resultado.append(t)
        if i + 1 == len(tokens):
            break
        sig = tokens[i + 1]
        izq_ok = t.tipo == "LIT" or t.es_op(RPAREN) or t.es_op(STAR) or t.es_op(PLUS) or t.es_op(OPTIONAL)
        der_ok = sig.tipo == "LIT" or sig.es_op(LPAREN)
        if izq_ok and der_ok:
            resultado.append(Token("OP", CONCAT))
    return resultado


def a_postfix(tokens):
    """Algoritmo Shunting Yard."""
    salida, pila = [], []
    for t in tokens:
        if t.tipo == "LIT":
            salida.append(t)
        elif t.es_op(LPAREN):
            pila.append(t)
        elif t.es_op(RPAREN):
            while pila and not pila[-1].es_op(LPAREN):
                salida.append(pila.pop())
            if not pila:
                raise ValueError("Paréntesis desbalanceados en la expresión regular")
            pila.pop()
        else:
            while (pila and not pila[-1].es_op(LPAREN)
                   and PRECEDENCIA[pila[-1].valor] >= PRECEDENCIA[t.valor]):
                salida.append(pila.pop())
            pila.append(t)
    while pila:
        t = pila.pop()
        if t.es_op(LPAREN):
            raise ValueError("Paréntesis desbalanceados en la expresión regular")
        salida.append(t)
    return salida


class Estado:
    _contador = 0

    def __init__(self):
        self.id = Estado._contador
        Estado._contador += 1
        self.transiciones = []  # lista de (frozenset de chars, Estado)
        self.epsilon = []  # lista de Estado


class AFN:
    def __init__(self, inicio, fin):
        self.inicio = inicio
        self.fin = fin


def thompson(postfix):
    """Construye un AFN a partir de la expresión en postfix."""
    pila = []
    for t in postfix:
        if t.tipo == "LIT":
            ini, fin = Estado(), Estado()
            ini.transiciones.append((t.valor, fin))
            pila.append(AFN(ini, fin))
        elif t.valor == CONCAT:
            b, a = pila.pop(), pila.pop()
            a.fin.epsilon.append(b.inicio)
            pila.append(AFN(a.inicio, b.fin))
        elif t.valor == UNION:
            b, a = pila.pop(), pila.pop()
            ini, fin = Estado(), Estado()
            ini.epsilon += [a.inicio, b.inicio]
            a.fin.epsilon.append(fin)
            b.fin.epsilon.append(fin)
            pila.append(AFN(ini, fin))
        elif t.valor in (STAR, PLUS, OPTIONAL):
            a = pila.pop()
            ini, fin = Estado(), Estado()
            ini.epsilon.append(a.inicio)
            a.fin.epsilon.append(fin)
            if t.valor in (STAR, OPTIONAL):
                ini.epsilon.append(fin)
            if t.valor in (STAR, PLUS):
                a.fin.epsilon.append(a.inicio)
            pila.append(AFN(ini, fin))
    if len(pila) != 1:
        raise ValueError("Expresión regular mal formada")
    return pila[0]


def cerradura_epsilon(estados):
    pila = list(estados)
    visitados = set(estados)
    while pila:
        e = pila.pop()
        for sig in e.epsilon:
            if sig not in visitados:
                visitados.add(sig)
                pila.append(sig)
    return visitados


def mover(estados, c):
    return {dest for e in estados for (chars, dest) in e.transiciones if c in chars}


class Regex:
    """Expresión regular compilada a un AFN de Thompson."""

    def __init__(self, patron):
        self.patron = patron
        tokens = insertar_concatenacion(tokenizar(patron))
        self.postfix = a_postfix(tokens)
        self.afn = thompson(self.postfix)

    def acepta(self, cadena):
        actuales = cerradura_epsilon({self.afn.inicio})
        for c in cadena:
            actuales = cerradura_epsilon(mover(actuales, c))
            if not actuales:
                return False
        return self.afn.fin in actuales

    def fallo_en(self, cadena):
        """Devuelve la posición donde la simulación se detuvo (-1 si acepta)."""
        actuales = cerradura_epsilon({self.afn.inicio})
        for i, c in enumerate(cadena):
            actuales = cerradura_epsilon(mover(actuales, c))
            if not actuales:
                return i
        return -1 if self.afn.fin in actuales else len(cadena)
