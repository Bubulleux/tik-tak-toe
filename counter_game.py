from helper import get_random_board, get_board_hash, offset_string, print_board, get_board
from range_xd import RangeXD
import random

boards = {}
board_calculate = 0
pass_board = 0
def count_board():
    start_board = {(x, y): 0 for x, y in RangeXD(3, 3)}
    print(get_board_hash(start_board))
    calculate_all_next_move(start_board)
    print(len(boards))
    print(board_calculate)
    print(pass_board)
    print(pass_board + board_calculate)

    # for hash, board in boards.items():
    #     print_board(board)
    #     print(hash,"\n\n")

    print("----------------\n\n")
    for i in range(20):
        random_board = get_random_board(random.randint(3, 9))
        hash = get_board_hash(random_board)
        found = hash[0] in boards.keys()
        if not found:
            print_board(random_board)
            print(hash, "\n")


def calculate_all_next_move(board, depth=0):
    board_hash, rotate = get_board_hash(board)
    global board_calculate, pass_board

    if depth >= 4:
        pass

    if board_hash in boards.keys():
        pass_board += 1
        return
    boards[board_hash] = board
    board_calculate += 1

    empty_cell = []
    a_plays_count = 0
    b_plays_count = 0
    for pos in RangeXD(3, 3):
        if board[pos] == 0:
            empty_cell.append(pos)
        elif board[pos] == 1:
            a_plays_count += 1
        else:
            b_plays_count += 1

    players_turn = -1 if a_plays_count > b_plays_count else 1

    for cell in empty_cell:
        new_board = board.copy()
        new_board[cell] = players_turn
        calculate_all_next_move(new_board, depth=depth + 1)


def test():
    # Test offset_string()
    input_string = "123456"
    assert offset_string(input_string, 3) == "456123"
    assert offset_string(input_string, 1) == "612345"
    assert offset_string(input_string, -1) == "234561"
    assert offset_string(input_string, 6) == "123456"
    assert offset_string(input_string, 7) == offset_string(input_string, 1)

    board_a = get_board("-X-------")
    board_b = get_board("-----X---")
    hash_a, rotate_a = get_board_hash(board_a)
    hash_b, rotate_b = get_board_hash(board_b)
    assert hash_b == hash_a