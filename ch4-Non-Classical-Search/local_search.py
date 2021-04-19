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

# Stochastic hill climbing

# First choice hill climbing

# Random restart hill climbing

# Simulated annealing

# Genetic algorithm (basic)