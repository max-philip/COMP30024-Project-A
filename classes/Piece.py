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
        if not self.type == Piece.EMPTY:
            print(str(start) + "->" + str(new_pos))
        board.update(Piece.BLACK)
        # board.print_board()

    def surrounded(self, pos, positions, kill_type):
        right = (pos[0]+1, pos[1])
        left = (pos[0]-1, pos[0])
        up = (pos[0], pos[1]-1)
        down = (pos[0], pos[1]+1)

        right_surr = self.check_kill_space(right, positions, kill_type)
        left_surr = self.check_kill_space(left, positions, kill_type)
        up_surr = self.check_kill_space(up, positions, kill_type)
        down_surr = self.check_kill_space(down, positions, kill_type)

        if (right_surr and left_surr) or (up_surr and down_surr):
            return True

    def check_kill_space(self, new_pos, positions, kill_type):
        is_kill = False

        if not new_pos in positions:
            is_kill = True
        elif (positions[new_pos].type == kill_type) or (positions[new_pos] == Piece.CORNER):
            is_kill = True

        return is_kill

    def valid_x(self, pos, positions):
        x_moves = [(-1, 0), (1, 0)]

        move1 = (pos[0] + x_moves[0][0], pos[1] + x_moves[0][1])
        move2 = (pos[0] + x_moves[1][0], pos[1] + x_moves[1][1])

        if (move1 not in positions) or (move2 not in positions):
            return []

        if positions[move1].type == Piece.CORNER:
            if move2 in positions:
                return [move2]

        if positions[move2].type == Piece.CORNER:
            if move1 in positions:
                return [move1]

        if (move1 in positions) and (move2 in positions):
            return [move1, move2]

    def valid_y(self, pos, positions):
        y_moves = [(0, -1), (0, 1)]

        move1 = (pos[0] + y_moves[0][0], pos[1] + y_moves[0][1])
        move2 = (pos[0] + y_moves[1][0], pos[1] + y_moves[1][1])

        if (move1 not in positions) or (move2 not in positions):
            return []

        if positions[move1].type == Piece.CORNER:
            if move2 in positions:
                return [move2]

        if positions[move2].type == Piece.CORNER:
            if move1 in positions:
                return [move1]

        if move1 in positions and move2 in positions:
            return [move1, move2]

    def get_kill_type(self):
        if self.type == Piece.WHITE:
            return Piece.BLACK
        elif self.type == Piece.BLACK:
            return Piece.WHITE
        else:
            return False

    def check_to_delete(self, positions, sol_space, kill_type):

        pos = (self.x, self.y)

        # print()
        # print(pos)
        # print(sol_space[pos])

        for axis in sol_space[pos]:
            # print("AXIS " + str(axis))
            to_delete = True

            # if axis == [] and self.next_to_corner(positions):
            #     to_delete = False

            for loc in axis:
                # print("LOC: " + str(loc))
                if not positions[loc].type == kill_type:
                    # print(loc)
                    to_delete = False

                if not loc and self.next_to_corner(positions):
                    to_delete = False

            if to_delete:
                return to_delete
            else:
                continue

        return False

    def next_to_corner(self, positions):
        pos = (self.x, self.y)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for move in directions:
            new_pos = pos[0] + move[0], pos[1] + move[1]
            if new_pos in positions:
                if positions[new_pos].type == Piece.CORNER:
                    return True

    def check_free(self, new_pos, positions):
        return (new_pos in positions) and (positions[new_pos].type == Piece.EMPTY)

    def get_moves(self, pos, positions):
        valid_moves = []

        bad_moves = []

        movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for move in movements:
            a = move[0]
            b = move[1]
            new_x = pos[0] + a
            new_y = pos[1] + b

            new_pos = (new_x, new_y)

            if self.check_free(new_pos, positions):
                if not self.surrounded(new_pos, positions, Piece.BLACK):
                    valid_moves.append(new_pos)
                else:
                    bad_moves.append(new_pos)
                    break
            elif new_pos in positions:
                new_pos = (new_pos[0] + a, new_pos[1] + b)
                if self.check_free(new_pos, positions):
                    valid_moves.append(new_pos)

        return valid_moves, bad_moves

    @staticmethod
    def manhattan_dist(start, end):
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def find_closest_enemies(self, pieces):
        pos = (self.x, self.y)
        kill_type = self.get_kill_type()

        closest = []

        for enemy_pos in pieces[kill_type]:
            dist = self.manhattan_dist(pos, enemy_pos)
            closest.append((dist, enemy_pos))

        closest.sort()

        if len(closest) == 1:
            return [closest[0][1]]
        else:
            return [closest[0][1], closest[1][1]]



