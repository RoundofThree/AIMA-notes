## Classical Search 

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

#### Problem 

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

##### Examples of problems

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

#### Search algorithms 

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

##### Uninformed strategies (blind)

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
    - 

4. Depth first search (graph search)

5. Depth limited search
4. Iterative deepening search 
5. Bidirectional search 

**Table summary**:


##### Informed strategies 

**Evaluation function**: `f(n)` 

1. Best first search 
2. Greedy best first search 
3. A* search 
4. Recursive best first search 
5. Simplified memory bounded A*

*Heuristics can be obtained via relaxation, precomputing patterns, or learning from experience (neural nets, decision trees, reinforcement learning).*