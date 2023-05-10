# projet-python-2023
l'IA se comporte comme suit :
- Si elle peut accéder à l'item, elle le fait directement et joue un tile "random"

- Si elle peut pas accéder à l'item dans ce tour-ci, elle va faire en sorte d'y arriver apres avoir jouer la tile. 
- Si elle y arrive tant mieux, si non elle va se rapprocher le plus possible de la case de l'item pour pouvoir l'atteindre les prochains tour

Nous ne prenosn pas en compte les autres joueurs car nous n'avons pas implémenté le code de manière à ce que "si mon adversaire est à coté de la tile, je vais le repousser"


#code 

- `index_to_coordinates(index)`: convertit un index de plateau en une paire de coordonnées de ligne et de colonne.
- `coordinates_to_index(x, y)`: convertit une paire de coordonnées de ligne et de colonne en un index de plateau.
- `manhattan_distance(a, b)`: calcule la distance de Manhattan (distance de taxi) entre deux points sur le plateau.
- `get_item_position(item, board)`: renvoie la position de ligne et de colonne d'un élément spécifié sur le plateau.
- `get_player_position(player, board)`: renvoie la position de ligne et de colonne d'un joueur spécifié sur le plateau.
- `AI.__init__(self, board, remaining_tile, player, target)`: initialise l'IA avec le plateau actuel, le nombre de tuiles restantes, l'ID du joueur et l'ID de l'élément cible.
- `generate_tile_insertions(tile)`: génère une liste de toutes les insertions de tuiles possibles sur le plateau pour une tuile donnée.
- `get_neighbors(board, position)`: renvoie une liste de toutes les positions de plateau voisines pour une position donnée.
- `get_closest_position(board, start, goal)`: calcule la position la plus proche d'une position cible donnée à partir d'une position de départ donnée sur le plateau.
- `apply_tile_insertion(board, tile, gate)`: insère une tuile donnée sur le plateau à une position de porte spécifiée.
