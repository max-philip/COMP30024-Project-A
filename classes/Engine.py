from classes.Board import Board


class Engine:

    CORNER = "X"
    WHITE = "O"
    BLACK = "@"
    EMPTY = "-"

    MASSACRE_TYPE = "Massacre"
    MOVES_TYPE = "Moves"

    game_board = Board

    def __init__(self):
        self.game_board = Board()

    def start(self):

        self.game_board.print_board()
        if self.game_board.type == self.MASSACRE_TYPE:
            self.massacre(self.BLACK)

        if self.game_board.type == self.MOVES_TYPE:
            self.count_moves(self.game_board.positions)

    def count_moves(self, positions):
        white_count = 0
        black_count = 0
        for xy in positions.keys():
            moves = positions[xy].get_moves(xy, positions)
            if positions[xy].type == self.WHITE:
                white_count += len(moves)
            if positions[xy].type == self.BLACK:
                black_count += len(moves)

        print(white_count)
        print(black_count)

    def massacre(self, kill_type):
        while self.game_board.pieces[kill_type]:
            self.game_board.make_solution_space(kill_type)
            curr_p = self.game_board.pieces[kill_type][0]
            enemies = self.game_board.positions[curr_p].find_closest_enemies(self.game_board.pieces)
            surrounding_x = self.game_board.positions[curr_p].valid_x(curr_p, self.game_board.positions)
            surrounding_y = self.game_board.positions[curr_p].valid_y(curr_p, self.game_board.positions)
            solution_index = 0
            if self.check_surrounding_same_type(curr_p, surrounding_x, surrounding_y)[0]:
                solution_index = self.check_surrounding_same_type(curr_p, surrounding_x, surrounding_y)[1]
                if solution_index == 0:
                    x_manhat = 0
                    for enemy in enemies:
                        for sol in self.game_board.black_solution_space[curr_p][0]:
                            x_manhat += Board.manhattan_dist(enemy, sol)

                    y_manhat = 0
                    for enemy in enemies:
                        for sol in self.game_board.black_solution_space[curr_p][-1]:
                            y_manhat += Board.manhattan_dist(enemy, sol)

                    if y_manhat > x_manhat:
                        solution_index = 0
                    else:
                        solution_index = -1
            else:
                self.game_board.pieces[self.BLACK].append(self.game_board.pieces[self.BLACK].pop(0))

            self.game_board.get_move_order(enemies, self.game_board.black_solution_space[curr_p][solution_index])
            self.game_board.update(self.BLACK)

    def check_surrounding_same_type(self, curr_p, surrounding_x, surrounding_y):
        has_same_neighbour = False
        for x in surrounding_x:
            if self.game_board.positions[x].type == self.game_board.positions[curr_p].type:
                has_same_neighbour = True

        if not has_same_neighbour:
            return True, 0

        has_same_neighbour = False
        for y in surrounding_y:
            if self.game_board.positions[y].type == self.game_board.positions[curr_p].type:
                has_same_neighbour = True

        if not has_same_neighbour:
            return True, -1

        return False, None

