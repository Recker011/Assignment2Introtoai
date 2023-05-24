# Converting general knowledge bases to 'Conjunctive Normal Form'

`Conjunctive normal form` is a clausal form where a sentence is a conjunction of one or more clauses, where each clause is a disjunction of literals.

```python
from Parse import Parse

class Sentence:
    def __init__(self, clause, connective=None):
        self.clause = clause
        self.connective = connective
        self.subclauses = []
```

The `Sentence` class allows you to create sentences that comprise of a clause, a connective and subclauses which are clauses separated by the main connective. Defining a sentence this way will make it possible to separate smaller clauses from the larger sentence and apply logical equivalence techniques at a smaller scale before combining them at the end.

## Method : parsesentence

```python
        bracketcounter = 0
        connectiveind = -1


        for i in range(len(self.clause)):

            if self.clause[i] == '(':
                bracketcounter = bracketcounter + 1
            elif self.clause[i] == ')':
                bracketcounter = bracketcounter - 1
            elif ((self.clause[i] == '<') and bracketcounter == 0) and connectiveind < 0:
                connectiveind = i
            elif (self.clause[i] == '=' and self.clause[i + 1] == '>') and bracketcounter == 0 and connectiveind < 0:
                connectiveind = i
            elif ((self.clause[i] == '&') and bracketcounter == 0) and connectiveind < 0:
                connectiveind = i
            elif ((self.clause[i] == '|') and bracketcounter == 0) and connectiveind < 0:
                connectiveind = i
            elif (self.clause[i] == '~') and self.clause[i+1] == '(' and self.clause[-1] == ')' and connectiveind < 0 or len(self.clause) == 2:
                connectiveind = i
```

Uses bracketcounter and connective indexes to locate the outermost brackets as well as the main connective that is currently outside of any nested parentheses.

```python
if connectiveind < 0:
            if self.clause[0] == '(' and self.clause[-1] == ')':
                self.clause = (self.clause[1:(len(self.clause)) - 1])
                self.parsesentence()
```

If there are no connectives outside of brackets, it means that all literals are entirely within a set of parentheses. This code block removes the outer layer.

```python
        else:
            if self.clause[connectiveind] == '<':
                lhs = self.clause[0:connectiveind]
                rhs = self.clause[connectiveind + 3: len(self.clause)]
                Sub1 = Sentence(lhs)
                Sub2 = Sentence(rhs)
                self.subclauses.append(Sub1)
                self.subclauses.append(Sub2)
                self.connective = '<=>'

            elif self.clause[connectiveind] == '=':
                lhs = self.clause[0:connectiveind]
                rhs = self.clause[connectiveind + 2: len(self.clause)]
                Sub1 = Sentence(lhs)
                Sub2 = Sentence(rhs)
                self.subclauses.append(Sub1)
                self.subclauses.append(Sub2)
                self.connective = '=>'

            elif self.clause[connectiveind] == '&':
                lhs = self.clause[0:connectiveind]
                rhs = self.clause[connectiveind + 1: len(self.clause)]
                Sub1 = Sentence(lhs)
                Sub2 = Sentence(rhs)
                self.subclauses.append(Sub1)
                self.subclauses.append(Sub2)
                self.connective = '&'

            elif self.clause[connectiveind] == '|':
                lhs = self.clause[0:connectiveind]
                rhs = self.clause[connectiveind + 2: len(self.clause)]
                Sub1 = Sentence(lhs)
                Sub2 = Sentence(rhs)
                self.subclauses.append(Sub1)
                self.subclauses.append(Sub2)
                self.connective = '||'

            elif self.clause[connectiveind] == '~':
                symbol = self.clause[connectiveind + 1:len(self.clause)]
                Sub1 = Sentence(symbol)
                self.subclauses.append(Sub1)
                self.connective = '~'
```

Uses the connective index to give the sentence an appropriate connective property. Also creates subclauses that are on the left and right hand side of the connective and initializes them as `Sentence` objects.

## Method : toCNF

```python

    def toCNF(self):
        self.parsesentence()

```

Method begins by using the `parsesentence` method to get the connective as well as subclauses of provided clause.

```python
        if self.connective == '<=>':
            self = self.bicon_elim()
            return self.toCNF()

        elif self.connective == '=>':
            self = self.implication_elim()
            if '~~' in self.clause:
                self = self.doublenegation_elim()
            return self.toCNF()

```

Checks whether the connective is an equivalence. If it is, then apply [`biconditional-elimination`](#method--bicon_elim) to the clause. If it is an implication connective, then apply [`implication-elimination`](#method--implication_elim) to the clause and check for [`double-negation`](#method--doublenegation_elim).

```python
        elif self.connective == '~':
            result = self.subclauses[0].toCNF()
            result.parsesentence()
            deMorgan_result = result.deMorgan()
            self = deMorgan_result.doublenegation_elim()
            return self.toCNF()
```

If the connective is a negation, it will only be cases where it is a single literal or a negation right outside of parentheses applied to all literals within said parentheses. The subclause within the brackets will then be put through the `toCNF` and `parsesentence` methods to get the respective connective. To the resulting clause, a [`deMorgan`](#method--demorgan) is applied prior to a [`double-negation`](#method--doublenegation_elim) check.

```python
        elif self.connective == '&':

            lhs = self.subclauses[0].toCNF()
            rhs = self.subclauses[1].toCNF()

            lhs.distributivity_conjunction()
            lhs.associativity_disjunction()
            rhs.distributivity_conjunction()
            rhs.associativity_disjunction()

```

If the connective is a conjunction, then the subclauses of the main clause must be taken separately and converted to a normal form before combining them back together. After converting both left and right hand side clauses, the [`distributivity of conjunction`](#method--distributivity_conjunction) law is applied to both sides.

```python
            if len(lhs.clause) <= 2 and len(rhs.clause) <= 2:
                self = Sentence('({}&{})'.format(
                    lhs.clause, rhs.clause), '&')
            elif len(lhs.clause) <= 2:
                self = Sentence('{}&({})'.format(
                    lhs.clause, rhs.clause), '&')
            elif len(rhs.clause) <= 2:
                self = Sentence('({})&{}'.format(
                    lhs.clause, rhs.clause), '&')
            else:
                self = Sentence('{}&{}'.format(
                    lhs.clause, rhs.clause), '&')

            return self

```

Before joining the two clauses together, the correct format is assessed. If both sides contain only a single literal, then they can be encased in a complete outer set of parentheses. If the left or right hand side has a single literal but the other side does not, then there will only be parentheses for the side without a single literal. If both sides do not have just a single literal then no parentheses will be applied to the final clause.

```python
        elif self.connective == '||':

            lhs = self.subclauses[0].toCNF()
            rhs = self.subclauses[1].toCNF()

            if len(lhs.clause) <= 2 and len(rhs.clause) <= 2:
                self = Sentence('({}||{})'.format(
                    lhs.clause, rhs.clause), '||')
            elif len(lhs.clause) <= 2:
                self = Sentence('{}||({})'.format(
                    lhs.clause, rhs.clause), '||')
            elif len(rhs.clause) <= 2:
                self = Sentence('({})||{}'.format(
                    lhs.clause, rhs.clause), '||')
            else:
                self = Sentence('{}||{}'.format(
                    lhs.clause, rhs.clause), '||')

            return self

```

If the connective is a `disjunction`, the process is very similar to when it is a `conjunction`. The subclauses are taken separately and converted to a normal form, then combined together after assessing the right format for parentheses.

## Method : bicon_elim

```python
        def bicon_elim(self):
        # Apply biconditional elimination [  a <=> b ------> a=>b & b=>a   ]

        eliminated_sentence = '({}=>{})'.format(
            self.subclauses[0].clause, self.subclauses[1].clause) + '&' + '({}=>{})'.format(self.subclauses[1].clause, self.subclauses[0].clause)
        result = Sentence(eliminated_sentence)
        return result
```

This method takes a clause and applies the logical equivalence rule of `biconditional elimination`, which states that an `equivalence` of two clauses is simply the `conjunction of the implication of the two clauses`. (example shown in code block)

## Method : implication_elim

```python
        def implication_elim(self):
        # Apply implication elimination [  a => b ------> ~a || b   ]

        eliminated_sentence = '~{}||{}'.format(
            self.subclauses[0].clause, self.subclauses[1].clause)
        result = Sentence(eliminated_sentence)
        return result
```

This method takes a clause and applies the logical equivalence rule of `implication elimination`, which states that the `implication` of two clauses is their `disjunction where the first clause is a negation`. (example shown in code block)

## Method : deMorgan

```python
       def deMorgan(self):
        # Apply deMorgan's law [  ~(a || b) ------> (~a & ~b)   ] OR [  ~(a & b) ------> (~a || ~b)   ]

        if self.connective == '&':
            result = Sentence('~{}||~{}'.format(
                self.subclauses[0].clause, self.subclauses[1].clause), '||')
            return result
        if self.connective == '||':
            result = Sentence('~{}&~{}'.format(
                self.subclauses[0].clause, self.subclauses[1].clause), '&')
            return result
```

This method applies the `deMorgan` rule of logical equivalence, which states that you can move a `negation` that encompasses a clause within parentheses inwards to give the `negated conjunction/disjunction of the literals within that clause`. If the connective is originally a `conjunction`, then it is changed to a `disjunction`, and vice versa.

## Method : doublenegation_elim

```python
        def doublenegation_elim(self):
        # Apply double negation elimination [  ~~a ------> a  ]

        negated_clause = Sentence(
            self.clause.replace('~~', ''), self.connective)
        return negated_clause
```

This method applies the `double-negation` rule of logical equivalence, which states that two negations stacked on top of each other will cancel out and result in no negation of the literal.

## Method : distributivity_conjunction

```python
        def distributivity_conjunction(self):
        # Apply distributivity of & over || [  a || (b & c)  ------> (a || b) & (a || c)  ]

        self.parsesentence()

        if self.connective == '||':
            lhs = self.subclauses[0]
            rhs = self.subclauses[1]
            if len(lhs.clause) > 1:
                lhs.parsesentence()
                if lhs.connective == '&':
                    self.clause = '({}||{})&({}||{})'.format(
                        rhs.clause, lhs.subclauses[0].clause, rhs.clause, lhs.subclauses[1].clause)
            elif len(rhs.clause) > 1:
                rhs.parsesentence()
                if rhs.connective == '&':
                    self.clause = '({}||{})&({}||{})'.format(
                        lhs.clause, rhs.subclauses[0].clause, lhs.clause, rhs.subclauses[1].clause)
```

This method applies the `distributivity of conjunction` rule of logical equivalence, which states that if there is a `disjunction of conjunction of literals`, the `conjunction can be moved outwards` by `creating a conjunction of disjunctions of the same literals`. This is done in the method by first using the `parsesentence` method to get the two sides of the disjunction, then checking which side has the single literal.

## Method : associativity_disjunction

```python
        def associativity_disjunction(self):
        # Apply associativity of ||  [  a || (b || c)  ------> (a || b || c)  ]

        self.parsesentence()
        if self.connective == '||':
            lhs = self.subclauses[0]
            rhs = self.subclauses[1]
            if len(lhs.clause) > 1 and lhs.clause[0] != '~':
                lhs.parsesentence()
                if lhs.connective == '||':
                    self.clause = '({}||{}||{})'.format(
                        rhs.clause, lhs.subclauses[0].clause, lhs.subclauses[1].clause)
            elif len(rhs.clause) > 1 and rhs.clause[0] != '~':
                rhs.parsesentence()
                if rhs.connective == '||':
                    self.clause = '({}||{}||{})'.format(
                        lhs.clause, rhs.subclauses[0].clause, rhs.subclauses[1].clause)
```

This method applies the `associativity of disjunctions` rule of logical equivalence, which states that if there is a `disjunction of a literal with a disjunction of a set of literals within parentheses`, the parentheses can be removed to `create an overall disjunction of literals`. This is done once again using the `parsesentence` method and getting subclauses to see which side of the disjunction has the single literal.
