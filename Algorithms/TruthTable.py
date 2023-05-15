import re

class TruthTable:
    @staticmethod
    def check(kb, query):
        # Extract all symbols from the knowledge base and query
        symbols = list(set(re.findall(r'[a-z]+[0-9]*', kb + query)))

        def evaluate(expression, values):
            # Replace symbols in the expression with their corresponding values
            for s in symbols:
                expression = expression.replace(s, str(values[s]))
            # Replace ~ with not and add a space after it
            expression = expression.replace('~', 'not ')
            # Replace & with and and | with or
            expression = expression.replace('&', ' and ').replace('|', ' or ')
            # Evaluate the resulting expression
            try:
                return eval(expression)
            except Exception as e:
                print(f"An error occurred while evaluating the expression: {e}")
                return False

        models = 0
        # Iterate over all possible combinations of truth values for the symbols
        for i in range(2**len(symbols)):
            # Assign truth values to symbols based on the current iteration
            values = {symbols[j]: (i >> j) & 1 for j in range(len(symbols))}
            # Check if the knowledge base is true with the current truth values
            if evaluate(kb, values):
                # Check if the query is also true with the current truth values
                if evaluate(query, values):
                    models += 1
                else:
                    return 'NO'
        return f'YES:{models}'
