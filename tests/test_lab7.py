import os
import unittest

from src.epsilon import eliminar_epsilon, encontrar_anulables
from src.grammar import ErrorGramatica, cargar_gramatica, validar_linea
from src.regex_engine import Regex

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ruta(nombre):
    return os.path.join(RAIZ, "gramaticas", nombre)


def como_texto(g):
    return {c: sorted("".join(x) for x in p) for c, p in g.producciones.items()}


class TestRegex(unittest.TestCase):
    def test_operadores(self):
        r = Regex("(a|b)*abb")
        self.assertTrue(r.acepta("abb"))
        self.assertTrue(r.acepta("babaabb"))
        self.assertFalse(r.acepta("ab"))
        self.assertTrue(Regex("a+b?").acepta("aaa"))
        self.assertFalse(Regex("a+b?").acepta("b"))


class TestValidacion(unittest.TestCase):
    def test_lineas_validas(self):
        for linea in ["S -> 0A0 | 1B1 | BB", "S→aAa|ε", "A -> C", "C -> S | ε"]:
            self.assertTrue(validar_linea(linea)[0], linea)

    def test_lineas_invalidas(self):
        for linea in ["s -> a", "S a", "S -> a |", "S -> | a", "SA -> a", "S -> a$b", "S ->"]:
            self.assertFalse(validar_linea(linea)[0], linea)

    def test_archivo_con_error(self):
        with self.assertRaises(ErrorGramatica):
            cargar_gramatica(ruta("gramatica_error.txt"), verbose=False)


class TestEpsilon(unittest.TestCase):
    def test_gramatica1(self):
        g = cargar_gramatica(ruta("gramatica1.txt"), verbose=False)
        self.assertEqual(encontrar_anulables(g, verbose=False), {"S", "A", "B", "C"})
        nueva, _ = eliminar_epsilon(g, verbose=False)
        self.assertEqual(como_texto(nueva), {
            "S": sorted(["0A0", "00", "1B1", "11", "BB", "B"]),
            "A": ["C"],
            "B": ["A", "S"],
            "C": ["S"],
        })

    def test_gramatica2(self):
        g = cargar_gramatica(ruta("gramatica2.txt"), verbose=False)
        self.assertEqual(encontrar_anulables(g, verbose=False), {"S", "A", "B", "C", "D"})
        nueva, _ = eliminar_epsilon(g, verbose=False)
        self.assertEqual(como_texto(nueva), {
            "S": sorted(["aAa", "aa", "bBb", "bb"]),
            "A": ["C", "a"],
            "B": ["C", "b"],
            "C": sorted(["CDE", "CE", "DE", "E"]),
            "D": sorted(["A", "B", "ab"]),
        })

    def test_sin_producciones_epsilon(self):
        for nombre in ["gramatica1.txt", "gramatica2.txt"]:
            g = cargar_gramatica(ruta(nombre), verbose=False)
            nueva, _ = eliminar_epsilon(g, verbose=False)
            for cuerpos in nueva.producciones.values():
                self.assertNotIn(tuple(), cuerpos)


if __name__ == "__main__":
    unittest.main()
