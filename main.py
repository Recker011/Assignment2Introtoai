import sys
from Algorithms.TruthTable import TruthTable
from Algorithms.ForwardChaining import ForwardChaining
from Algorithms.BackwardChaining import BackwardChaining
from Algorithms.Rete import Rete
from Algorithms.WalkSAT import WalkSAT
from Algorithms.Resolution import Resolution
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

    # filetype = Parse.checkfiletype(filename)
    
    # if filetype == 'HC':
    #     kb, query = Parse.parse(filename)
    # elif filetype == 'GK':
    #     kb, query = Sentence.parse(filename)
    # else:
    #     print('Incorrect file type')

    if method == 'tt':
        kb, query = Sentence.parse(filename)
        result = TruthTable.check(kb, query)
    elif method == 'fc':
        kb, query = Parse.parse(filename)
        result = ForwardChaining.check(kb, query)
    elif method == 'bc':
        kb, query = Parse.parse(filename)
        result = BackwardChaining.check(kb, query)
    elif method == 'rt':
        kb, query = Parse.parse(filename)
        result = Rete.check(kb, query)
    elif method == 'ws':
        kb, query = Sentence.parse(filename)
        result = WalkSAT.check(kb, query)
    elif method == 'rs':
        kb, query = Sentence.parse(filename)
        result = Resolution.check(kb, query)
    else:
        print("Invalid method. Method must be TT, FC or BC.")
        sys.exit(1)

    print(result)

if __name__ == '__main__':
    main()