from collections import namedtuple
import numpy as np 

class Game:
    """A game has a utility for each state and a terminal test."""
    def actions(self, state):
        """Return a list of possible moves from this state."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state by applying move to current state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the utility value of the state for the player."""
        raise NotImplementedError

    def terminal_test(self, state): 
        """Similar to goal_test of a Problem."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is."""
        return state.to_move 

    def display(self, state):
        print(state)

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def play_game(self, *players):
        state = self.initial 
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move) 
                if self.terminal_test(state):
                    self.display(state) 
                    return self.utility(state, self.to_move(self.initial))

# Game state, similar to Node in search problems 
GameState = namedtuple('GameState', 'to_move, utility, board, moves')

class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self, h=3, v=3, k=3):
        self.h = h
        self.v = v
        self.k = k
        moves = [(x, y) for x in range(1, h + 1)
                 for y in range(1, v + 1)]
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '.'), end=' ')
            print()
    
    # auxiliary functions 
    def compute_utility(self, board, move, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        if (self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (1, -1)) or
                self.k_in_row(board, move, player, (1, 1))):
            return +1 if player == 'X' else -1
        else:
            return 0

    def k_in_row(self, board, move, player, delta_x_y):
        """Return true if there is a line through move on board for player."""
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n >= self.k

# ___________________________________________________________________________
# Naive minimax adversarial search: return next optimal move
def minmax(state, game):
    """Calculate the best move."""
    player = game.to_move(state)  # current player 
    # min_value -> (utility, move)
    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player), None 
        min_v = np.inf 
        next_m = None 
        for a in game.actions(state):
            v2, a2 = max_value(game.result(state, a))
            if v2 < min_v:
                min_v, next_m = v2, a 
        return min_v, next_m
    
    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player), None 
        max_v = -np.inf 
        next_m = None 
        for a in game.actions(state):
            v2, a2 = min_value(game.result(state, a))
            if v2 > max_v:
                max_v, next_m = v2, a 
        return max_v, next_m 
    # main body of the algorithm 
    value, move = max_value(state)
    return move 


# alpha-beta pruning 
def alpha_beta_search(state, game):
    player = game.to_move(state)
    # use alpha and beta in min_value
    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        min_v = np.inf 
        move = None 
        for a in game.actions(state):
            v2, a2 = max_value(game.result(state, a), alpha, beta)
            if v2 < min_v:
                min_v, move = v2, a 
                beta = min(beta, min_v)
            if min_v <= alpha:  # alpha is the current max value of the parent max layer. 
                return min_v, move
        return min_v, move 

    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        max_v, move = -np.inf, None
        for a in game.actions(state):
            v2, a2 = min_value(game.result(state, a), alpha, beta)
            if v2 > max_v:
                max_v, move = v2, a 
                alpha = max(alpha, max_v)
            if max_v >= beta:  # beta is the current min value (upper bound of the parent min layer)
                return max_v, move 
        return max_v, move 

    # main body of the algorithm 
    value, move = max_value(state, -np.inf, np.inf) 
    return value 

# Alpha beta with cutoff test and heuristic evaluation function 
def alpha_beta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    player = game.to_move(state) 

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -np.inf 
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth+1))
            if v >= beta:
                return v 
            alpha = max(alpha, v)
        return v 

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = np.inf 
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth+1))
            if v <= alpha:
                return v 
            beta = min(beta, v)
        return v 

    # body of the main algorithm
    cutoff_test = (cutoff_test or (lambda state, depth: depth>d or game.terminal_test(state)))
    eval_fn = (eval_fn or (lambda state: game.utility(state, player)))
    best_score = -np.inf 
    beta = np.inf 
    move = None 
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            move = a 
    return move 

# Probabilistic cut algorithm

# Iterative deepening minimax 

# Stochastic alpha beta minimax 

# Monte Carlo alpha beta simulation

# TODO: chess player (with time limit) with all improvements:
# Transposition table, iterative deepening with dynamic killer move heuristics,
# Material value heuristics, quiescence search, singular extension, 
# probabilistic cut forward pruning, table lookup for opening and endgames