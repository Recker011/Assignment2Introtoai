import re

class TruthTable:

    @staticmethod
    def check(kb, query):
        symbols = list(set(re.findall(r'[a-z]+[0-9]*', kb + query)))
        def evaluate(expression, values):
            for s in symbols:
                expression = expression.replace(s, str(values[s]))
            return eval(expression)
        models = 0
        for i in range(2**len(symbols)):
            values = {symbols[j]: (i >> j) & 1 for j in range(len(symbols))}
            if evaluate(kb, values):
                if evaluate(query, values):
                    models += 1
                else:
                    return 'NO'
        return f'YES:{models}'