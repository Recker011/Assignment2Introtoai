import sys
from TTchecking import TTchecking
from ForwardChaining import ForwardChaining
from BackwardChaining import BackwardChaining
from Sentence import Sentence
from KB import KB

# Define a function to parse the input file and extract the knowledge base and query
def parse_input_file(filename):
    try:
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
            lines = [line.replace(' ', '').strip() for line in lines]
            tell_list, ask_list = lines[1].split(';'), lines[3].split(';')
            tell, ask = list(filter(None, tell_list)), list(filter(None, ask_list))
            kb = KB()
            for sentence in tell:
                kb.tell(sentence)
            query = Sentence(ask[0])
            return kb, query
    except FileNotFoundError:
        # Error handling for file not found
        print(f"Error: file {filename} not found.")
        sys.exit(1)
    except IndexError:
        # error handling for wrong formatting of input text
        print(f"Error: file {filename} is not in the correct format.")
        sys.exit(1)

# Define a function to implement the Truth Table checking algorithm
def tt_checking(kb, query):
    tt = TTchecking(kb.clauses, query)
    result = tt.check()
    return result

# Define a function to implement the Forward Chaining algorithm
def forward_chaining(kb, query):
    fc = ForwardChaining(kb.clauses, query)
    result = fc.check
    return result

# Define a function to implement the Backward Chaining algorithm
def backward_chaining(kb, query):
    bc = BackwardChaining(kb.clauses, query)
    result = bc.check
    return result

# Main function
def main():
    if len(sys.argv) != 3:
        print("Usage: python iengine.py [method] [filename]")
        sys.exit(1)

    method = sys.argv[1]
    filename = sys.argv[2]

    kb, query = parse_input_file(filename)

    if method == 'TT':
        result = tt_checking(kb, query)
    elif method == 'FC':
        result = forward_chaining(kb, query)
    elif method == 'BC':
        result = backward_chaining(kb, query)
    else:
        print("Invalid method. Method must be TT, FC or BC.")
        sys.exit(1)

    print(result)

if __name__ == '__main__':
    main()
