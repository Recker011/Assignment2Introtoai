from Parse import Parse

kb = '((~a & c) | (~c & a) | (~d & c) | (~d & a)) & ((~a & d) | (~c & d) | (~c & a) | (~d & a))'

print(Parse.is_horn_clause(kb))