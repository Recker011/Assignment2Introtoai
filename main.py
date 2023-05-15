from Parse import Parse
from Sentence import Sentence
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python iengine.py [method] [filename]")
        sys.exit(1)

    method = sys.argv[1].lower()
    filename = sys.argv[2]

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
    algorithm_module = __import__('Algorithms.' + algorithm_module, fromlist=[algorithm_module])
    
    kb, query = parse_module.parse(filename)
    result = algorithm_module.check(kb, query)

    print(result)

if __name__ == '__main__':
    main()
