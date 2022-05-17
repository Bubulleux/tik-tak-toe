from range_xd import RangeXD
import random

SYMBOLS = {
    0: "-",
    1: "X",
    -1: "O"
}

LINES = [
    # Horizontal Lines
    (0, 0, 1, 0),
    (0, 1, 1, 0),
    (0, 2, 1, 0),
    # Vertical Lines
    (0, 0, 0, 1),
    (1, 0, 0, 1),
    (2, 0, 0, 1),
    # Diagonal Lines
    (0, 0, 1, 1),
    (2, 0, -1, 1),
]


def get_best_play(board):
    empty_cells = []
    play_a = 0
    play_b = 0
    for pos in RangeXD(3, 3):
        if board[pos] == 0:
            empty_cells.append(pos)
        elif board[pos] == 1:
            play_a += 1
        else:
            play_b += 1

    player_turn = -1 if play_a > play_b else 1
    play_score = {}
    for cell in empty_cells:
        new_board = board.copy()
        new_board[cell] = player_turn
        lines_score = calc_lines(new_board)
        is_win = player_turn * 3 in lines_score
        is_lose = player_turn * 2 * -1 in lines_score
        if is_win:
            play_score[cell] = 3
            continue

        if is_lose:
            play_score[cell] = -3
            continue
        play_score[cell] = sum(lines_score) * player_turn / len(lines_score)

    print(play_score)
    max_score = max(play_score.values())
    possible_play = []
    for pos, score in play_score.items():
        if score == max_score:
            possible_play.append(pos)
    print(possible_play)
    return random.choice(possible_play)




def board_is_win(board):
    lines_score = calc_lines(board)
    full = 0 not in board.values()
    for scores in lines_score:
        if scores == 3 or scores == -3:
            return scores / 3
    return 0 if full else None

def calc_lines(board):
    lines_score = []
    for x, y, v_x, v_y in LINES:
        line_content = []
        for i in range(3):
            line_content.append(board[(x + v_x * i, y + v_y * i)])
        lines_score.append(get_line_score(line_content))
    return lines_score


def get_line_score(line_content):
    plays_a = 0
    plays_b = 0
    for cell in line_content:
        if cell == 1:
            plays_a += 1
        elif cell == -1:
            plays_b += 1

    if plays_a != 0 and plays_b != 0:
        return 0
    if plays_a == 0 and plays_b == 0:
        return 0

    if plays_a != 0:
        return plays_a
    if plays_b != 0:
        return plays_b * -1


def get_string_ascii(board):
    line = "+-+-+-+"
    output = line
    for row in range(3):
        output += f"\n|{SYMBOLS[board[0, row]]}|{SYMBOLS[board[1, row]]}|{SYMBOLS[board[2, row]]}|\n{line}"
    return output

def print_board(board):
    print(get_string_ascii(board))


def main():
    while True:
        board = {pos: 0 for pos in RangeXD(3, 3)}
        player = 1
        ia_id = -1
        while board_is_win(board) is None:
            if player == ia_id:
                play_pos = get_best_play(board)
                board[play_pos] = player
            else:
                print_board(board)
                entry = int(input("Where did you want play? "))
                board[entry % 3, entry // 3] = player
            player *= -1
        print(board_is_win(board))
        print_board(board)


main()

