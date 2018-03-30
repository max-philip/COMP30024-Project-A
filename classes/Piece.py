class Piece:

    # Piece types
    CORNER = "X"
    WHITE = "O"
    BLACK = "@"
    EMPTY = "-"

    X_AXIS = "x"
    Y_AXIS = "y"

    # Possible initial directions from a position
    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Object type, x and y co-ordinates
    type = str
    x = int
    y = int

    # Piece initialiser
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y

    # Make a move for a piece to a new position, printing each movement made
    # by a white piece
    def move(self, new_pos, board):
        start = (self.x, self.y)
        self.x = new_pos[0]
        self.y = new_pos[1]

        # For non-empty pieces, movements are displayed
        if not self.type == Piece.EMPTY:
            print(str(start) + "->" + str(new_pos))

        # Update black pieces after every move
        board.update(Piece.BLACK)

    # Returns True if a piece at a specified location is surrounded by a
    # specified playing piece on either the x or y axis.
    def surrounded(self, pos, positions, kill_type):
        right = (pos[0]+1, pos[1])
        left = (pos[0]-1, pos[0])
        up = (pos[0], pos[1]-1)
        down = (pos[0], pos[1]+1)

        # Checks whether an enemy is in each of the four immediate directions
        right_surr = self.check_kill_space(right, positions, kill_type)
        left_surr = self.check_kill_space(left, positions, kill_type)
        up_surr = self.check_kill_space(up, positions, kill_type)
        down_surr = self.check_kill_space(down, positions, kill_type)

        if (right_surr and left_surr) or (up_surr and down_surr):
            return True

    # Returns True if a space is a "kill space" - a space that has enemies
    # arraged such that the playing piece is eliminated if it moves into it
    def check_kill_space(self, new_pos, positions, kill_type):
        is_kill = False

        if new_pos not in positions:
            is_kill = True

        # Is a "kill space" if surrounded by enemy pieces or an enemy piece
        # and a corner
        elif (positions[new_pos].type == kill_type) \
                or (positions[new_pos] == Piece.CORNER):
            is_kill = True

        return is_kill

    # Returns a list of valid moves along either the x or y axis of a piece.
    def valid_xy(self, pos, positions, axis):

        # Set move modifiers based on axis
        if axis == self.X_AXIS:
            moves = [(-1, 0), (1, 0)]

        if axis == self.Y_AXIS:
            moves = [(0, -1), (0, 1)]

        # Set possible moves
        move1 = (pos[0] + moves[0][0], pos[1] + moves[0][1])
        move2 = (pos[0] + moves[1][0], pos[1] + moves[1][1])

        # Check validity by whether the positions are on the board and if a
        # corner piece is involved
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

    # Helper function that gets the enemy piece type for an input piece type
    def get_kill_type(self):
        if self.type == Piece.WHITE:
            return Piece.BLACK
        elif self.type == Piece.BLACK:
            return Piece.WHITE
        else:
            return False

    # Returns True if a solution (or pair of solutions) for a location has
    # the required pieces for deletion of a playing piece
    def check_to_delete(self, positions, sol_space, kill_type):

        pos = (self.x, self.y)

        # Must check if either axis in the solution space is entirely filled
        for axis in sol_space[pos]:
            to_delete = True

            for loc in axis:
                if not positions[loc].type == kill_type:
                    to_delete = False

                if not loc and self.next_to_corner(positions):
                    to_delete = False

            if to_delete:
                return to_delete
            else:
                continue

        return False

    # Returns true if a position is next to a corner piece
    def next_to_corner(self, positions):
        pos = (self.x, self.y)

        # Check if a corner piece is in any direction
        for move in self.DIRECTIONS:
            new_pos = pos[0] + move[0], pos[1] + move[1]
            if new_pos in positions:
                if positions[new_pos].type == Piece.CORNER:
                    return True

    # Returns True if a position is currently empty (occupied by "-")
    def check_free(self, new_pos, positions):
        return (new_pos in positions) and \
               (positions[new_pos].type == Piece.EMPTY)

    # Gets a list of possible moves that a piece at a specified position can
    # make. Returns both a valid list of moves and a list of "bad" moves
    # that shouldn't be made (will result in the piece getting eliminated)
    def get_moves(self, pos, positions):
        valid_moves = []

        bad_moves = []

        # Checks moves that can be made in all four directions
        for move in self.DIRECTIONS:
            a = move[0]
            b = move[1]
            new_x = pos[0] + a
            new_y = pos[1] + b

            new_pos = (new_x, new_y)

            # Checks if the immediate position is free
            if self.check_free(new_pos, positions):
                if not self.surrounded(new_pos, positions, Piece.BLACK):
                    valid_moves.append(new_pos)
                else:
                    bad_moves.append(new_pos)

            # Then checks if it can make a jump move if the immediate space is
            # currently occupied
            elif new_pos in positions:
                new_pos = (new_pos[0] + a, new_pos[1] + b)
                if self.check_free(new_pos, positions):
                    valid_moves.append(new_pos)

        return valid_moves, bad_moves

    # Calculate the manhattan distance between two points on the board
    @staticmethod
    def manhattan_dist(start, end):
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    # Finds the closest enemy pieces to a piece, returning up to two closest
    # pieces. Returns one enemy piece if only one solution must be filled
    def find_closest_enemies(self, pieces):
        pos = (self.x, self.y)
        kill_type = self.get_kill_type()

        closest = []

        # Goes through the current enemy pieces on the board and appends the
        # closest pieces
        for enemy_pos in pieces[kill_type]:
            dist = self.manhattan_dist(pos, enemy_pos)
            closest.append((dist, enemy_pos))

        closest.sort()

        if len(closest) == 1:
            return [closest[0][1]]
        else:
            return [closest[0][1], closest[1][1]]
