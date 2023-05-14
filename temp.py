# Truth table checking function

import re

def truth_table_check(kb, query):

    symbols = list(set(re.findall(r'[a-z]+[0-9]*', kb)))
    def evaluate(expression, values):
        for s in symbols:
            expression = expression.replace(s, str(values[s]))
        return eval(expression)
    models = 0
    for i in range(2**len(symbols)):
        values = {symbols[j]: (i >> j) & 1 for j in range(len(symbols))}
        if evaluate(kb, values):
            if evaluate(query, values):
                models += 1
            else:
                return 'NO'
    return f'YES:{models}'


# Forward chaining checking function

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


# Backward chaining checking algorithm

def backward_chaining(KB, q):
    # Split the KB into clauses
    clauses = KB.split("; ")
    # Initialize the inferred dictionary
    inferred = {}
    for clause in clauses:
        if "=>" in clause:
            premise, conclusion = clause.split(" => ")
            inferred[conclusion] = False
        else:
            inferred[clause] = True
    # Initialize the entailed list
    entailed = []
    # Call the recursive BC function
    result = BC(KB, q, inferred, entailed)
    if result:
        return "YES: " + ", ".join(entailed)
    else:
        return "NO"

def BC(KB, q, inferred, entailed):
    # Check if the query is already known to be true
    if inferred[q]:
        return True
    # Find all implications with q as the conclusion
    implications = [clause for clause in KB.split("; ") if "=>" in clause and clause.split(" => ")[1] == q]
    for implication in implications:
        # Split the implication into premise and conclusion
        premise, conclusion = implication.split(" => ")
        # Check if all premises are true
        premises = premise.split("&")
        all_true = True
        for p in premises:
            # Recursively call BC on each premise
            if not BC(KB, p, inferred, entailed):
                all_true = False
                break
        # If all premises are true
        if all_true:
            # Add q to the entailed list and mark it as inferred
            entailed.append(q)
            inferred[q] = True
            return True
    return False


#Old main program

import sys
from TruthTable import TruthTable
from ForwardChaining import ForwardChaining
from BackwardChaining import BackwardChaining
from Sentence import Sentence
from KB import KB

# Define a function to parse the input file and extract the knowledge base and query
def parse_input_file(filename):
    try:
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
            lines = [line.replace(' ', '').strip() for line in lines]
            tell_list, ask_list = lines[1].split(';'), lines[3].split(';')
            tell, ask = list(filter(None, tell_list)), list(filter(None, ask_list))
            kb = KB()
            for sentence in tell:
                kb.tell(sentence)
            query = Sentence(ask[0])
            return kb, query
    except FileNotFoundError:
        # Error handling for file not found
        print(f"Error: file {filename} not found.")
        sys.exit(1)
    except IndexError:
        # error handling for wrong formatting of input text
        print(f"Error: file {filename} is not in the correct format.")
        sys.exit(1)

# Define a function to implement the Truth Table checking algorithm
def tt_checking(kb, query):
    tt = TTchecking(kb.clauses, query)
    result = tt.check()
    return result

# Define a function to implement the Forward Chaining algorithm
def forward_chaining(kb, query):
    fc = ForwardChaining(kb.clauses, query)
    result = fc.check
    return result

# Define a function to implement the Backward Chaining algorithm
def backward_chaining(kb, query):
    bc = BackwardChaining(kb.clauses, query)
    result = bc.check
    return result

# Main function
def main():
    if len(sys.argv) != 3:
        print("Usage: python iengine.py [method] [filename]")
        sys.exit(1)

    method = sys.argv[1]
    filename = sys.argv[2]

    kb, query = parse_input_file(filename)

    if method == 'TT':
        result = tt_checking(kb, query)
    elif method == 'FC':
        result = forward_chaining(kb, query)
    elif method == 'BC':
        result = backward_chaining(kb, query)
    else:
        print("Invalid method. Method must be TT, FC or BC.")
        sys.exit(1)

    print(result)

if __name__ == '__main__':
    main()
    
    
# parse function

def parse_input_file(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        lines = [line.replace(' ', '').strip() for line in lines]
        t, a = lines[1].split(';'), lines[3].split(';')
        tell, ask = list(filter(None, t)), list(filter(None, a))
    return tell, ask

# Example usage
kb, query = parse_input_file('test_HornKB.txt')
print('KB:', kb)
print('Query:', query)


# Rete algorithm

def rete(KB, query):
    def implies(fact):
        return fact.split('=>')[1] if '=>' in fact else None

    def entails(fact):
        return set(fact.split('=>')[0].split('&')) if '=>' in fact else set()

    def is_fact(fact):
        return '=>' not in fact

    agenda = [fact for fact in KB if is_fact(fact)]
    inferred = {}
    entailed_facts = []
    while agenda:
        p = agenda.pop(0)
        if p == query[0]:
            entailed_facts.append(p)
            return f'YES: {", ".join(entailed_facts)}'
        inferred[p] = True
        for fact in KB:
            premises = entails(fact)
            if all(inferred.get(premise) for premise in premises):
                q = implies(fact)
                if q and not inferred.get(q):
                    entailed_facts.append(q)
                    agenda.append(q)
    return 'NO'

KB = ['p2=>p3', 'p3=>p1', 'c=>e', 'b&e=>f', 'f&g=>h', 'p1=>d', 'p1&p3=>c', 'a', 'b', 'p2']
query = ['d']
print(rete(KB, query))
