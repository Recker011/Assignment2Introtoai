from Sentence import Sentence


class KB:
    def __init__(self):
        self.clauses = []
        self.symbols = []

    def tell(self, sentence):
        new_sentence = Sentence(sentence)
        self.clauses.append(new_sentence)
        for symbol in new_sentence.symbols:
            if symbol not in self.symbols:
                self.symbols.append(symbol)

    def get_clauses(self):
        return self.clauses
    
    def get_symbols(self):
        return self.symbols
    
    def get_symbols(self):
        
        symbols = set()
        for char in self.clause:
            if char.isalpha() and char not in symbols:
                symbols.add(char)
        return list(symbols)