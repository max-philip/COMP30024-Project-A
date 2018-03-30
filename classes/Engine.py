from classes.Board import Board
from classes.Piece import Piece


class Engine:

    # Game types
    MASSACRE_TYPE = "Massacre"
    MOVES_TYPE = "Moves"

    # Board object
    game_board = Board

    # Engine initialiser
    def __init__(self):
        self.game_board = Board()

    # Begins the game, and determines the game type
    def start(self):
        if self.game_board.type == self.MASSACRE_TYPE:
            # Run a massacre of the black pieces
            self.massacre(Piece.BLACK)

        if self.game_board.type == self.MOVES_TYPE:
            # Count and print all possible moves
            self.count_moves(self.game_board.positions)

    # Counts and prints the number of possible moves that the white and black
    # pieces can make. Whites are displayed first, then blacks are displayed
    def count_moves(self, positions):
        white_count = 0
        black_count = 0

        # Iterate over all positions on the board, and counts all the possible
        # moves that can be made
        for xy in positions.keys():
            moves = positions[xy].get_moves(xy, positions)
            if positions[xy].type == Piece.WHITE:
                white_count += len(moves[0]) + len(moves[1])
            if positions[xy].type == Piece.BLACK:
                black_count += len(moves[0]) + len(moves[1])

        # Print the possible move counts
        print(white_count)
        print(black_count)

    # Eliminates all the pieces of type "kill_type". Prints all of the moves
    # made.
    def massacre(self, kill_type):

        # Continues while there are still "kill_type" pieces on the board
        while self.game_board.pieces[kill_type]:

            # Make a solution space, select the current piece, and the
            # surrounding pieces on the x and y axes
            self.game_board.make_solution_space(kill_type)
            curr_p = self.game_board.pieces[kill_type][-1]
            enemies = self.game_board.positions[curr_p].find_closest_enemies\
                (self.game_board.pieces)
            surround_x = self.game_board.positions[curr_p].valid_xy\
                (curr_p, self.game_board.positions, Piece.X_AXIS)
            surround_y = self.game_board.positions[curr_p].valid_xy\
                (curr_p, self.game_board.positions, Piece.Y_AXIS)

            # Calculates which of the possible solutions to the current
            # "kill_type" piece are the easiest to reach, then moves the
            # playing pieces there.
            solution_index = 0
            if self.check_surrounding_same_type(curr_p, surround_x,
                                                surround_y)[0]:

                solution_index = self.check_surrounding_same_type\
                (curr_p, surround_x, surround_y)[1]

                if solution_index == 0:
                    x_manhat = 0
                    for enemy in enemies:
                        for sol in self.game_board.black_sol_space[curr_p][0]:
                            x_manhat += Piece.manhattan_dist(enemy, sol)

                    y_manhat = 0
                    for enemy in enemies:
                        for sol in self.game_board.black_sol_space[curr_p][-1]:
                            y_manhat += Piece.manhattan_dist(enemy, sol)

                    # Pick based on total manhattan distance values
                    if y_manhat > x_manhat:
                        solution_index = 0
                    else:
                        solution_index = -1

            else:
                self.game_board.pieces[Piece.BLACK].append\
                    (self.game_board.pieces[Piece.BLACK].pop())

            self.game_board.move_in_order(enemies,
                    self.game_board.black_sol_space[curr_p][solution_index])

            self.game_board.update(Piece.BLACK)

    # Checks if a piece's surrounding spaces are occupied by a piece of the
    # same type. This allows for faster selection of which solution to go
    # for, since, for example, two adjacent black pieces on the x axis can
    # be immediately ruled out for a solution space on the x axis.
    def check_surrounding_same_type(self, curr_p, surround_x, surround_y):
        has_same_neighbour = False

        # Returns True if there is a same neighbour, and the index of the
        # solution space to be used
        for x in surround_x:
            if self.game_board.positions[x].type == \
                    self.game_board.positions[curr_p].type:

                has_same_neighbour = True

        if not has_same_neighbour:
            return True, 0

        has_same_neighbour = False
        for y in surround_y:
            if self.game_board.positions[y].type == \
                    self.game_board.positions[curr_p].type:
                has_same_neighbour = True

        if not has_same_neighbour:
            return True, -1

        return False, None

