from Parse import Parse

class ForwardChaining:
    @staticmethod
    def check(kb, q):
        kbtype = Parse.checkkbtype(kb)
        if kbtype == "HC":
            # Initialize the count of premises for each implication
            count = {}
            # Initialize the inferred dictionary
            inferred = {}
            # Initialize the agenda with known facts
            agenda = []
            for clause in kb:
                # Check if the clause is an implication
                if "=>" in clause:
                    # Split the clause into premise and conclusion
                    premise, conclusion = clause.split("=>")
                    # Count the number of premises
                    count[conclusion.strip()] = len(premise.split("&"))
                    inferred[conclusion.strip()] = False
                else:
                    # Add the fact to the agenda
                    agenda.append(clause.strip())
                    inferred[clause.strip()] = True
            # Initialize the entailed list
            entailed = []
            while agenda:
                # Pop the first symbol from the agenda
                p = agenda.pop(0)
                # Add the symbol to the entailed list
                entailed.append(p)
                # Check if the symbol is the query
                if p == q[0]:
                    return "YES: " + ", ".join(entailed) # outputs YES and order of entailed facts
                # For each implication in the kb
                for clause in kb:
                    if "=>" in clause:
                        premise, conclusion = clause.split("=>")
                        # If p is one of the premises
                        if p in premise.split("&"):
                            # Decrease the count of premises for this implication
                            count[conclusion.strip()] -= 1
                            # If all premises are true
                            if count[conclusion.strip()] == 0:
                                # Add the conclusion to the agenda
                                if not inferred[conclusion.strip()]:
                                    agenda.append(conclusion.strip())
                                    inferred[conclusion.strip()] = True
            return "NO"
        else:
            return "The Knowledge Base is not in Horn Clause format"
