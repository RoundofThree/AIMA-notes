# Tutorial 3 ─ Classical Planning

## Towers of Hanoi

- Three pegs: left, centre, right
- Three discs: small, medium, large

The objective is:

- Move discs between pegs one at a time. 
- Must reach peg on right hand side. 
- Ensure no disc is ever atop a smaller disc. 

## Exercise 1

**Question**: Write a PDDL domain for this problem. 

**Answer**:

```pddl
(define (domain hanoi)

(:requirements :strips)

(:predicates 
    (on ?x ?y)  ; x and y can be disc or peg 
    (clear ?x) ; x can be disc or peg
    (smaller ?x ?y) ; x and y can be disc or peg 
    (disc ?x)  ; whether x is a disc 
)

(:action move
    :parameters (?disc ?from ?to)
    :precondition (and 
        (clear ?disc) 
        (clear ?to) 
        (disc ?disc) 
        (smaller ?disc ?to) 
        (on ?disc ?from)
    )
    :effect  (and 
        (on ?disc ?to) 
        (not (on ?disc ?from)) 
        (clear ?from) 
        (not (clear ?to))
    )
)

)
```

## Exercise 2

**Question**: Write the initial and goal state of the PDDL problem. 

**Answer**:

```pddl
(define (problem tutorial_problem) (:domain hanoi)
(:objects small medium large left centre right)

(:init
    (on small medium) (on medium large) (on large left)
    (clear small) (clear centre) (clear right) 
    (disc small) (disc medium) (disc large)
    (smaller small medium) (smaller small large) 
    ; pegs are infinitely large, larger than any disc
    (smaller small left) (smaller small centre) (smaller small right)
    (smaller medium large) (smaller medium left) (smaller medium centre) (smaller medium right)
    (smaller large left) (smaller large centre) (smaller large right)
)

(:goal (and 
    (on small medium) 
    (on medium large) 
    (on large right)
))

)
```
