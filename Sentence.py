import re


class Sentence:
    def __init__(self, clause, connective = None):
        self.clause = clause
        self.connective = connective
        self.subclauses = []

    def parsesentence(self):
    
        bracketcounter = 0
        connectiveind = -1
                 
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
            
        if connectiveind < 0:
            if self.clause[0] == '(' and self.clause[-1] == ')':
                self.clause = (self.clause[1:(len(self.clause)) - 1])
                self.parsesentence()                 
                    
               
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
                
    
    def printClauses(self):
        print('Original Sentence: ' + self.clause)
        
        if len(self.subclauses) > 1:
            print('Left : {}    Connective: {}     Right: {}'.format(self.subclauses[0].clause,self.connective, self.subclauses[1].clause))
            for i in self.subclauses:
                i.parsesentence()
                i.printClauses()
            
        elif len(self.subclauses) == 1:
            print("Symbol:   {}".format(self.subclauses[0]))
            print("Connective:  {}".format(self.connective))
            
    
    def toCNF(self):
        
        self.parsesentence()
                       
        if self.connective == '<=>':
            eliminated = self.bicon_elim()

            return eliminated.toCNF()
                                
        elif self.connective == '=>':
            eliminated = self.implication_elim()
            
            if '=>' in eliminated.clause:
                return eliminated.toCNF()
            else:
                neg_check = eliminated.doublenegation_elim()
                return neg_check
            
        elif self.connective == '~':
            result = self.subclauses[0].toCNF()
            result.parsesentence()         
            deMorgan_result = result.deMorgan()        
            doublenegated_result = deMorgan_result.doublenegation_elim()
            return doublenegated_result
                                            
        elif self.connective == '&':
            lhs = self.subclauses[0]
            rhs = self.subclauses[1]
            result_lhs = lhs.toCNF()
            result_rhs = rhs.toCNF()
            
            if len(result_lhs.clause) > 1 and len(result_rhs.clause) > 1 and '(' not in result_lhs.clause:
                final = Sentence('({})&({})'.format(result_lhs.clause, result_rhs.clause), '&')
            elif len(result_lhs.clause) > 1 and '(' not in result_lhs.clause:
                final = Sentence('({})&{}'.format(result_lhs.clause, result_rhs.clause), '&')
            elif len(result_rhs.clause) > 1 and '(' not in result_rhs.clause:
                final = Sentence('{}&({})'.format(result_lhs.clause, result_rhs.clause), '&')
            else:
                final = Sentence('{}&{}'.format(result_lhs.clause, result_rhs.clause), '&')
            
            a = re.split(r'&\s*(?![^()]*\))', final.clause)
            
            final.clause = ""
            
            for i in a:
                i = Sentence(i)
                i.distributivity_conjunction()
                print(i.clause)    
                final.clause = final.clause + i.clause

            return final
            
                    
        elif self.connective == '||':
            lhs = self.subclauses[0]
            rhs = self.subclauses[1]
            
            if '=>' in lhs.clause or '<=>' in lhs.clause:
                result_lhs = lhs.toCNF()
            else:
                result_lhs = lhs
            if '=>' in rhs.clause or '<=>' in rhs.clause:
                result_rhs = rhs.toCNF()
            else:
                result_rhs = rhs
                  
            if len(result_lhs.clause) > 2 and len(result_rhs.clause) > 2 and '(' not in result_lhs.clause:
                final = Sentence('({})||({})'.format(result_lhs.clause, result_rhs.clause), '||')
            elif len(result_lhs.clause) > 2 and '(' not in result_lhs.clause:
                final = Sentence('({})||{}'.format(result_lhs.clause, result_rhs.clause), '||')
            elif len(result_rhs.clause) > 2 and '(' not in result_rhs.clause:
                final = Sentence('{}||({})'.format(result_lhs.clause, result_rhs.clause), '||')
            else:
                final = Sentence('{}||{}'.format(result_lhs.clause, result_rhs.clause), '||')       
            return final                                   
        else:
            return self 
        
    
    def bicon_elim(self):      
        eliminated_sentence = '({}=>{})'.format(self.subclauses[0].clause,self.subclauses[1].clause) + '&' +  '({}=>{})'.format(self.subclauses[1].clause,self.subclauses[0].clause)
        result = Sentence(eliminated_sentence)
        
        return result

    def implication_elim(self):
        eliminated_sentence = '~{}||{}'.format(self.subclauses[0].clause,self.subclauses[1].clause)
        result = Sentence(eliminated_sentence)
        return result
    
    def deMorgan(self):
        
        if self.connective == '&':
            result = Sentence('~{}||~{}'.format(self.subclauses[0].clause, self.subclauses[1].clause), '||')
            return result
        if self.connective == '||':
            result = Sentence('~{}&~{}'.format(self.subclauses[0].clause, self.subclauses[1].clause), '&')
            return result
    
    def doublenegation_elim(self):
        negated_clause = Sentence(self.clause.replace('~~', ''), self.connective)
        return negated_clause
        
    def distributivity_conjunction(self):
        self.parsesentence()
        if self.connective == '||':
            lhs = self.subclauses[0]
            rhs = self.subclauses[1]
            if len(lhs.clause) > 1:
                lhs.parsesentence()
                if lhs.connective == '&':
                    self.clause = '(({}||{})&({}||{}))'.format(rhs.clause, lhs.subclauses[0].clause, rhs.clause, lhs.subclauses[1].clause)
            elif len(rhs.clause) > 1:
                rhs.parsesentence()
                if rhs.connective == '&':
                    self.clause = '(({}||{})&({}||{}))'.format(lhs.clause, rhs.subclauses[0].clause, lhs.clause, rhs.subclauses[1].clause)
                
        
    
#sentence = Sentence('(a<=>(c=>~d))')

#sentence = sentence.toCNF()

#print(sentence.clause)

#'~a||(~c||~d)&(c&d)||a&b&(~b||a)'











    



   





    
    


