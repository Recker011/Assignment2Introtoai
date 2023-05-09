from Sentence import Sentence
from TTchecking import TTchecking


class KB:
    def __init__(self):
        self.clauses = []

    def tell(self, sentence):
        self.clauses.append(Sentence(sentence))

    def ask(self, query):
        query_sentence = Sentence(query)
        return TTchecking(self.clauses, query_sentence).check()