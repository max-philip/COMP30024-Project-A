from classes.Piece import Piece


class Board:

    MAX_LEN = 8
    PIECE_TYPES = 4

    positions = {}
    pieces = {}
    type = ""

    CORNER = "X"
    WHITE = "O"
    BLACK = "@"
    EMPTY = "-"

    black_solution_space = {}
    white_solution_space = {}
    #empty_solution_space = {}

    def __init__(self):
        self.positions, self.pieces, self.type = self.populate_dict()
        self.black_solution_space = self.make_solution_space(self.BLACK)
        self.white_solution_space = self.make_solution_space(self.WHITE)
        #self.empty_solution_space = self.make_solution_space(self.EMPTY)

    # Takes in raw input of board and fills positions and pieces dictionaries
    def populate_dict(self):

        # Initialise dicts
        positions = {}
        pieces = {}

        # Positions dictionary stores positions as keys and pieces as values
        for i in range(self.MAX_LEN):
            row = input().split(" ")
            for j in range(self.MAX_LEN):
                curr_piece = Piece(row[j], j, i)
                positions[(j, i)] = curr_piece

                # Pieces dictionary stores positions for each piece type
                if row[j] in pieces:
                    pieces[row[j]].append((j, i))
                else:
                    pieces[row[j]] = [(j, i)]

        # Gets the type of game - in this case either Moves or Massacre
        game_type = input()
        return positions, pieces, game_type

    # Prints out the current board
    def print_board(self):
        for i in range(self.MAX_LEN):
            for j in range(self.MAX_LEN):
                print(self.positions[(j, i)].type + " ", end='')
            print()

    # Moves a piece from a starting position to a final one
    def move_piece(self, start_pos, final_pos):
        piece = self.positions[start_pos]
        end_piece = self.positions[final_pos]
        piece_type = piece.type

        # Only makes the move if the final position is empty. Updates both the
        # positions and pieces dictionaries.
        if self.positions[final_pos].type == self.EMPTY:
            piece.move(final_pos, self)
            end_piece.move(start_pos, self)

            self.positions[final_pos] = piece
            self.positions[start_pos] = end_piece

            self.pieces[piece_type].remove(start_pos)
            self.pieces[piece_type].append(final_pos)

            self.pieces[self.EMPTY].remove(final_pos)
            self.pieces[self.EMPTY].append(start_pos)

    def update(self, move_type):

        if move_type == self.WHITE:
            kill_type = self.BLACK
            sols = self.white_solution_space
        else:
            kill_type = self.WHITE
            sols = self.black_solution_space

        for pos in self.positions.keys():
            piece = self.positions[pos]
            if (pos in self.pieces[move_type]) and (piece.check_to_delete(self.positions, sols, piece.get_kill_type())):
                self.remove_piece(pos)

    def remove_piece(self, pos):
        piece_type = self.positions[pos].type
        self.positions[pos].type = self.EMPTY
        self.pieces[piece_type].remove(pos)
        self.pieces[self.EMPTY].append(pos)
        # print(self.pieces)

    def make_solution_space(self, piece_type):
        sol_space = {}

        for piece in self.pieces.keys():
            if piece == piece_type:
                for pos in self.pieces[piece]:
                    sol_space[pos] = []

        for sol in sol_space:
            sol_space[sol].append(self.positions[sol].valid_x(sol, self.positions))
            sol_space[sol].append(self.positions[sol].valid_y(sol, self.positions))

        return sol_space

    @staticmethod
    def manhattan_dist(start, end):
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def search_board(self, curr_pos, final_pos, visited):

        visited.append(curr_pos)

        if curr_pos == final_pos:
            return visited

        p_queue = []

        frontier = self.positions[curr_pos].get_moves(curr_pos, self.positions)

        for node in frontier:
            if node not in visited:
                p_queue.append((self.manhattan_dist(node, final_pos), node))

        p_queue.sort(reverse=True)

        if p_queue:
            return self.search_board(p_queue.pop()[1], final_pos, visited)
        else:
            return visited

    def get_move_order(self, enemies, final_positions):

        move_order = []
        for i in range(len(final_positions)):
            enemy = enemies[i]
            #move_order.append(self.search_board(enemy, final_positions[i], []))
            move_order = self.search_board(enemy, final_positions[i], [])

            if len(move_order) == 1:
                continue
            else:
                for i in range(len(move_order) - 1):
                    self.move_piece(move_order[i], move_order[i+1])
                    # self.update("@")
                    #print(move_order)
