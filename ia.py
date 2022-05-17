import random

import helper
from range_xd import RangeXD
import math

WIN_LINES = [
    # Horizontal line
    (0, 0, 1, 0),
    (0, 1, 1, 0),
    (0, 2, 1, 0),
    # Vertical line
    (0, 0, 0, 1),
    (1, 0, 0, 1),
    (2, 0, 0, 1),
    # Slanting line
    (0, 0, 1, 1),
    (0, 2, 1, -1),
]


def get_move_win_rate(board, depth=0, tree=None):
    empty_cell, player_turn = get_next_move(board)
    if len(empty_cell) == 0:
        return {}

    move_score = {}

    for play in empty_cell:
        new_board = board.copy()
        new_board[play] = player_turn
        new_board_score = get_board_score(new_board)
        if new_board_score == 0:
            next_move_scores = get_move_win_rate(new_board, depth=depth + 1)
            if len(next_move_scores) != 0:

                new_board_score = min([score * player_turn for score in next_move_scores.values()]) \
                    * (1 if depth % 2 == 0 else 0.9)
            else:
                new_board_score = 0

        move_score[play] = new_board_score
    return move_score


def get_next_move(board):
    player_turn = 1
    empty_cell = []
    for pos in RangeXD(3, 3):
        if board[pos] == 0:
            empty_cell.append(pos)
        else:
            player_turn *= -1

    return empty_cell, player_turn


def get_board_score(board):
    scores = []
    for start_x, start_y, vel_x, vel_y in WIN_LINES:
        line_content = []
        for i in range(3):
            line_content.append(board[start_x + vel_x * i, start_y + vel_y * i])
        scores.append(get_line_score(line_content))
    return min(max(sum(scores), -1), 1)


def get_line_score(line):
    assert len(line) == 3

    if line in [[-1, -1, -1], [1, 1, 1]]:
        return line[0]
    return 0


def test():
    test_board_1 = helper.get_board("X-X"
                                    "OO-"
                                    "---")
    test_board_2 = helper.get_board("XXX"
                                    "OO-"
                                    "---")
    test_board_3 = helper.get_board("X-X"
                                    "OOO"
                                    "-X-")
    test_board_4 = helper.get_board("X-O"
                                    "-O-"
                                    "--X")
    # assert get_board_score(test_board_2) == 1
    # assert get_board_score(test_board_3) == -1
    # assert get_move_win_rate(test_board_1) == [(1, 0, +1), (2, 1, +0), (0, 2, -1), (1, 2, -1), (1, 2, -1)]

    helper.print_board(test_board_4, get_move_win_rate(test_board_4))


def get_player_play(board):
    helper.print_board(board)
    print("----------------")
    output = None
    while output is None:
        entry = input("Where did you want play? ")
        try:
            entry = int(entry)
        except TypeError:
            print("Unvalide answere")
            continue

        if entry >= 10 or entry < 1:
            print("Unvalide aswere")
            continue

        pos = ((entry - 1) % 3, 2 - (entry - 1) // 3)
        if board[pos] != 0:
            print("Unvalide aswere")
            continue
        output = pos
    return output


def play_game():
    board = {pos: 0 for pos in RangeXD(3, 3)}
    i = 0
    turn = 1
    ia_turn = -1
    while get_board_score(board) == 0 and i != 9:
        if turn == ia_turn:
            ia_plays = get_move_win_rate(board)
            best_score = max([score * turn for score in ia_plays.values()]) * turn
            moves = [move for move, score in ia_plays.items() if best_score == score]
            print(ia_plays)
            print(moves)
            board[random.choice(moves)] = turn
        else:
            board[get_player_play(board)] = turn
        turn *= -1
        i += 1

    helper.print_board(board)


if __name__ == "__main__":
    test()
    exit()
    while True:
        play_game()
        print("\n\n\n\n" + "-" * 100)
