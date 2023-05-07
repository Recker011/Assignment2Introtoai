class BackwardChaining:
    def __init__(self, kb, query):
        self.kb = [clause.toCNF() for clause in kb]
        self.query = query
        self.agenda = [query]
        self.count = {}
        self.inferred = {}
        self.symbols = self.get_symbols(self.kb + [query])
        for symbol in self.symbols:
            self.inferred[symbol] = False
        for clause in self.kb:
            if clause.connective == '&':
                for subclause in clause.subclauses:
                    if subclause.connective == '||':
                        self.count[subclause] = len(subclause.subclauses)
            elif clause.connective == '||':
                self.count[clause] = len(clause.subclauses)

    def get_symbols(self, sentences):
        symbols = set()
        for sentence in sentences:
            for char in sentence.clause:
                if char.isalpha() and char not in symbols:
                    symbols.add(char)
        return sorted(list(symbols))

    def check(self):
        while len(self.agenda) > 0:
            q = self.agenda.pop(0)
            if not self.inferred[q.clause]:
                self.inferred[q.clause] = True
                for clause in [c for c in self.kb if c.connective == '&' or c.connective == '||']:
                    if clause.connective == '&':
                        for subclause in clause.subclauses:
                            if subclause.connective == '||' and q.clause in subclause.clause:
                                if subclause in self.count:
                                    self.count[subclause] -= 1
                                if self.count[subclause] == 0:
                                    if clause.clause == self.query.clause:
                                        return 'YES'
                                    else:
                                        self.agenda.extend(clause.subclauses)
                    elif clause.connective == '||' and q.clause in clause.clause:
                        if clause in self.count:
                            self.count[clause] -= 1
                        if self.count[clause] == 0:
                            if clause.clause == self.query.clause:
                                return 'YES'
                            else:
                                self.agenda.extend(clause.subclauses)
        return 'NO'