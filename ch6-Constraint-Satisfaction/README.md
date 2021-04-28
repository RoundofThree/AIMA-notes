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
**Constraint graph**: graph that connects variables as nodes with constraints as edges. <br />


**n-ary CSP**: 