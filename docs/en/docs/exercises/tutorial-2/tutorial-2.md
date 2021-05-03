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

- For scope $(F, E)$: $\{(autonomous, human-op), (human-op, autonomous)\}$
- For scope $(F, A)$: $\{(autonomous, human-op), (human-op, autonomous)\}$
- For scope $(F, D)$: $\{(autonomous, human-op), (human-op, autonomous)\}$
- For scope $(E, A)$: $\{(autonomous, human-op), (human-op, autonomous)\}$
- For scope $(E, D)$: $\{(autonomous, human-op), (human-op, autonomous)\}$
- For scope $(A, D)$: $\{(autonomous, human-op), (human-op, autonomous)\}$

The constraint $C2$ implies a unary relation: 

- For scope $(F)$: $\{(autonomous)\}$

## Question f
**Question**: Step through the process of maintaining arc consistency of your model by applying the $REVISE$ algorithm (in both directions) to the variables $E$ and $A$. Given the binary relation between them that you have constructed, are any values pruned from either domain?

**Answer**: 

Steps:

1. `REVISE(csp, var=E)`

2. `REVISE(csp, var=A)`

Solution:

- $F = autonomous$, $E = human-op$, $A = human-op$
