## Reinforcement learning

Objective: learn the optimal policy from observed rewards without knowledge of full model environment and the reward function. 

**Agent designs**: 
| Agent design | Choose action based on... | Note |
| -- | -- | -- |
| Utility-based agent (not really RL) | Utility of states | MUST know the states to which its actions will lead. |
| Q-learning agent | Action utility | Don't need to know the outcome of the actions, so cannot look ahead. | 
| Reflex agent | Policy (state->action) | |

### Passive RL

The policy `pi` is fixed. The goal is to learn the `U^pi` function through many trials, much like policy evaluation, but without knowing the transition model `P(s'|s,a)` nor the reward function `R(s)`. 

#### Direct utility estimation
Utility of a state `U^pi(s)` is `E[reward-to-go from s]`, where reward-to-go is the reward from that state onwards. Therefore, the problem is reduced to supervised learning inductive learning. 

However, many functions violate the Bellman equations, because it does not consider the expected utility of a state's successor states. Thus often converges very slowly. 

#### Adaptive dynamic programming
Learn the transition model `P(s'|s,pi(s))` and the reward function `R(s)`, and solve the MDP (fit the Bellman equations) via DP.

To **learn the transition model**, it can be viewed as a supervised learning problem of getting `s'` from known `s` and `a`, or as a probability table which is updated in each trial. 

To **solve the MDP** in a set of continually changing and probabilistic transition models, we can use **modified policy iteration**. It solves the `|S|` Bellman equations with `|S|` unknowns, but it also uses a simplified **value iteration algorithm** to update the `U(s)` after each change to the learnt transition model. Because the model changes slightly, the `U(s)` converges quickly. However, it is intractable for large state spaces (usual issue for DP). 

To **choose a policy** based on a single estimated model may teach to erroneous things, instead:
1. Bayesian reinforcement learning: choose a policy that works well on range of models which have a reasonable chance of being the true model. 

`pi* = argmax_{pi}(summation_{h}(P(h|e)*u(pi, h)))`,

where `u(pi, h)` is the `E[U(s)]` averaged over all `s`. 

2. Robust control theory: choose the policy that gives the best outcome in the worst case over the set of all transition models `H`.

`pi* = argmax_{pi}(min_{h}(u(pi, h)))`

Often the models considered to be in `H` should have `P(h|e)` exceed some likelihood threshold. 

#### Temporal-difference learning
Unlike ADP, this is a model-free approach. It is not required to learn the transition model `P(s'|s,a)`. Instead, the `U^{pi}(s)` is updated when a transition occurs from `s` to `s'`. While ADP adjusts the `U^{pi}(s)` with all its successor states, TD adjusts it with that of a single successor state `s'`. It is slower in convergence than ADP but requires fewer computation resources, as TD does not have to maintain the consistency with the model `P` after every move.

`U^{pi}(s) = U^{pi}(s) + alpha * (R(s) + gamma * U^{pi}(s') - U^{pi}(s))`,

where `alpha` is the learning rate and `gamma` is the discount factor. The `alpha` can be a constant but can also be a function `alpha(s)` that decreases as the number of times `s` is visited increases, to ensure convergence. 

#### ADP and TD: Prioritized sweeping

ADP inefficiency lays in the fact that it has to adjust **all states** after any change in the model `P`, when any transition happens. We can use **prioritized sweeping heuristic** to choose to make adjustments to states whose likely successors (according to `P`) have just undergone a *large* adjustment. As the `P` becomes more accurate, one could choose to decrease the minimum adjustment size that triggers the sweep. 

### Active RL
The agent needs to decide which action to take (policy) as well as learn the `U^pi`. 

#### Greedy agent
Learn the model `P` and compute the optimal policy with `passive ADP`. Pure exploitation. 
This seldom converges to the optimal policy in the long term, because it "stopped learning". 

Therefore, we need an exploration policy (bandit problem). 

#### ADP with exploration function
Value iteration with an ADP agent, changing the update function to use an optimistic estimate of the `U`, `U+`. The exploration function `f(u, n)` where `u` is the utility estimate and `n` is the number of times the state-action has been visited. The `f(u, n)` should be decreasing in `n` and increasing in `u`. It converges quickly towards optimal performance. 

`U+(s) = R(s) + gamma * max_{a}(f(summation_{s'}(P(s'|s,a) * U+(s')), N(s, a)))`

An example of `f(u, n)` is:

```Haskell
f(u, n) = 
    | n < Ne = R+
    | otherwise = u
```

where `Ne` is a constant and `R+` is the optimistic estimate of the best possible estimate obtainable in any state. 

#### Q-Learning 
TD method but using Q-values instead of utility values. Because of the relationship between `U(s)` and `Q(s,a)`:

```
U(s) = max_{a}(Q(s, a))  # U of a state is the utility of choosing the best action in that state
```

The update function is (identical to TD):

```
Q(s,a) = Q(s,a) + alpha * (R(s) + gamma * max_{a'}(Q(s', a')) - Q(s, a))
```

The next action can be chosen using the exploration function: 
```
a_next = argmax_{a'}(f(Q(s', a'), N(s', a')))
```

A close relative of Q-learning is SARSA.

These converge more slowly than ADP. 

### Generalization in RL




