class BackwardChaining:
    def __init__(self, kb, query):
        self.kb = [clause.toCNF() for clause in kb]
        self.query = query
        self.agenda = [query]
        self.inferred = {}
        self.symbols = self.get_symbols(kb + [query])
        for symbol in self.symbols:
            self.inferred[symbol] = False

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
            print(f"Processing query: {q.clause}")
            if not self.inferred[q.clause]:
                print(f"Inferred[{q.clause}] is False")
                self.inferred[q.clause] = True
                for clause in [c for c in self.kb if c.connective == '&']:
                    print(f"Processing clause: {clause.clause}")
                    for subclause in clause.subclauses:
                        print(f"Processing subclause: {subclause.clause}")
                        if subclause.connective == '||' and q.clause in subclause.clause:
                            print(f"Found subclause: {subclause.clause}")
                            if all(self.inferred[symbol] for symbol in subclause.symbols):
                                print(f"All symbols in subclause are inferred")
                                if subclause.clause == self.query.clause:
                                    return 'YES'
                                else:
                                    self.agenda.append(subclause)
                                    print(f"Adding {subclause.clause} to agenda")
        return 'NO'