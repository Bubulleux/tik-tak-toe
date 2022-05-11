from range_xd import RangeXD
import hashlib
import random

SYMBOLS = {
    0: "-",
    1: "X",
    -1: "O"
}
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
    return
    for i in range(10):
        random_board = get_random_board(random.randint(0, 9))
        found = get_board_hash(random_board) in boards.keys()
        if not found:
            print_board(random_board)



def get_random_board(plays_count):
    output = {(x, y): 0 for x, y in RangeXD(3, 3)}
    empty_cell = [(x, y) for x,y in RangeXD(3, 3)]
    for i in range(plays_count):
        cell = random.choice(empty_cell)
        empty_cell.remove(cell)
        output[cell] = (-1) ** i
    return output

def calculate_all_next_move(board, depth=0):
    board_hash, rotate = get_board_hash(board)
    global board_calculate, pass_board

    if depth >= 3:
        return

    if board_hash in boards.keys():
        pass_board += 1
        #print_board(board)
        #print()
        #print_board(boards[board_hash])
        return
    boards[board_hash] = board
    board_calculate += 1

    print_board(board)
    print(depth, board_hash, rotate)


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



def get_board_hash(board):
    cell_order = [
        (0, 0),
        (1, 0),
        (2, 0),
        (2, 1),
        (2, 2),
        (1, 2),
        (0, 2),
        (0, 1),
    ]
    board_string = "".join([SYMBOLS[board[cell]] for cell in cell_order])
    strings = [offset_string(board_string, i) + SYMBOLS[board[(1, 1)]] for i in range(0, 8, 2)]
    hashes = [int(hashlib.sha256(_string.encode()).hexdigest(), 16) for _string in strings]
    min_hash = min(hashes)
    min_index = hashes.index(min_hash)
    # print(board_string)
    # print(strings)
    # print(hashes)
    return min_hash, min_index


def offset_string(input_string, offset):
    length = len(input_string)
    output = ""
    for i in range(length):
        output += input_string[(i - offset) % length]
    return output

def get_string_ascii(board):
    line = "+-+-+-+"
    output = line
    for row in range(3):
        output += f"\n|{SYMBOLS[board[0, row]]}|{SYMBOLS[board[1, row]]}|{SYMBOLS[board[2, row]]}|\n{line}"
    return output

def print_board(board):
    print(get_string_ascii(board))

def get_board(string_board):
    output = {}
    if len(string_board) != 9:
        raise TypeError()
    for x, y in RangeXD(3, 3):
        value = 0
        for key, value in SYMBOLS.items():
            if value == string_board[x + y * 3]:
                value = key
                break
        output[x, y] =  value
    return output

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