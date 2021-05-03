from utils import * 
from sortedcontainers import SortedSet 
from collections import defaultdict, Counter 

# CSP
class CSP(Problem):
    def __init__(self, variables, domains, neighbors, constraints):
        super().__init__(())
        variables = variables or list(domains.keys())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints 
        self.curr_domains = None 
        self.pruned_pairs = self._construct_pruned_pairs()

    def _construct_pruned_pairs(self):
        return {var1: {val1: {var2: set() for var2 in self.neighbors[var1]} for val1 in self.domains[var1]} for var1 in self.variables}
    
    def assign(self, var, val, assignment):
        assignment[var] = val 

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]

    def nconflicts(self, var, val, assignment):
        # the efficiency can be improved 
        def conflict(var2):
            return var2 in assignment and not self.constraints(var, val, var2, assignment[var2])
        return count(conflict(v) for v in self.neighbors[var])

    # for search algorithms 
    def actions(self, state):
        if len(state) == len(self.variables):
            return []
        else:
            assignment = dict(state)
            var = first([v for v in self.variables if v not in assignment])
            return [(var, val) for val in self.domains[var]
                    if self.nconflicts(var, val, assignment) == 0]

    def result(self, state, action):
        (var, val) = action 
        return state + ((var, val),)

    def goal_test(self, state):
        assignment = dict(state)
        # assigned and no conflicts
        return (len(assignment) == len(self.variables) 
                and all(self.nconflicts(var, assignment[var], assignment) == 0
                        for var in self.variables))

    # for constraint propagation 
    def support_pruning(self):
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, val):
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != val]
        self.curr_domains[var] = [val]
        return removals 

    def prune(self, var, val, removals):
        self.curr_domains[var].remove(val)
        if removals is not None:
            removals.append((var, val))

    def prune_pair(self, var1, val1, var2, val2, removals):
        self.pruned_pairs[var1][val1][var2].add(val2)
        self.pruned_pairs[var2][val2][var1].add(val1)

    def choices(self, var):
        return (self.curr_domains or self.domains)[var]

    def infer_assignment(self):
        """Return assignment for those variables with only one value in curr_domain"""
        self.support_pruning()
        return {v: self.curr_domains[v][0]
                for v in self.variables if 1 == len(self.curr_domains[v])}

    def restore(self, removals):
        for B, b in removals:
            self.curr_domains[B].append(b)

    # for min-conflicts local search
    def conflicted_vars(self, current):
        return [var for var in self.variables
                if self.nconflicts(var, current[var], current) > 0]

# Node consistency
def node_consistency(csp: CSP, removals=None):
    csp.support_pruning()
    for var in csp.variables:
        conflicting_domain = filter(lambda val: csp.nconflicts(var, val, {}) > 0, csp.curr_domains[var])
        if len(conflicting_domain) == len(csp.curr_domains):
            return False 
        for c in conflicting_domain:
            csp.prune(var, c, removals)
    assignment = csp.infer_assignment()
    # assign 
    for var in assignment.keys():
        removals.update(csp.suppose(var, assignment[var]))
    return True 

# AC3
def AC3(csp: CSP, queue=None, removals=None, arc_heuristic=dom_j_up):
    if queue is None:
        queue = {(Xi, Xj) for Xi in csp.variables for Xj in csp.neighbors[Xi]}
    csp.support_pruning()
    queue = arc_heuristic(csp, queue)
    checks = 0
    while queue:
        (Xi, Xj) = queue.pop()
        revised, checks = revise(csp, Xi, Xj, removals, checks)
        if revised:
            if not csp.curr_domains[Xi]:
                return False, checks 
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True, checks 

# Used in forward checking as well as AC3
def revise(csp: CSP, Xi, Xj, removals, checks=0):
    revised = False 
    for x in csp.curr_domains[Xi]:
        conflict = True 
        for y in csp.curr_domains[Xj]:
            if csp.constraints(Xi, x, Xj, y) and y not in csp.pruned_pairs[Xi][x][Xj]:
                conflict = False 
            checks += 1 
            if not conflict:
                break 
        if conflict:
            csp.prune(Xi, x, removals)
            revised = True 
    return revised, checks 

# Order the arcs (Xi, Xj) with len(dom(Xj)) greatest first
def dom_j_up(csp, queue):
    return SortedSet(queue, key=lambda arc: neg(len(csp.curr_domains[arc[-1]])))

# AC3b, improved with double-support domain-heuristic 
# See paper: http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.25.9439
def AC3b(csp: CSP, queue=None, removals=None, arc_heuristic=dom_j_up):
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    csp.support_pruning()
    queue = arc_heuristic(csp, queue)
    while queue:
        (Xi, Xj) = queue.pop()
        Si_p, Sj_p, Sj_u = partition(csp, Xi, Xj)
        # if there are no supported vi, conflict 
        if not Si_p:
            return False 
        # either need to revise all other domains 
        revised = False 
        for x in set(csp.curr_domains[Xi]) - Si_p:
            csp.prune(Xi, x, removals)
            revised = True 
        if revised:
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
        # double support
        if (Xj, Xi) in queue:
            if isinstance(queue, set):
                queue.difference_update({(Xj, Xi)})
            else:
                queue.difference_update((Xj, Xi))
            for vj_p in Sj_u:
                for vi_p in Si_p:
                    conflict = True
                    if csp.constraints(Xj, xj_p, Xi, vi_p):
                        conflict = False 
                        Sj_p.add(vj_p)
                    if not conflict:
                        break 
            revised = False 
            for x in set(csp.curr_domains[Xj]) - Sj_p:
                csp.prune(Xj, x, removals)
                revised = True 
            if revised:
                for Xk in csp.neighbors[Xj]:
                    if Xk != Xi:
                        queue.add((Xk, Xj))
    return True 

def partition(csp: CSP, Xi, Xj):
    """Return Si_p, Sj_p, Sj_u - Sj_p. Subscript p means supported, subscript u means unknown."""
    Si_p = set()
    Sj_p = set()
    Sj_u = set(csp.curr_domains[Xj])
    for vi_u in csp.curr_domains[Xi]:
        conflict = True 
        # find a vj, better not supported, so that both (i, j) and (j, i) are checked (double-support) 
        for vj_u in Sj_u - Sj_p:
            if csp.constraints(Xi, vi_u, Xj, vj_u):
                conflict = False 
                Si_p.add(vi_u)  # mark as supported with respect to Xj
                Sj_p.add(vj_u)
            if not conflict:
                break 
        # if cannot find a vj which is not supported (not in Sj_p)
        if conflicts:
            for vj_p in Sj_p:
                # single-support check 
                if csp.constraints(Xi, vi_u, Xj, vj_u):
                    conflict = False 
                    Si_p.add(vi_u)
                if not conflict:
                    break 
    return Si_p, Sj_p, Sj_u - Sj_p 

# AC4
def AC4(csp: CSP, queue=None, removals=None, arc_heuristic=dom_j_up):
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk for csp.neighbors[Xi]}
    csp.support_pruning()
    queue = arc_heuristic(csp, queue)
    # auxiliary variables to find which variables to prune when a domain is changed
    support_counter = Counter()
    supported = defaultdict(set)
    unsupported = []
    while queue:
        Xi, Xj = queue.pop()
        revised = False 
        for x in csp.curr_domains[Xi]:
            for y in csp.curr_domains[Xj]:
                if csp.constraints(Xi, x, Xj, y):
                    support_counter[(Xi, x, Xj)] += 1
                    supported[(Xj, y)].add((Xi, x))
            if support_counter[(Xi, x, Xj)] == 0:
                csp.prune(Xi, x, removals)
                revised = True 
                unsupported.append((Xi, x))
        if revised:
            if not csp.curr_domains[Xi]:
                return False
    # core logic: only insert pairs that are needed 
    while unsupported:
        Xj, y = unsupported.pop()
        for Xi, x in supported[(Xj, y)]:
            revised = False 
            if x in csp.curr_domains[Xi]:
                support_counter[(Xi, x, Xj)] -= 1
                if support_counter[(Xi, x, Xj)] == 0:
                    csp.prune(Xi, x, removals)
                    revised = True
                    unsupported.append((Xi, x))
            if revised:
                if not csp.curr_domains[Xi]:
                    return False
    return True 



# PC2
def PC2(csp: CSP, queue=None, removals=None, arc_heuristic=dom_j_up):
    if queue is None:
        for var1 in csp.variables:
            for var2 in csp.neighbors[var1]:
                queue = {(var1, var2, var3) for var3 in csp.variables if var1 != var3 and var2 != var3}
    csp.support_pruning()
    while queue:
        var1, var2, var3 = queue.pop()
        if revise3(csp, var1, var2, var3, removals):
            for Xk in set(csp.variables) - {var1, var2}:
                queue.add((Xk, var1, var2))
                queue.add((Xk, var2, var1))
            # revise arc consistency 
            revised = revise(csp, var1, var2) or revise(csp, var2, var1)
            # determine if invalid return False
            if len(csp.domains[var1]) == 0 or len(csp.domains[var2]) == 0:
                return False
    return True 


def revise3(csp: CSP, Xi, Xj, Xk, removals):
    revised = False 
    for vi in csp.curr_domains[Xi]:
        for vj in csp.curr_domains[Xj]:
            if not csp.constraints(Xi, vi, Xj, vj) or vj in csp.pruned_pairs[Xi][vi][Xj]:
                continue 
            conflict = True 
            # for each valid pair (Xi, Xj)
            for vk in csp.curr_domains[Xk]:
                if csp.constraints(Xi, vi, Xk, vk) and csp.constraints(Xj, vj, Xk, vk):
                    conflict = False 
                    break 
            if conflict:
                csp.prune_pair(Xi, vi, Xj, vj, removals)
                revised = True 
    return revised 

# Alldiff constraint propagation 

# Atmost constraint propagation

# Bounds propagation 

# Variable ordering
def mrv(csp: CSP, assignment):
    return argmin_random_tie([v for v in csp.variables if v not in assignment],
                                key=lambda var: remaining_values(csp, var, assignment))

def remaining_values(csp: CSP, var, assignment):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        return count(csp.nconflicts(var, val, assignment) == 0 for val in csp.domains[var])

# Value ordering 
def lcv(csp: CSP, var, assignment):
    return sorted(csp.choices(var), key=lambda val: csp.nconflicts(var, val, assignment))

# Inference 
def forward_checking(csp: CSP, var, val, assignment, removals=None):
    csp.support_pruning()
    queue = [var2 for var2 in csp.neighbors[var] if var2 not in assignment]
    for var2 in queue:
        for val2 in csp.curr_domains[var2]:
            if not csp.constraints(var, val, var2, val2):
                csp.prune(var2, val2, removals)
        if not csp.curr_domains[var2]:
            return False
    return True 

def mac(csp: CSP, var, val, assignment, removals, constraint_propagation=AC3b):
    return constraint_propagation(csp, {(Xi, var) for Xi in csp.neighbors[var]}, removals)

# CSP solver with backtracking 
def backtracking_search(csp: CSP, select_variable=mrv, order_domain_values=lcv, inference=forward_checking):
    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_variable(csp, assignment)
        for val in order_domain_values(csp, var, assignment):
            if csp.nconflicts(var, val, assignment) == 0:
                csp.assign(var, val, assignment)
                removals = csp.suppose(var, val)
                if inference(csp, var, val, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result 
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None 
        
    result = backtrack({})
    return result

# CSP with conflict directed backjumping 

# CSP solver with min conflicts 
def min_conflicts(csp: CSP, limit=100):
    csp.current = current = {}  # assignment 
    for var in csp.variables:
        val = min_conflicts_val(csp, var, current)
        csp.assign(var, val, current)
    for i in range(limit):
        conflicted = csp.conflicted_vars(current)
        if not conflicted:
            return current 
        var = random.choice(conflicted)
        val = min_conflicts_val(csp, var, current)
        csp.assign(var, val, current)
    return {}

def min_conflicts_val(csp: CSP, var, assignment):
    return argmin_random_tie(csp.domains[var], key=lambda val: csp.nconflicts(var, val, assignment))

# CSP tree solver
def csp_tree_solver(csp: CSP):
    assignment = {}
    # check is tree 
    # topological sort
    # enforce consistency for each edge 
    # fill the assignment  
    return assignment 

# Cutset conditioning 

# Tree decomposition 

