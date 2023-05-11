from TruthTable import TruthTable
from ForwardChaining import ForwardChaining
from BackwardChaining import BackwardChaining
from Parse import Parse

def ttcheck():
    kb = '(~p2 | p3) & (~p3 | p1) & (~c | e) & (~b | ~e | f) & (~f | ~g | h) & (~p1 | d) & (~p1 | ~p3 | c) & a & b & p2'
    query = 'd'
    result = TruthTable.check(kb, query)
    print(result)
    
def fccheck():
    filename = "test_HornKB.txt"
    kb, query = Parse.parse(filename)
    result = ForwardChaining.check(kb, query)
    print(result)
    
def bccheck():
    filename = "test_HornKB.txt"
    kb, query = Parse.parse(filename)
    result = BackwardChaining.check(kb, query)
    print(result)
    
def testparse():
    filename = "test_HornKB.txt"
    kb, query = Parse.parse(filename)
    print('KB:', kb)
    print('Query:', query)
    
def typecheck():
    filename = "test_genericKB.txt"
    kbtype = Parse.checktype(filename)
    print(kbtype)
    
#ttcheck()
#fccheck()
#bccheck()
#testparse()
typecheck()