# Constraint Satisfaction problems

Unlike searching algorithms, CSP search algorithms use a **factored representation** over **atomic representation**. It enables to use *general-purpose domain independent heuristics* rather than *problem-specific* heuristics. 

CSP definition: 
- Set of variables **X**
- Set of domains **D**, each domain is a set of allowable values for a specific variable 
- Set of constraints **C**, each constraint is a tuple `tuple(scope, relation)` 

**Scope of constraint**: tuple of variables that participate in the constraint. <br />
**Relation of constraint**: list of all tuples of values that satisfy the constraint. Can also be a function, such as the precedence constraint `T1 + d1 <= T2`, disjunctive constraint `C1 or C2`... <br />
**Consistent assignment**: no constraint violations. <br />
**Complete assignment**: all variables are assigned. <br />

Types of variables:
- With discrete finite domains
- With discrete infinite domains
    - Constraints described with a constraint language 
    - There are general algorithms to solve CSP with **linear constraints** on integer variables
    - No general algorithms to solve **nonlinear constraints** on integer variables
- With continuous domains: **linear programming**, **quadratic programming**, ...

Types of constraints:
- **n-ary constraint**: n is the number of variables of the `scope` tuple. 
- **Global constraint**: n is an arbitrary number of variables, eg. `Alldiff`. 
- **Preference constraint**: unlike absolute constraints, CSP with preferences can be solved with optimization search methods as a **constraint optimization problem**, eg. linear programming. 

**Constraint graph**: graph that connects variables as nodes with constraints as edges. Only for CSPs with only binary constraints.  <br />
**Constraint hypergraph**: variables are nodes (circles) and constraints are hypernodes (squares). <br />

**Theorem**: Every finite domain constraint can be reduced to a set of binary constraints. This can be done with **dual graph transformation**:
```
Original CSP:
Variables: x, y, z
Domains: [1,2,3], [1,2,3], [1,2,3]
Constraints: 
1. x + y = z   => <x,y,z>, {(1,2,3), (2,1,3), (1,1,2)}
2. x < y       => <x,y>, {(1,2), (1,3), (2,3)}
---
Dual graph:
Variables: 
1. c1 represents constraint 1
2. c2 
Domains: 
1. dom(c1) = {(1,2,3), (2,1,3), (1,1,2)}
2. dom(c2) = {(1,2), (1,3), (2,3)}
Constraints (one for each pair of original constraints that share variables):
1. <c1, c2>, c1.x = c2.x and c1.y = c2.y  
```

*Note*: KCL INT module defines *n-ary CSP* as that the CSP has n different domains. 

## Constraint propagation
It is a type of **inference**. Inference can be used as a preprocessing step for search, intertwined with search or maybe solve the CSP without search. The idea is to enforce **local consistency**. Depending on the number of variables involved, there are different types:

### Node consistency
Ensure all values in the variable's domain satisfy the unary constraints. 

Algorithm: remove the unary constraints and modify the domains accordingly. 

## Arc consistency 
Ensure any variable `Xi` is arc-consistent with every other variable `Xj`. Here we assume a CSP with only binary constraints. 

`Xi` is arc-consistent with `Xj` if for every value in `Di` there is some value in `Dj` that satisfy the binary constraint on arc `(Xi, Xj)`. 

Algorithm: AC-3.

Procedure:
- Queue (a set really) to store arcs (constraints)
- Pop an arc `(Xi, Xj)` from the queue
- For each value in domain `Di = dom(Xi)`:
    - If there exists a value in `Dj = dom(Xj)` that satisfies the constraint `<Xi, Xj>`, then continue
    - Else remove the value from `Di` and enqueue all arcs `{(Xk, Xi) | k in 1..n and k != i} `
 
Complexity: `O(cd^3)`

*Note*: for hyperarc consistency, `Xi` is generalized arc consistent with respect to n-ary constraint if for every value in the domain `Di` there exists a tuple of values that is a member of the constraint. 

## Path consistency 
Ensure any set of 2 variables `{Xi, Xj}` is path-consistent with every other variable. 

`{Xi, Xj}` is path-consistent with `Xm` if for every assignment `{Xi=a, Xj=b}` there exists an assignment to `Xm` that satisfies the constraints `<Xi, Xm>` and `<Xj, Xm>`. 

Algorithm: PC-2

Procedure: similar to AC-3. 

Complexity: `O()`

## K-consistency 
A CSP is k-consistent if for any set of consistent k-1 variables, there exists a consistent value for any kth variable. 

A **strongly k-consistent** CSP is (1..k) consistent. If `k = n`, and the CSP is strongly k-consistent, we are guaranteed to find the solution in `O(d*n^2)`. But enforcing strong consistency for higher order requires time and space exponencial to `k`, which makes it unfeasible for higher `k`. 

## Global constraints 
Alldiff algorithm:
1. Find variable with singleton domain, if not found then terminate
2. Remove the value in singleton domain from all other domains 
3. If there is an empty domain, return failure
4. Repeat 

Atmost (resource constraint):
1. Check the sum of minimum value of each domain `Dx`. 
2. If this sum > limit, return failure
3. Else enforce consistency by deleting values `v` from domains such that `v + min(D1) + min(D2) + ... (except the domain of v) + min(Dn) > limit`. 

Atmost (continuous bounded resource constraint):
For every variable X, and for both lower and upper bound, there exists a value in `dom(Y)` for every Y. 

## Backtracking search 
Backtracking search deals with partial assignments until a complete assignment is found. It is based on depth first search. 

**Commutativity** is an important property of CSPs such that the order of application of a set of actions (in this case assignments) has no effect on the outcome. For each layer of CSP, the solver can focus on only one variable.  

Performance can be tweaked in the following areas:
1. Variable ordering 
2. Value ordering
3. Inference at each step of the search 
4. Backjumping 

### Variable ordering
**Minimum remaining values heuristic (MRV)** (or most constrained): variable with fewest legal values in domain.

To break a tie, 

**Degree heuristic**: variable involved in the largest number of constraints on other unassigned variables (unassigned!). 

### Value ordering
**Least-constraining-value heuristic (LCV)**: value that rules out the fewest choices for other variables. 

### Inference during search 
AC-3 and other local consistency algorithms are applied before the search starts. But during search, 

#### Forward checking 
When `X` gets assigned, for each unassigned variable, remove from its domain the values that are not arc-consistent with `X`.  

Forward checking works better with MRV heuristic. 

*Note*: when the domain of `Y` is changed, the arc consistency of all other variables with respect to `Y` is NOT revised. 

#### Maintaining Arc Consistency (MAC)
Run AC-3 but with initial queue with only the arcs `(Xj, Xi)` where `Xi` is just assigned and `Xj` is any unassigned variable. 

### Backjumping 

**Conflict set**: set of assignments that is inconsistent. These assignments are responsible for emptying the domain of a variable. 
For each variable, keep a set. Add assignment `X=x` to conflict set of `Y` whenever this assignments causes a reduction of the domain of `Y`. If the domain of `Y` turns empty, add the conflict set of `Y` to `X`.

**Conflict directed backjumping**: use the standard conflict sets (easily computed with forward checking). Backjump to the most recent assignment in the current conflict set. Update the conflict set of the current variable by adding the previous conflict set. 

```
conf(Xi) <-- conf(Xi) union conf(Xj) - {Xi}
```

**Constraint learning and no-good cache**: learn the minimum set of variables in the conflict set that causes the problem. A no-good cache is an important technique in modern CSP solvers. 

## Local search 
Local search starts with a complete assignment. It is feasible for online agents. 

`MIN-CONFLICTS` algorithm: select a random variable and assign a value that minimizes the number of violated constraints. 

Plateaux can be avoided with sideways moves and **tabu search**, which stores a small list of recently visited states and forbids the algorithm to return to those states. 

**Constraint weighting**: each constraint has weight 1. After each move, add 1 to the still conflicted constraints. This adds topology to the plateaux and concentrates the search to difficult constraints.  

## CSP complexity and problem decomposition

**Connected components** of the constraint graph can be solved as independent subproblems. The complexity converts `O(d^n)` to `O(n/c * d^c)`. 

**Tree-structured** problems can be solved in linear time. By definition, any two variables are connected by only one path. The algorithm applies topological sorting and makes the graph **directed arc-consistent** in `O(nd^2)`. This means we don't have to backtrack.  

There are two approaches to convert a CSP into a tree-structured CSP.

### Cutset conditioning 
1. Find the smallest cycle cutset S. The constraint graph minus the cycle cutset is a tree. 
2. For each assignment to S, revise the domains for other variables and solve the tree CSP. 

Finding the smallest cycle cutset is NP-hard. 
The time complexity of the decomposed problem is `O(d^c * (n-c) * d^2)`

### Tree decomposition 
Decompose into independent subproblems. Each subproblem is a node of a megavariable. 
**Tree width** is one less than the size of the largest subproblem. 
After decomposition, the time complexity is `O(n * d ^{w+1})`, where `w` is the tree width. 
Finding the decomposition of a minimal tree width is NP-hard. 

### Value symmetry

Another performance tweak is to break value symmetry by adding a symmetry-breaking constraint. For example, this could be an arbitrary ordering constraint `A < B < C` such that permutations are not possible. 