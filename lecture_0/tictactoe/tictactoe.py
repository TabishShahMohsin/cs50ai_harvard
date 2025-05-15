"""
Tic Tac Toe Player
"""

import math
import random
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    return X if ((board[0]+board[1]+board[2]).count(X)+(board[0]+board[1]+board[2]).count(O)) % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions_set.add((i, j))
    
    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = deepcopy(board)
    if board[action[0]][action[1]] != EMPTY or action[0] < 0 or action[1] < 0:
        raise ValueError("Invalid Move")
    board_copy[action[0]][action[1]] = player(board)

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        checker = True
        for j in range(2):
            if board[i][j] != board[i][j+1]:
                checker = False
        if checker and board[i][j] in [X, O]:
            return board[i][j]

    for i in range(3):
        checker = True
        for j in range(2):
            if board[j][i] != board[j+1][i]:
                checker = False
        if checker and board[j][i] in [X, O]:
            return board[j][i]

    checker = True
    for i in range(2):
        if board[i][i] != board[i+1][i+1]:
            checker = False
    if checker and board[i][i] in [X, O]:
        return board[i][i]

    checker = True
    for i in range(2):
        if board[i][2-i] != board[i+1][2-i-1]:
            checker = False
    if checker and board[i][2-i] in [X, O]:
        return board[i][2-i]


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # checking if the baord has a winner or has reached tie
    if winner(board) != None or (board[0]+board[1]+board[2]).count(X)+(board[0]+board[1]+board[2]).count(O) == 9:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    actions_sorted = [[], [], []]
    if terminal(board) == True:
        return None

    # Storing the minimax value of all next choices
    for i in actions(board):
        actions_sorted[minimax_recursive(result(board, i))+1].append(i)

    # Choosing the move so to maximize the score for computer
    if player(board) == O:
        if actions_sorted[0] != []:
            return random.choice(actions_sorted[0])
        elif actions_sorted[1] != []:
            return random.choice(actions_sorted[1])
        return random.choice(actions_sorted[2])

    # Choosing to maximize the score for the computer for x
    if actions_sorted[2] != []:
        return random.choice(actions_sorted[2])
    elif actions_sorted[1] != []:
        return random.choice(actions_sorted[1])
    return random.choice(actions_sorted[0])


def minimax_recursive(board):
    """
    Finds the minimax value of the board considering all considerable (alpha - beta prunning) possible moves.
    """

    # Base condition
    if terminal(board):
        return utility(board)

    # Initializing maximum as minimum number possible and vice-versa
    maximum = -1
    minimum = 1

    # Find minimax value for all next moves, so to apply random if needed in the future
    for i in actions(board):
        if player(board) == O:
            minimum = min(minimax_recursive(result(board, i)), minimum)
            if minimum == -1:
                break
        else:
            maximum = max(minimax_recursive(result(board, i)), maximum)
            if maximum == 1:
                break
    if player(board) == X:
        return maximum
    return minimum
