from itertools import product
from Sentence import Sentence

class TTchecking:
    def __init__(self, kb, query):
        self.kb = kb
        self.query = query
        self.symbols = self.get_symbols(kb + [query])
        self.model = {}

    def get_symbols(self, sentences):
        symbols = set()
        for sentence in sentences:
            for char in sentence.clause:
                if char.isalpha() and char not in symbols:
                    symbols.add(char)
        return list(symbols)

    def check_all(self, kb, query, symbols, model):
        if not symbols:
            if self.pl_true(kb, model):
                return self.pl_true(query, model)
            else:
                return True
        else:
            p = symbols[0]
            rest = symbols[1:]
            return (self.check_all(kb, query, rest, {**model, p: True}) and
                    self.check_all(kb, query, rest, {**model, p: False}))

    def pl_true(self, sentence, model):
        if isinstance(sentence, list):
            return all(self.pl_true(s, model) for s in sentence)
        elif sentence.clause[0] == '~':
            return not self.pl_true(Sentence(sentence.clause[1:]), model)
        elif '&' in sentence.clause:
            left_clause = Sentence(sentence.clause.split('&')[0])
            right_clause = Sentence('&'.join(sentence.clause.split('&')[1:]))
            return self.pl_true(left_clause, model) and self.pl_true(right_clause, model)
        elif '|' in sentence.clause:
            left_clause = Sentence(sentence.clause.split('|')[0])
            right_clause = Sentence('|'.join(sentence.clause.split('|')[1:]))
            return self.pl_true(left_clause, model) or self.pl_true(right_clause, model)
        else:
            return model.get(sentence.clause)

    def check(self):
        return self.check_all(self.kb, self.query, self.symbols, {})