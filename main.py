from Parse import Parse
from Sentence import Sentence
from Algorithms.TruthTable import TruthTable
import importlib
import sys

def main():
    # if len(sys.argv) != 3:
    #     print("Usage: python iengine.py [method] [filename]")
    #     sys.exit(1)

    # method = sys.argv[1].lower()
    # filename = sys.argv[2]
    
    method = 'tt'
    filename = 'Test-Files/test_genericKB.txt'

    algorithms = {
        'tt': ('Sentence', 'TruthTable'),
        'fc': ('Parse', 'ForwardChaining'),
        'bc': ('Parse', 'BackwardChaining'),
        'rete': ('Parse', 'Rete'),
        'walksat': ('Sentence', 'WalkSAT')
    }

    if method not in algorithms:
        print("Invalid method. Method must be TT, FC, BC, RETE or WALKSAT.")
        sys.exit(1)

    parse_module, algorithm_module = algorithms[method]
    parse_module = globals()[parse_module]
    algorithm_module = importlib.import_module(algorithm_module)
   

    # kb, query = parse_module.parse(filename)
    
    # kb = '(~p2 | p3) & (~p3 | p1) & (~c | e) & (~b | ~e | f) & (~f | ~g | h) & (~p1 | d) & (~p1 | ~p3 | c) & a & b & p2'
    # query = 'd'
    
    # algorithm_module.check(kb, query)


if __name__ == '__main__':
    main()