# Adversarial search

Game definition:
- Initial state 
- Player given state `PLAYER(s)`
- Legal actions `ACTIONS(s)`
- Transition model `RESULT(s, a)`
- Terminal test `TERMINAL-TEST(s)`
- Utility, similar to value function `UTILITY(s, p)`

Optimal solutions are expressed as a **contingent strategy**. 

## Minimax algorithm
- Recursive depth first 
- Time complexity: `O(b^m)`
- Space complexity: `O(bm)` (or `O(m)` if actions are generated one at a time)

For **zero sum two player games**, it is enough to associate each node with a single value (to be maximised or minimised). <br />
For **multiplayer games**, a vector of values is needed for each node, representing the utility from each player's viewpoint. 

Often there are more complicated behavior in game that lead to higher long term utility, 
such as alliance. 

## Alpha Beta pruning 

If the player has a better choice at the parent node of `n` or further up, it will never reach `n`. 

**Alpha**: the value of the best choice for MAX
**Beta**: the value of the best choice for MIN

Other improvements:
- Transposition table, memo map state to utility vector/value (discarding some useless states, if the state space is too large)
- Move ordering with killer move heuristics to make time complexity closed to `O(b^{m/2})` limit. Better move ordering can be informed from iterative deepening search. 

## Real time search
When it is not feasible to search the entire game tree, use a heuristic evaluation function 
and cutoff the search at non terminal states. 

### Heuristic valuation function
- **Expected value**: one way is to calculate various **features** of the state. Depending on the features, the 
states are classified in **equivalent classes**, which have probability values for a lose, win or draw. 

- **Weighted linear function**: give an approximate **material value** for each feature, then compute the weighted sum. This assumes the features influence is independent, which can be 
avoided with nonlinear combinations. The weights can be estimated by machine learning techniques. 

### Cutoff test
The cutoff test looks at the state and the depth. `CUTOFF-TEST(state, depth)`.

A simple approach is to return true when the depth is greater than some fixed depth limit or when the state is terminal. 

A more robust approach is to run iterative deepening, and cutoff when time runs out. 

**Quiescence**: states that are unlikely to exhibit wild swings in the near future. Cutoff should only happen in quiescent states, so extra **quiescence search** is needed when the player runs out of time.  

**Horizon effect**: problem that the program unnecessarily delays an unavoidable damage by 
an opponent's move. This can be mitigated with **singular extensions**, a move that is by large better than other moves. When the search reaches the depth limit, the algorithm checks if the singular extension is a legal move, it allows the move to be considered. 

## Forward pruning
Prune some moves at some node without further consideration. Note that alpha-beta pruning is 
pruning backwards. 

**Beam search**: consider only the k best moves according to the evaluation function. This is dangerous.

**Probabilistic cut algorithm**: Use statistics to estimate how likely a score of `v` at depth `d` is outside `(alpha, beta)`. If it is probably outside the window, then prune. 
[View paper](https://wiki.cs.pdx.edu/cs542-spring2013/papers/buro/probcut.pdf).

## Table lookup 
For openings, the program can rely on human expertise, eg in chess, moves within ten moves
can be informed from previously played games. 

For endgames, the computer can pregenerate a **policy** for each state. The generation involves a retrograde minimax search. 

## Stochastic games
Add a **chance node** layer along with MAX nodes and MIN nodes. It computes the expected minimax value as the weighted sum of all possible outcomes. 

To avoid sensitivity to randomness, the evaluation function must be a positive linear transformation 
of the probability of the expected utility of the position. 

**Alpha beta pruning**: in chance nodes, we need the average which requires the expectiminimax 
values of all children. However, we can arrive at bounds for the average without looking
at every node. 

### Monte Carlo simulation 
From a start position, let the computer simulate a lot of games with random dice. Then approximate the value of the node positions. 

## Partially observable games
### Deterministic
Example game is Kriegspiel.

AND-OR graph search with belief states to find guaranteed checkmates. 

**Probabilistic checkmates**. 

### Stochastic
Example games are card games.

- Consider all possible deals, solve each deal as if it were a fully observable game. 

```
argmax_a Summation_s P(s) * MINIMAX(RESULT(s, a))
```

- If too many deals, we can resort to Monte Carlo simulation with a random sample of N deals,
where the probability of deal s appearing in the sample is proportional to `P(s)`. 
