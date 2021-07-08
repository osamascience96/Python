from os import system
from os import name as sys_name
from sys import argv
from time import sleep
from random import choice

try:
    from termcolor import colored
except ImportError:
    def colored(x):
        return x


class Move(object):
    def __init__(self, score, index):
        self.score = score
        self.index = index


def init_mode():
    return 2

def get_input(prompt=' Input integer: ', max_limit=0, exception_cmd='pass'):
    """Getting input from user. Function checks it to be integer in
    specified range"""
    while True:
        try:
            value = int(input(prompt))
            if 0 < value <= max_limit:
                return value
            else:
                raise ValueError
        except ValueError:
            exec(exception_cmd)


def draw_board(board):
    print('\n ╔═══╦═══╦═══╗\n\
 ║ {0} ║ {1} ║ {2} ║\n\
 ╠═══╬═══╬═══╣\n\
 ║ {3} ║ {4} ║ {5} ║\n\
 ╠═══╬═══╬═══╣\n\
 ║ {6} ║ {7} ║ {8} ║\n\
 ╚═══╩═══╩═══╝ '.format(*board))


def player_move(board):
    while True:
        player_move = get_input(' Input your move: ', 9,
                                'print(" Invalid move")') - 1
        if is_free(player_move, board):
            return player_move
        else:
            print(" Space is not free")


def is_free(move, board):
    return board[move] == '-'


def change_sign(sign):
    return 'X' if sign == 'O' else 'O'


def change_player(player):
    if mode == 1:
        return 'PLAYER X' if player == 'PLAYER O' else 'PLAYER O'
    elif mode == 2:
        return 'PLAYER X' if player == 'AI O' else 'AI O'
    else:
        return 'AI X' if player == 'AI O' else ' AI O'


def empty_indices(board):
    return [i for i in range(len(board)) if board[i] == '-']


def win_check(sign, board):
    """This function checks for a winner. Returns information needed to
    'win_light' function (next one)."""

    # Horizontal win check
    for i in range(0, 7, 3):
        if sign \
                == board[i] \
                == board[i + 1] \
                == board[i + 2]:
            return 'h', i

    # Vertical win check
    for i in range(3):
        if sign \
                == board[i] \
                == board[i + 3] \
                == board[i + 6]:
            return 'v', i

    # / diagonal win check
    if sign \
            == board[0] \
            == board[4] \
            == board[8]:
        return 'dl', None

    # \ diagonal win check
    elif sign \
            == board[2] \
            == board[4] \
            == board[6]:
        return 'dr', None

    return False


def win_light(key, i, sign):
    """Substitutes win combination with red symbols"""
    global light_board
    light_board = real_board.copy()
    color = colored(sign, 'red')
    if key == 'h':
        light_board[i] = color
        light_board[i + 1] = color
        light_board[i + 2] = color
    elif key == 'v':
        light_board[i] = color
        light_board[i + 3] = color
        light_board[i + 6] = color
    elif key == 'dl':
        light_board[0] = color
        light_board[4] = color
        light_board[8] = color
    elif key == 'dr':
        light_board[2] = color
        light_board[4] = color
        light_board[6] = color


def draw_win_board(player):
    try:
        brd = light_board
        print(player, 'WINS!')
        draw_board(brd)
        brd = real_board if brd == light_board else light_board
    except KeyboardInterrupt:
        pass


def minimax(sign, board, is_max_sign=True, depth=0):
    """Return a best move for a sign in a board."""
    depth += 1
    new_board = board.copy()
    empty_spots = empty_indices(new_board)
    if is_max_sign:
        max_sign = sign
        min_sign = change_sign(sign)
    else:
        max_sign = change_sign(sign)
        min_sign = sign

    # Check for base case
    if win_check(max_sign, new_board):
        score = Move(100 - depth, None)
        return score
    elif win_check(min_sign, new_board):
        score = Move(depth - 100, None)
        return score
    elif len(empty_spots) == 0:
        score = Move(0, None)
        return score

    moves = []
    for i in empty_spots:
        move = Move(None, i)
        new_board[i] = sign
        if is_max_sign:
            result = minimax(min_sign, new_board, False, depth)
        else:
            result = minimax(max_sign, new_board, True, depth)
        move.score = result.score
        new_board[i] = '-'  # Revert changes made to board
        moves.append(move)

    if is_max_sign:
        best_score = -1000
        for i in range(len(moves)):
            if moves[i].score > best_score:
                best_move = i
                best_score = moves[i].score
    else:
        best_score = 1000
        for i in range(len(moves)):
            if moves[i].score < best_score:
                best_move = i
                best_score = moves[i].score

    return moves[best_move]  # Return index of best move for passed board


if __name__ == "__main__":
    # let the init board be an empty array
    init_board = []
    file_name = argv[1]
    file = open(file_name, 'r')
    Line = file.readlines()

    # append the array in the init_board
    for line in Line:
        array = (line.strip()).split(" ")
        for char in array:
            init_board.append(char)

    file.close()

    # Start of the Program

    State_1 = ["-", "X", "-", "O", "O", "-", "-", "X", "-"]
    State_2 = ["-", "X", "-", "O", "O", "X", "-", "X", "-"]

    # Clear screen procedure depends on OS type
    if sys_name == 'posix': 
        def clear():
            system('clear')
    elif sys_name == 'nt':
        def clear():
            system('cls')

    # START MESSAGE
    clear()
    print(' Welcome to the TicTacToe!\nShowing current state as per given input example:')
    draw_board(init_board)
    print('Press any key to proceed...')
    input()

    # START
    clear()
    mode = init_mode()
    State_3 = ["-", "X", "O", "O", "O", "X", "-", "X", "-"]
    State_4 = ["-", "X", "O", "O", "O", "X", "X", "X", "-"]
    State_5 = ["-", "X", "O", "O", "O", "X", "X", "X", "O"]
    State_6 = ["-", "X", "O", "O", "O", "X", "X", "X", "O"]
    Final_State = ["X", "X", "O", "O", "O", "X", "X", "X", "O"]
        

    # get the infromation at each state only for x
    def GetStateInformation(move, board, win_status, sign):
        if sign == 'X':
            available_slots = empty_indices(board)
            if (win_status != False or len(available_slots) <= 3):
                print("The State of Terminals for X are: " + str(len(available_slots)))
                if (win_status != False and mode != 1):
                    print("X have wins at " + str(move) + " index")
                    print("X loss at one state only")
                    print("X draw at one state only")
            else:
                howmany = int(len(available_slots) / 2)
                print("Non-Terminals for X are: " + str(len(available_slots)))
                if(mode != 1):
                    print("X have a guarnteed win at index " + str(move))
                    print("X have a guarnteed loss in " + str(howmany) + " states")
                    print("X have a guarnteed draw in " + str(howmany) + " states")

    while True:
        game_finished = False
        clear()
        real_board = init_board
        clear()
        if mode == 1:
            print("Human X vs Human O")
            current_sign = 'O'
            while True:
                current_player = 'Player X' if current_sign == 'X' else 'Player O'
                print(current_player)
                draw_board(real_board)
                move = player_move(real_board)
                GetStateInformation(move, real_board, False, current_sign)
                real_board[move] = current_sign
                win = win_check(current_sign, real_board)
                if win:
                    win_light(*win, current_sign)
                    draw_win_board(current_player)
                    game_finished = True
                    break
                elif '-' in real_board:
                    draw_board(real_board)
                    current_sign = change_sign(current_sign)
                else:
                    draw_board(real_board)
                    game_finished = True
                    print("Draw")
                    break
        if mode == 2:
            print("Human X vs AI O")
            current_player = 'AI O'
            current_sign = 'O' if current_player == 'AI O' else 'X'
            while True:
                first_move = True if current_sign == 'O' else False
                print(current_player)
                draw_board(real_board)
                if current_sign == 'X':
                    move = player_move(real_board)
                    real_board[move] = current_sign
                    win = win_check(current_sign, real_board)
                elif first_move:
                    first_move = False
                    move = minimax(current_sign, real_board, True).index
                    real_board[move] = current_sign
                    win = win_check(current_sign, real_board)
                else:
                    pass

                if win:
                    win_light(*win, current_sign)
                    draw_win_board(current_player)
                    game_finished = True
                    GetStateInformation(minimax('X', real_board, True).index, real_board, win, current_sign)
                    break
                elif '-' in real_board:
                    draw_board(real_board)
                    GetStateInformation(minimax('X', real_board, True).index, real_board, win, current_sign)
                    current_sign = change_sign(current_sign)
                    current_player = change_player(current_player)
                else:
                    draw_board(real_board)
                    game_finished = True
                    GetStateInformation(minimax('X', real_board, True).index, real_board, win, current_sign)
                    print("Draw")
                    break

        if mode == 3:
            print("AI X vs AI O")
            current_player = 'AI O'
            current_sign = 'O' if current_player == 'AI O' else 'X'
            while True:
                first_move = True if current_sign == 'O' else False
                print(current_player)
                if current_sign == 'X':
                    move = minimax(current_sign, real_board, True).index
                    real_board[move] = current_sign
                    win = win_check(current_sign, real_board)
                elif first_move:
                    first_move = False
                    move = minimax(current_sign, real_board, True).index
                    real_board[move] = current_sign
                    win = win_check(current_sign, real_board)
                else:
                    pass

                if win:
                    win_light(*win, current_sign)
                    draw_win_board(current_player)
                    game_finished = True
                    GetStateInformation(move, real_board, win, current_sign)
                    print("")
                    break
                elif '-' in real_board:
                    draw_board(real_board)
                    GetStateInformation(move, real_board, win, current_sign)
                    print("")
                    current_sign = change_sign(current_sign)
                    current_player = change_player(current_player)
                else:
                    draw_board(real_board)
                    game_finished = True
                    GetStateInformation(move, real_board, win, current_sign)
                    print("")
                    print("Draw")
                    break

        if game_finished:
            break

