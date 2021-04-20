import * from utils


# Undeterministic env

# Recursive DFS and or graph search
def and_or_graph_search(problem):
    def or_search(state, problem, path):
        if problem.goal_test(state):
            return []
        if state in path:
            return None 
        for action in problem.actions(state):
            plan = and_search(problem.result(state, action), problem, path+[state,])
            if plan is not None:
                return [action, plan]

    def and_search(states, problem, path):
        plan = {}
        for s in states:
            plan[s] = or_search(s, problem, path)
            if plan[s] is None:
                return None 
        return plan
    
    return or_search(problem.initial, problem, [])

# TODO: best first and or graph search

# TODO: belief state problem for sensorless with pruning 

# TODO: belief state and or graph for partial observation env 