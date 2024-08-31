from statistics import mean, stdev
from minimax import minimax
import math
import random
import time



class Node:

    def __init__(self, game, move=None, parent=None):
        # self.value = 0
        self.value = []
        self.visits = 0
        self.game = game
        self.move = move
        self.parent = parent
        self.children = []
        self.is_terminal = False
        self.terminal_value = 0
        self.minimax_tested = False

    def weight(self, c):
        if self.visits == 0:
            return math.inf

        if self.is_terminal:
            return self.terminal_value

        ucb = math.log(self.parent.visits / self.visits)
        avg = mean(self.value)
        std = stdev(self.value, avg) if len(self.value) > 1 else 0
        return avg + c * math.sqrt(ucb * min(1/4, std + 2*ucb))

    def best_move(self, c):
        return max(self.children, key=lambda child: child.weight(c)).move

    def non_terminal_children(self):
        return [child for child in self.children if not child.is_terminal]

    def select(self, c):
        return max(self.non_terminal_children(), key=lambda child: child.weight(c))

    def expand(self):
        for move in self.game.moves():
            child_game = self.game.copy()
            child_game.play(move)
            self.children.append(Node(child_game, move, self))

        if len(self.children) == 0:
            return self

        return random.choice(self.children)

    def declare_terminal(self, winner):
        self.is_terminal = True
        if winner != self.game.player_name():
            self.terminal_value = math.inf
        elif winner is not None:
            self.terminal_value = -math.inf

    def simulate(self):
        if winner := self.game.winner():
            self.declare_terminal(winner)

        simulation_game = self.game.copy()
        while len(moves := simulation_game.moves()) > 0:
            simulation_game.play(random.choice(moves))
        return simulation_game.winner()

    def minimax(self, depth):
        if not self.minimax_tested:
            self.minimax_tested = True
            minimax_result = minimax(self.game, depth)
            if minimax_result != 0:
                winner = self.game.player_name() if minimax_result == math.inf else self.game.opposite_player()
                # winner = self.game.opposite_player() if minimax_result == math.inf else self.game.player_name()
                self.declare_terminal(winner)
                return winner

    def backpropagation(self, winner):
        self.visits += 1
        if winner != self.game.player_name():
            if len(self.children) > 0 and all(c.terminal_value == -math.inf for c in self.children):
                self.terminal_value = math.inf
                self.is_terminal = True
            else:
                self.value.append(1)
        elif winner is not None:
            if any(c.terminal_value == math.inf for c in self.children):
                self.terminal_value = -math.inf
                self.is_terminal = True
            else:
                self.value.append(-1)
        else:
            self.value.append(0)

        if self.parent is not None:
            self.parent.backpropagation(winner)

    def backpropagation_with_minimax(self, winner, depth, is_previous_terminal=None):
        self.visits += 1
        if winner != self.game.player_name():
            if any(c.terminal_value == -math.inf for c in self.children):
                if all(c.terminal_value == -math.inf for c in self.children):
                    self.terminal_value = math.inf
                    self.is_terminal = True
                elif is_previous_terminal:
                    if self.minimax(depth) is None:
                        self.value.append(1)
                    else:
                        self.value.append(1)
                else:
                    self.value.append(1)
            else:
                self.value.append(1)
        elif winner is not None:
            if any(c.terminal_value == math.inf for c in self.children):
                self.terminal_value = -math.inf
                self.is_terminal = True
            else:
                self.value.append(-1)
        else:
            self.value.append(0)

        if self.parent is not None:
            self.parent.backpropagation_with_minimax(winner, depth, self.is_terminal)


def mcts(game, duration=1, c=1.3, *args, **kwargs):
    start = time.time()
    root = Node(game)

    while time.time()-start < duration:
        node = root
        while len(node.non_terminal_children()) > 0:
            node = node.select(c)

        node = node.expand()
        node.backpropagation(node.simulate())

    return root.best_move(c)


def mcts_mr(game, depth=2, duration=1, c=1.3, *args, **kwargs):
    start = time.time()
    root = Node(game)

    while time.time()-start < duration:
        node = root
        while len(node.non_terminal_children()) > 0:
            node = node.select(c)

        node = node.expand()
        winner = node.minimax(depth)
        if winner is not None:
            node.backpropagation(winner)
        else:
            node.backpropagation(node.simulate())

    return root.best_move(c)


def mcts_ms(game, depth=2, visits=100, duration=1, c=1.3, *args, **kwargs):
    start = time.time()
    root = Node(game)

    while time.time()-start < duration:
        node = root
        while len(node.non_terminal_children()) > 0:
            node = node.select(c)
            if node.visits == visits:
                break

        if node.visits == visits:
            winner = node.minimax(depth)
            if winner is not None:
                node.backpropagation(winner)
                continue

        node = node.expand()
        node.backpropagation(node.simulate())

    return root.best_move(c)


def mcts_mb(game, depth=2, duration=1, c=1.3, *args, **kwargs):
    start = time.time()
    root = Node(game)

    while time.time()-start < duration:
        node = root
        while len(node.non_terminal_children()) > 0:
            node = node.select(c)

        node = node.expand()
        node.backpropagation_with_minimax(node.simulate(), depth)

    return root.best_move(c)
