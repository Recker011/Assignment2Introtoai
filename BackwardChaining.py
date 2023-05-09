from Sentence import Sentence

class BackwardChaining:
    def __init__(self, kb, query):
        self.kb = kb
        self.query = query
        self.agenda = [query.clause]
        self.counts = {}
        self.inferred = {}
        self.clauses = []
        for sentence in kb:
            sentence = sentence.toCNF()
            if '=>' in sentence.clause:
                lhs, rhs = sentence.clause.split('=>')
                lhs = lhs.strip('()')
                if '&' in lhs:
                    premises = lhs.split('&')
                else:
                    premises = [lhs]
                self.clauses.append((premises, rhs))
                if rhs not in self.counts:
                    self.counts[rhs] = 0
                self.counts[rhs] += 1
            else:
                self.agenda.append(sentence.clause)
        print(f"Initial agenda: {self.agenda}")
        print(f"Initial counts: {self.counts}")
        print(f"Clauses: {self.clauses}")

    def check(self):
        while self.agenda:
            p = self.agenda.pop(0)
            print(f"Processing: {p}")
            if p == self.query.clause:
                return 'YES'
            if p not in self.inferred:
                self.inferred[p] = True
                for clause in self.clauses:
                    premises, rhs = clause
                    if p in premises:
                        print(f"Reducing count for {rhs}")
                        self.counts[rhs] -= 1
                        if self.counts[rhs] == 0:
                            print(f"Adding {rhs} to agenda")
                            self.agenda.append(rhs)
        return 'NO'

    def get_symbols(self, sentence):
        symbols = []
        for char in sentence:
            if char.isalpha() and char not in symbols:
                symbols.append(char)
        return symbols