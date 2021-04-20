import functools 
import heapq
import random 
import bisect

def is_in(elt, seq):
    """Similar to (elt in seq), but comparing with 'is' """
    return any(x is elt for x in seq)


def memoize(fn, slot=None, maxsize=32):
    """Memoize fn: make it remember the computed value for any argument list.
    If slot is specified, store result in that slot of first argument.
    If slot is false, use lru_cache for caching the values."""
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        @functools.lru_cache(maxsize=maxsize)
        def memoized_fn(*args):
            return fn(*args)

    return memoized_fn

# Problem and node classes
class Problem:
    """The abstract class for a formal problem. """
    
    def __init__(self, initial, goal=None) -> None:
        self.initial = initial
        self.goal = goal 

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal 

    def path_cost(self, c, state1, action, state2):
        """Cost of solution path that arrives at state2 from state1 via action, 
        assuming cost c to get to state1."""
        return c+1

    def value(self, state):
        """For optimisation problems (local search)."""
        raise NotImplementedError

    def random_state(self):
        """Return a random state. Useful for random restart and local beam search."""
        raise NotImplementedError

class Node:
    """Node in search tree."""
    def __init__(self, state, parent=None, action=None, path_cost=0) -> None:
        self.state = state # current state
        self.parent = parent  # from which Node 
        self.action = action # from which action 
        self.path_cost = path_cost # path_cost so far
        self.depth = 0 # depth in search tree 
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self) -> str:
        return f'<Node {self.state}>'

    def __lt__(self, node) -> bool:
        return self.state < node.state 

    def expand(self, problem) -> list:
        """List of reachable nodes in one step."""
        return [self.child_node(problem, action) for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node 

    def solution(self):
        node, path_back = self, [] 
        while node:
            path_back.append(node)
            node = node.parent 
        return list(reversed(path_back))

    # equal if same state 
    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state 

    def __hash__(self):
        return hash(self.state) 

# Data structures
class PriorityQueue:
    """A Queue in which the minimum (or maximum) element (as determined by f and
    order) is returned first.
    If order is 'min', the item with minimum f(x) is
    returned first; if order is 'max', then it is the item with maximum f(x).
    Also supports dict-like lookup."""

    def __init__(self, order='min', f=lambda x: x):
        self.heap = []
        if order == 'min':
            self.f = f
        elif order == 'max':  # now item with max f(x)
            self.f = lambda x: -f(x)  # will be popped first
        else:
            raise ValueError("Order must be either 'min' or 'max'.")

    def append(self, item):
        """Insert item at its correct position."""
        heapq.heappush(self.heap, (self.f(item), item))

    def extend(self, items):
        """Insert each item in items at its correct position."""
        for item in items:
            self.append(item)

    def pop(self):
        """Pop and return the item (with min or max f(x) value)
        depending on the order."""
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')

    def __len__(self):
        """Return current capacity of PriorityQueue."""
        return len(self.heap)

    def __contains__(self, key):
        """Return True if the key is in PriorityQueue."""
        return any([item == key for _, item in self.heap])

    def __getitem__(self, key):
        """Returns the first value associated with key in PriorityQueue.
        Raises KeyError if key is not present."""
        for value, item in self.heap:
            if item == key:
                return value
        raise KeyError(str(key) + " is not in the priority queue")

    def __delitem__(self, key):
        """Delete the first occurrence of key."""
        try:
            del self.heap[[item == key for _, item in self.heap].index(True)]
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.heap)

# ______________________________________________________________________________
# argmin and argmax

identity = lambda x: x


def argmin_random_tie(seq, key=identity):
    """Return a minimum element of seq; break ties at random."""
    return min(shuffled(seq), key=key)


def argmax_random_tie(seq, key=identity):
    """Return an element with highest fn(seq[i]) score; break ties at random."""
    return max(shuffled(seq), key=key)


def shuffled(iterable):
    """Randomly shuffle a copy of iterable."""
    items = list(iterable)
    random.shuffle(items)
    return items

# __________________________________________________________________________________
# Maths and statistics

def probability(p):
    """Return true with probability p."""
    return p > random.uniform(0.0, 1.0)

def weighted_sampler(seq, weights):
    totals = []
    for w in weights:
        totals.append(w + totals[-1] if totals else w)
    return lambda: seq[bisect.bisect(totals, random.uniform(0, totals[-1]))]