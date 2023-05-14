def to_cnf(sentence):
    # split the sentence into clauses
    clauses = sentence.split(';')
    cnf = []
    for clause in clauses:
        clause = clause.strip()
        # evaluate expressions within brackets first
        while '(' in clause:
            start = clause.rfind('(')
            end = clause.find(')', start)
            subclause = clause[start+1:end]
            subcnf = to_cnf(subclause)
            clause = clause[:start] + subcnf + clause[end+1:]
        if '<=>' in clause:
            # convert biconditional to conjunction of two implications
            p, q = clause.split('<=>')
            p = p.strip()
            q = q.strip()
            cnf.append(f'({p} => {q}) & ({q} => {p})')
        elif '=>' in clause:
            # convert implication to disjunction
            p, q = clause.split('=>')
            p = p.strip()
            q = q.strip()
            if '&' in p:
                # distribute disjunction over conjunction
                literals = p.split('&')
                literals = [literal.strip() for literal in literals]
                cnf.append(f'(~({" & ".join(literals)}) | {q})')
            else:
                cnf.append(f'(~{p} | {q})')
        elif '&' in clause:
            # conjunction of literals
            literals = clause.split('&')
            for literal in literals:
                literal = literal.strip()
                cnf.append(literal)
        elif '||' in clause:
            # disjunction of literals
            literals = clause.split('||')
            disjunction = ' | '.join(literals)
            cnf.append(f'({disjunction})')
        else:
            # single literal
            cnf.append(clause)
    return ' & '.join(cnf)

# example usage
sentence = 'p2=> p3; p3 => p1; c => e; b&e => f; f&g => h; p1=>d; p1&p3 => c; a; b; p2;'
cnf = to_cnf(sentence)
print(cnf)
