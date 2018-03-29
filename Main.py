from classes.Board import Board
from classes.Piece import Piece

game_over = False

my_board = Board()

my_board.print_board()

while my_board.pieces["@"]:
    my_board.make_solution_space("@")
    curr_black = my_board.pieces["@"][0]
    enemies = my_board.positions[curr_black].find_closest_enemies(my_board.pieces)
    my_board.get_move_order(enemies, my_board.black_solution_space[curr_black][0])
    my_board.print_board()
    my_board.update("@")
    my_board.print_board()



# my_board.make_solution_space("@")
#
# my_board.move_piece((6,4), (7,4))
#
# my_board.print_board()
#
# my_board.move_piece((7,4), (7,5))
#
# my_board.update("@")
#
# my_board.print_board()
#
# enemies = my_board.positions[(4,3)].find_closest_enemies(my_board.pieces)
#
#
# my_board.get_move_order(enemies, my_board.black_solution_space[(4,3)][0])
#
# my_board.print_board()