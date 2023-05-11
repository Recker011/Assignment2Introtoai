import random
import string

def convert_cnf(cnf_str):
    # Split the CNF statement into clauses
    clauses = cnf_str.split(" & ")
    new_clauses = []
    for clause in clauses:
        # Remove the parentheses
        clause = clause[1:-1]
        # Split the clause into literals
        literals = clause.split(" | ")
        new_literals = []
        for literal in literals:
            # Check if the literal is negative
            if "~" in literal:
                # Remove the negation symbol and add a randomized new clause
                new_literal = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                new_literals.append(new_literal)
            else:
                new_literals.append(literal)
        # Join the new literals with "or" and add parentheses
        new_clause = "(" + " | ".join(new_literals) + ")"
        new_clauses.append(new_clause)
    # Join the new clauses with "and"
    new_cnf = " & ".join(new_clauses)
    return new_cnf

cnf_str = "(~p2 | p3) & (~p3 | p1) & (~c | e) & (~b | ~e | f) & (~f | ~g | h) & (~p1 | d) & (~p1 | ~p3 | c) & a & b & p2"
result = convert_cnf(cnf_str)
print(result)
