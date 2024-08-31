from mcts import *


class Player:

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def model(self, game):
        if self.name == 'random':
            return random.choice(game.moves())
        elif self.name == 'mcts':
            return mcts(game, *self.args, **self.kwargs)
        elif self.name == 'mcts-mr':
            return mcts_mr(game, *self.args, **self.kwargs)
        elif self.name == 'mcts-ms':
            return mcts_ms(game, *self.args, **self.kwargs)
        elif self.name == 'mcts-mb':
            return mcts_mb(game, *self.args, **self.kwargs)
        else:
            raise Exception(f"No implementation for player {self.name}")


def simulate_game(game, player1, player2):
    while len(game.moves()) > 0:
        move = player1.model(game)
        game.play(move)
        if len(game.moves()) > 0:
            move = player2.model(game)
            game.play(move)

    winner = game.winner()
    if winner == 'X':
        return player1.name
    if winner == 'O':
        return player2.name
    return 'Draw'


def simulate_series(game_creator, number_of_games, model1, model2):
    winners = dict()
    players = [model1, model2]
    for _ in range(number_of_games):
        random.shuffle(players)
        first_player = players[0]
        second_player = players[1]

        winner = simulate_game(game_creator(), first_player, second_player)
        winners[winner] = winners.get(winner, 0) + 1

    return winners
