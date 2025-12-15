# board.py

WIN_LINES = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6)
]

class Board:
    def __init__(self, cells=None):
        self.cells = cells if cells else ['-'] * 9

    def copy(self):
        return Board(self.cells.copy())

    def legal_moves(self):
        return [i for i in range(9) if self.cells[i] == '-']

    def make_move(self, idx, player):
        self.cells[idx] = player

    def is_terminal(self):
        return self.winner() is not None or '-' not in self.cells

    def winner(self):
        for a,b,c in WIN_LINES:
            if self.cells[a] == self.cells[b] == self.cells[c] != '-':
                return self.cells[a]
        if '-' not in self.cells:
            return 'D'
        return None
