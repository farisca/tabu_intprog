from docutils.nodes import table
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

class RecentMemory:

    def __init__(self, iterations, dimensions, initial_point):
        self.num_iterations = iterations
        self.recent_list = [0 for i in range(0, dimensions)]
        self.previous_point = initial_point
        print('Creating recent memory...')
        print(self.recent_list)

    def update(self, point):
        #print(self.previous_point)
        # if point's component is changed update list to 0 else increment
        for i in range(0, len(self.previous_point)):
            if self.previous_point[i] == point[i]:
                self.recent_list[i] += 1
            else:
                self.recent_list[i] = 0
        self.previous_point = point
        print('Updating recent memory...')

class LongTermMemory:
    def __init__(self):
        self.lista = []

class TabuSearch:
    intensify = False

    def __init__(self, problem, max_iter, options):
        self.problem = problem
        self.tabu_list = TabuList()
        self.max_iter = max_iter
        self.iteration = 0
        self.tabu_list.add(self.problem.initial_point)
        # print(self.find_accessible_points(self.find_neighbourhood()))
        if 'diversification' in options:
            self.diversify = True
        if 'intensify' in options:
            self.intensify = True
            self.recent_memory = RecentMemory(options[options.index('intensify') + 1], self.problem.dimension, self.problem.initial_point)


    def find_neighbourhood(self):
        neighbourhood = []
        # Find possible moves across each dimension
        changes = []
        for i in range(0, self.problem.dimension):
            if self.intensify:
                print(self.recent_memory.recent_list)
                if self.recent_memory.recent_list[i] > self.recent_memory.num_iterations:
                    print('Postoji')
                    changes.append([self.problem.current_point[i], self.problem.current_point[i], self.problem.current_point[i]])
                else:
                    changes.append([self.problem.current_point[i] - 1, self.problem.current_point[i], self.problem.current_point[i] + 1])
            else:
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
                #print("Current point: ", self.problem.current_point, " better: ", neighbourhood[i])
                maximum_point = neighbourhood[i]
                maximum_value = self.problem.objective_function(neighbourhood[i])
            #if self.tabu_list.contains(neighbourhood[i]):
                #print("Point ", neighbourhood[i], " in tabu list!")
        self.problem.current_point = maximum_point
        self.tabu_list.add(self.problem.current_point)
        if maximum_value > self.problem.objective_function(self.problem.best_point):
            self.problem.best_point = maximum_point
        self.tabu_list.refresh()
        if self.intensify:
            self.recent_memory.update(maximum_point)
        self.iteration += 1

def f(x):
    return 8 * x[0] +  5 * x[1] + 3 * x[2] + 6 * x[3] + 4 * x[4]

def c1(x):
    return 2 * x[0] +  5 * x[1] + 1 * x[2] + 4 * x[3] + 3 * x[4] <= 17

def c2(x):
    return x[0] >= 0 and x[1] >= 0 and x[2] >= 0 and x[3] >= 0 and x[4] >= 0

def c3(x):
    return x[0] <= 4 and x[1] <= 3 and x[2] <= 4 and x[3] <= 2 and x[4] <= 2

def c4(x):
    return x[1] >= -4 + x[0]

a = IntegerProblem('min', f, [0,0,0,0,0], [c1, c2, c3])

tabu_search = TabuSearch(a,7, ['intensify', 4])
while tabu_search.iteration < tabu_search.max_iter:
    tabu_search.next_iteration()
print("Best solution:")
print(tabu_search.problem.best_point)
print("Objective funcion value:")
print(tabu_search.problem.objective_function(tabu_search.problem.best_point))
print("Current point: ", tabu_search.problem.current_point)
print("Tabu list:")
for i in range(0, len(tabu_search.tabu_list.tabu_list)):
    print(tabu_search.tabu_list.tabu_list[i].point, tabu_search.tabu_list.tabu_list[i].time)