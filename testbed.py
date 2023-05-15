from Algorithms.TruthTable import TruthTable
from Algorithms.ForwardChaining import ForwardChaining
from Algorithms.BackwardChaining import BackwardChaining
from Algorithms.Rete import Rete
from Algorithms.WalkSAT import WalkSAT
from Parse import Parse

def ttcheck():
    kb = '(~p2 | p3) & (~p3 | p1) & (~c | e) & (~b | ~e | f) & (~f | ~g | h) & (~p1 | d) & (~p1 | ~p3 | c) & a & b & p2'
    query = '~d'
    result = TruthTable.check(kb, query)
    #print(query)
    print(result)
    
def fccheck():
    filename = "Test-Files/test_HornKB.txt"
    kb, query = Parse.parse(filename)
    result = ForwardChaining.check(kb, query)
    #print(query)
    print(result)
    
def bccheck():
    # filename = "Test-Files/test_HornKB.txt"
    # kb, query = Parse.parse(filename)
    # print(kb)
    # print(query)
    kb = ['p2=>p3', 'p3=>p1', 'c=>e', 'b&e=>f', 'f&g=>h', 'p1=>d', 'p1&p3=>c', 'a', 'b', 'p2']
    query = ['d']
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
    filename = "Test-Files/test_genericKB.txt"
    kbtype = Parse.checktype(filename)
    print(kbtype)
    
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
    

#ttcheck()
#fccheck()
bccheck()
#retecheck()
#testparse()
#hftorbcheck()
#typecheck()
#walksatcheck()