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
# Successor function (no actions needed, because we can directly get the successors)
problem.successors(state: State) -> list(State)
```

Defines goal and performance measures
- Goal test
- Path cost (sum of step costs)

```Python
problem.goal_test(state: State) -> bool # or check full environment
problem.step_cost(currstate: State, action: Action, nextstate: State) -> int
```

##### Examples of problems

- Vacuum world
- 8-puzzle -> a sliding-block puzzle (NP complete)
- 8-queens incremental formulation
- 8-queens complete-state formulation 
- Route finding problems
- Touring problems
- VLSI layout problems
- Robot navigation 
- Automatic assembly sequencing 
- Protein design 

#### Search algorithms 

Infrastructure of search:
- Tree search or graph search 
- Node
- Queue

##### Uninformed strategies 

1. Breadth first search 
2. Uniform cost search 
3. Depth first search (similar, depth limited search)
4. Iterative deepening search 
5. Bidirectional search 

##### Informed strategies 

1. Best first search 
2. Greedy best first search 
3. A* search 
4. Recursive best first search 
5. Simplified memory bounded A*

*Heuristics can be obtained via relaxation, precomputing patterns, or learning from experience (neural nets, decision trees, reinforcement learning).*