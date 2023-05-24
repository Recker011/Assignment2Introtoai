from Sentence import Sentence

class Resolution:
     
    @staticmethod
    def check(kb, query):
         
        clauses = kb.replace('(','').replace(')','').split('&')
        clauses.extend(negation(query))
         
        new = set()
         
        while True:
            pairs = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j in range(i+1, len(clauses))]
             
            for (clause_i, clause_j) in pairs:
                resolvents = resolve(clause_i, clause_j)
                if 0 in resolvents:
                    return True
                if resolvents:
                    new = new.union(set(resolvents))
            if new.issubset(set(clauses)):
                return False
            for clause in new:
                if clause not in clauses:
                    clauses.append(clause)
   

def getliterals(clause):
    clause = clause.split('|')
    return clause


def resolve(clause_i, clause_j):
    resolvents = []
    
    ci = getliterals(clause_i)
    cj = getliterals(clause_j)
    
    for i in ci:
        for j in cj:
            if i == '~' + j or '~' + i == j:
                clauses = ci + cj
                clauses.remove(i)
                clauses.remove(j)
                if len(clauses) == 0:
                    resolvents.append(0)
                    return resolvents
                resolvents.append(association(set(clauses)))

    return resolvents

def association(literals):
    final = '|'.join(literals)
    return final

def negation(query):
    if len(query) == 1:
        return '~' + query
    elif len(query) == 2:
        return query[1]
    else:
        query = Sentence('~' + '(' + revert(query) + ')')
        query = query.toCNF().associativity_disjunction()
        
        query = query.replace('(','').replace(')','').split('&')
        return query
    
def revert(clause):
    return clause.replace('|', '||')
    
kb, query = Sentence.parse('Test-Files/test_genericKB_1.txt')

a = Resolution.check(kb, query)

print(a)


