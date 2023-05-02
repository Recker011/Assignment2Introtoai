# Inference Engine

This project implements an inference engine for propositional logic using Truth Table (TT) checking, Backward Chaining (BC) and Forward Chaining (FC) algorithms.

## Overview

The program takes as input a method (TT, FC or BC), and a filename containing the knowledge base and query in the specified format. The knowledge base consists of Horn clauses separated by semicolons and the query is a propositional symbol. The program determines whether the query is entailed from the knowledge base using the selected algorithm and outputs an answer of the form YES or NO.

## Usage

To run the program, use the following command:

```
python iengine.py [method] [filename]
```

where `method` can be either `TT` (for Truth Table checking), `FC` (for Forward Chaining), or `BC` (for Backward Chaining) to specify the algorithm, and `filename` is for the text file consisting of the problem.

For example:

```
python iengine.py FC test1.txt
```

## Input File Format

The problems are stored in simple text files consisting of both the knowledge base and the query:

- The knowledge base follows the keyword `TELL` and consists of Horn clauses separated by semicolons.
- The query follows the keyword `ASK` and consists of a proposition symbol.

For example, the following could be the content of one of the test files (`test1.txt`):

```
TELL
p2=> p3; p3 => p1; c => e; b&e => f; f&g => h; p1=>d; p1&p3 => c; a; b; p2;
ASK
d
```

## Output Format

The standard output is an answer of the form YES or NO, depending on whether the `ASK`(ed) query `q` follows from the `TELL`(ed) knowledge base `KB`. When the method is TT and the answer is YES, it should be followed by a colon (`:`) and the number of models of `KB`. When the method is FC or BC and the answer is YES, it should be followed by a colon (`:`) and the list of propositional symbols entailed from `KB` that has been found during the process.
