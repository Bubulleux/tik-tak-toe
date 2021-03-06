import hashlib
import random

from range_xd import RangeXD


SYMBOLS = {
    0: "-",
    1: "X",
    -1: "O"
}


def get_random_board(plays_count):
    output = {(x, y): 0 for x, y in RangeXD(3, 3)}
    empty_cell = [(x, y) for x,y in RangeXD(3, 3)]
    for i in range(plays_count):
        cell = random.choice(empty_cell)
        empty_cell.remove(cell)
        output[cell] = (-1) ** i
    return output


def get_board_hash(board, rotated=False):
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
    if rotated:
        strings = [offset_string(board_string, i) + SYMBOLS[board[(1, 1)]] for i in range(0, 8, 2)]
        hashes = [int(hashlib.sha256(_string.encode()).hexdigest(), 16) for _string in strings]
        min_hash = min(hashes)
        min_index = hashes.index(min_hash)
    else:
        min_hash = int(hashlib.sha256((board_string + SYMBOLS[board[(1, 1)]]).encode()).hexdigest(), 16)
        min_index = 0

    return min_hash, min_index


def offset_string(input_string, offset):
    length = len(input_string)
    output = ""
    for i in range(length):
        output += input_string[(i - offset) % length]
    return output


def get_string_ascii(board, plays=None, high_light=None):
    line = "+-------" * 3 + "+"
    output = line
    cell_content = {}
    # print(board, "\n", plays)
    if plays is None:
        plays = {}

    for pos, value in board.items():
        if pos in plays:
            cell_content[pos] = str(round(plays[pos], 3)).center(7)
        else:
            if high_light == pos:
                cell_content[pos] = f"_{SYMBOLS[value]}_".center(7)
            else:
                cell_content[pos] = SYMBOLS[value].center(7)

    for row in range(3):
        output += f"\n|{cell_content[0, row]}|{cell_content[1, row]}|{cell_content[2, row]}|\n{line}"
    return output


def print_board(board, plays=None, high_light=None):
    print(get_string_ascii(board, plays=plays, high_light=high_light))


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
        output[x, y] = value
    return output
