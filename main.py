import sys

# Define a function to parse the input file and extract the knowledge base and query
def parse_input_file(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        tell = lines[0].split(' ')[1]
        ask = lines[1].split(' ')[1]
        return tell, ask

# Define a function to implement the Truth Table checking algorithm
def tt_checking(kb, query):
    # The implementation of Truth Table checking algorithm here
    pass

# Define a function to implement the Forward Chaining algorithm
def forward_chaining(kb, query):
    # The implementation of Forward Chaining algorithm here
    pass

# Define a function to implement the Backward Chaining algorithm
def backward_chaining(kb, query):
    # The implementation of Backward Chaining algorithm here
    pass

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