import random

class WalkSAT:
    
    @staticmethod
    def check(kb, query, max_flips=1000, p=0.5):
        # Convert KB and query to CNF
        kb = kb.split('&')
        kb = [clause.strip().replace('(', '').replace(')', '').split('|') for clause in kb]
        kb = [[literal.strip() for literal in clause] for clause in kb]
        query = query.split('&')
        query = [clause.strip().replace('(', '').replace(')', '').split('|') for clause in query]
        query = [[literal.strip() for literal in clause] for clause in query]

        # Get all symbols
        symbols = set()
        for clause in kb:
            for literal in clause:
                symbols.add(literal.strip().replace('~', ''))
        for clause in query:
            for literal in clause:
                symbols.add(literal.strip().replace('~', ''))
        symbols = list(symbols)

        # Initialize model randomly
        model = {symbol: random.choice([True, False]) for symbol in symbols}

        # Evaluate clauses
        def evaluate_clause(clause, model):
            for literal in clause:
                if literal.startswith('~'):
                    if not model[literal[1:]]:
                        return True
                else:
                    if model[literal]:
                        return True
            return False

        # Evaluate KB and query
        def evaluate(kb, query, model):
            for clause in kb:
                if not evaluate_clause(clause, model):
                    return False
            for clause in query:
                if not evaluate_clause(clause, model):
                    return False
            return True

        # WalkSAT algorithm
        for i in range(max_flips):
            if evaluate(kb, query, model):
                return 'YES'
            false_clauses = [clause for clause in kb + query if not evaluate_clause(clause, model)]
            clause = random.choice(false_clauses)
            if random.random() < p:
                symbol = random.choice(list(model.keys()))
            else:
                min_false = float('inf')
                best_symbol = None
                for literal in clause:
                    symbol = literal.replace('~', '')
                    model[symbol] = not model[symbol]
                    false_count = sum([not evaluate_clause(c, model) for c in kb + query])
                    if false_count < min_false:
                        min_false = false_count
                        best_symbol = symbol
                    model[symbol] = not model[symbol]
                symbol = best_symbol
            model[symbol] = not model[symbol]
        return 'NO'