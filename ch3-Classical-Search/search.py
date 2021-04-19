from utils import *
from collections import deque 
import sys 
import numpy as np

# Breadth-first tree search 
def breadth_first_tree_search(problem) -> Node:
    frontier = deque([Node(problem.initial)]) # FIFO 
    while frontier:
        node = frontier.popleft()
        if problem.goal_test(node.state):
            return node 
        frontier.extend(node.expand(problem))
    return None 

# Depth-first tree search 
def depth_first_tree_search(problem) -> Node:
    frontier = [Node(problem.initial)] # LIFO
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
    return None

# Depth-first graph search 
def depth_first_graph_search(problem) -> Node:
    frontier = [Node(problem.initial)] # LIFO
    explored = set() 
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node 
        explored.add(node.state)
        frontier.extend(child for child in node.expand(problem)
                        if child.state not in explored and child not in frontier)
    return None 

# Breadth-first graph search 
def breadth_first_graph_search(problem) -> Node:
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node 
    frontier = deque([node])
    explored = set() 
    while frontier:
        node = frontier.popleft() 
        explored.add(node.state) 
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier: 
                if problem.goal_test(child.state):
                    return child 
                frontier.append(child)
    return None 

# Best-first graph search 
def best_first_graph_search(problem, f, display=False) -> Node:
    f = memoize(f, 'f')   # memoize
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)  # open list, to be explored
    frontier.append(node) 
    explored = set()  # closed list, explored 
    while frontier:
        node = frontier.pop()
        # check if goal state 
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remaining.")
            return node
        # add to closed list 
        explored.add(node.state)
        for child in node.expand(problem):  # expand child states
            if child.state not in explored and child not in frontier:  # add to the open list 
                frontier.add(child) 
            elif child in frontier:
                if f(child) < frontier[child]:  # update the open list if needed 
                    del frontier[child]
                    frontier.append(child)  
    return None 

# Iterative deepening A* search
def idastar(problem, h=None) -> Node:
    h = memoize(h or problem.h, 'h')

    def dfs_contour(node, f_limit):
        next_f = np.inf
        if h(node) > f_limit:
            return None, h(node)
        if problem.goal_test(node.state):
            return node, f_limit
        successors = node.expand(problem)
        for s in successors:
            solution, newf = dfs_contour(s, f_limit)
            if solution is not None:
                return solution, f_limit
            next_f = min(next_f, newf)
        return None, next_f

    node = Node(problem.initial)
    f_limit = h(node)
    while True:
        # explore with contour = limit
        solution, f_limit = dfs_contour(node, f_limit)
        if solution is not None:
            return solution
        if f_limit == np.inf:
            return "failure"
    
# Recursive best-first search
def recursive_best_first_search(problem, h=None) -> Node:
    h = memoize(h or problem.h, 'h')
    
    def rec(problem, node, flimit):
        if problem.goal_test(node.state):
            return node, 0
        successors = node.expand(problem)
        if len(successors) == 0:
            return None, np.inf
        for s in successors:
            s.f = max(s.path_cost + h(s), node.f) # update the f(n) of each visited node 
        while True:
            # order by the lowest f value 
            successors.sort(key=lambda x: x.f)
            best = successors[0]
            if best.f > flimit:
                return None, best.f 
            if len(successors)>1:
                alternative = successors[1].f 
            else:
                alternative = np.inf
            result, best.f = rec(problem, best, min(alternative, flimit))
            if result is not None:  # return the first result found 
                return result, best.f 
    node = Node(problem.initial) 
    node.f = h(node)
    result, best_f = rec(problem, node, np.inf) 
    return result 

# f(n) = g(n)
def uniform_cost_search(problem, display=False) -> Node:
    return best_first_graph_search(problem, lambda node: node.path_cost, display)

# f(n) = h(n)
greedy_best_first_graph_search = best_first_graph_search 

# f(n) = g(n) + h(n)
def astar_search(problem, h=None, display=False) -> Node:
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda node: node.path_cost + h(node), display) 
        
# Depth-limited search 
def depth_limited_search(problem, limit=50) -> Node:
    def recursive_dls(node, problem, limit):
        if problem.goal_test(node.state):
            return node 
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_ocurred = False 
            for child in node.expand(problem):  # expand child nodes, even visited ones because there's no closed list
                result = recursive_dls(child, problem, limit-1)
                if result == 'cutoff':
                    cutoff_ocurred = True 
                elif result is not None:
                    return result 
                return 'cutoff' if cutoff_ocurred else None 

    return recursive_dls(Node(problem.initial), problem, limit)

# Iterative deepening search 
def iterative_deepening_search(problem):
    for depth in range(sys.maxsize):  # avoid stack overflow 
        result = depth_limited_search(problem, depth)
        if result != 'cutoff':
            return result 

# Bidirectional best-first search 
# https://webdocs.cs.ualberta.ca/~holte/Publications/MM-AAAI2016.pdf -- BBFS whose forward and backward searches are guaranteed to meet in the middle 
# Keep two open lists and two tables of reached states 
def bidirectional_search(problem):
    e = 0  # in graph problem, e is the min edge 
    gF, gB = {Node(problem.initial): 0}, {Node(problem.goal): 0}
    openF, openB = [Node(problem.initial)], [Node(problem.goal)] # open lists
    closedF, closedB = [], []  # closed lists 
    U = np.inf 

    def extend(U, open_dir, open_other, g_dir, g_other, closed_dir):
        n = find_key(C, open_dir, g_dir) # next node to extend 
        
        open_dir.remove(n)
        closed_dir.append(n)

        for c in n.expand(problem):
            if c in open_dir or c in closed_dir:
                if g_dir[c] <= problem.path_cost(g_dir[n], n.state, None, c.state):
                    continue # not optimal
                open_dir.remove(c) 

            g_dir[c] = problem.path_cost(g_dir[n], n.state, None, c.state)  # update the cost function g(x)
            open_dir.append(c) # add to open list 
            # if c can be joined with the other direction, update the current optimal cost 
            if c in open_other:
                U = min(U, g_dir[c] + g_other[c])

        return U, open_dir, closed_dir, g_dir 

    def find_min(open_dir, g):
        pr_min, pr_min_f = np.inf, np.inf 
        for n in open_dir:
            f = g[n] + problem.h(n)  # total_cost + heuristic, such as a-star
            pr = max(f, 2 * g[n]) # novel way of ordering the open list, 2g(n)>f(n) iff g(n)>h(n) iff n far from start
            pr_min = min(pr_min, pr)
            pr_min_f = min(pr_min_f, f) 

        return pr_min, pr_min_f, min(g.values()) 

    def find_key(pr_min, open_dir, g):
        """Finds key in open_dir with value equal to pr_min and minimum g value."""
        m = np.inf 
        node = Node(-1) 
        for n in open_dir:
            pr = max(g[n] + problem.h(n), 2 * g[n])
            if pr == pr_min:
                if g[n] < m:
                    m = g[n]
                    node = n 

        return node 

    while openF and openB:
        pr_min_f, f_min_f, g_min_f = find_min(openF, gF) 
        pr_min_b, f_min_b, g_min_b = find_min(openB, gB) 
        C = min(pr_min_f, pr_min_b)
        # terminating condition
        if U <= max(C, f_min_f, f_min_b, g_min_f + g_min_b + e):
            return U

        if C == pr_min_f:
            # extend forward 
            U, openF, closedF, gF = extend(U, openF, openB, gF, gB, closedF) 
        else:
            # extend backward 
            U, openB, closedB, gB = extend(U, openB, openF, gB, gF, closedB)

    return np.inf

# Simplified memory bounded A* search
# TODO

# Example problem 
class EightPuzzle(Problem):
    def __init__(self, initial, goal=(1,2,3,4,5,6,7,8,0)):
        super().__init__(initial, goal) 
    
    def find_blank_square(self, state):
        return state.index(0)

    def actions(self, state):
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square % 3 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 3:
            possible_actions.remove('UP')
        if index_blank_square % 3 == 2:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal 

    def check_solvability(self, state):
        inversion = 0
        for i in range(len(state)):
            for j in range(i+1, len(state)):
                if (state[i]>state[j]) and state[i]!=0 and state[j]!=0:
                    inversion += 1
        return inversion % 2 == 0

    # number of misplaced tiles, heuristic 
    def h(self, node):
        return sum(s != g for (s, g) in zip(node.state, self.goal))
