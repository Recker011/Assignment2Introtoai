from TruthTable import TruthTable
from ForwardChaining import ForwardChaining
from BackwardChaining import BackwardChaining
from Parse import Parse

def ttcheck():
    kb = '((~a & c) | (~c & a) | (~d & c) | (~d & a)) & ((~a & d) | (~c & d) | (~c & a) | (~d & a))'
    query = '~d & (~g | ~f)'
    result = TruthTable.check(kb, query)
    #print(query)
    print(result)
    
def fccheck():
    filename = "test_HornKB.txt"
    kb, query = Parse.parse(filename)
    result = ForwardChaining.check(kb, query)
    #print(query)
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
    
ttcheck()
#fccheck()
#bccheck()
#testparse()
#typecheck()