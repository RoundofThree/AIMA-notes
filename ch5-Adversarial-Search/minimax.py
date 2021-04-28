from collections import namedtuple
import numpy as np 
import random 
import copy # deepcopy
import itertools 
from collections import defaultdict 
import math 

class Game:
    def actions(self, state):
        raise NotImplementedError

    def result(self, state, move):
        raise NotImplementedError

    def utility(self, state, player):
        raise NotImplementedError

    def terminal_test(self, state): 
        return not self.actions(state)

    def to_move(self, state):
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
GameState = namedtuple('GameState', ['to_move', 'utility', 'board', 'moves'])

class TicTacToe(Game):
    def __init__(self, h=3, v=3, k=3):
        self.h = h
        self.v = v
        self.k = k
        moves = [(x, y) for x in range(1, h + 1)
                 for y in range(1, v + 1)]
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

    def actions(self, state):
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

# Probabilistic cut algorithm: forward pruning

# Iterative deepening minimax 

# TODO: chess player (with time limit) with all improvements:
# Transposition table, iterative deepening with dynamic killer move heuristics,
# Material value heuristics, quiescence search, singular extension, 
# probabilistic cut forward pruning, table lookup for opening and endgames

# _________________________________________________________________________
# Stochastic games
StochasticGameState = namedtuple('StochasticGameState', ['to_move', 'utility', 'board', 'moves', 'chance'])

class StochasticGame(Game):
    def chances(self, state):
        raise NotImplementedError

    def outcome(self, state, chance):
        raise NotImplementedError

    def probability(self, chance):
        raise NotImplementedError

    def play_game(self, *players): # player is a lambda
        state = self.initial
        while True:
            for player in players:
                chance = random.choice(self.chances(state))
                state = self.outcome(state, chance)
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))

# Stochastic minimax 
def expectiminimax(state, game):
    player = game.to_move(state)
    # CHANCE node
    def chance_node(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        sum_chances = 0
        num_chances = len(game.chances(state))
        for chance in game.chances(state):
            utility = 0
            if state.to_move == player:
                utility = max_value(state)
            else:
                utility = min_value(state)
            sum_chances += utility * game.probability(chance)
        return sum_chances / num_chances
    # MAX node
    def max_value(state):
        v = -np.inf
        for a in game.actions(state):
            v = max(v, chance_node(game.result(state, a)))
        return v
    # MIN node
    def min_value(state):
        v = np.inf 
        for a in game.actions(state):
            v = min(v, chance_node(game.result(state, a)))
        return v 

    return max(game.actions(state), key=lambda a: chance_node(state, a), default=None)

# Stochastic alpha beta minimax is much less effective: cannot prune on average values
## each node has a range [min, max] = [min of min of chance nodes, max of max of chance nodes] 
## the ranges become too unrestricive


# Monte Carlo tree search (MCTS) simulation for deterministic games
# for each node, keep t (total value) and n (number of visits)
# Upper Confidence Bound 1 (UCT) -> choose largest candidate to explore further
# x1 + C*sqrt(ln(N) / ni)
# STEPS: select, expand, simulate, back propagate
MonteCarloState = namedtuple('MonteCarloState', ['state', 'total_value', 'visited_number', 'parent', 'untried_actions', 'children'])

def monte_carlo_tree_search(state, game, simulationNum=100):
    def select(node):
        while not game.terminal_test(node.state):
            if len(node.untried_actions) > 0:
                return expand(node)   # initialize and return next unexpanded node
            else:
                node = best_child(node)
        return node 
    # expand next untried action 
    def expand(node):
        action = node.untried_actions.pop() # remove untried action 
        res_state = game.result(node.state, action)
        ret = MonteCarloState(state=res_state, total_value=0, visited_number=0, parent=node, untried_actions=game.actions(res_state), children=[])
        node.children.append(ret)
        return ret
    
    def best_child(node, c_param=0.1):
        choices_weights = [c.total_value/c.visited_number + c_param * np.sqrt(2 * np.log(node.visited_number) / c.visited_number) for c in node.children]
        return node.children[np.argmax(choices_weights)]

    def simulate(node):
        current_state = node.state 
        while not game.terminal_test(current_state):
            action = rollout_policy(node, game.actions(current_state))
            current_state = game.result(current_state, action)
        # return 1, 0, -1 depending on game final state 
        return game.score(current_state)
    
    # random policy (not informed by minimax) also converges 
    def rollout_policy(node):
        """Select a move from these actions."""
        possible_moves = game.actions(node.state)
        return possible_moves[np.random.randint(len(possible_moves))]

    def backpropagate(node, reward):
        node.total_value += reward # 1, 0, -1
        node.visited_number += 1
        if node.parent:
            backpropagate(node.parent)

    def best_action(state, simulationNum=100):
        node = MonteCarloState(state=state, total_value=0, visited_number=0, parent=None, untried_actions=game.actions(state), children=[])
        for i in range(simulationNum):
            to_explore = select(node)
            reward = simulate(to_explore)
            backpropagate(to_explore, reward)
        return best_child(node)

    return best_action(state, simulationNum)

# ___________________________________________________________________________________________
# Online MCTS


class MCTS:
    def __init__(self, c_param, game):
        self.c_param = c_param or math.sqrt(2)
        self.game = game 

    def choose(self, node):
        if game.terminal_test(node.state):
            raise RuntimeError('Already terminated')
        if not node.children:
            # find random successor of this node 
            return 

        return max(node.children, key=lambda n: -np.inf if n.visited_number == 0 else n.total_value / n.visited_number)

    # Train one iteration 
    def rollout(self, node):
        leaf = select(node)
        reward = self.simulate(leaf)
        self.backpropagate(leaf, reward) 

    # select node to explore 
    def select(self, node):
        while True:
            # if node is terminal 
            if game.terminal_test(node.state):
                return node
            # if node is unexplored 
            if len(node.untried_actions) > 0:
                # expand the next untried action 
                return expand(node)
            node = uct_select(node) 

    def expand(self, node):
        action = node.untried_actions.pop() # remove untried action 
        res_state = game.result(node.state, action)
        ret = MonteCarloState(state=res_state, total_value=0, visited_number=0, parent=node, untried_actions=game.actions(res_state), children=[])
        node.children.append(ret)
        return ret

    def simulate(self, node):
        invert_reward = True 
        state = node.state 
        while True:
            if game.terminal_test(state):
                reward = game.score(state)
                return -1 * reward if invert_reward else reward 
            state = rollout_policy(state)  
            invert_reward = not invert_reward

    def backpropagate(self, node, reward):
        node.visited_number += 1
        node.total_value += reward 
        if node.parent:
            self.backpropagate(node.parent, reward)

    # rollout policy can be random, depth limited minimax informed
    # generate a child node 
    def rollout_policy(self, state):
        actions = game.actions(state)
        return actions[np.random.randint(len(actions))]

    # select a child node of param node 
    def uct_select(self, node):
        # assert its children have all been explored 
        assert len(node.untried_actions) == 0 

        log_N = math.log(node.visited_number)
        def uct(n):
            return n.total_value/n.visited_number + self.c_param * math.sqrt(log_N / n.visited_number)
        return max(node.children, key=uct)

# Backgammon
class Backgammon(StochasticGame):
    def __init__(self):
        point = {'W': 0, 'B': 0}
        board = [point.copy() for index in range(24)]
        board[0]['B'] = board[23]['W'] = 2
        board[5]['W'] = board[18]['B'] = 5
        board[7]['W'] = board[16]['B'] = 3
        board[11]['B'] = board[12]['W'] = 5
        self.allow_bear_off = {'W': False, 'B': False}
        self.direction = {'W': -1, 'B': 1}
        self.initial = StochasticGameState(to_move='W',
                                           utility=0,
                                           board=board,
                                           moves=self.get_all_moves(board, 'W'), chance=None)

    def actions(self, state):
        player = state.to_move
        moves = state.moves
        if len(moves) == 1 and len(moves[0]) == 1:
            return moves
        legal_moves = []
        for move in moves:
            board = copy.deepcopy(state.board)
            if self.is_legal_move(board, move, state.chance, player):
                legal_moves.append(move)
        return legal_moves

    def result(self, state, move):
        board = copy.deepcopy(state.board)
        player = state.to_move
        self.move_checker(board, move[0], state.chance[0], player)
        if len(move) == 2:
            self.move_checker(board, move[1], state.chance[1], player)
        to_move = ('W' if player == 'B' else 'B')
        return StochasticGameState(to_move=to_move,
                                   utility=self.compute_utility(board, move, player),
                                   board=board,
                                   moves=self.get_all_moves(board, to_move), chance=None)

    def utility(self, state, player):
        return state.utility if player == 'W' else -state.utility

    def terminal_test(self, state):
        return state.utility != 0

    def get_all_moves(self, board, player):
        all_points = board
        taken_points = [index for index, point in enumerate(all_points)
                        if point[player] > 0]
        if self.checkers_at_home(board, player) == 1:
            return [(taken_points[0],)]
        moves = list(itertools.permutations(taken_points, 2))
        moves = moves + [(index, index) for index, point in enumerate(all_points)
                         if point[player] >= 2]
        return moves

    def display(self, state):
        board = state.board
        player = state.to_move
        print("current state : ")
        for index, point in enumerate(board):
            print("point : ", index, "	W : ", point['W'], "    B : ", point['B'])
        print("to play : ", player)

    def compute_utility(self, board, move, player):
        util = {'W': 1, 'B': -1}
        for idx in range(0, 24):
            if board[idx][player] > 0:
                return 0
        return util[player]

    def checkers_at_home(self, board, player):
        sum_range = range(0, 7) if player == 'W' else range(17, 24)
        count = 0
        for idx in sum_range:
            count = count + board[idx][player]
        return count

    def is_legal_move(self, board, start, steps, player):
        """Move is a tuple which contains starting points of checkers to be
		moved during a player's turn. An on-board move is legal if both the destinations
		are open. A bear-off move is the one where a checker is moved off-board.
        It is legal only after a player has moved all his checkers to his home."""
        dest1, dest2 = vector_add(start, steps)
        dest_range = range(0, 24)
        move1_legal = move2_legal = False
        if dest1 in dest_range:
            if self.is_point_open(player, board[dest1]):
                self.move_checker(board, start[0], steps[0], player)
                move1_legal = True
        else:
            if self.allow_bear_off[player]:
                self.move_checker(board, start[0], steps[0], player)
                move1_legal = True
        if not move1_legal:
            return False
        if dest2 in dest_range:
            if self.is_point_open(player, board[dest2]):
                move2_legal = True
        else:
            if self.allow_bear_off[player]:
                move2_legal = True
        return move1_legal and move2_legal

    def move_checker(self, board, start, steps, player):
        """Move a checker from starting point by a given number of steps"""
        dest = start + steps
        dest_range = range(0, 24)
        board[start][player] -= 1
        if dest in dest_range:
            board[dest][player] += 1
            if self.checkers_at_home(board, player) == 15:
                self.allow_bear_off[player] = True

    def is_point_open(self, player, point):
        """A point is open for a player if the no. of opponent's
        checkers already present on it is 0 or 1. A player can
        move a checker to a point only if it is open."""
        opponent = 'B' if player == 'W' else 'W'
        return point[opponent] <= 1

    def chances(self, state):
        """Return a list of all possible dice rolls at a state."""
        dice_rolls = list(itertools.combinations_with_replacement([1, 2, 3, 4, 5, 6], 2))
        return dice_rolls

    def outcome(self, state, chance):
        """Return the state which is the outcome of a dice roll."""
        dice = tuple(map((self.direction[state.to_move]).__mul__, chance))
        return StochasticGameState(to_move=state.to_move,
                                   utility=state.utility,
                                   board=state.board,
                                   moves=state.moves, chance=dice)

    def probability(self, chance):
        """Return the probability of occurrence of a dice roll."""
        return 1 / 36 if chance[0] == chance[1] else 1 / 18