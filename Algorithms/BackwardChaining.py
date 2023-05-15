class BackwardChaining:
    @staticmethod
    def check(KB, q):
        # Initialize the inferred dictionary
        inferred = {}
        for clause in KB:
            if "=>" in clause:
                premise, conclusion = clause.split("=>")
                inferred[conclusion.strip()] = False
            else:
                inferred[clause.strip()] = False
        # Initialize the entailed list
        entailed = []
        # Call the recursive BC function
        result = BackwardChaining.BC(KB, q[0], inferred, entailed)
        if result:
            return "YES: " + ", ".join(entailed)  # outputs the YES and order of entailed facts
        else:
            return "NO"

    @staticmethod
    def BC(KB, q, inferred, entailed):
        # Check if the query is already known to be true or if it's a fact in the KB
        if inferred[q] or q in KB:
            return True
        # Find all implications with q as the conclusion
        implications = [clause for clause in KB if "=>" in clause and clause.split("=>")[1].strip() == q]
        for implication in implications:
            # Split the implication into premise and conclusion
            premise, conclusion = implication.split("=>")
            # Check if all premises are true
            premises = premise.split("&")
            all_true = True
            for p in premises:
                # Recursively call BC on each premise
                if not BackwardChaining.BC(KB, p.strip(), inferred, entailed):
                    all_true = False
                    break
            # If all premises are true
            if all_true:
                # Add q to the entailed list and mark it as inferred
                entailed.append(q)
                inferred[q] = True
                return True
        return False

