from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Variable:
    """
    - fila, col: posición en el tablero (0-8)
    - valor: valor asignado (1-9) o None si no está asignada
    - fija: True si la celda venía rellena en el tablero inicial
    - dominio: lista de valores posibles para esta variable
    """
    fila: int
    col: int
    valor: Optional[int] = None
    fija: bool = False
    dominio: List[int] = field(default_factory=lambda: list(range(1, 10)))

    def __hash__(self):
        return hash((self.fila, self.col))

    def __repr__(self):
        if self.fija:
            return f"Var({self.fila},{self.col})[Fija={self.valor}]"
        return f"Var({self.fila},{self.col})[val={self.valor}, dom={self.dominio}]"
