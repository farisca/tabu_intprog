<b>Python solver for integer programming problems using Tabu search.</b>

<a href="https://github.com/farisca/tabu_intprog/blob/master/seminarski-tabu_integer.pdf?raw=true">Documentation (in Bosnian)</a>

TabuSearch.py contains all the code.

<b>Example of usage:</b>

An integer programming problem has to be created:

```python
problem = IntegerProblem('max', f, [c1, c2])</code>
```
which means that we are looking for the maximum of the function f:
```python
def f(x):
  return 8 * x[0] +  5 * x[1] + 3 * x[2] + 6 * x[3] + 4 * x[4]
```
c1 and c2 are constraints defined as:
```python
def c1(x):
    return 2 * x[0] +  5 * x[1] + 1 * x[2] + 4 * x[3] + 3 * x[4] <= 17

def c2(x):
    return x[0] >= 0 and x[1] >= 0 and x[2] >= 0 and x[3] >= 0 and x[4] >= 0
```

Next, a tabu search has to be created:
```python
tabu_search = TabuSearch(problem, 12, ['intensify', 2])
```
The first parameter is the integer programming problem defined above, the second is the number of iterations and the third parameter are options, which in this case allow the use of intensification after the second iteration.
The iterations are done by calling the ```next_iteration``` method:
```python
while tabu_search.iteration < tabu_search.max_iter:
  tabu_search.next_iteration()
  plt = tabu_search.plot([0, 9, 0, 6], 2, ['delay', 0.5])
```
The last line enables the visualization of the search process and the result is the following graph where the optimum is marked in red and tabu solutions are circled:
![alt tag width="100"](http://s3.postimg.org/6kgu9pdpv/tabu.png)
