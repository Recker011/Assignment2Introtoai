class Conv:
    @staticmethod
    def convert(statement):
        # remove all spaces from the statement
        statement = statement.replace(' ', '')
        # split the statement into clauses
        clauses = Conv.split_clauses(statement)
        horn_clauses = []
        for clause in clauses:
            # remove the outer brackets
            clause = clause.strip('()')
            # split the clause into literals
            literals = Conv.split_literals(clause)
            positive_literals = []
            negative_literals = []
            for literal in literals:
                if '~' in literal:
                    negative_literals.append(literal.replace('~', ''))
                else:
                    positive_literals.append(literal)
            # check if the clause is a horn clause
            if len(positive_literals) <= 1:
                if len(negative_literals) > 0 and len(positive_literals) == 1:
                    horn_clause = '&'.join(negative_literals) + ' => ' + positive_literals[0]
                elif len(negative_literals) == 0 and len(positive_literals) == 1:
                    horn_clause = positive_literals[0]
                else:
                    horn_clause = '&'.join(negative_literals)
                horn_clauses.append(horn_clause)
            else:
                return 'The given CNF statement cannot be converted to Horn clause.'
        return '; '.join(horn_clauses)

    @staticmethod
    def split_clauses(statement):
        # split the statement into clauses by '&'
        # taking into account the brackets for grouping
        clauses = []
        start_index = 0
        bracket_count = 0
        for i, char in enumerate(statement):
            if char == '(':
                bracket_count += 1
            elif char == ')':
                bracket_count -= 1
            elif char == '&' and bracket_count == 0:
                clauses.append(statement[start_index:i])
                start_index = i + 1
        clauses.append(statement[start_index:])
        return clauses

    @staticmethod
    def split_literals(clause):
        # split the clause into literals by '|'
        # taking into account the brackets for grouping
        literals = []
        start_index = 0
        bracket_count = 0
        for i, char in enumerate(clause):
            if char == '(':
                bracket_count += 1
            elif char == ')':
                bracket_count -= 1
            elif char == '|' and bracket_count == 0:
                literals.append(clause[start_index:i])
                start_index = i + 1
        literals.append(clause[start_index:])
        return literals


statement = '(~p2 | p3) & (~p3 | p1) & (~c | e) & (~b | ~e | f) & (~f | ~g | h) & (~p1 | d) & (~p1 | ~p3 | c) & a & b & p2'
result = Conv.convert(statement)
print(result)
