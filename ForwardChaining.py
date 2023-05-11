def forward_chaining(KB, q):
    # Convert KB to Conjunctive Normal Form (CNF)
    KB = KB.split(' & ')
    for i in range(len(KB)):
        KB[i] = KB[i].replace('(', '').replace(')', '').split(' | ')

    # Initialize count, inferred and agenda
    count = {}
    inferred = {}
    agenda = []
    for i, clause in enumerate(KB):
        if len(clause) == 1:
            literal = clause[0]
            if literal[0] == '~':
                inferred[literal[1:]] = False
            else:
                inferred[literal] = True
            agenda.append(literal)
        else:
            count[i] = len(clause)

    # Forward chaining algorithm
    entailed = []
    while len(agenda) > 0:
        p = agenda.pop(0)
        if p == q:
            entailed.insert(0, p)
            return 'YES: ' + ', '.join(entailed)
        if p not in entailed:
            inferred[p] = True
            entailed.insert(0, p)
        for i, clause in enumerate(KB):
            if p in clause:
                if i in count: # Check if key exists in count dictionary
                    count[i] -= 1
                    if count[i] == 0:
                        for literal in clause:
                            if literal[0] == '~':
                                if literal[1:] != p and (literal[1:] not in inferred or inferred[literal[1:]] == False):
                                    inferred[literal[1:]] = False
                            else:
                                if literal != p and (literal not in inferred or inferred[literal] == False):
                                    inferred[literal] = True
                                    agenda.append(literal)
    return 'NO'






KB = '(a & d | c)'
q = 'd'
result = forward_chaining(KB, q)
print(result)
