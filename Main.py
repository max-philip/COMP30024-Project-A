from classes.Board import Board
from classes.Piece import Piece


def check_surrounding_same_type(pos):
    has_same_neighbour = False
    for x in surrounding_x:
        if my_board.positions[x].type == my_board.positions[curr_black].type:
            has_same_neighbour = True

    if not has_same_neighbour:
        return True, 0

    has_same_neighbour = False
    for y in surrounding_y:
        if my_board.positions[y].type == my_board.positions[curr_black].type:
            has_same_neighbour = True

    if not has_same_neighbour:
        return True, -1

    return False


game_over = False

my_board = Board()

my_board.print_board()

while my_board.pieces["@"]:
    my_board.make_solution_space("@")
    curr_black = my_board.pieces["@"][0]
    enemies = my_board.positions[curr_black].find_closest_enemies(my_board.pieces)
    surrounding_x = my_board.positions[curr_black].valid_x(curr_black, my_board.positions)
    surrounding_y = my_board.positions[curr_black].valid_y(curr_black, my_board.positions)

    if check_surrounding_same_type(curr_black)[0]:
        solution_index = check_surrounding_same_type(curr_black)[1]
    else:
        my_board.pieces["@"].append(my_board.pieces["@"].pop(0))

    my_board.get_move_order(enemies, my_board.black_solution_space[curr_black][solution_index])
    # my_board.print_board()
    my_board.update("@")
    my_board.print_board()
