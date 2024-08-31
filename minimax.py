import math

INF = math.inf


def minimax(game, depth):
    def evaluate_board(inner_game):
        winner = inner_game.winner()
        if winner == game.player_name():
            return INF
        elif winner == game.opposite_player():
            return -INF
        return 0

    def minimax_alpha_beta(game, depth, alpha=-math.inf, beta=math.inf, maximizing_player=True):

        if depth == 0 or game.winner():
            return evaluate_board(game)

        if maximizing_player:
            max_eval = -INF
            for move in game.moves():
                game_copy = game.copy()
                game_copy.play(move)
                eval = minimax_alpha_beta(game_copy, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval
        else:
            min_eval = INF
            for move in game.moves():
                game_copy = game.copy()
                game_copy.play(move)
                eval = minimax_alpha_beta(game_copy, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval

    return minimax_alpha_beta(game, depth)