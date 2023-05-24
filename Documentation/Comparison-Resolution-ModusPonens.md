# Differences between logical inference through Resolution vs Modus Ponens

Resolution and Modus Ponens are both ways of inferring propositional logic.

## Resolution

Resolution is an inference rule that uses proof of contradiction to prove the validity of queries. It takes a knowledge base in the Conjunctive Normal Form and compares the clauses separated by conjunctions against each other to prove that the NEGATION of the initial query is not true. This is shown by cancelling out complimentary literals until an empty clause is or is not produced. If an empty clause is produced, then the negation of the query is not valid, thus the query MUST be true by proof of contradiction.

## Modus Ponens

Modus Ponens is an inference rule that states that if a clause A is true, and if A implies B, then B must also be true.

## Completeness and Differences

Modus Ponens REQUIRES that the knowledge base is only consisted of Horn Clauses, which are clauses where at most only one literal is positive. In this case, Modus Ponens is complete in linear time. However for all knowledge bases in general, it is not complete. For more general clauses we need a more powerful inference rule in the form of logical resolution, which is complete and sound for all knowledge bases, however it operates with exponential time.
