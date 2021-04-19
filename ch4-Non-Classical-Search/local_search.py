from utils import *
import numpy as np 

# Steepest ascent hill climbing
def hill_climbing(problem):
    current = Node(problem.initial)
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
def hill_climbing_sideways(problem, max_consecutive_sideways):
    current = Node(problem.initial)
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

# Stochastic hill climbing



# First choice hill climbing

# Random restart hill climbing

# Simulated annealing
def exp_schedule(k=20, lam=0.005, limit=100):
    """One possible schedule function for simulated annealing"""
    return lambda t: (k * np.exp(-lam * t) if t < limit else 0)


def simulated_annealing(problem, schedule=exp_schedule()):
    """[Figure 4.5] CAUTION: This differs from the pseudocode as it
    returns a state instead of a Node."""
    current = Node(problem.initial)
    for t in range(sys.maxsize):
        T = schedule(t)
        if T == 0:
            return current.state
        neighbors = current.expand(problem)
        if not neighbors:
            return current.state
        next_choice = random.choice(neighbors)
        delta_e = problem.value(next_choice.state) - problem.value(current.state)
        if delta_e > 0 or probability(np.exp(delta_e / T)):
            current = next_choice


# Genetic algorithm (basic)


# 8 queens problem
