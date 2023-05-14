# Explanation of the Backward Chaining Implementation

The `BackwardChaining` class is an implementation of a backward chaining algorithm for checking if a given `query` can be inferred from a given knowledge base `KB`. The class contains two methods: `check` and `BC`.

## The `check` Method

```python
@staticmethod
def check(KB, q):
    # Initialize the inferred dictionary
    inferred = {}
    for clause in KB:
        if "=>" in clause:
            premise, conclusion = clause.split("=>")
            inferred[conclusion.strip()] = False
        else:
            inferred[clause.strip()] = False
    # Initialize the entailed list
    entailed = []
    # Call the recursive BC function
    result = BackwardChaining.BC(KB, q[0], inferred, entailed)
    if result:
        return "YES: " + ", ".join(entailed)  # outputs the YES and order of entailed facts
    else:
        return "NO"
```

The `check` method takes two arguments: `KB`, which represents a knowledge base in the form of a list of strings representing facts and rules; and `q`, which represents a query in the form of a list containing a single string representing a fact to be checked.

The method initializes two variables: `inferred`, which is a dictionary that keeps track of which facts have been inferred; and `entailed`, which is an empty list that will keep track of the order in which facts are entailed.

The method then calls the recursive `BC` method with the knowledge base, the query, the `inferred` dictionary, and the `entailed` list as arguments. If the result of this call is `True`, it returns `'YES'` along with the entailed facts; otherwise, it returns `'NO'`.

## The `BC` Method

```python
def BC(KB, q, inferred, entailed):
    # Check if the query is already known to be true
    if inferred[q]:
        return True
    # Find all implications with q as the conclusion
    implications = [clause for clause in KB if "=>" in clause and clause.split("=>")[1].strip() == q]
    for implication in implications:
        # Split the implication into premise and conclusion
        premise, conclusion = implication.split("=>")
        # Check if all premises are true
        premises = premise.split("&")
        all_true = True
        for p in premises:
            # Recursively call BC on each premise
            if not BackwardChaining.BC(KB, p.strip(), inferred, entailed):
                all_true = False
                break
        # If all premises are true
        if all_true:
            # Add q to the entailed list and mark it as inferred
            entailed.append(q)
            inferred[q] = True
            return True
    return False
```

The `BC` method takes four arguments: `KB`, which represents a knowledge base in the form of a list of strings representing facts and rules; `q`, which represents a query in the form of a string representing a fact to be checked; `inferred`, which is a dictionary that keeps track of which facts have been inferred; and `entailed`, which is a list that keeps track of the order in which facts are entailed.

The method first checks if the query is already known to be true (i.e., present in the `inferred` dictionary with a value of `True`) and returns `True` if it is. If it is not already known to be true, it finds all implications in the knowledge base with the query as their conclusion and loops over them.

For each implication, it splits it into its premise and conclusion and checks if all premises are true by splitting them at any conjunction symbols (`'&'`) and recursively calling itself on each one. If all premises are true (i.e., if all recursive calls return `True`), it adds the query to the list of entailed facts, marks it as inferred in the `inferred` dictionary with a value of `True`, and returns `True`.

If none of the implications with the query as their conclusion have all true premises (i.e., if none of them cause the method to return early), it returns `False`.

This implementation of the backward chaining algorithm uses recursion to check if a given query can be inferred from a given knowledge base. It starts with the query and works backward by finding implications with that query as their conclusion and checking their premises until either it finds that all premises for an implication are true or there are no more implications to check. If it finds that all premises for an implication are true, it returns `'YES'` along with the entailed facts; otherwise, it returns `'NO'`.