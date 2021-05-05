# Tutorial 2 ─ Constraint Satisfaction Problems 

## Background information

There are four robots in a room: Felix (**F**), Emax (**E**), Alpha (**A**) and Dixar (**D**). Each robot is either **autonomous** or **human-operated**. We are given the following two facts:

- Given any two of the robots, **at least one of the two is human-op**. 
- Robot **F is autonomous**.

The objective of the puzzle is to determine from these two facts **how many of the robots are human-operated and how many of them are autonomous**.

## Question a

**Question**: What are the variables of the puzzle?

**Answer**:

Variables: *F*, *E*, *A*, *D*. 

Each variable represents a robot. 

## Question b

**Question**: What are the domains of the variables?

**Answer**: 

Domains: $\{autonomous, human-op\}$, $\{autonomous, human-op\}$, $\{autonomous, human-op\}$, $\{autonomous, human-op\}$

Each variable has the same domain $\{autonomous, human-op\}$. 

## Question c

**Question**: How do you write the constraint that robot F is autonomous?

**Answer**: Constraint is expressed as a tuple $<scope, relation>$. A relation can be expressed as a set of tuples. Therefore, the constraint is $<\{F\}, \{(autonomous)\}>$.

## Question d

**Question**: Write down a set of constraints, in propositional logic, that fully describes the puzzle. 

**Answer**: 

We define one propositional variable for each CSP variable. Because the domains for each of the CSP variables only have two elements, we can define the negation of the propositional variable as the other domain element. For example, 

$f$ represents $F = autonomous$. <br />
$\neg f$ represents $F = human-op$.

- At least one of any two robots is human operated. 

To express this constraint, enumerate all the combinations of two. Then assert that any of these combinations should have one negated literal. There are $6$ combinations.

$C1 = (\lnot f \lor \neg e) \land (\lnot f \lor \neg a) \land (\lnot f \lor \neg d) \land (\lnot e \lor \neg a) \land (\lnot e \lor \neg d) \land (\lnot a \lor \neg d)$

- F is autonomous

$C2 = f$

Then, combine the two constraints with a conjunction.

$C1 \land C2$

## Question e
**Question**: Write down the binary relations implied by the constraints from (d), as explicit set of pairs. Are there any non-binary relations in the problem? If so, which one?

**Answer**:

The constraint $C1$ expressed as binary relations:

- For scope $(F, E)$: $\{(autonomous, human-op), (human-op, autonomous), (human-op, human-op)\}$
- For scope $(F, A)$: $\{(autonomous, human-op), (human-op, autonomous), (human-op, human-op)\}$
- For scope $(F, D)$: $\{(autonomous, human-op), (human-op, autonomous), (human-op, human-op)\}$
- For scope $(E, A)$: $\{(autonomous, human-op), (human-op, autonomous), (human-op, human-op)\}$
- For scope $(E, D)$: $\{(autonomous, human-op), (human-op, autonomous), (human-op, human-op)\}$
- For scope $(A, D)$: $\{(autonomous, human-op), (human-op, autonomous), (human-op, human-op)\}$

The constraint $C2$ implies a unary relation: 

- For scope $(F)$: $\{(autonomous)\}$

Therefore, by combining the two constraints:

- For scope $(F, E)$: $\{(autonomous, human-op)\}$
- For scope $(F, A)$: $\{(autonomous, human-op)\}$
- For scope $(F, D)$: $\{(autonomous, human-op)\}$
- For scope $(E, A)$: $\{(autonomous, human-op), (human-op, autonomous), (human-op, human-op)\}$
- For scope $(E, D)$: $\{(autonomous, human-op), (human-op, autonomous), (human-op, human-op)\}$
- For scope $(A, D)$: $\{(autonomous, human-op), (human-op, autonomous), (human-op, human-op)\}$

## Question f
**Question**: Step through the process of maintaining arc consistency of your model by applying the $REVISE$ algorithm (in both directions) to the variables $E$ and $A$. Given the binary relation between them that you have constructed, are any values pruned from either domain?

**Answer**: 

Steps:

1. `REVISE(csp, E, A)`
    1. For $E = autonomous$:
        1. A valid assignment to $A$ is $A = human-op$, so $autonomous$ is not pruned from $dom(E)$
    2. For $E = human-op$:
        1. A valid assignment to $A$ is $A = human-op$ or $A = autonomous$, so $human-op$ is not pruned from $dom(E)$
1. `REVISE(csp, A, E)`
    1. For $A = autonomous$:
        1. A valid assignment to $E$ is $E = human-op$, so $autonomous$ is not pruned from $dom(A)$
    2. For $A = human-op$:
        1. A valid assignment to $E$ is $E = human-op$ or $E = autonomous$, so $human-op$ is not pruned from $dom(A)$

By revising the arc consistency of $(E, A)$ and $(A, E)$ no values are pruned. If we revise all the variables against $F$:

1. `REVISE(csp, E, F)`
    1. For $E = autonomous$:
        1. Given C1, $F = autonomous$, so there are no matching pairs in the binary relation. $autonomous$ is pruned from $dom(E)$
    2. For $E = human-op$:
        1. A valid assignment to $F$ is $F = autonomous$, so $human-op$ is not pruned from $dom(E)$

After which $dom(E) = \{human-op\}$.

The same process is applied for other variables:

2. `REVISE(csp, A, F)` $\to dom(A) = \{human-op\}$
3. `REVISE(csp, D, F)` $\to dom(D) = \{human-op\}$


Solution:

- $F = autonomous$, $E = human-op$, $A = human-op$, $D = human-op$
