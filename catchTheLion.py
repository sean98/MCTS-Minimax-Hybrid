from functools import lru_cache
import numpy as np


class CatchTheLion:
    def __init__(self):
        self.board = np.array([
            ['G', 'L', 'E'],
            [' ', 'C', ' '],
            [' ', 'c', ' '],
            ['e', 'l', 'g'],
        ])
        self.current_player = 1  # 1 for lowercase (bottom), -1 for uppercase (top)
        self.captured_pieces = {1: [], -1: []}  # Stores captured pieces for each player

    def copy(self):
        new_game = CatchTheLion()
        new_game.board = np.copy(self.board)
        new_game.current_player = self.current_player
        new_game.captured_pieces = {1: self.captured_pieces[1][:], -1: self.captured_pieces[-1][:]}
        return new_game

    def clear_cache(self):
        self.moves.cache_clear()
        self.player_name.cache_clear()
        self.opposite_player.cache_clear()
        self.winner.cache_clear()
        self.__str__.cache_clear()
        self.is_current_player_piece.cache_clear()
        self.__is_valid_move.cache_clear()

    def play(self, move):
        if isinstance(move, tuple) and len(move) == 2:  # Regular move
            (src_row, src_col), (dst_row, dst_col) = move
            piece = self.board[src_row, src_col]

            if self.board[dst_row, dst_col] != ' ':
                self.capture_piece(dst_row, dst_col)

            self.board[dst_row, dst_col] = piece
            self.board[src_row, src_col] = ' '

            if piece.lower() == 'c' and dst_row == (3 if self.current_player == 1 else 0):
                self.board[dst_row, dst_col] = 'h' if self.current_player == 1 else 'H'  # Promote Chick to Chicken

        elif isinstance(move, tuple) and len(move) == 3:  # Drop move
            piece, dst_row, dst_col = move
            self.board[dst_row, dst_col] = piece.lower() if self.current_player == 1 else piece.upper()
            self.captured_pieces[self.current_player].remove(piece)

        self.switch_player()
        self.clear_cache()

    @lru_cache(maxsize=None)
    def moves(self):
        if self.winner() is not None:
            return []

        possible_moves = []
        directions = {
            'c': [(1, 0)],
            'g': [(0, -1), (0, 1), (-1, 0), (1, 0)],
            'e': [(-1, -1), (-1, 1), (1, -1), (1, 1)],
            'h': [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (1, -1)],
            'l': [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)],
        }
        for src_row in range(4):
            for src_col in range(3):
                if self.is_current_player_piece(src_row, src_col):
                    piece = self.board[src_row, src_col]
                    for dr, dc in directions[piece.lower()]:
                        dr *= -self.current_player  # if upper player than go down
                        dst_row, dst_col = src_row + dr, src_col + dc
                        if self.__is_valid_move(dst_row, dst_col):
                            possible_moves.append(((src_row, src_col), (dst_row, dst_col)))

        # Add drop moves
        for piece in self.captured_pieces[self.current_player]:
            for src_row in range(4):
                for src_col in range(3):
                    if self.board[src_row, src_col] == ' ':
                        possible_moves.append((piece, src_row, src_col))

        return possible_moves

    @lru_cache(maxsize=None)
    def player_name(self):
        if self.current_player == 1:
            return 'X'
        return 'O'

    @lru_cache(maxsize=None)
    def opposite_player(self):
        if self.current_player == -1:
            return 'X'
        return 'O'

    @lru_cache(maxsize=None)
    def winner(self):
        if 'L' not in self.board:
            return 'X'
        if 'l' not in self.board:
            return 'O'

    @lru_cache(maxsize=None)
    def __str__(self):
        return "\n".join(" | ".join(row) for row in self.board) + '\n'

    def switch_player(self):
        self.current_player = -self.current_player

    @lru_cache(maxsize=None)
    def is_current_player_piece(self, row, col):
        piece = self.board[row, col]
        return (piece.islower() and self.current_player == 1) or (piece.isupper() and self.current_player == -1)

    @lru_cache(maxsize=None)
    def __is_valid_move(self, dst_row, dst_col):
        if not (0 <= dst_row < 4 and 0 <= dst_col < 3):
            return False
        return not self.is_current_player_piece(dst_row, dst_col)

    def capture_piece(self, row, col):
        piece = self.board[row, col].lower()
        self.captured_pieces[self.current_player].append(piece)
        self.board[row, col] = ' '