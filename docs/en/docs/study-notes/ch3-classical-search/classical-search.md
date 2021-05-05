# Classical Search 

Agent: goal-based agent called **problem solving agent**. 

Representation: atomic. 

Environment: observable, discrete, known, deterministic. 

Process: 

- Goal formulation -> set of states to consider a goal. Goal helps organize the behavior by limiting the objectives of the agent. 
- Problem formulation -> level of detail of actions and states. Avoid too much detail that brings uncertainty. 
- Search algorithm -> take problem and output a sequence of actions as solution 
- Execution while ignoring percepts

```
goal <- FORMULATE_GOAL(current_state)
problem <- FORMULATE_PROBLEM(current_state, goal)
solution <- SEARCH(problem)
```

## Problem 

Definition of state space (a directed graph):

- Initial state
- Actions applicable in s for any state s
- Transition model or successor function

```Python
problem.initial_state -> State 
problem.actions(state: State) -> list(Action)
# Transition model
problem.result(state: State, action: Action) -> State
# Successor function (no actions() needed, because we can directly get the successors)
problem.successors(state: State) -> list(State)
```

Defines goal and performance measures:

- Goal test
- Path cost (sum of step costs)

```Python
problem.goal_test(state: State) -> bool # or check full environment
problem.step_cost(currstate: State, action: Action, nextstate: State) -> int
```

An **optimal solution** has the lowest path cost amongst all solutions.

In **problem formulation**, **abstraction** involves removing as much details as possible 
while retaining validity and ensuring that the abstract actions are easy to carry out. 

### Examples of problems

- Vacuum world
- 8-puzzle -> a sliding-block puzzle (NP complete)

It has 9!/2 reachable states. 

- 8-queens incremental formulation: from an empty state, incrementally add queens

States: any arrangement of 0..8 queens <br />
Initial state: empty board <br />
Actions: add a queen to current state <br />
Transition model: state + action => state with added queen <br />
Goal test: 8 queens and none attacking <br />

It has
<img src="https://render.githubusercontent.com/render/math?math=\frac{64!}{(64-8)!}">
possible sequences to search. 

An improvement is to prune the illegal states: <br />
States: any valid arrangement 0..8 queens <br />
Actions: add a queen to any **leftmost** empty column such that it is not attacked <br />

- 8-queens complete-state formulation: start with all the queens in the board. See Chapter 6 for an efficient algorithm. 

- Route finding problems: commercial travel advice systems
- Touring problems: <br />
States: current position and the set of visited positions <br />
An example of touring problem is TSP. <br />
- VLSI layout problems: place cells (cell layout) and wire them (channel routing) <br />
- Robot navigation 
- Automatic assembly sequencing: eg. protein design 

## Search algorithms 

**Frontier/Open list**: set of all leaf nodes available for expansion at any given point. <br />
Redundant paths can cause a tractable problem to become intractable. Some problem formulations
can eliminate redundant paths (see 8-queens). But in some problems (eg. whose actions are reversible) can't. 

**Explored set/Closed list**: set of all expanded nodes to avoid redundant paths. <br />
By adding a closed list to the infrastructure, the `TREE-SEARCH` becomes a `GRAPH-SEARCH`.

**Infrastructure of search**:
- Node: a node is not a state, but a bookkeeping of the search. See [Node class](search.py).
    - State: the current state
    - Parent: the previous node 
    - Action: the previous action
    - Path cost
- Frontier data structure: queue (LIFO, FIFO and priority queue)
- Closed list data structure: hash table with a right notion of equality between states

**Performance measure**:
- Completeness: if there is solution, it will find one
- Optimality: it will find an optimal solution
- Time complexity: number of nodes evaluated 
- Space complexity: number of nodes stored in memory

Time and space complexities are expressed in terms of:
1. Branching factor `b` max num of successors 
2. Depth `d` of the shallowest goal node 
3. Max length of any path in the state space `m`

**Effectiveness**:
- Search cost: time or space used to find the goal 
- Total cost: search cost + path cost 

### Uninformed strategies (blind)

1. Breadth first search 
    - Frontier: FIFO queue
    - Goal test before adding to the frontier 
    - Completeness: yes, as long as `b`is finite
    - Optimality: shallowest goal node is the optimal for unit-cost steps 
    - Time complexity: `O(b^d)`
    - Space complexity: `O(b^{d-1}` for closed list, `O(b^d)` for open list
2. Uniform cost search 
    - Frontier: priority queue with priority lowest `g(n)=path cost`
    - Goal test when selected for expansion to avoid suboptimality 
    - Better node replaces the same node in the frontier
    - Comleteness: yes, provided every step cost > epsilon
    - Optimality: yes
    - Time and space complexity: `O(b^{1 + floor(C* / e)})`, where `C*`is optimal cost, `e` is minimum action cost.
    - This is different from breadth first search in that it is optimal for any step cost, 
    but if all step costs are the same, breadth first search is faster.
3. Depth first search (tree search)
    - Frontier: LIFO queue
    - Completeness: no, may loop forever
    - Optimality: no
    - Time complexity: `O(b^m)`, where `m` is the maximum depth of any node, which may be INF
    - Space complexity: `O(bm)` 

4. Depth first search (graph search)
    - Frontier: LIFO queue
    - Completeness: yes, given state space is finite
    - Optimality: no
    - Time complexity: `O(b^m)`
    - Space complexity: `O(b^m)` 

5. Backtracking search (depth first search):
    - Generate only one successor at a time
    - Modify the current state rather than copy the state, need to undo modifications
    - Space complexity: `O(m)`, one state description and `O(m)` actions

6. Depth limited search
    - Completeness: yes, given `l >= d`
    - Optimality: yes, given `l == d`
    - The diameter of the state space is a good depth limit

7. Iterative deepening search (**Preferred uninformed when search space is large and the depth d is not known**)
    - It combines breadth first search and depth first search
    - Completeness: yes, given the state space is finite
    - Optimality: yes, given the path cost is a nondecreasing function of the depth of the node
    - Time complexity: `O(b^d)` as BFS
    - Space complexity: `O(bm)`

A hybrid approach is to run BFS until almost all memory is consumed, then run IDS from all
the nodes in the frontier. 

8. Bidirectional search 
    - Only when there is an explicit goal state
    - Time complexity: `O(b^{d/2})`
    - Space complexity: `O(b^{d/2})`, one frontier must be in memory, but the other can run IDS

### Informed strategies 

**Evaluation function**: `f(n)`, most include a **heuristic function** `h(n)`, which is the estimated cost of the cheapest path from the state at node `n` to a goal state. 

1. Greedy best first search
    - `f(n) = h(n)`
    - Completeness: no (tree search, infinite loop), yes (graph search, given finite state space)
    - Time complexity: `O(b^m)`
2. A* search 
    - `f(n) = g(n) + h(n)`
    - Completeness: yes
    - Optimality: yes
    - Optimally efficient: smallest number of expanded nodes for given heuristic  
    - Conditions: 
        1. Admissible heuristics: `f(n) < cost of solution path`
        2. Consistent heuristics: `h(n) <= h(n') + c(n, a, n')`, where c is the cost of action
        3. Tree search is optimal if admissible
        4. Graph search is optimal if consistent, because `f(n)` is nondecreasing 
    - Time complexity: `O(b^{ed})`, only expands nodes with `f(n) > C*`, where `C*` is the optimal cost 
    - Space complexity: `O(b^{ed})`, where e is the relative error `(h - h*)/h*`, which makes 
    it unfeasible for large state spaces
3. Iterative deepening A* search
    - DFS 
    - Increasing limits on `f(n)` f-contour
    - Completeness: yes, as A* 
    - Optimality: yes, if heuristics conditions are met
    - Time complexity: depends on the number of different heuristic values
    - Space complexity: `O(bf*/delta)`, where delta is the smallest step cost and f* is the optimal cost
    - Excessive node generation if every node has a different `f(n)`
4. Recursive best first search 
    - Similar to recursive depth-first search that searches the most optimal successor node but with `f_limit` variable to keep track of the best alternative path available from any ancestor of the current node 
    - Excessive node generation because `h` is usually less optimistic when closer to the goal
    - Completeness: yes, as A* 
    - Optimality: yes, if `h` is admissible
    - Time complexity: depends on how often the best path changes 
    - Space complexity: `O(bd)`
5. Simplified memory bounded A*
    - A* expanding until the memory = closed list + open list
    - Drop the worst leaf node in open list
    - For each new successor, the `f(n)` is propagated back up the tree (update occurs after full expansion)
    - Completeness: yes, if `d < memory size`
    - Optimality: yes, if reachable in memory size 

```Python
def smastar(problem, h=None, MAX):
    def backup(node):
        if completed(node) and node.parent is not None:
            oldf = node.f
            node.f = least f cost of all successors 
            if oldf != node.f:
                backup(node.parent)

    openL = binary tree of binary trees
    root = Node(problem.initial)
    openL.add(root)
    used = 1

    # logic
    while True:
        if len(openL) == 0:
            return "failure"
        best = openL.best() # deepest least f node
        if problem.goal_test(best):
            return best
        succ = next_successor(best)
        succ.f = max(best.f, succ.path_cost + h(succ))
        if completed(best): # all successors have been evaluated 
            backup(best)
        if best.expand(problem) all in memory:
            openL.remove(best)
        used = used + 1
        if used > MAX:
            deleted = openL.remove_worst()
            remove deleted from its parents successors list
            openL.add(deleted.parent)
            used = used - 1
        openL.add(succ)

```

### Heuristics
**Effective branching factor**: `N+1 = 1 + b* + (b*)^2 + (b*)^3 + ... + (b*)^d`. The `b*` is ideally close to 1. A better heuristics dominates a worse heuristics, `hbest(n) > hworse(n)`. 

*Heuristics can be obtained via relaxation, precomputing patterns, or learning from experience (neural nets, decision trees, reinforcement learning).*

To have the best of all heuristics:
```
h(n) = max {h1(n), h2(n), h3(n), ... } 
```
**Pattern databases**: store exact solution costs for every possible subproblem instance, to compute an admissible heuristics for each complete state during the search. 

**Disjoint pattern databases**: they are additive 