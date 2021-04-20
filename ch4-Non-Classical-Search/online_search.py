import * from utils

class OnlineSearchProblem(Problem):
    """Deterministic and a fully observable environment."""

    def __init__(self, initial, goal, graph):
        super().__init__(initial, goal)
        self.graph = graph

    def actions(self, state):
        return self.graph.graph_dict[state].keys()

    def output(self, state, action):
        return self.graph.graph_dict[state][action]

    def h(self, state):
        """Returns least possible cost to reach a goal for the given state."""
        return self.graph.least_costs[state]

    def c(self, s, a, s1):
        """Returns a cost estimate for an agent to move from state 's' to state 's1'."""
        return 1

    def update_state(self, percept):
        raise NotImplementedError

    def goal_test(self, state):
        if state == self.goal:
            return True
        return False


class OnlineDFSAgent:
    def __init__(self, problem):
        self.problem = problem
        self.s = None
        self.a = None
        self.untried = dict()
        self.unbacktracked = dict()
        self.result = {}

    def __call__(self, percept):
        s1 = self.update_state(percept)
        if self.problem.goal_test(s1):
            self.a = None
        else:
            if s1 not in self.untried.keys():
                self.untried[s1] = self.problem.actions(s1)
            if self.s is not None:
                if s1 != self.result[(self.s, self.a)]:
                    self.result[(self.s, self.a)] = s1
                    self.unbacktracked[s1].insert(0, self.s)
            if len(self.untried[s1]) == 0:
                if len(self.unbacktracked[s1]) == 0:
                    self.a = None
                else:
                    # else a <- an action b such that result[s', b] = POP(unbacktracked[s'])
                    unbacktracked_pop = self.unbacktracked.pop(s1)
                    for (s, b) in self.result.keys():
                        if self.result[(s, b)] == unbacktracked_pop:
                            self.a = b
                            break
            else:
                self.a = self.untried.pop(s1)
        self.s = s1
        return self.a

    def update_state(self, percept):
        return percept

class LRTAStarAgent:
    def __init__(self, problem):
        self.problem = problem
        # self.result = {}      # no need as we are using problem.result
        self.H = {}
        self.s = None
        self.a = None

    def __call__(self, s1):  # as of now s1 is a state rather than a percept
        if self.problem.goal_test(s1):
            self.a = None
            return self.a
        else:
            if s1 not in self.H:
                self.H[s1] = self.problem.h(s1)
            if self.s is not None:
                # self.result[(self.s, self.a)] = s1    # no need as we are using problem.output

                # minimum cost for action b in problem.actions(s)
                self.H[self.s] = min(self.LRTA_cost(self.s, b, self.problem.output(self.s, b),
                                                    self.H) for b in self.problem.actions(self.s))

            # an action b in problem.actions(s1) that minimizes costs
            self.a = min(self.problem.actions(s1),
                         key=lambda b: self.LRTA_cost(s1, b, self.problem.output(s1, b), self.H))

            self.s = s1
            return self.a

    def LRTA_cost(self, s, a, s1, H):
        """Returns cost to move from state 's' to state 's1' plus
        estimated cost to get to goal from s1."""
        print(s, a, s1)
        if s1 is None:
            return self.problem.h(s)
        else:
            # sometimes we need to get H[s1] which we haven't yet added to H
            # to replace this try, except: we can initialize H with values from problem.h
            try:
                return self.problem.c(s, a, s1) + self.H[s1]
            except:
                return self.problem.c(s, a, s1) + self.problem.h(s1)