# Non-Classical Search 

These algorithms are designed for task environments other than finding the shortest path to a goal in a fully-observable, deterministic and discrete environment (that classical search assumes). It is also called **local search**. The path to the goal is not important. The aim is to find find the best state according to an **objective function** (**optimization**).

Properties:
- Completeness: always find a goal if it exists
- Optimality: always find the global minimum/maximum

## Deterministic discrete environments
- Steepest ascent hill climbing / greedy local search
    - Choose the best successor
    - Completeness: no
    - Does not maintain a search tree in memory
    - Can get stuck for: local maxima, ridges, plateaux (which may be a shoulder)
    - Variation: allow sideways moves, limiting the number of consecutive sideways moves
- Stochastic hill climbing
    - Choose a random successor from successors whose `f(s)` is better
    - Completeness: no
    - Slower convergence
- First choice hill climbing
    - Choose the first generated successor whose `f(s)` is better
    - Suitable for when a state has many successors
    - Completeness: no
- Random restart hill climbing
    - Randomly generate initial states, run hill climbing, repeat until a goal is found
    - Completeness: yes
    - Expected number of restarts: `1/p` if each hill climbing has `p` probability of success
- Simulated annealing 
    - Choose a random move:
        - If the successor has better `f(s)`, current = successor
        - Otherwise, accept with probability `P = T / \delta{E}`, where `T = temperature` 
    - Decrease the `T`
    - VLSI layout problem, large scale optimizations...
- Local beam search
    - Start with k random states, select the best k successors in the set of all successors and repeat until a goal is found
    - Different to random restart hill climbing in that information is shared along all instances, but this can cause concentration in one instance (lack of diversity)
- Stochastic local beam search
    - Choose k successors at random, with `P(s)` proportional to `f(s)`
    - Increase diversity to local beam search 
- Genetic algorithm -> mutation and crossover
    - **Population** contains random k initial **individuals**, represented as bitstrings
    - Choose parents, the `P` of being chosen is proportional to **fitness function**
    - **Crossover**: there are different crossover operations, eg. split point
    - **Mutation**: small probability, eg `1/m`, where `m = len(bitstring)`

## Deterministic continuous environments

We can discretize the search space with a fixed `\delta`. Stochastic hill climbing and simulated annealing don't need to discretize for they choose successors randomly with `\delta` vector magnitude. 
 
**Gradient** (for multivariate problem, the gradient is only local):
```
\nabla f = (\frac{\partial f}{\partial x_1}, \frac{\partial f}{\partial x_2}, \frac{\partial f}{\partial x_3})
```
**Empirical gradient**: for non differentiable functions, interact with the environment. 

Each step update, where `x` is a vector: 
```
x <- x + \alpha * \nabla f(x)
```
`\alpha` is a small constant, which can be adjusted during the search. For example, 
**linear search** doubles `\alpha` until `f` starts to decrease. 

- Newton Raphson method 

In univariate calculus, 
```
x <- x - g(x) / g'(x)
```

In matrix-vector form in multivariate calculus,
```
x <- x - H_{f}^{-1}(x) * \nabla f(x)
```

`H_f` is the Hessian matrix:
```
H_{i, j} = \frac{\partial^2 f}{\partial x_i \partial x_j}
```

- Linear programming and Convex optimisation

## Non-deterministic environments
For non-deterministic or partially observable environments, the **percepts** become very important. 

**Non-deterministic transition model**: returns a set of possible outcomes <br />
**Contingent solution**: tree of if-then-else statements <br />
**OR node**: the agent chooses the action to perform. Input is a state. <br />
**AND node**: the environment chooses the outcome. Input is a set of states. <br />
**Cyclic solution**: a possible solution may be to try an action repeatedly until eventually reaching the goal.

Algorithms: 

- Recursive DFS AND-OR graph search
    - To avoid cycles, return failure if the current state is a state on the path from the root.
- BFS or Best first search, A* and so... AND-OR graph search

## Partially observable environments
**Belief state**: possible physical states the agent may be in

### Sensorless problems
The state space consists of belief states instead of physical states. In this space, the
problem is fully observable. Therefore, the solution is not a contingent one, but a 
sequence of actions. 

Problem definition:
- Belief states: `2^n`, where n is the number of physical states
- Initial state: usually set of all states in P
- Actions: union of all actions (if illegal actions have no effect) or intersection of all (safer) actions
- Transition model: `b' = {s' : s' = result(s, a) and s in b}`
- Goal: all s in `b` belief state satisfy the goal test
- Path cost: assume same for all actions for simplicity

Pruning: if a belief state is solvable, its superset and subset is guaranteed to be solvable. 

Algorithms:
- All search algorithms applied to the problem expressed in belief state space 

#### Incremental belief state search 
The size of the belief state may be too large: a state needs to encode `|P|` states information.

A solution is to work on a solution for one physical state at once. Afterwards, this solution
is applied to another physical state in the belief state. If this fails, the whole process
is repeated with another solution for the first state. 

It detects failure fairly quickly. 

### With observation
The problem definition is the same as for sensorless problems, except for the transition model. The transition model has three stages:

- Prediction: `b' = PREDICT(b, a)`. This is the same transition function for sensorless problems. 
- Observation prediction (not used when executing): `POSSIBLE-PERCEPTS(b') = {o : o = PERCEPT(s) and s in b'}`
- Update: `UPDATE(b', o) = {s : o = PERCEPT(s) and s in b'}`. Set of states in `b'` that could have produced the percept `o`. 

Unlike sensorless problems, the percepts are not null and depending on the percept received, 
the output belief state is different. Thus, the solution involves **contingencies**. 

Algorithms: 
- AND-OR graph search applied to the problem expressed in belief state space

During execution, the agent needs to maintain its current belief state.

## Unknown environments 
**Online search**: interleaves computation and execution. It has to explore and then build
heuristics. 

**Competitive ratio**: ratio of path cost in online search over path cost when the space is already explored. 

**Safely explorable state space**: where some goal state is reachable from every reachable
state. No dead ends, reversible actions. 

The agent has access to:
- `ACTIONS(s)`: all legal actions from s
- Step cost function given the agent has visited the destination
- Goal test
- May have a heuristics `h(s)`

### Online Depth first search agent
It applies DFS. 

The agent maintains:
- Map `RESULT[s, a]`
- Dict `UNBACKTRACKED[s]` to parent state
- Dict `UNTRIED[s]` to untried actions (branches)

If the goal is right next to the initial state, the agent may waste a lot of time exploring
the other branch before backtracking and returning. To solve this problem, an **iterative deepening DFS** variant can be used, which is very effective for uniform trees.  

Because DFS needs to backtrack, the state space actions need to be reversible. 

### Learning real-time A* agent (LRTA*)
It applies hill climbing. 

The agent maintains:
- Map `RESULT[s, a]`
- Current best estimate `H[s]`. Initially, this is `h(s)` by **optimism under uncertainty**. 
The value gets updated after the agent moves to another state. 

The **action selection rule** and the **update rule** can be customized. 

The agent can learn general rules, such as when `UP` action is executed the y coordinate
is increased. This is covered in [chapter 18](ch18-Example-Learning/README.md).