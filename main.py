import sys
from Algorithms.TruthTable import TruthTable
from Algorithms.ForwardChaining import ForwardChaining
from Algorithms.BackwardChaining import BackwardChaining
from Algorithms.Rete import Rete
from Algorithms.WalkSAT import WalkSAT
from Sentence import Sentence
from Parse import Parse
#from KB import KB


# Main function
def main():
    if len(sys.argv) != 3:
        print("Usage: python iengine.py [method] [filename]")
        sys.exit(1)

    method = sys.argv[1].lower()
    filename = sys.argv[2]

    filetype = Parse.checkfiletype(filename)
    
    if filetype == 'HC':
        kb, query = Parse.parse(filename)
    elif filetype == 'GK':
        kb, query = Sentence.parse(filename)
    else:
        print('Incorrect file type')

    if method == 'tt':
        result = TruthTable.check(kb, query)
    elif method == 'fc':
        result = ForwardChaining.check(kb, query)
    elif method == 'bc':
        result = BackwardChaining.check(kb, query)
    elif method == 'rt':
        result = Rete.check(kb, query)
    elif method == 'ws':
        result = WalkSAT.check(kb, query)
    else:
        print("Invalid method. Method must be TT, FC or BC.")
        sys.exit(1)

    print(result)

if __name__ == '__main__':
    main()