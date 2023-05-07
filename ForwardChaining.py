from Sentence import Sentence

class ForwardChaining:
    def __init__(self, kb, query):
        self.kb = kb
        self.query = query

    def check(self):
        count = {}
        inferred = {}
        agenda = []

        for clause in self.kb:
            if len(clause.subclauses) == 0:
                agenda.append(clause.clause)
            else:
                count[clause] = len(clause.subclauses)

        while agenda:
            p = agenda.pop(0)
            if p == self.query.clause:
                return 'YES'
            if p not in inferred:
                inferred[p] = True
                for clause in self.kb:
                    if p in [subclause.clause for subclause in clause.subclauses]:
                        count[clause] -= 1
                        if count[clause] == 0:
                            if clause.connective == '=>':
                                agenda.append(clause.subclauses[-1].clause)
                            else:
                                agenda.append(clause.clause)
        return 'NO'