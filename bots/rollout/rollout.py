#!/usr/bin/env python
"""


"""

from api import State, util
import random


class Bot:

    __max_depth = -1
    __randomize = True

    def __init__(self, randomize=True, depth=2, roll_depth = 20, num_samples = 3):
        self.__randomize = randomize
        self.__max_depth = depth
        self.__num_samples = num_samples
        self.__depth = roll_depth

    def get_move(self, state, info = None):
        val, move = self.value(state, info=info)

        return move # to do nothing, return None

    def value(self, state, alpha=float('-inf'), beta=float('inf'), depth = 0, info=None):
        """
        Return the value of this state and the associated move
        :param State state:
        :param float alpha: The highest score that the maximizing player can guarantee given current knowledge
        :param float beta: The lowest score that the minimizing player can guarantee given current knowledge
        :param int depth: How deep we are in the tree
        :return val, move: the value of the state, and the best move.
        """
        if info is not None: # debug information
            if 'nodes_visited' not in info:
                info['nodes_visited'] = 0
            info['nodes_visited'] += 1

        if state.finished():
            return (1.0, None) if state.winner() == 1 else (-1.0, None)

        if depth == self.__max_depth:
            return self.evaluate(state), None

        best_value = float('-inf') if maximizing(state) else float('inf')
        best_move = None

        moves = state.moves()

        if self.__randomize:
            random.shuffle(moves)

        for move in moves:

            next_state = state.next(move)
            value, _ = self.value(next_state, alpha, beta, depth = depth + 1, info=info)

            if maximizing(state):
                if value > best_value:
                    best_value = value
                    best_move = move
                    alpha = best_value
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                    beta = best_value

            # Prune the search tree
            # We know this state will never be chosen, so we stop evaluating its children
            if beta <= alpha:

                # print ' ab break on ', alpha, beta
                break

        return best_value, best_move

    def evaluate(self,
                 state     # type: State
    
            ):
        # type: () -> float
        """
        Evaluates the value of the given state for the given player
    
        :param state: The state to evaluate
        :param player: The player for whom to evaluate this state (1 or 2)
        :return: A float representing the value of this state for the given player. The higher the value, the better the
            state is for the player.
        """
    
        score = 0.0
        player=state.whose_turn()     # type: int
        for _ in range(self.__num_samples):
    
            st = state.clone()
    
            # Do some random moves
            for i in range(self.__depth):
                if st.finished():
                    break
    
                st = st.next(random.choice(st.moves()))
    
            score += util.ratio_ships(state, player)
    
        return score/float(self.__num_samples)

def maximizing(state):
    """
    Whether we're the maximizing player (1) or the minimizing player (2).

    :param state:
    :return:
    """
    return state.whose_turn() == 1

