from classes.Piece import Piece


class Board:

    # Maximum size of the board
    MAX_LEN = 8

    positions = {}
    pieces = {}
    type = str

    black_solution_space = {}
    white_solution_space = {}

    def __init__(self):
        self.positions, self.pieces, self.type = self.populate_dict()
        self.black_solution_space = self.make_solution_space(Piece.BLACK)
        self.white_solution_space = self.make_solution_space(Piece.WHITE)

    # Take in raw input of board and fills positions and pieces dictionaries
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

    # Print out the current board
    def print_board(self):
        for i in range(self.MAX_LEN):
            for j in range(self.MAX_LEN):
                print(self.positions[(j, i)].type + " ", end='')
            print()

    # Move a piece from a starting position to a final one
    def move_piece(self, start_pos, final_pos):
        piece = self.positions[start_pos]
        end_piece = self.positions[final_pos]
        piece_type = piece.type

        # Only makes the move if the final position is empty. Updates both the
        # positions and pieces dictionaries.
        if self.positions[final_pos].type == Piece.EMPTY:
            piece.move(final_pos, self)
            end_piece.move(start_pos, self)

            self.positions[final_pos] = piece
            self.positions[start_pos] = end_piece

            self.pieces[piece_type].remove(start_pos)
            self.pieces[piece_type].append(final_pos)

            self.pieces[Piece.EMPTY].remove(final_pos)
            self.pieces[Piece.EMPTY].append(start_pos)

    # Update the state of all the pieces of a specific type on the board
    def update(self, move_type):

        # Set the solution space according to the type updated
        if move_type == Piece.WHITE:
            sols = self.white_solution_space
        else:
            sols = self.black_solution_space

        # Go through the positions on the board and removes pieces that are in
        # a state where they are eliminated
        for pos in self.positions.keys():
            piece = self.positions[pos]
            if (pos in self.pieces[move_type]) and (piece.check_to_delete(self.positions, sols, piece.get_kill_type())):
                self.remove_piece(pos)

    # Remove a piece at a specified position on the board
    def remove_piece(self, pos):

        # Switch the positions of the piece and the empty space
        piece_type = self.positions[pos].type
        self.positions[pos].type = Piece.EMPTY
        self.pieces[piece_type].remove(pos)
        self.pieces[Piece.EMPTY].append(pos)

    # Create a dictionary of the possible solutions for each piece of a
    # specified type, where the positions of each piece are the keys
    def make_solution_space(self, piece_type):
        sol_space = {}

        # Initialise the solution space keys
        for piece in self.pieces.keys():
            if piece == piece_type:
                for pos in self.pieces[piece]:
                    sol_space[pos] = []

        #
        for sol in sol_space:
            if self.positions[sol].valid_x(sol, self.positions):
                sol_space[sol].append(self.positions[sol].valid_x(sol, self.positions))
            if self.positions[sol].valid_y(sol, self.positions):
                sol_space[sol].append(self.positions[sol].valid_y(sol, self.positions))

        return sol_space

    def search_board(self, curr_pos, final_pos, visited):

        visited.append(curr_pos)

        if curr_pos == final_pos:
            return visited

        p_queue = []

        frontier = self.positions[curr_pos].get_moves(curr_pos, self.positions)[0]

        for node in frontier:
            if node not in visited:
                p_queue.append((Piece.manhattan_dist(node, final_pos), node))

        p_queue.sort(reverse=True)

        if p_queue:
            return self.search_board(p_queue.pop()[1], final_pos, visited)
        else:
            return visited

    def get_move_order(self, enemies, final_positions):

        for i in range(len(final_positions)):
            enemy = enemies[i]
            move_order = self.search_board(enemy, final_positions[i], [])

            if len(move_order) == 1:
                continue
            else:
                for j in range(len(move_order) - 1):
                    self.move_piece(move_order[j], move_order[j+1])
