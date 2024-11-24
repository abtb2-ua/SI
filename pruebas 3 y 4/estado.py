# Lista Frontera estará siempre ordenada por coste, de forma que siempre se escoja la primera posición
# (que es la de menor coste)

# CLASE ESTADO
# Antecesor
# Coste = coste(antecesor) + movimiento
# g(n)
# h(n) [de momento 0 -> búsqueda en anchura, mira todo el mapa]
# Casilla

# Heurística: hay que explicar las alternativas en la memoria y compararlas
# ¿Sirve la distancia de Manhattan? No
# ¿Sirve la distancia de bloques? No
# ¿Sirve la distancia euclídea? Sí, es admisible (multiplicando por 1.5 el resultado de la euclídea si tienes tiempo)
# ¿Sirve la distancia de chevichev? Sí, es admisible (max{|dx|,|dy|} + 0.5xmin{|dx|,|dy|})

class Estado:
    def __init__(self, casilla, antecesor=None, g=0, h=0):
        self.casilla = casilla        # Casilla actual del estado
        self.antecesor = antecesor    # Nodo antecesor (de dónde proviene)
        self.g = g                    # Coste desde el inicio hasta este nodo
        self.h = h                    # Heurística (estimación de coste al objetivo)
        self.f = g + h                # f(n) = g(n) + h(n)

    def __eq__(self, other):
        return self.casilla == other.casilla

    def __lt__(self, other):
        return self.f < other.f
