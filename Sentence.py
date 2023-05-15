import re


class Sentence:
    def __init__(self, clause, connective=None):
        self.clause = clause
        self.connective = connective
        self.subclauses = []

    def parsesentence(self):
        
        #Keep track of which bracket layer it is currently at and get position of outermost connective
        bracketcounter = 0
        connectiveind = -1

        
        #check for connective position
        for i in range(len(self.clause)):  

            if self.clause[i] == '(':
                bracketcounter = bracketcounter + 1
            elif self.clause[i] == ')':
                bracketcounter = bracketcounter - 1
            elif ((self.clause[i] == '<') and bracketcounter == 0) and connectiveind < 0:
                connectiveind = i
            elif (self.clause[i] == '=' and self.clause[i + 1] == '>') and bracketcounter == 0 and connectiveind < 0:
                connectiveind = i
            elif ((self.clause[i] == '&') and bracketcounter == 0) and connectiveind < 0:
                connectiveind = i
            elif ((self.clause[i] == '|') and bracketcounter == 0) and connectiveind < 0:
                connectiveind = i
            elif (self.clause[i] == '~') and self.clause[i+1] == '(' and self.clause[-1] == ')' or len(self.clause) == 2:
                connectiveind = i

        #Remove negligible brackets
        if connectiveind < 0:
            if self.clause[0] == '(' and self.clause[-1] == ')':
                self.clause = (self.clause[1:(len(self.clause)) - 1])
                self.parsesentence()

        #Create subclauses with respective connective
        else:
            if self.clause[connectiveind] == '<':
                lhs = self.clause[0:connectiveind]
                rhs = self.clause[connectiveind + 3: len(self.clause)]
                Sub1 = Sentence(lhs)
                Sub2 = Sentence(rhs)
                self.subclauses.append(Sub1)
                self.subclauses.append(Sub2)
                self.connective = '<=>'

            elif self.clause[connectiveind] == '=':
                lhs = self.clause[0:connectiveind]
                rhs = self.clause[connectiveind + 2: len(self.clause)]
                Sub1 = Sentence(lhs)
                Sub2 = Sentence(rhs)
                self.subclauses.append(Sub1)
                self.subclauses.append(Sub2)
                self.connective = '=>'

            elif self.clause[connectiveind] == '&':
                lhs = self.clause[0:connectiveind]
                rhs = self.clause[connectiveind + 1: len(self.clause)]
                Sub1 = Sentence(lhs)
                Sub2 = Sentence(rhs)
                self.subclauses.append(Sub1)
                self.subclauses.append(Sub2)
                self.connective = '&'

            elif self.clause[connectiveind] == '|':
                lhs = self.clause[0:connectiveind]
                rhs = self.clause[connectiveind + 2: len(self.clause)]
                Sub1 = Sentence(lhs)
                Sub2 = Sentence(rhs)
                self.subclauses.append(Sub1)
                self.subclauses.append(Sub2)
                self.connective = '||'

            elif self.clause[connectiveind] == '~':
                symbol = self.clause[connectiveind + 1:len(self.clause)]
                Sub1 = Sentence(symbol)
                self.subclauses.append(Sub1)
                self.connective = '~'

    def toCNF(self):
        self.parsesentence()

        #Apply biconditional elimination if equivalence connective is found
        if self.connective == '<=>':
            self = self.bicon_elim()
            return self.toCNF()

        #Apply implication elimination if equivalence connective is found
        elif self.connective == '=>':
            self = self.implication_elim()
            if '~~' in self.clause:
                self = self.doublenegation_elim()
            return self.toCNF()

        #Check if deMorgan is applicable and if double negation can be applied
        elif self.connective == '~':
            result = self.subclauses[0].toCNF()
            result.parsesentence()
            deMorgan_result = result.deMorgan()
            self = deMorgan_result.doublenegation_elim()
            return self.toCNF()

        elif self.connective == '&':
            #Split subclauses and convert to cnf separately
            
            lhs = self.subclauses[0].toCNF()
            rhs = self.subclauses[1].toCNF()

            #Check if distributivity and associativity can be applied to either side
            lhs.distributivity_conjunction()
            lhs.associativity_disjunction()
            rhs.distributivity_conjunction()
            rhs.associativity_disjunction()

            #Go through bracket cases to decide what bracket format should be applied to the clause
            if len(lhs.clause) <= 2 and len(rhs.clause) <= 2:
                self = Sentence('({}&{})'.format(
                    lhs.clause, rhs.clause), '&')
            elif len(lhs.clause) <= 2:
                self = Sentence('{}&({})'.format(
                    lhs.clause, rhs.clause), '&')
            elif len(rhs.clause) <= 2:
                self = Sentence('({})&{}'.format(
                    lhs.clause, rhs.clause), '&')
            else:
                self = Sentence('{}&{}'.format(
                    lhs.clause, rhs.clause), '&')

            return self

        elif self.connective == '||':
            #Split subclauses and convert to cnf separately
            
            lhs = self.subclauses[0].toCNF()
            rhs = self.subclauses[1].toCNF()

            #Go through bracket cases to decide what bracket format should be applied to the clause
            if len(lhs.clause) <= 2 and len(rhs.clause) <= 2:
                self = Sentence('({}||{})'.format(
                    lhs.clause, rhs.clause), '||')
            elif len(lhs.clause) <= 2:
                self = Sentence('{}||({})'.format(
                    lhs.clause, rhs.clause), '||')
            elif len(rhs.clause) <= 2:
                self = Sentence('({})||{}'.format(
                    lhs.clause, rhs.clause), '||')
            else:
                self = Sentence('{}||{}'.format(
                    lhs.clause, rhs.clause), '||')

            return self

        else:
            return self  #If single literal then return itself

    def bicon_elim(self):
        #Apply biconditional elimination [  a <=> b ------> a=>b & b=>a   ]
        
        eliminated_sentence = '({}=>{})'.format(
            self.subclauses[0].clause, self.subclauses[1].clause) + '&' + '({}=>{})'.format(self.subclauses[1].clause, self.subclauses[0].clause)
        result = Sentence(eliminated_sentence)
        return result

    def implication_elim(self):
        #Apply implication elimination [  a => b ------> ~a || b   ]
        
        eliminated_sentence = '~{}||{}'.format(
            self.subclauses[0].clause, self.subclauses[1].clause)
        result = Sentence(eliminated_sentence)
        return result

    def deMorgan(self):
        #Apply deMorgan's law [  ~(a || b) ------> (~a & ~b)   ] OR [  ~(a & b) ------> (~a || ~b)   ]
        
        if self.connective == '&':
            result = Sentence('~{}||~{}'.format(
                self.subclauses[0].clause, self.subclauses[1].clause), '||')
            return result
        if self.connective == '||':
            result = Sentence('~{}&~{}'.format(
                self.subclauses[0].clause, self.subclauses[1].clause), '&')
            return result

    def doublenegation_elim(self):
        #Apply double negation elimination [  ~~a ------> a  ]
        
        negated_clause = Sentence(
            self.clause.replace('~~', ''), self.connective)
        return negated_clause

    def distributivity_conjunction(self):
        #Apply distributivity of & over || [  a || (b & c)  ------> (a || b) & (a || c)  ]
        
        self.parsesentence()

        if self.connective == '||':
            lhs = self.subclauses[0]
            rhs = self.subclauses[1]
            if len(lhs.clause) > 1:
                lhs.parsesentence()
                if lhs.connective == '&':
                    self.clause = '({}||{})&({}||{})'.format(
                        rhs.clause, lhs.subclauses[0].clause, rhs.clause, lhs.subclauses[1].clause)
            elif len(rhs.clause) > 1:
                rhs.parsesentence()
                if rhs.connective == '&':
<<<<<<< HEAD
                    self.clause = '({}||{})&({}||{})'.format(
                        lhs.clause, rhs.subclauses[0].clause, lhs.clause, rhs.subclauses[1].clause)

    def associativity_disjunction(self):
        #Apply associativity of ||  [  a || (b || c)  ------> (a || b || c)  ]
        
        self.parsesentence()
        if self.connective == '||':
            lhs = self.subclauses[0]
            rhs = self.subclauses[1]
            if len(lhs.clause) > 1 and lhs.clause[0] != '~':
                lhs.parsesentence()
                if lhs.connective == '||':
                    self.clause = '({}||{}||{})'.format(
                        rhs.clause, lhs.subclauses[0].clause, lhs.subclauses[1].clause)
            elif len(rhs.clause) > 1 and rhs.clause[0] != '~':
                rhs.parsesentence()
                if rhs.connective == '||':
                    self.clause = '({}||{}||{})'.format(
                        lhs.clause, rhs.subclauses[0].clause, rhs.subclauses[1].clause)
                    

sentence = Sentence('(a<=>(c=>~d))&b&(b=>a)')

sentence = sentence.toCNF()

print(sentence.clause)

# '(a<=>(c=>~d))&b&(b=>a)'
# 'a<=>(b<=>c)'
=======
                    self.clause = '(({}||{})&({}||{}))'.format(lhs.clause, rhs.subclauses[0].clause, lhs.clause, rhs.subclauses[1].clause)
                    
    def parse(filename):
        
        pass
>>>>>>> cc9a825e8f0b9fe95dfcf186e7b07475c46d0e1f
