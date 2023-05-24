from Algorithms.TruthTable import TruthTable
from Algorithms.ForwardChaining import ForwardChaining
from Algorithms.BackwardChaining import BackwardChaining
from Algorithms.Rete import Rete
from Algorithms.WalkSAT import WalkSAT
from Algorithms.Resolution import Resolution
from Sentence import Sentence
from Parse import Parse

def ttcheck():
    kb = '((~a | ~c | ~d) & (a | c) & b & (~b | a) & c & (~f | g))'
    query = '~d & (g | ~f)'
    result = TruthTable.check(kb, query)
    #print(query)
    print(result)
    
def fccheck():
    filename = "Test-Files/test_Horn1.txt"
    kb, query = Parse.parse(filename)
    result = ForwardChaining.check(kb, query)
    #print(query)
    print(result)
    
def bccheck():
    filename = "Test-Files/test_HornKB.txt"
    kb, query = Parse.parse(filename)
    # print(kb)
    # print(query)
    # kb = ['p2=>p3', 'p3=>p1', 'c=>e', 'b&e=>f', 'f&g=>h', 'p1=>d', 'p1&p3=>c', 'a', 'b', 'p2']
    # query = ['d']
    result = BackwardChaining.check(kb, query)
    print(result)
    
def retecheck():
    filename = "Test-Files/test_HornKB.txt"
    kb, query = Parse.parse(filename)
    rules, new_query = Parse.HFtoRB(kb, query)
    result = Rete.check(rules, new_query)
    print(result)
    
def testparse():
    filename = "Test-Files/test_HornKB.txt"
    kb, query = Parse.parse(filename)
    print('KB:', kb)
    print('Query:', query)
    
def typecheck():
    kb = '(~p2 | p3) & (~p3 | p1) & (~c | e) & (~b | ~e | f) & (~f | ~g | h) & (~p1 | d) & (~p1 | ~p3 | c) & a & b & p2'
    kbtype = Parse.checkkbtype(kb)
    print(kbtype)

def checkfiletype():
    filename = 'Test-Files/test_HornKB.txt'
    print(Parse.checkfiletype(filename))
    
    
def hftorbcheck():
    filename = "Test-Files/test_HornKB.txt"
    kb, query = Parse.parse(filename)
    rules, new_query = Parse.HFtoRB(kb, query)
    print(rules)
    print(query)
    
def walksatcheck():
    kb = '(~p2 | p3) & (~p3 | p1) & (~c | e) & (~b | ~e | f) & (~f | ~g | h) & (~p1 | d) & (~p1 | ~p3 | c) & a & b & p2'
    query = 'd'
    print(WalkSAT.check(kb, query))
    
def sentencecheck():
    filename = "Test-Files/test_HornKB.txt"
    kb, query = Sentence.parse(filename)
    print(f"KB:{kb}\nQuery:{query}")

def resolutioncheck():
    kb = '(~p2 | p3) & (~p3 | p1) & (~c | e) & (~b | ~e | f) & (~f | ~g | h) & (~p1 | d) & (~p1 | ~p3 | c) & a & b & p2'
    query = 'd'
    print(Resolution.check(kb, query))

#ttcheck()
#fccheck()
#bccheck()
#retecheck()
#testparse()
#hftorbcheck()
#typecheck()
#walksatcheck()
#checkfiletype()
#sentencecheck()
resolutioncheck()