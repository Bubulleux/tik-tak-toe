import random

import helper
from range_xd import RangeXD
import math
import treePlot

# All possible win line (start x, start y, move x, move y)
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

# stock all the already calculated win score of board
board_value_cache = {}


def get_move_win_rate(board, depth=0, tree: treePlot.Tree = None, previous_play=None):
    """
    Give the win rate of all possible move
    :param board:
    :param depth:
    :param tree:
    :param previous_play:
    :return dictionary of the move a the win value:
    """

    empty_cell, player_turn = get_next_move(board)

    if previous_play is None:
        previous_play = ()

    if len(empty_cell) == 0:    # Check is the board in full or not
        return {}

    move_score = {}
    if tree is not None:
        tree.add_node(previous_play, (board, 0))

    for play in empty_cell:
        # Duplicate the board and apply the current play
        new_board = board.copy()
        new_board[play] = player_turn

        # Get the board hash and check if the board has already been calculated
        board_hash = get_board_hash(new_board)
        if board_hash in board_value_cache.keys():
            move_score[play] = board_value_cache[board_hash]
            continue

        new_board_score = get_board_score(new_board)  # Check if the board is a winning board
        if new_board_score == 0:
            # Get the score of the board by resistivity
            next_move_scores = get_move_win_rate(new_board, depth=depth + 1, tree=tree,
                                                 previous_play=previous_play + (play,))
            if len(next_move_scores) != 0:  # Check if is the last play
                # Get the best enemy play
                new_board_score = min([score * player_turn for score in next_move_scores.values()]) \
                                  * player_turn
            else:
                new_board_score = 0

        board_value_cache[get_board_hash(new_board)] = new_board_score  # Put the board score in the cache
        move_score[play] = new_board_score
        if tree is not None:
            tree.add_node(previous_play + (play,), (new_board_score, new_board))
    return move_score


def get_board_hash(board):
    """
    Returns a unique number of the board
    :param board:
    :return a unique number:
    """
    board_string = "".join([str(value + 1) for value in board.values()])
    return int(board_string, 3)


def get_next_move(board):
    """
    Returns all the possible move and who is the players at play
    :param board:
    :return all empty cell and the player turn:
    """
    player_turn = 1
    empty_cell = []
    for pos in RangeXD(3, 3):
        if board[pos] == 0:
            empty_cell.append(pos)
        else:
            player_turn *= -1

    return empty_cell, player_turn


def get_board_score(board):
    """
    Returns whether the board is a winner or not
    :param board:
    :return 1, -1 or 0:
    """
    scores = []
    for start_x, start_y, vel_x, vel_y in WIN_LINES:    # Check each line
        line_content = []
        for i in range(3):  # Put the content of each line in a list
            line_content.append(board[start_x + vel_x * i, start_y + vel_y * i])
        scores.append(get_line_score(line_content))  # Get the win value of that line
    return min(max(sum(scores), -1), 1)  # Calculate if the board is win or not


def get_line_score(line):
    """
    Returns the score of a line
    :param line:
    :return 1, -1 or 0:
    """
    assert len(line) == 3

    if line in [[-1, -1, -1], [1, 1, 1]]:
        return line[0]
    return 0


def print_node(key, node):
    score, board = node
    print(score)
    helper.print_board(board, high_light=key[-1])
    print("-" * 20)


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
    test_board_5 = helper.get_board("---"
                                    "---"
                                    "---")
    # assert get_board_score(test_board_2) == 1
    # assert get_board_score(test_board_3) == -1
    # assert get_move_win_rate(test_board_1) == [(1, 0, +1), (2, 1, +0), (0, 2, -1), (1, 2, -1), (1, 2, -1)]
    current_board = test_board_5
    tree = treePlot.Tree(current_board)
    win_rate = get_move_win_rate(current_board, tree=tree)
    plot = treePlot.TreePlot(tree)
    plot.on_click_node = print_node
    plot.node_size = 50

    plot.show()
    helper.print_board(current_board, win_rate)


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
    ia_turn = 1
    while get_board_score(board) == 0 and i != 9:
        if turn == ia_turn:
            ia_plays = get_move_win_rate(board)
            best_score = max([score * turn for score in ia_plays.values()]) * turn
            moves = [move for move, score in ia_plays.items() if best_score == score]
            print(ia_plays)
            print(moves)
            print(len(board_value_cache))
            board[random.choice(moves)] = turn
        else:
            board[get_player_play(board)] = turn
        turn *= -1
        i += 1

    helper.print_board(board)


if __name__ == "__main__":
    # test()
    # exit()
    while True:
        play_game()
        print("\n\n\n\n" + "-" * 100)
