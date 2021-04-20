from utils import *
import numpy as np 
import random

# Steepest ascent hill climbing
def hill_climbing(problem, initial=None):
    current = Node(initial if initial is not None else problem.initial)
    while True:
        neighbors = current.expand(problem)
        if not neighbors:
            break
        neighbor = argmax_random_tie(neighbors, key=lambda node: problem.value(node.state))
        if problem.value(neighbor.state) <= problem.value(current.state):
            break 
        current = neighbor
    return current.state

# Steepest ascent with sideways moves
def hill_climbing_sideways(problem, max_consecutive_sideways, initial=None):
    current = Node(initial if initial is not None else problem.initial)
    consec = 0
    while True:
        neighbors = current.expand(problem)
        if not neighbors:
            break
        neighbor = argmax_random_tie(neighbors, key=lambda node: problem.value(node.state))
        if problem.value(neighbor.state) < problem.value(current.state):
            break
        if problem.value(neighbor.state) == problem.value(current.state):
            consec = consec + 1
        else:
            consec = 0
        if consec > max_consecutive_sideways:
            break 
        current = neighbor 
    return current.state

# Stochastic hill climbing (without sideways)
def stochastic_hill_climbing(problem: Problem, initial=None):
    current = Node(initial if initial is not None else problem.initial)
    while True:
        neighbors = current.expand(problem)
        current_value = problem.value(current.state)
        if not neighbors:
            break
        neighbors = list(filter(lambda node: problem.value(node.state) > current_value, neighbors))
        if not neighbors:
            break
        current = random.choice(neighbors)
    return current.state 


# First choice hill climbing
def first_choice_hill_climbing(problem: Problem, initial=None):
    current = Node(initial if initial is not None else problem.initial)
    while True:
        old_state = current.state 
        actions = problem.actions(current.state)
        for a in actions:
            result = problem.result(current.state, a) # result state
            if problem.value(result) > problem.value(current.state):
                next_node = Node(result, current, a, problem.path_cost(current.path_cost, current.state, a, result))
                current = next_node
                break
        if current.state == old_state:  
            break # in local maximum 
    return current.state 


# Random restart hill climbing
def random_restart_hill_climbing(problem: Problem):
    while True:
        current = problem.random_state()
        current = hill_climbing(problem, current)
        if problem.goal_test(current):
            break
    return current

# Local beam search. Stop when max_nodes have been expanded. 
def local_beam_search(problem: Problem, k=10, max_nodes=10000):
    nodes = [Node(problem.random_state()) for i in range(k)]
    visited = set()  # closed list 
    while True:
        # neighbors should not have repeated elements 
        neighbors = list(set([candidate for node in nodes for candidate in node.expand(problem) if candidate.state not in visited]))
        nodes = sorted(neighbors, key=lambda node: problem.value(node.state))[:k]
        # update visited 
        visited.update(nodes)
        if len(visited) > max_nodes:
            break
    return argmax_random_tie(nodes, lambda node: problem.value(node.state))

# Stochastic local beam search
def stochastic_local_beam_search(problem: Problem, k=10, max_nodes=10000):
    nodes = [Node(problem.random_state()) for i in range(k)]
    visited = set()  # closed list 
    while True:
        neighbors = list(set([candidate for node in nodes for candidate in node.expand(problem) if candidate.state not in visited]))
        # choose k based weighted distribution
        f_values = map(lambda node: problem.value(node.state), neighbors)
        sampler = weighted_sampler(neighbors, f_values)
        nodes = [sampler() for i in range(k)]
        visited.update(nodes)
        if len(visited) > max_nodes:
            break
    return argmax_random_tie(nodes, lambda node: problem.value(node.state))


# Simulated annealing
def exp_schedule(k=20, lam=0.005, limit=100):
    """One possible schedule function for simulated annealing"""
    return lambda t: (k * np.exp(-lam * t) if t < limit else 0)


def simulated_annealing(problem, schedule=exp_schedule()):
    current = Node(problem.initial)
    for t in range(sys.maxsize):
        T = schedule(t) # as t grows larger, T decreases 
        if T == 0: # absolute zero temperature 
            return current.state
        neighbors = current.expand(problem)
        if not neighbors:
            return current.state
        next_choice = random.choice(neighbors)
        delta_e = problem.value(next_choice.state) - problem.value(current.state)
        if delta_e > 0 or probability(np.exp(delta_e / T)):
            current = next_choice


# Genetic algorithm (basic)
def genetic_algorithm(population, fitness_f, gene_pool=[0,1], f_thres=None, ngen=1000, pmut=0.1):
    """
    ngen: Number of generations
    population: Initial states 
    fitness_f: Fitness function 
    """
    for i in range(ngen):
        population = [mutate(recombine(*select(2, population, fitness_f)), gene_pool, pmut)
                        for i in range(len(population))]
        fittest_individual = fitness_threshold(fitness_f, f_thres, population)
        if fittest_individual:
            return fittest_individual
    return max(population, key=fitness_f)

def fitness_threshold(fitness_f, f_thres, population):
    if not f_thres:
        return None 
    fittest_individual = max(population, key=fitness_f)
    if fitness_f(fittest_individual) >= f_thres:
        return fittest_individual
    return None 

def select(r, population, fitness_f):
    fitnesses = map(fitness_f, population)
    sampler = weighted_sampler(population, fitnesses)
    return [sampler() for i in range(r)]


def recombine(x, y):
    """
    x and y are cromosomes. For this specific RECOMBINE(), they have to be iterable. 
    """
    n = len(x)
    c = random.randrange(0, n) # random split point 
    return x[:c] + y[c:]

def mutate(x, gene_pool, pmut):
    if random.uniform(0, 1) >= pmut:
        return x 
    n = len(x)
    g = len(gene_pool)
    c = random.randrange(0, n)
    r = random.randrange(0, g)
    new_gene = gene_pool[r]
    return x[:c] + [new_gene] + x[c+1:]

def recombine_uniform(x, y):
    n = len(x)
    result = [0] * n
    indexes = random.sample(range(n), n) # shuffle indices
    for i in range(n):
        idx = indexes[i]
        result[idx] = x[idx] if i < n/2 else y[idx]
    return "".join(str(r) for r in result)

# Generate random population from gene pool
def init_population(pop_number: int, gene_pool, state_length: int):
    population = []
    g = len(gene_pool)
    for i in range(pop_number):
        new_individual = [gene_pool[random.randrange(0, g) for j in range(state_length)]
        population.append(new_individual)
    return population


# N queens problem incremental definition 
class NQueensProblem(Problem):
    def __init__(self, N):
        super().__init__(tuple([-1] * N))
        self.N = N

    def actions(self, state):
        """In the leftmost empty column, try all non-conflicting rows."""
        if state[-1] != -1:
            return []  # All columns filled; no successors
        else:
            col = state.index(-1)
            return [row for row in range(self.N)
                    if not self.conflicted(state, row, col)]

    def result(self, state, row):
        """Place the next queen at the given row."""
        col = state.index(-1)
        new = list(state[:])
        new[col] = row
        return tuple(new)

    def conflicted(self, state, row, col):
        """Would placing a queen at (row, col) conflict with anything?"""
        return any(self.conflict(row, col, state[c], c)
                   for c in range(col))

    def conflict(self, row1, col1, row2, col2):
        """Would putting two queens in (row1, col1) and (row2, col2) conflict?"""
        return (row1 == row2 or  # same row
                col1 == col2 or  # same column
                row1 - col1 == row2 - col2 or  # same \ diagonal
                row1 + col1 == row2 + col2)  # same / diagonal

    def goal_test(self, state):
        """Check if all columns filled, no conflicts."""
        if state[-1] == -1:
            return False
        return not any(self.conflicted(state, state[col], col)
                       for col in range(len(state)))

    def h(self, node):
        """Return number of conflicting queens for a given node"""
        num_conflicts = 0
        for (r1, c1) in enumerate(node.state):
            for (r2, c2) in enumerate(node.state):
                if (r1, c1) != (r2, c2):
                    num_conflicts += self.conflict(r1, c1, r2, c2)

        return num_conflicts

# For local search 
class CompleteStateNQueens(Problem):
    def __init__(self, N):
        self.N = N
        super().__init__(self.random_state()) # change 

    def random_state(self):
        return tuple([r for c in range(self.N) for r in range(self.N)])

    def actions(self, state):
        """
        Change any column to any value not already in. Conflicting states are allowed. 
        """
        return [tuple(r, c) for r in range(self.N) for c in range(self.N)
                if state[c] != r]
    
    def result(self, state, action):
        """
        action: tuple(row, col)
        """
        new = list(state[:])
        new[action[1]] = action[0]
        return tuple(new) 

    def conflicted(self, state, row, col):
        """Would placing a queen at (row, col) conflict with anything?"""
        return any(self.conflict(row, col, state[c], c)
                   for c in range(col))

    def conflict(self, row1, col1, row2, col2):
        """Would putting two queens in (row1, col1) and (row2, col2) conflict?"""
        return (row1 == row2 or  # same row
                col1 == col2 or  # same column
                row1 - col1 == row2 - col2 or  # same \ diagonal
                row1 + col1 == row2 + col2)  # same / diagonal

    def goal_test(self, state):
        """Check if no conflicts."""
        return not any(self.conflicted(state, state[col], col)
                       for col in range(len(state)))

    def h(self, node):
        """Return number of conflicting queens for a given node"""
        num_conflicts = 0
        for (r1, c1) in enumerate(node.state):
            for (r2, c2) in enumerate(node.state):
                if (r1, c1) != (r2, c2):
                    num_conflicts += self.conflict(r1, c1, r2, c2)
        return num_conflicts

# Use Genetic algorithm to solve N queens
def nqueens_genetic_algorithm(problem: CompleteStateNQueens, ngen=1000, pmut=0.1, n=20):
    # randomly generate an initial population of n states
    population = [problem.random_state() for i in range(n)]
    return genetic_algorithm(population, lambda node: problem.N - problem.h(node), [i in range(N)], N, ngen, pmut)
    