import sys

trail = {}
literal_list = {}
def parse_dimacs(filename):
    clauses = []
    with open(filename, 'r') as input_file:
        for line in input_file:
            if line[0] in ['c', 'p']:
                continue
            literals = list(map(int, line.split()))
            assert literals[-1] == 0
            literals = literals[:-1]
            clauses.append(literals)
    return clauses

def literal_values(CNF_Formula):
    temp_dict = {}
    for clause in CNF_Formula:
        for literal in clause:
            if abs(literal) not in temp_dict.keys():
                temp_dict[abs(literal)] = None

    # sort the literal_values
    for i in sorted(temp_dict.keys()):
        literal_list[i] = temp_dict[i]

def DPLL(CNF_Formula):
    trail.clear()
    if not BCP():
        return "UNSAT"
    while True:
        if not decide():
            return "SAT"                                                                                                                                                                                                                                                                                                                                                                                                                                          n                                                                                                                                                
        while not BCP():
            if not backtrack():
                return "UNSAT"

def BCP():
    return False

def decide():
    # If all variables are assigned then return false
    if None not in literal_list.values():
        return False

    # Otherwise choose the unassigned variables e.g x
    # choose value v ∈ {0,1}
    # assigned value to variable x
    # push value to stack 'trail'
    # return True
    for i in literal_list.keys():
        if literal_list[i] == None:
            literal_list[i] = False
            trail[i] = [False, False]
    return True

def backtrack():
    while True:
        # If stack 'trail' is empty then return false
        if not bool(trail):
            return False

        # pop the last item from stack 'trail'
        v = trail.popitem()

        # Check the flip bit : If it is False, Need to flip the value against the literal & update the flip signal to True
        if not v[1][1]:
            trail[v[0]] = [not(v[1][0]), True]
            return True

clauses = parse_dimacs("C:\\Users\\MUHAMMAD USMAN\\Downloads\\solver\\example-1.cnf")
print(clauses)
literal_values(clauses)
print( "List : ", literal_list)
print(DPLL(clauses))
print(trail)