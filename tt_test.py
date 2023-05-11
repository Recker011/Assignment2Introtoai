def forward_chaining(KB, q):
    # Convert KB to Conjunctive Normal Form (CNF)
    KB = KB.split(' & ')
    for i in range(len(KB)):
        KB[i] = KB[i].replace('(', '').replace(')', '').split(' | ')

    # Initialize count, inferred and agenda
    count = {}
    inferred = {}
    agenda = []
    for clause in KB:
        if len(clause) == 1:
            agenda.append(clause[0])
        else:
            for literal in clause:
                if literal not in count:
                    count[literal] = 0
                count[literal] += 1

    # Forward chaining algorithm
    entailed = []
    while len(agenda) > 0:
        p = agenda.pop(0)
        if p == q:
            entailed.insert(0, p)
            return 'YES: ' + ', '.join(entailed)
        if p not in inferred:
            inferred[p] = True
            entailed.insert(0, p)
            for clause in KB:
                if p in clause:
                    for literal in clause:
                        if literal != p:
                            count[literal] -= 1
                            if count[literal] == 0:
                                agenda.append(literal)
    return 'NO'

# Test the algorithm with the given example
KB = '(~p2 | p3) & (~p3 | p1) & (~c | e) & (~b | ~e | f) & (~f | ~g | h) & (~p1 | d) & (~p1 | ~p3 | c) & a & b & p2'
q = 'd'
print(forward_chaining(KB, q))
