from Sentence import Sentence

class Resolution:
     
    @staticmethod
    def check(kb, query):
        #Remove parentheses and separate clauses by conjunction into a list
        
        clauses = kb.replace('(','').replace(')','').split('&')
        clauses.extend(negation(query)) #Negate the query and add to list of clauses
         
        new = set()
         
        while True:
            pairs = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j in range(i+1, len(clauses))] #Create pairs of clauses
             
            for (clause_i, clause_j) in pairs:
                resolvents = resolve(clause_i, clause_j) #Resolve each pair of clauses and return the resolvents
                if 0 in resolvents: #Check for empty clause(0) in resolvents
                    print(YES)
                if resolvents:
                    new = new.union(set(resolvents)) #Create union with returned resolvents
            if new.issubset(set(clauses)): #Check if union of resolvents is a subset of the list of clauses
                print(NO)
            for clause in new: #Add resolvents to list of clauses if not already in the list
                if clause not in clauses:
                    clauses.append(clause)
   

def getliterals(clause):
    #Get individual literals from a disjuncton of literals
    
    clause = clause.split('|')
    return clause


def resolve(clause_i, clause_j):
    resolvents = []
    
    ci = getliterals(clause_i)
    cj = getliterals(clause_j)
    
    #Compare literals in the clause pair with each other
    
    for i in ci: 
        for j in cj:
            if i == '~' + j or '~' + i == j: #Check if literals are complimentary
                clauses = ci + cj
                clauses.remove(i) #Resolve complimentary literals
                clauses.remove(j)
                if len(clauses) == 0: #Check if there is an empty clause
                    resolvents.append(0) 
                    return resolvents
                resolvents.append(association(set(clauses))) #Create disjunction of resolvents and return it

    return resolvents

def association(literals):
    #Create a disjunction of literals
    
    final = '|'.join(literals)
    return final

def negation(query):
    if len(query) == 1: #If query is a single literal, return negated 
        return ['~' + query]
    elif len(query) == 2: #If query is a negated literal, return positive literal
        return query[1]
    else:
        #If query is more complex, negate then apply logical equivalence rules to convert to a CNF form again
        
        query = Sentence('~' + '(' + revert(query) + ')') 
        query = query.toCNF()
        query.distributivity_conjunction()
        
        final = query.clause.replace('(','').replace(')','').replace('||', '|').split('&') #Split clause by conjunction and return
        return final
    
def revert(clause):
    #Change disjunction connective to be used with Sentence class
    
    return clause.replace('|', '||')
