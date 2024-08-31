from concurrent.futures import ProcessPoolExecutor
from utils import simulate_series, Player
from catchTheLion import CatchTheLion
from othello import Othello
import multiprocessing


def experiment(game, n_games, player1, player2, file_name):
    print(f'Starting {file_name}\n')
    results = simulate_series(game, n_games, player1, player2)
    with open(f'{file_name}', 'w') as f:
        f.write(f'{results}')
    print(f'Finished {file_name} with result: {results}\n')


if __name__ == '__main__':
    n_games = 100
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        # Play Othello mcts-mr on depth
        for depth in range(1, 5):
            executor.submit(
                experiment, Othello, n_games,
                Player('mcts', duration=1, c=0.7),
                Player('mcts-mr', duration=1, c=0.7, depth=depth),
                f'Othello - mcts vs mcts-mr-{depth}'
            )

        # Play Othello mcts-mb on depth
        for depth in range(1, 7):
            executor.submit(
                experiment, Othello, n_games,
                Player('mcts', duration=1, c=0.7),
                Player('mcts-mb', duration=1, c=0.7, depth=depth),
                f'Othello - mcts vs mcts-mb-{depth}'
            )

        # Play Othello mcts-ms (2 and 4) on visits
        for visits in [0, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]:
            executor.submit(
                experiment, Othello, n_games,
                Player('mcts', duration=1, c=0.7),
                Player('mcts-ms', duration=1, c=0.7, depth=2, visits=visits),
                f'Othello - mcts vs mcts-ms-2-visits-{visits}'
            )
            executor.submit(
                experiment, Othello, n_games,
                Player('mcts', duration=1, c=0.7),
                Player('mcts-ms', duration=1, c=0.7, depth=4, visits=visits),
                f'Othello - mcts vs mcts-ms-4-visits-{visits}'
            )

        # play Othello best models on duration
        for duration in [0.25, 0.5, 1, 2.5, 5]:
            executor.submit(
                experiment, Othello, n_games,
                Player('mcts', duration=duration, c=0.7),
                Player('mcts-mr', duration=duration, c=0.7, depth=1),
                f'Othello - mcts vs mcts-mr-1 with duration {duration}'
            )
            executor.submit(
                experiment, Othello, n_games,
                Player('mcts', duration=duration, c=0.7),
                Player('mcts-ms', duration=duration, c=0.7, depth=2, visits=50),
                f'Othello - mcts vs mcts-ms-2-visits-50 with duration {duration}'
            )
            executor.submit(
                experiment, Othello, n_games,
                Player('mcts', duration=duration, c=0.7),
                Player('mcts-mb', duration=duration, c=0.7, depth=2),
                f'Othello - mcts vs mcts-mb-2 with duration {duration}'
            )

        # Play Catch The Lion mcts-mr on depth
        for depth in range(1, 5):
            executor.submit(
                experiment, CatchTheLion, n_games,
                Player('mcts', duration=1, c=0.7),
                Player('mcts-mr', duration=1, c=0.7, depth=depth),
                f'CatchTheLion - mcts vs mcts-mr-{depth}'
            )

        # Play Catch The Lion mcts-mb on depth
        for depth in range(1, 7):
            executor.submit(
                experiment, CatchTheLion, n_games,
                Player('mcts', duration=1, c=0.7),
                Player('mcts-mb', duration=1, c=0.7, depth=depth),
                f'CatchTheLion - mcts vs mcts-mb-{depth}'
            )
            # Play mcts-ms (2 and 4) on visits

        # Play Catch The Lion  mcts-ms (2, 4 and 6) on visits
        for visits in [0, 1, 2, 5, 10, 20, 50, 100]:
            executor.submit(
                experiment, CatchTheLion, n_games,
                Player('mcts', duration=1, c=0.7),
                Player('mcts-ms', duration=1, c=0.7, depth=2, visits=visits),
                f'CatchTheLion - mcts vs mcts-ms-2-visits-{visits}'
              )
            executor.submit(
                experiment, CatchTheLion, n_games,
                Player('mcts', duration=1, c=0.7),
                Player('mcts-ms', duration=1, c=0.7, depth=4, visits=visits),
                f'CatchTheLion - mcts vs mcts-ms-4-visits-{visits}'
              )
            executor.submit(
                experiment, CatchTheLion, n_games,
                Player('mcts', duration=1, c=0.7),
                Player('mcts-ms', duration=1, c=0.7, depth=6, visits=visits),
                f'CatchTheLion - mcts vs mcts-ms-6-visits-{visits}'
            )

        # play CatchTheLion best models on duration
        for duration in [0.25, 0.5, 1, 2.5, 5]:
            executor.submit(
                experiment, CatchTheLion, n_games,
                Player('mcts', duration=duration, c=0.7),
                Player('mcts-mr', duration=duration, c=0.7, depth=1),
                f'CatchTheLion - mcts vs mcts-mr-1 with duration {duration}'
            )
            executor.submit(
                experiment, CatchTheLion, n_games,
                Player('mcts', duration=duration, c=0.7),
                Player('mcts-ms', duration=duration, c=0.7, depth=4, visits=2),
                f'CatchTheLion - mcts vs mcts-ms-4-visits-2 with duration {duration}'
            )
            executor.submit(
                experiment, CatchTheLion, n_games,
                Player('mcts', duration=duration, c=0.7),
                Player('mcts-mb', duration=duration, c=0.7, depth=4),
                f'CatchTheLion - mcts vs mcts-mb-4 with duration {duration}'
            )
