from itertools import product

class TTchecking:
    def __init__(self, kb, query):
        self.kb = kb
        self.query = query
        self.symbols = self.get_symbols(kb + [query])
        self.num_models = 0
        self.memo = {}

    def get_symbols(self, sentences):
        symbols = set()
        for sentence in sentences:
            for char in sentence.clause:
                if char.isalpha() and char not in symbols:
                    symbols.add(char)
        return sorted(list(symbols))

    def pl_true(self, sentence, model):
        if sentence in self.memo:
            return self.memo[sentence]
        if sentence.clause == 'True':
            return True
        elif sentence.clause == 'False':
            return False
        elif len(sentence.clause) == 1:
            return model[sentence]
        elif sentence.connective == '=>':
            lhs, rhs = sentence.subclauses
            result = (not self.pl_true(lhs, model)) or self.pl_true(rhs, model)
            self.memo[sentence] = result
            return result
        elif sentence.connective == '&':
            lhs, rhs = sentence.subclauses
            result = self.pl_true(lhs, model) and self.pl_true(rhs, model)
            self.memo[sentence] = result
            return result
        elif sentence.connective == '||':
            lhs, rhs = sentence.subclauses
            result = self.pl_true(lhs, model) or self.pl_true(rhs, model)
            self.memo[sentence] = result
            return result
        elif sentence.connective == '<=>':
            lhs, rhs = sentence.subclauses
            result = self.pl_true(lhs, model) == self.pl_true(rhs, model)
            self.memo[sentence] = result
            return result
        elif sentence.connective == '~':
            negated_sentence = sentence.subclauses[1:]
            result = not self.pl_true(negated_sentence, model)
            self.memo[sentence] = result
            return result

    def check_all(self, kb, query, symbols, model):
        if not symbols:
            if all(self.pl_true(kb_clause, model) for kb_clause in kb):
                self.num_models += 1
                return self.pl_true(query, model)
            else:
                return True
        else:
            p = symbols[0]
            rest = symbols[1:]
            return (self.check_all(kb, query, rest, {**model, p: True}) and 
                    self.check_all(kb, query, rest,{**model,p: False}))

    def check(self):
        if self.check_all(self.kb,self.query,self.symbols.copy(),{}):
            return f'YES'
        else:
            return 'NO'