from Sentence import Sentence

class KB:
    def __init__(self):
        self.sentences = []
        
    def tell(self, sentence):
        self.sentences.append(sentence)
        pass
    
    def ask(self):
        pass
    
    
    
    
sentence = Sentence('b<=>a')

kb = KB()

kb.tell(sentence)

kb.toCNF(kb.sentences[0])

print(kb.sentences[0].clause)







