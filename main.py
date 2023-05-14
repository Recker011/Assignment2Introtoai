from Algorithms.TruthTable import TruthTable
from Algorithms.ForwardChaining import ForwardChaining
from Algorithms.BackwardChaining import BackwardChaining
from Parse import Parse
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python iengine.py [method] [filename]")
        sys.exit(1)

    method = sys.argv[1]
    filename = sys.argv[2]
    
    kbtype = Parse.checktype(filename)
    
    if kbtype == 'HC':
        kb, query = Parse.parse(filename)
    elif kbtype == 'GK':
        # put the kb and query from sentence parsing from the sentence class i legit have no clue how that works i am mortally scared of messing with that class
        pass
    
    

    if method == 'TT':
        result = TruthTable.check(kb, query)
    elif method == 'FC':
        result = ForwardChaining.check(kb, query)
    elif method == 'BC':
        result = BackwardChaining.check(kb, query)
    else:
        print("Invalid method. Method must be TT, FC or BC.")
        sys.exit(1)

    print(result)

if __name__ == '__main__':
    main()