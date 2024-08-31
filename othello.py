from functools import lru_cache
import numpy as np


class Othello:
    SIZE = 8
    EMPTY = 0
    BLACK = 1
    WHITE = -1

    def __init__(self, player=BLACK, board=None):
        self.player = player
        if board is None:
            self.board = np.zeros((Othello.SIZE, Othello.SIZE), dtype=np.int8)
            c1 = Othello.SIZE//2
            c2 = (Othello.SIZE-1)//2
            self.board[c1, c1] = self.board[c2, c2] = Othello.BLACK
            self.board[c1, c2] = self.board[c2, c1] = Othello.WHITE
        else:
            self.board = board

    def copy(self):
        return Othello(self.player, self.board.copy())

    def clear_cache(self):
        self.moves.cache_clear()
        self.player_name.cache_clear()
        self.opposite_player.cache_clear()
        self.winner.cache_clear()
        self.is_valid_move.cache_clear()
        self.__str__.cache_clear()

    def play(self, move):
        row, col = move[0], move[1]
        self.board[row, col] = self.player
        opponent = -self.player
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            r, c = row + dr, col + dc
            pieces_to_flip = []
            while 0 <= r < Othello.SIZE and 0 <= c < Othello.SIZE and self.board[r, c] == opponent:
                pieces_to_flip.append((r, c))
                r += dr
                c += dc
            if len(pieces_to_flip) > 0 and 0 <= r < Othello.SIZE and 0 <= c < Othello.SIZE and self.board[r, c] == self.player:
                for rr, cc in pieces_to_flip:
                    self.board[rr, cc] = self.player
        self.player = opponent
        self.clear_cache()

    @lru_cache(maxsize=None)
    def is_valid_move(self, row, col):
        if self.board[row, col] != 0:
            return False
        opponent = -self.player
        valid = False
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            r, c = row + dr, col + dc
            count = 0
            while 0 <= r < Othello.SIZE and 0 <= c < Othello.SIZE and self.board[r, c] == opponent:
                r += dr
                c += dc
                count += 1
            if count > 0 and 0 <= r < Othello.SIZE and 0 <= c < Othello.SIZE and self.board[r, c] == self.player:
                valid = True
                break
        return valid

    @lru_cache(maxsize=None)
    def moves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                if self.is_valid_move(r, c):
                    moves.append((r, c))
        return moves

    @lru_cache(maxsize=None)
    def player_name(self):
        if self.player==1: return 'X'
        else: return 'O'

    @lru_cache(maxsize=None)
    def opposite_player(self):
        if self.player==-1: return 'X'
        else: return 'O'

    @lru_cache(maxsize=None)
    def winner(self):
        if len(self.moves()) == 0:
            black = np.count_nonzero(self.board == 1)
            white = np.count_nonzero(self.board == -1)
            if black > white:
                return 'X'
            elif black < white:
                return 'O'

    @lru_cache(maxsize=None)
    def __str__(self):
        result = ''
        for i, col in enumerate(self.board):
            result += f'{Othello.SIZE-i} | {" | ".join(col.astype(str)).replace("0", " ").replace("-1", "O").replace("1", "X")}\n'
        result += f'  | {" | ".join((np.arange(Othello.SIZE  )+1).astype(str))}\n'
        return result