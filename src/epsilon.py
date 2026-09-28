"""
Eliminación de producciones-ε.

Algoritmo:
  1. Encontrar los símbolos anulables (A es anulable si A ⇒* ε):
       - Base: si A → ε, A es anulable.
       - Inducción: si A → X1 X2 ... Xk y todos los Xi son anulables, A es anulable.
  2. Para cada producción A → X1 ... Xk con m símbolos anulables, generar los 2^m
     casos posibles (cada anulable presente o ausente). Se descartan los cuerpos
     vacíos (producciones-ε) y las producciones triviales A → A.
"""

from itertools import product

from .grammar import Gramatica


def encontrar_anulables(g, verbose=True):
    anulables = {cabeza for cabeza, cuerpos in g.producciones.items() if tuple() in cuerpos}
    if verbose:
        print("Paso 1: símbolos anulables")
        print(f"  Base (X → ε): {{{', '.join(sorted(anulables))}}}")

    iteracion = 1
    cambio = True
    while cambio:
        cambio = False
        nuevos = set()
        for cabeza, cuerpos in g.producciones.items():
            if cabeza in anulables or cabeza in nuevos:
                continue
            for cuerpo in cuerpos:
                if cuerpo and all(s in anulables for s in cuerpo):
                    nuevos.add(cabeza)
                    if verbose:
                        print(f"  Iteración {iteracion}: {cabeza} es anulable por "
                              f"{cabeza} → {Gramatica.cuerpo_a_str(cuerpo)}")
                    break
        if nuevos:
            anulables |= nuevos
            cambio = True
            iteracion += 1

    if verbose:
        print(f"  Conjunto de anulables: {{{', '.join(sorted(anulables))}}}\n")
    return anulables


def producciones_anulables(g, anulables, verbose=True):
    """Producciones cuyo cuerpo contiene al menos un símbolo anulable (o es ε)."""
    resultado = [(cabeza, cuerpo) for cabeza, cuerpos in g.producciones.items()
                 for cuerpo in cuerpos if not cuerpo or any(s in anulables for s in cuerpo)]
    if verbose:
        print("Producciones anulables (contienen ε o algún símbolo anulable):")
        for cabeza, cuerpo in resultado:
            print(f"  {cabeza} → {Gramatica.cuerpo_a_str(cuerpo)}")
        print()
    return resultado


def expandir(cuerpo, anulables):
    """Genera los 2^m cuerpos posibles quitando/manteniendo cada símbolo anulable."""
    posiciones = [i for i, s in enumerate(cuerpo) if s in anulables]
    casos = []
    for mascara in product([True, False], repeat=len(posiciones)):
        quitar = {p for p, mantener in zip(posiciones, mascara) if not mantener}
        casos.append(tuple(s for i, s in enumerate(cuerpo) if i not in quitar))
    return posiciones, casos


def eliminar_epsilon(g, verbose=True):
    anulables = encontrar_anulables(g, verbose)
    producciones_anulables(g, anulables, verbose)

    if verbose:
        print("Paso 2: nuevas producciones (2^m casos por producción)")

    nueva = Gramatica(g.inicial)
    for cabeza, cuerpos in g.producciones.items():
        for cuerpo in cuerpos:
            if not cuerpo:
                if verbose:
                    print(f"  {cabeza} → ε: se elimina\n")
                continue
            posiciones, casos = expandir(cuerpo, anulables)
            m = len(posiciones)
            if verbose:
                simbolos = ", ".join(cuerpo[p] for p in posiciones) or "ninguno"
                print(f"  {cabeza} → {Gramatica.cuerpo_a_str(cuerpo)}   "
                      f"(m = {m}: {simbolos}; 2^{m} = {2 ** m} casos)")
            for caso in casos:
                texto = Gramatica.cuerpo_a_str(caso)
                if not caso:
                    motivo = "descartada (ε)"
                elif caso == (cabeza,):
                    motivo = "descartada (trivial)"
                else:
                    ya_estaba = caso in nueva.producciones.get(cabeza, [])
                    nueva.agregar(cabeza, caso)
                    motivo = "repetida" if ya_estaba else "agregada"
                if verbose and m > 0:
                    print(f"      {cabeza} → {texto:12} {motivo}")
                elif verbose:
                    print(f"      sin símbolos anulables: se conserva")
            if verbose:
                print()

    # Conservar el orden de los no-terminales y omitir los que quedan sin producciones.
    for cabeza in g.producciones:
        nueva.producciones.setdefault(cabeza, [])
    nueva.producciones = {c: p for c, p in nueva.producciones.items() if p}

    if verbose and g.inicial in anulables:
        print(f"Nota: {g.inicial} es anulable, por lo que ε ∈ L(G). La gramática resultante "
              f"genera L(G) − {{ε}}.\n")
    return nueva, anulables
