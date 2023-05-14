# WalkSAT vs DPLL

WalkSAT and DPLL (Davis-Putnam-Logemann-Loveland) are two algorithms for solving the Boolean satisfiability problem (SAT). While both algorithms aim to determine whether a given propositional logic formula is satisfiable, they use different approaches to solve the problem.

## WalkSAT

WalkSAT is a local search algorithm that tries to find a satisfying assignment for a given propositional logic formula in conjunctive normal form (CNF). It starts with a random assignment of truth values to the variables in the formula and iteratively tries to improve the assignment by flipping the truth value of one variable at a time. The variable to flip is chosen either randomly or based on a heuristic that tries to maximize the number of satisfied clauses.

WalkSAT is an incomplete solver, which means that it can only find satisfying assignments but cannot prove unsatisfiability. If WalkSAT fails to find a satisfying assignment within a given number of iterations, it returns "don't know".

## DPLL

DPLL is a backtracking-based search algorithm that tries to find a satisfying assignment for a given propositional logic formula in CNF. It works by recursively splitting the search space into smaller subproblems based on the values assigned to the variables in the formula. At each step, DPLL chooses a variable and assigns it a truth value. It then simplifies the formula by removing all clauses that are satisfied by the assignment and all literals that are falsified by the assignment. If the simplified formula contains an empty clause, then DPLL backtracks and tries a different assignment.

DPLL is a complete solver, which means that it can find satisfying assignments and prove unsatisfiability. If DPLL fails to find a satisfying assignment, it returns "unsatisfiable" along with a proof of unsatisfiability.

## Comparison

WalkSAT and DPLL use different approaches to solve the SAT problem. WalkSAT uses local search with heuristics while DPLL uses backtracking with clause learning. In general, DPLL/CDCL solvers are much faster on structured SAT instances while WalkSAT is faster on random k-SAT instances.