def parse_input_file(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
<<<<<<< Updated upstream
        tell = lines[1]
        ask = lines[3]
        return tell, ask
=======
        tell_line = lines[1].replace(" ", "")
        ask_line = lines[3].replace(" ", "")
        tell = tell_line.split(";")
        ask = [ask_line]
        return tell[:-1], ask
>>>>>>> Stashed changes

def checkparsein():
    line1, line2 = parse_input_file("C:\\Users\\Randew Kumarasinghe\\Desktop\\COS30019\\Assignment2Introtoai\\Assignment2Introtoai\\test.txt")
    print(line1, line2)
<<<<<<< Updated upstream
=======


def checkTTcheck():
    filename = "test.txt"
    print(f"Reading input file: {filename}")
    kb, query = parse_input_file(filename)
    print(f"kb: {kb}")
    print(f"query: {query}")
    if not query:
        print("Error: query list is empty")
        return
    tt = TTchecking(kb, query[0])
    result = tt.check()
    print(result)
>>>>>>> Stashed changes
    
checkparsein()