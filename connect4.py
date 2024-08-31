from scipy.signal import convolve2d
from functools import lru_cache
import numpy as np


class Connect4:
    COLS = 7
    ROWS = 6

    def __init__(self, player=1, board=None):
        self.player = player
        if board is None:
            self.board = np.zeros((Connect4.COLS, Connect4.ROWS), dtype=int).copy()
        else:
            self.board = board

    def copy(self):
        return Connect4(self.player, self.board.copy())

    def clear_cache(self):
        self.moves.cache_clear()
        self.player_name.cache_clear()
        self.opposite_player.cache_clear()
        self.winner.cache_clear()
        self.__str__.cache_clear()

    def play(self, col):
        row = np.where(self.board[col] == 0)[0][-1]
        self.board[col][row] = self.player
        self.player = -self.player
        self.clear_cache()

    @lru_cache(maxsize=None)
    def moves(self):
        if self.winner():
            return np.asarray([])
        return np.where((self.board == 0).max(axis=1))[0]

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
        result = convolve2d(self.board, np.ones((1, 4))/4, mode='valid')
        if np.any(result == 1): return 'X'
        elif np.any(result == -1): return 'O'
        result = convolve2d(self.board, np.ones((4, 1))/4, mode='valid')
        if np.any(result == 1): return 'X'
        elif np.any(result == -1): return 'O'
        result = convolve2d(self.board, np.eye(4)/4, mode='valid')
        if np.any(result == 1): return 'X'
        elif np.any(result == -1): return 'O'
        result = convolve2d(self.board, np.fliplr(np.eye(4))/4, mode='valid')
        if np.any(result == 1): return 'X'
        elif np.any(result == -1): return 'O'

    @lru_cache(maxsize=None)
    def __str__(self):
        result = ''
        for i, col in enumerate(self.board.T):
            result += f'{Connect4.ROWS-i} | {" | ".join(col.astype(str)).replace("0", " ").replace("-1", "O").replace("1", "X")}\n'
        result += f'  | {" | ".join((np.arange(Connect4.COLS)+1).astype(str))}\n'
        return result