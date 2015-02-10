import math
import itertools

class IntegerProblem:
    def __init__(self, type, objective_function, initial_point, constraints):
        if not(type == 'min' or type == 'max'):
            raise Exception("Type has to be min or max!")
        else:
            self.type = type
            self.objective_function = objective_function
            self.current_point = initial_point
            self.constraints = constraints
            self.dimension = len(initial_point)
            self.best_point = initial_point
            self.fitness = self.objective_function(self.current_point)
            self.initial_point = initial_point

class TabuItem:
    def __init__(self, point):
        self.point = point
        self.dimension = len(point)
        self.time = 5

    def __eq__(self, other):
        for i in range(0, self.dimension):
            if self.point[i] != other.point[i]:
                return False
        return True

    def reduce_time(self):
        self.time = self.time - 1

class TabuList:
    tabu_list = []

    def __init(self):
        self.tabu_list = []

    def add(self, point):
        tabu_item = TabuItem(point)
        for i in range(0, len(self.tabu_list)):
            if self.tabu_list[i] == tabu_item:
                self.tabu_list[i].reduce_time()
                return
        self.tabu_list.append(tabu_item)

    def contains(self, point):
        for i in range(0, len(self.tabu_list)):
            if self.tabu_list[i] == TabuItem(point):
                return True
        return False

    def refresh(self):
        self.tabu_list = [item for item in self.tabu_list if item.time != 1]

        for i in range(0, len(self.tabu_list)):
            self.tabu_list[i].reduce_time()

class TabuSearch:
    def __init__(self, problem, max_iter, options):
        self.problem = problem
        self.tabu_list = TabuList()
        self.max_iter = max_iter
        self.iteration = 0
        self.tabu_list.add(self.problem.initial_point)
        # print(self.find_accessible_points(self.find_neighbourhood()))
        if 'diversification' in options:
            self.diversify = True
        if 'intrinsification' in options:
            self.intrinsification = True

    def find_neighbourhood(self):
        neighbourhood = []
        # Find possible moves across each dimension
        changes = []
        for i in range(0, self.problem.dimension):
            changes.append([self.problem.current_point[i] - 1, self.problem.current_point[i], self.problem.current_point[i] + 1])
        # Find neighbourhood
        for r in itertools.product(*changes):
            # Don't add the current point to the neighbourhood
            if list(r) != self.problem.current_point:
                neighbourhood.append(list(r))
        return neighbourhood

    def find_accessible_neighbourhood(self, neighbourhood):
        accessible_neighbourhood = []
        for i in range(0, len(neighbourhood)):
            satisfies = True
            # Check if point satisfies the constraints
            for j in range(0, len(self.problem.constraints)):
                if not self.problem.constraints[j](neighbourhood[i]):
                    satisfies = False
            if satisfies:
                accessible_neighbourhood.append(neighbourhood[i])
        return accessible_neighbourhood

    def next_iteration(self):
        neighbourhood = self.find_accessible_neighbourhood(self.find_neighbourhood())
        maximum_point = self.problem.current_point
        maximum_value = self.problem.objective_function(neighbourhood[0])
        for i in range(1, len(neighbourhood)):
            if not self.tabu_list.contains(neighbourhood[i]):
                print("Current point: ", self.problem.current_point, " better: ", neighbourhood[i])
                maximum_point = neighbourhood[i]
                maximum_value = self.problem.objective_function(neighbourhood[i])
            if self.tabu_list.contains(neighbourhood[i]):
                print("Point ", neighbourhood[i], " in tabu list!")
        self.problem.current_point = maximum_point
        self.tabu_list.add(self.problem.current_point)
        if maximum_value > self.problem.objective_function(self.problem.best_point):
            self.problem.best_point = maximum_point
        self.tabu_list.refresh()
        self.iteration += 1

def f(x):
    return x[0] + x[1]

def c1(x):
    return x[0] + x[1] <=6

def c2(x):
    return x[0] + x[1] >= -2

def c3(x):
    return x[1] <= 1 + x[0]

def c4(x):
    return x[1] >= -4 + x[0]

a = IntegerProblem('min', f, [0,0], [c1,c2,c3,c4])

tabu_search = TabuSearch(a,5, ['diversify'])
while tabu_search.iteration < tabu_search.max_iter:
    tabu_search.next_iteration()
print("Best solution:")
print(tabu_search.problem.best_point)
print("Current point: ", tabu_search.problem.current_point)
print("Tabu list:")
for i in range(0, len(tabu_search.tabu_list.tabu_list)):
    print(tabu_search.tabu_list.tabu_list[i].point, tabu_search.tabu_list.tabu_list[i].time)