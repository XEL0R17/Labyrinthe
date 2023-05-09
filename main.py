import heapq
from copy import deepcopy


SIZE = 7
MY_USERNAME = 'A_star'

GATES = {
    # Décale la colonne de haut à bas
    "A": 1,
    "B": 3,
    "C": 5,
    # Décale la ligne de droite à gauche
    "D": 13,
    "E": 27,
    "F": 41,
    # Décale la colonne de bas à haut
    "G": 47,
    "H": 45,
    "I": 43,
    # Décale la ligne de gauche à droite
    "J": 35,
    "K": 21,
    "L": 7,
}


DIRECTIONS = [
    (-1, 0),  # N
    (0, 1),   # E
    (1, 0),   # S
    (0, -1),  # W= 1
]
