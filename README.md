# tabu_intprog
Python solver for integer programming problems using Tabu search.

<a href="https://github.com/farisca/tabu_intprog/blob/master/seminarski-tabu_integer.pdf?raw=true">Documentation (in Bosnian)</a>

TabuSearch.py contains all the code.

Example of usage:
An integer programming problem has to be created:
problem = IntegerProblem('max', f, [c1, c2], ['intensify', 2])
which means that we are looking for the maximum of the function f:
def f(x):
  
