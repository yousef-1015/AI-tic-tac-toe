# heuristic.py
from board import WIN_LINES

def classical_eval(board, player):
    opponent = 'O' if player == 'X' else 'X'
    score = 0

    for line in WIN_LINES:
        p = sum(1 for i in line if board.cells[i] == player)
        o = sum(1 for i in line if board.cells[i] == opponent)
        
        # Strong emphasis on near-wins
        if p == 2 and o == 0:
            score += 50  # About to win
        elif p == 1 and o == 0:
            score += 1   # Potential line
        
        if o == 2 and p == 0:
            score -= 40  # Must block
        elif o == 1 and p == 0:
            score -= 1   # Opponent's potential

    # Center control bonus
    if board.cells[4] == player:
        score += 3
    elif board.cells[4] == opponent:
        score -= 3
    
    # Corner control bonus
    corners = [0, 2, 6, 8]
    for c in corners:
        if board.cells[c] == player:
            score += 2
        elif board.cells[c] == opponent:
            score -= 2

    return score
