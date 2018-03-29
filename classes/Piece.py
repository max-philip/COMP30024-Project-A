class Piece:

    CORNER = "X"
    WHITE = "O"
    BLACK = "@"
    EMPTY = "-"

    type = str
    x = int
    y = int

    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y

    def move(self, new_pos, board):
        start = (self.x, self.y)
        self.x = new_pos[0]
        self.y = new_pos[1]
        if not self.type == self.EMPTY:
            print(str(start) + "->" + str(new_pos))
        board.update("@")

    def valid_x(self, pos, positions):
        x_moves = [(-1, 0), (1, 0)]
        solutions = []

        for move in x_moves:
            new_pos = (pos[0] + move[0], pos[1] + move[1])
            if (new_pos in positions) and (positions[new_pos].type != self.CORNER):
                solutions.append(new_pos)

        return solutions

    def valid_y(self, pos, positions):
        y_moves = [(0, -1), (0, 1)]
        solutions = []

        for move in y_moves:
            new_pos = (pos[0] + move[0], pos[1] + move[1])
            if (new_pos in positions) and (positions[new_pos].type != self.CORNER):
                solutions.append(new_pos)

        return solutions

    def get_kill_type(self, piece_type):
        if piece_type == self.WHITE:
            return self.BLACK
        elif piece_type == self.BLACK:
            return self.WHITE
        else:
            return False

    def check_to_delete(self, positions, sol_space):

        pos = (self.x, self.y)
        piece_type = positions[pos].type
        kill_type = self.get_kill_type(piece_type)

        # print(sol_space)
        # for i in positions:
        #     print(str(i) + str(positions[i].type))

        for axis in sol_space[pos]:
            to_delete = True
            for loc in axis:
                # print(str(loc) + " " + str(positions[loc].type) + " " + str(kill_type))
                if (not positions[loc].type == kill_type):
                    to_delete = False

            if to_delete:
                # print("AXIS: "+str(axis))
                return to_delete
            else:
                continue

        return False

    def check_free(self, new_pos, positions):
        return (new_pos in positions) and (positions[new_pos].type == self.EMPTY)

    def get_moves(self, pos, positions):
        valid_moves = []

        movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for move in movements:
            a = move[0]
            b = move[1]
            new_x = pos[0] + a
            new_y = pos[1] + b

            new_p = (new_x, new_y)

            if self.check_free(new_p, positions):
                valid_moves.append(new_p)
            elif new_p in positions:
                new_p = (new_p[0] + a, new_p[1] + b)
                if self.check_free(new_p, positions):
                    valid_moves.append(new_p)

        return valid_moves

    @staticmethod
    def manhattan_dist(start, end):
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def find_closest_enemies(self, pieces):
        piece_type = self.type
        pos = (self.x, self.y)
        kill_type = self.get_kill_type(piece_type)

        closest = []

        for enemy_pos in pieces[kill_type]:
            dist = self.manhattan_dist(pos, enemy_pos)
            closest.append((dist, enemy_pos))

        closest.sort()

        return [closest[0][1], closest[1][1]]



