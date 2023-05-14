# WalkSAT Class

The `WalkSAT` class implements the WalkSAT algorithm for solving the Boolean satisfiability problem. The class contains a single static method named `check` that takes in a knowledge base and a query in conjunctive normal form (CNF) and returns whether the query can be inferred from the knowledge base or not.

## check Method

The `check` method takes four arguments: `kb`, `query`, `max_flips`, and `p`. The `kb` argument is a string representing the knowledge base in CNF. The `query` argument is a string representing the query in CNF. The `max_flips` argument is an integer representing the maximum number of flips the algorithm will perform before giving up. The `p` argument is a float between 0 and 1 representing the probability of choosing a random symbol to flip.

Here's an example of how to call the `check` method:

```python
result = WalkSAT.check(kb, query)
```

### Converting KB and Query to CNF

The first step in the `check` method is to convert the input knowledge base and query from strings to lists of lists representing clauses and literals in CNF. This is done by splitting the input strings on the `'&'` character to get the clauses, then splitting each clause on the `'|'` character to get the literals. Any extra spaces and parentheses are removed from the clauses and literals.

```python
# Convert KB and query to CNF
kb = kb.split('&')
kb = [clause.strip().replace('(', '').replace(')', '').split('|') for clause in kb]
kb = [[literal.strip() for literal in clause] for clause in kb]
query = query.split('&')
query = [clause.strip().replace('(', '').replace(')', '').split('|') for clause in query]
query = [[literal.strip() for literal in clause] for clause in query]
```
The knowledge base `'(~p2 | p3) & (~p3 | p1) & (~c | e) & (~b | ~e | f) & (~f | ~g | h) & (~p1 | d) & (~p1 | ~p3 | c) & a & b & p2'` is already in conjunctive normal form (CNF), so it doesn't need to be converted. However, the `check` method of the `WalkSAT` class still processes the input knowledge base string to split it into clauses and literals and remove any extra spaces and parentheses.

Here's how the input knowledge base string is processed by the `check` method:

1. The input knowledge base string is split on the `'&'` character to get the clauses: `kb = kb.split('&')`.
2. Each clause is stripped of any extra spaces and parentheses are removed: `kb = [clause.strip().replace('(', '').replace(')', '').split('|') for clause in kb]`.
3. Each clause is then split on the `'|'` character to get the literals: `kb = [clause.strip().replace('(', '').replace(')', '').split('|') for clause in kb]`.
4. Each literal is stripped of any extra spaces: `kb = [[literal.strip() for literal in clause] for clause in kb]`.

After these steps, the input knowledge base string is converted to a list of lists representing clauses and literals in CNF. For the given input knowledge base string, the resulting list of lists would be:

```python
[
    ['~p2', 'p3'],
    ['~p3', 'p1'],
    ['~c', 'e'],
    ['~b', '~e', 'f'],
    ['~f', '~g', 'h'],
    ['~p1', 'd'],
    ['~p1', '~p3', 'c'],
    ['a'],
    ['b'],
    ['p2']
]
```

Each inner list represents a clause and each element within an inner list represents a literal within that clause.

### Getting All Symbols

The next step is to get all symbols that appear in the knowledge base and query. This is done by iterating over all clauses and literals and adding any symbols (literals without the `'~'` negation symbol) to a set. The set is then converted to a list.

```python
# Get all symbols
symbols = set()
for clause in kb:
    for literal in clause:
        symbols.add(literal.strip().replace('~', ''))
for clause in query:
    for literal in clause:
        symbols.add(literal.strip().replace('~', ''))
symbols = list(symbols)
```

### Initializing Model Randomly

After getting all symbols, a model is initialized randomly. The model is a dictionary where the keys are symbols and the values are randomly chosen Boolean values representing whether the symbol is true or false.

```python
# Initialize model randomly
model = {symbol: random.choice([True, False]) for symbol in symbols}
```

After processing the input knowledge base string to split it into clauses and literals, the `check` method of the `WalkSAT` class gets all symbols that appear in the knowledge base and query. For the given input knowledge base string `'(~p2 | p3) & (~p3 | p1) & (~c | e) & (~b | ~e | f) & (~f | ~g | h) & (~p1 | d) & (~p1 | ~p3 | c) & a & b & p2'`, the set of symbols would be `{'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'p1', 'p2', 'p3'}`.

After getting all symbols, a model is initialized randomly. The model is a dictionary where the keys are symbols and the values are randomly chosen Boolean values representing whether the symbol is true or false. Since the values are chosen randomly, the model will be different each time the `check` method is called.

Here's an example of a possible model that could be generated for the given input knowledge base string:

```python
{
    'a': True,
    'b': False,
    'c': True,
    'd': False,
    'e': True,
    'f': False,
    'g': True,
    'h': False,
    'p1': True,
    'p2': False,
    'p3': True
}
```

In this example model, the symbols `'a'`, `'c'`, `'e'`, `'g'`, `'p1'`, and `'p3'` are assigned the value `True`, while the symbols `'b'`, `'d'`, `'f'`, `'h'`, and `'p2'` are assigned the value `False`. It should be noted that this is just one possible model and the actual model generated by the `check` method will likely be different due to the random initialization.


### Evaluating Clauses

Next, two helper functions are defined for evaluating clauses and evaluating the entire knowledge base and query given a model. The `evaluate_clause` function takes a clause and a model as arguments and returns whether the clause is true under the given model. This is done by iterating over all literals in the clause and checking if any of them are true under the given model. If any literal is true, then the entire clause is true.

```python
# Evaluate clauses
def evaluate_clause(clause, model):
    for literal in clause:
        if literal.startswith('~'):
            if not model[literal[1:]]:
                return True
        else:
            if model[literal]:
                return True
    return False
```

### Evaluating KB and Query

The `evaluate` function takes a knowledge base, a query, and a model as arguments and returns whether both the knowledge base and query are true under the given model. This is done by calling the `evaluate_clause` function on each clause in both the knowledge base and query. If any clause is false, then the entire knowledge base or query is false.

```python
# Evaluate KB and query
def evaluate(kb, query, model):
    for clause in kb:
        if not evaluate_clause(clause, model):
            return False
    for clause in query:
        if not evaluate_clause(clause, model):
            return False
    return True
```

### WalkSAT Algorithm

After defining these helper functions, the WalkSAT algorithm itself is implemented. The algorithm iterates for a maximum number of flips specified by the `max_flips` argument. In each iteration, it first checks if both the knowledge base and query are true under the current model by calling the `evaluate` function. If they are both true, then it returns 'YES' to indicate that the query can be inferred from the knowledge base.

If the knowledge base and query are not both true under the current model, then the algorithm chooses a random clause that is false under the current model. It then flips a random symbol in that clause with probability `p` or chooses the symbol that results in the minimum number of false clauses when flipped with probability `1-p`. The chosen symbol is then flipped in the model and the algorithm continues to the next iteration.

If the maximum number of flips is reached without finding a model that satisfies both the knowledge base and query, then the algorithm returns 'NO' to indicate that the query cannot be inferred from the knowledge base.

```python
# WalkSAT algorithm
for i in range(max_flips):
    if evaluate(kb, query, model):
        return 'YES'
    false_clauses = [clause for clause in kb + query if not evaluate_clause(clause, model)]
    clause = random.choice(false_clauses)
    if random.random() < p:
        symbol = random.choice(list(model.keys()))
    else:
        min_false = float('inf')
        best_symbol = None
        for literal in clause:
            symbol = literal.replace('~', '')
            model[symbol] = not model[symbol]
            false_count = sum([not evaluate_clause(c, model) for c in kb + query])
            if false_count < min_false:
                min_false = false_count
                best_symbol = symbol
            model[symbol] = not model[symbol]
        symbol = best_symbol
    model[symbol] = not model[symbol]
return 'NO'
```