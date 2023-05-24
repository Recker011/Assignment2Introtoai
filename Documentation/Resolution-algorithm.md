# Explaining the resolution algorithm implementation

The resolution algorithm works by taking a conjunction of clauses in the `Conjunctive Normal Form` and repeatedly applying `resolution` to it. `Resolution` is simply checking for complimentary literals and removing them from the pairs of clauses that are compared. Resolution proves entailment by proof of contradiction. This is done by inserting the `negation of the query` into the knowledge base and checking that some pair of clauses during the resolution process will result in an `empty clause`, which means that the knowledge base does not entail the query. However, by proving that the `negation of the query` is not valid, by `contradiction`, the query must then be valid.

The resolution algorithm works for all knowledge bases instead of simply horn clauses but works in exponential time, however it is far more expressive as well.

# Method : check

```python

        @staticmethod
    def check(kb, query):

        clauses = kb.replace('(', '').replace(')', '').split('&')
        clauses.extend(negation(query))

```

The check method takes two parameters `kb` and `query` which is the knowledge base and query respectively. The parentheses of the knowledge base, which is in a conjunctive normal form, are removed and the clauses are split by conjunctions to give a list of clauses that the knowledge base is comprised of. The [`negation`](#method--negation) of the query is then added to the set of clauses for `proof by contradiction`.

```python

        new = set()

        while True:
            pairs = [(clauses[i], clauses[j]) for i in range(len(clauses))
                     for j in range(i+1, len(clauses))]

```

A set instance `new` is created. A loop is started and pairs of clauses are created using the clauses of the `knowledge base` as well as the `negated query`.

```python

            for (clause_i, clause_j) in pairs:
                resolvents = resolve(clause_i, clause_j)
                if 0 in resolvents:
                    return True
                if resolvents:
                    new = new.union(set(resolvents))
            if new.issubset(set(clauses)):
                return False

```

Each pair of clauses is resolved against each other. If there is a `0 in the list of resolvents`, that means that `there was an empty clause and the contradiction is proven`, if not, a `union is created with the resolvents` which is then compared with the original list of clauses from the `knowledge base`. If the union of resolvents happens to be `a subset of the original clauses`, then we return `False` as it means that the resolvents are repeating themselves and the contradiction cannot be proven.

```python

            for clause in new:
                if clause not in clauses:
                    clauses.append(clause)

```

The `clauses in the union` are added to the `original set of clauses` if they are not already there.

# Method : resolve

```python

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

```

An empty list `resolvents` is created. The individual literals of the pair of clauses is obtained using the [`getliterals`](#method--getliterals) method. Each literal is compared against each other to see if they are `complimentary` and are then removed from the list of literals. If there are `no literals left` in the list, then the `contradiction is proven` and a `0` is returned. If the lsit is not empty, then the literals are `added to the list of resolvents` as a disjunction using the [`association`](#method--association) method and the `resolvents are returned`.

# Method : getliterals

```python

    def getliterals(clause):
        clause = clause.split('|')
        return clause

```

Gets the `individual literals` of the clause provided by `splitting them by disjunction`.

# Method : association

```python

    def association(literals):
    final = '|'.join(literals)
    return final

```

Returns the `disjunction of literals` from a provided list.

# Method : negation

```python

    def negation(query):
        if len(query) == 1:
            return ['~' + query]
        elif len(query) == 2:
            return query[1]
        else:
            query = Sentence('~' + '(' + revert(query) + ')')
            query = query.toCNF()
            query.distributivity_conjunction()

            final = query.clause.replace('(', '').replace(
                ')', '').replace('||', '|').split('&')
            return final

```

Returns the `negation of a literal` if it is a `single literal`. Returns the `double-negated literal` if the given literal is `already negated` to begin with. If the provided query is more complex, a `Sentence` object is created and the clause is moved through the `toCNF` as well as `distributivity_conjunction` methods to get the negated query in a `conjunctive normal form`. The parentheses are then removed from the resulting query and `split by conjunctions` to be added to the original list of `knowledge base clauses`.
