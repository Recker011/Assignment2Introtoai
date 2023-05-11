def forward_chaining(KB, q):
    # Split the KB into clauses
    clauses = KB.split("; ")
    # Initialize the count of premises for each implication
    count = {}
    # Initialize the inferred dictionary
    inferred = {}
    # Initialize the agenda with known facts
    agenda = []
    for clause in clauses:
        # Check if the clause is an implication
        if "=>" in clause:
            # Split the clause into premise and conclusion
            premise, conclusion = clause.split(" => ")
            # Count the number of premises
            count[conclusion] = len(premise.split("&"))
            inferred[conclusion] = False
        else:
            # Add the fact to the agenda
            agenda.append(clause)
            inferred[clause] = True
    # Initialize the entailed list
    entailed = []
    while agenda:
        # Pop the first symbol from the agenda
        p = agenda.pop(0)
        # Add the symbol to the entailed list
        entailed.append(p)
        # Check if the symbol is the query
        if p == q:
            return "YES: " + ", ".join(entailed)
        # For each implication in the KB
        for clause in clauses:
            if "=>" in clause:
                premise, conclusion = clause.split(" => ")
                # If p is one of the premises
                if p in premise.split("&"):
                    # Decrease the count of premises for this implication
                    count[conclusion] -= 1
                    # If all premises are true
                    if count[conclusion] == 0:
                        # Add the conclusion to the agenda
                        if not inferred[conclusion]:
                            agenda.append(conclusion)
                            inferred[conclusion] = True
    return "NO"

KB = "p2 => p3; p3 => p1; c => e; b&e => f; f&g => h; p1 => d; p1&p3 => c; a; b; p2"
q = "d"
result = forward_chaining(KB, q)
print(result)
