# alphabeta.py
import math

def alphabeta(board, depth, alpha, beta, maximizing, player, eval_fn):
    opponent = 'O' if player == 'X' else 'X'
    winner = board.winner()

    # Check terminal states first (they override depth)
    if winner == player:
        return 1000 + depth  # Prefer faster wins
    if winner == opponent:
        return -1000 - depth  # Prefer slower losses
    if winner == 'D':
        return 0
    
    # If depth limit reached, use evaluation function
    if depth == 0:
        return eval_fn(board, player)

    if maximizing:
        value = -math.inf
        for move in board.legal_moves():
            b = board.copy()
            b.make_move(move, player)
            value = max(value, alphabeta(b, depth-1, alpha, beta, False, player, eval_fn))
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value
    else:
        value = math.inf
        for move in board.legal_moves():
            b = board.copy()
            b.make_move(move, opponent)
            value = min(value, alphabeta(b, depth-1, alpha, beta, True, player, eval_fn))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value
