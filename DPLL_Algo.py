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
    if not BCP(CNF_Formula):
        #print("First")
        return False
    while True:
        if not decide():
            return True
        while not BCP(CNF_Formula):
            if not backtrack():
                #print("Second")
                return False

def BCP(CNF_Formula):

    # Check IF: the clause have single literal ? THEN: Assign value such that the clause becomes TRUE
    for clause in CNF_Formula:
        if len(clause) == 1:
            #print("Less than 1")
            # IF literal is positive, which means it is without negation, so we need to assign TRUE value
            if clause[0] > 0:
                literal_list[clause[0]] = True
                trail[clause[0]] = [True, True]
            # ELSE literal is negative, which means it is with negation, so we need to assign FALSE value
            else:
                literal_list[abs(clause[0])] = False
                trail[abs(clause[0])] = [False, True]

    # Find the unit clause implying that a variable x must be set to value v ∈ {0,1}
    # Check the clauses that have more than one literal
    for clause in CNF_Formula:
        falseCount = 0
        unAssigned_variable = 0
        if len(clause) != 1:
            #print("Greater than 1", clause)
            for literal in clause:
                # Check IF literal value is assigned in stack 'trail'
                if abs(literal) in trail.keys():
                    if (literal > 0 and trail[abs(literal)][0]==True) or (literal < 0 and trail[abs(literal)][0]==False):
                        break
                    else:
                        falseCount = falseCount + 1
                # IF literal value is not assigned in stack, it means it is unassigned varaible
                elif abs(literal) not in trail.keys():
                    # IF: two unassigned variable found in clause THEN: it is Unresolved clause & we don't need to check it further
                    if unAssigned_variable == 0:
                        unAssigned_variable = literal
                    else:
                        break

            if(falseCount == (len(clause)-1)):
                if(unAssigned_variable > 0):
                    literal_list[unAssigned_variable] = True
                    trail[unAssigned_variable] = [True, True]
                else:
                    literal_list[abs(unAssigned_variable)] = False
                    trail[abs(unAssigned_variable)] = [False, True]

    #print("After Assign : ", trail)
    # Check for unsatisfied clause
    for clause in CNF_Formula:
        #print(clause)
        falseCount = 0
        for literal in clause:
            if abs(literal) in trail.keys():
                if literal > 0 and trail[abs(literal)][0]== True:
                    #print("Here 1 ", literal)
                    break
                elif literal < 0 and trail[abs(literal)][0]== False:
                    #print("Here 2 ", literal)
                    break
                else:
                    #print("Here 3 ", literal)
                    falseCount = falseCount + 1

        if falseCount == len(clause):
            #print("BCP Return False")
            return False
    #print("BCP Return True")
    return True








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
            #print("In decide : ", trail)
            #print("In decide : ", literal_list)
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

#clauses = parse_dimacs("C:\\Users\\MUHAMMAD USMAN\\Downloads\\benchmarks\\example-10.cnf")
clauses = parse_dimacs(sys.argv[1])
#print(clauses)
literal_values(clauses)
#print("List : ", literal_list)
if DPLL(clauses):
    print("sat")
    exit(10)
else:
    print("unsat")
    exit(20)
#print("List : ", literal_list)