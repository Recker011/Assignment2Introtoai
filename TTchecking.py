from itertools import product

class TTchecking:
    def __init__(self, kb, query):
        self.kb = kb
        self.query = query
        self.symbols = self.get_symbols(kb + [query])
    
    # Extract all the symbols (propositional variables) from the list.
    def get_symbols(self, sentences):
        symbols = set()
        for sentence in sentences:
            for char in sentence:
                if char.isalpha() and char not in symbols:
                    symbols.add(char)
        return sorted(list(symbols))
    
    # Evaluates whether a given sentence is true under a given model.
    def pl_true(self, sentence, model):
        if sentence == 'True':
            return True
        elif sentence == 'False':
            return False
        elif len(sentence) == 1:
            return model[sentence]
        elif '=>' in sentence:
            lhs, rhs = sentence.split('=>')
            return (not self.pl_true(lhs, model)) or self.pl_true(rhs, model)
        elif '&' in sentence:
            lhs, rhs = sentence.split('&')
            return self.pl_true(lhs, model) and self.pl_true(rhs, model)
        elif '||' in sentence:
            lhs, rhs = sentence.split('||')
            return self.pl_true(lhs, model) or self.pl_true(rhs, model)
        elif '<=>' in sentence:
            lhs, rhs = sentence.split('<=>')
            return self.pl_true(lhs, model) == self.pl_true(rhs, model)
        elif '~' in sentence:
            negated_sentence = sentence[1:]
            return not self.pl_true(negated_sentence, model)
    
    # Recursively checks all the possible models to determine if the query can be inferred from the knowledge base
    def check_all(self, kb, query, symbols, model):
        if not symbols:
            if all(self.pl_true(kb_clause, model) for kb_clause in kb):
                return self.pl_true(query, model)
            else:
                return True
        else:
            p = symbols[0]
            rest = symbols[1:]
            return (self.check_all(kb, query, rest, {**model, p: True}) and
                    self.check_all(kb, query, rest, {**model, p: False}))
    
    def check(self):
        return self.check_all(self.kb, self.query, self.symbols.copy(), {})