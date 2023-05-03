import sys
from TTchecking import TTchecking
from ForwardChaining import ForwardChaining
from BackwardChaining import BackwardChaining

# Define a function to parse the input file and extract the knowledge base and query
def parse_input_file(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        tell = lines[1]
        ask = lines[3]
        return tell, ask

# Define a function to implement the Truth Table checking algorithm
def tt_checking(kb, query):
    tt = TTchecking(kb, query)
    result = tt.check
    return result

# Define a function to implement the Forward Chaining algorithm
def forward_chaining(kb, query):
    fc = ForwardChaining(kb, query)
    result = fc.check
    return result

# Define a function to implement the Backward Chaining algorithm
def backward_chaining(kb, query):
    bc = BackwardChaining(kb, query)
    result = bc.check
    return result

if __name__ == '__main__':
# Check if the correct number of command line arguments have been passed
    if len(sys.argv) != 3:
        print("Usage: python iengine.py [method] [filename]")
        sys.exit(1)

# Extract the method and filename from the command line arguments
method = sys.argv[1]
filename = sys.argv[2]

# Parse the input file to extract the knowledge base and query
kb, query = parse_input_file(filename)

# Call the appropriate algorithm based on the selected method
if method == 'TT':
    result = tt_checking(kb, query)
elif method == 'FC':
    result = forward_chaining(kb, query)
elif method == 'BC':
    result = backward_chaining(kb, query)
else:
    print("Invalid method. Method must be TT, FC or BC.")
    sys.exit(1)

# Print the result
print(result)