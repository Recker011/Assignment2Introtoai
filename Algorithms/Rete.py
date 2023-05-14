class Rete:
    
    def implies(fact):
        return fact.split('=>')[1] if '=>' in fact else None

    
    def entails(fact):
        return set(fact.split('=>')[0].split('&')) if '=>' in fact else set()

    
    def is_fact(fact):
        return '=>' not in fact

    @staticmethod
    def check(KB, query):
        agenda = [fact for fact in KB if Rete.is_fact(fact)]
        inferred = {}
        entailed_facts = []

        while agenda:
            p = agenda.pop(0)

            if p == query[0]:
                entailed_facts.append(p)
                return f'YES: {", ".join(entailed_facts)}'

            inferred[p] = True

            for fact in KB:
                premises = Rete.entails(fact)
                if all(inferred.get(premise) for premise in premises):
                    q = Rete.implies(fact)
                    if q and not inferred.get(q):
                        entailed_facts.append(q)
                        agenda.append(q)
        return 'NO'
