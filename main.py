import heapq
from copy import deepcopy
from simulation import server_state


SIZE = 7
MY_USERNAME = 'XS'

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


def index_to_coordinates(index):
    return index // SIZE, index % SIZE


def coordinates_to_index(x, y):
    return x * SIZE + y


def manhattan_distance(a, b):
    ax, ay = a
    bx, by = b
    return abs(ax - bx) + abs(ay - by)


def get_item_position(item, board):
    for i in range(SIZE):
        for j in range(SIZE):
            tile = board[i][j]
            if tile.item == item:
                return i, j


def get_player_position(player, board):
    for i in range(SIZE):
        for j in range(SIZE):
            tile = board[i][j]
            if tile.player == player:
                return i, j


class AI:
    def __init__(self, board, remaining_tile, player, target):
        self.board = board
        self.tile = remaining_tile
        self.player = player
        self.target = target

    def generate_tile_insertions(self, tile):
        tile_orientations = [
            Tile(N=tile.N, E=tile.E, S=tile.S, W=tile.W),
            Tile(N=tile.W, E=tile.N, S=tile.E, W=tile.S),
            Tile(N=tile.S, E=tile.W, S=tile.N, W=tile.E),
            Tile(N=tile.E, E=tile.S, S=tile.W, W=tile.N),
        ]

        return [{"tile": orientation, "gate": gate} for orientation in tile_orientations for gate in GATES.keys()]

    def get_neighbors(self, board, position):
        neighbors = []
        x, y = position

        for dx, dy in DIRECTIONS:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < SIZE and 0 <= new_y < SIZE:
                tile = board[x][y]
                neighbor = board[new_x][new_y]
                if tile.N and neighbor.S and (dx, dy) == (-1, 0):
                    neighbors.append((new_x, new_y))
                elif tile.E and neighbor.W and (dx, dy) == (0, 1):
                    neighbors.append((new_x, new_y))
                elif tile.S and neighbor.N and (dx, dy) == (1, 0):
                    neighbors.append((new_x, new_y))
                elif tile.W and neighbor.E and (dx, dy) == (0, -1):
                    neighbors.append((new_x, new_y))
        return neighbors

    def get_closest_position(self, board, start, goal):
        open_set = [(manhattan_distance(start, goal), 0, start, [])]
        closed_set = set()
        closest_path = None
        closest_distance = float("inf")

        while open_set:
            _, cost, current, path = heapq.heappop(open_set)
            current_distance = manhattan_distance(current, goal)

            if current == goal:
                return current

            if current_distance < closest_distance:
                closest_distance = current_distance
                closest_path = path + [current]

            if current not in closed_set:
                closed_set.add(current)
                neighbors = self.get_neighbors(board, current)
                for neighbor in neighbors:
                    new_cost = cost + 1
                    new_path = path + [current]
                    heapq.heappush(open_set,
                                   (manhattan_distance(neighbor, goal) + new_cost, new_cost, neighbor, new_path))

        closest_position = closest_path.pop()
        closest_position = (closest_position[0], closest_position[1])
        return closest_position

    def apply_tile_insertion(self, board, tile, gate):
        row, col = index_to_coordinates(GATES[gate])

        tile_out = None  # tile qui sort de la grille

        if row == 0:  # insertion sur une case en haut
            tile_out = board[SIZE-1][col]
            for i in range(SIZE - 1, row, -1):
                board[i][col] = board[i - 1][col]

        elif row == SIZE - 1:  # insertion sur une case en bas
            tile_out = board[0][col]
            for i in range(0, row, 1):
                board[i][col] = board[i + 1][col]

        elif col == 0:  # insertion sur une case à gauche
            tile_out = board[row][SIZE-1]
            for j in range(SIZE - 1, col, -1):
                board[row][j] = board[row][j - 1]

        elif col == SIZE - 1:  # insertion sur une case à droite
            tile_out = board[row][0]
            for j in range(0, col, 1):
                board[row][j] = board[row][j + 1]

        tile.player = tile_out.player   # s'il y avait un joueur ou un item sur la case sortante,
        tile.item = tile_out.item       # on la met sur la case entrante, sinon ça sera None
        board[row][col] = tile          # Insère la tile

        return board

    def get_move(self):
        closest_position = None
        best_action = None
        min_distance = float("inf")
        possible_actions = self.generate_tile_insertions(self.tile)
        for action in possible_actions:
            temp_board = deepcopy(self.board)
            tile = action["tile"]
            gate = action["gate"]

            new_board = self.apply_tile_insertion(temp_board, tile, gate)
            start = get_player_position(self.player, new_board)
            goal = get_item_position(self.target, new_board)

            position = self.get_closest_position(new_board, start, goal)
            if position == goal:
                return tile, gate, position

            elif manhattan_distance(position, goal) < min_distance:
                best_action = action
                closest_position = position

        return best_action["tile"], best_action["gate"], closest_position


class Tile:
    def __init__(self, N=True, E=True, S=True, W=True, item=None, player=None):
        self.N = N
        self.E = E
        self.S = S
        self.W = W
        self.item = item
        self.player = player


class State:
    def __init__(self, state):
        self.players = state["players"]
        self.current = state["current"]
        self.positions = state["positions"]
        self.target = state["target"]
        self.remaining = state["remaining"]

        self.tile = Tile(N=state["tile"]["N"], E=state["tile"]["E"], S=state["tile"]["S"], W=state["tile"]["W"],
                         item=state["tile"]["item"])

        self.board = []
        for x in range(SIZE):
            row = []
            for y in range(SIZE):
                i = x * SIZE + y
                tile = state["board"][i]
                tile = Tile(**tile)
                if i in self.positions:
                    position = self.positions.index(i)
                    tile.player = self.players[position]

                row.append(tile)
            self.board.append(row)


def main():
    current_state = server_state  # Hypothèse que server_state vienne du serveur.
    # TODO: Récupérer les states avec une boucle "While not end_game" depuis le serveur serveur au
    #  lieu de "server_state" servant d'exemple

    players = current_state["players"]
    current_player_index = current_state["current"]
    if players[current_player_index] == MY_USERNAME:  # si c'est mon tour
        state = State(current_state)

        player = MY_USERNAME
        ai = AI(state.board, state.tile, player, state.target)
        tile, gate, new_coord = ai.get_move()
        new_position = coordinates_to_index(new_coord[0], new_coord[1])

        move = {
            "tile": {"N": tile.N, "E": tile.E, "S": tile.S, "W": tile.W, "item": None},
            "gate": gate,
            "new_position": new_position
        }
        print(move)
        # TODO: Envoyer le mouvement au serveur au lieu de le print


if __name__ == '__main__':
    main()