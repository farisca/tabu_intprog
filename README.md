# tabu_intprog
Solving integer programming problems using Tabu search

Example of usage:
```HTML
<verbatim>def f(x):
    return 8 * x[0] +  5 * x[1] + 3 * x[2] + 6 * x[3] + 4 * x[4]

def c1(x):
    return 2 * x[0] +  5 * x[1] + 1 * x[2] + 4 * x[3] + 3 * x[4] <= 17

def c2(x):
    return x[0] >= 0 and x[1] >= 0 and x[2] >= 0 and x[3] >= 0 and x[4] >= 0

def c3(x):
    return x[0] <= 4 and x[1] <= 3 and x[2] <= 4 and x[3] <= 2 and x[4] <= 2

a = IntegerProblem('min', f, [0,0,0,0,0], [c1, c2, c3])
tabu_search = TabuSearch(a,7, ['intensify', 4])

</verbatim>
