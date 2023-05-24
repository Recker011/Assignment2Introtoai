from Parse import Parse

class Rete:
    @staticmethod
    def implies(fact):
        # Returns the right side of the implication if it exists
        return fact.split('=>')[1] if '=>' in fact else None

    @staticmethod
    def entails(fact):
        # Returns the left side of the implication as a set if it exists
        return set(fact.split('=>')[0].split('&')) if '=>' in fact else set()

    @staticmethod
    def is_fact(fact):
        # Returns True if the fact is not an implication
        return '=>' not in fact

    @staticmethod
    def check(KB, query):
        # Initialize agenda with facts from KB
        agenda = [fact for fact in KB if Rete.is_fact(fact)]
        inferred = {}
        entailed_facts = []
        kbtype = Parse.checkkbtype(KB)
        if kbtype == "HC":
            # Initialize network with facts from KB
            network = {}
            for fact in KB:
                premises = Rete.entails(fact)
                for premise in premises:
                    if premise not in network:
                        network[premise] = []
                    network[premise].append(fact)

            # Initialize agenda with facts from KB
            agenda = [fact for fact in KB if Rete.is_fact(fact)]
            inferred = {}
            entailed_facts = []

        while agenda:
            p = agenda.pop(0)

            # If p matches the query, return YES with entailed facts
            if p == query[0]:
                entailed_facts.append(p)
                return f'YES: {", ".join(entailed_facts)}'

            inferred[p] = True

            if p in network:
                for fact in network[p]:
                    premises = Rete.entails(fact)
                    # If all premises are inferred, add the implication to entailed facts and agenda
                    if all(inferred.get(premise) for premise in premises):
                        q = Rete.implies(fact)
                        if q and not inferred.get(q):
                            entailed_facts.append(q)
                            agenda.append(q)
            return 'NO'
        else:
            return "The Knowledge Base is not in Horn Clause format"
