import math
import itertools
import matplotlib.pyplot as plt
import numpy as np
import time

class IntegerProblem:
    def __init__(self, type, objective_function, initial_point, constraints):
        if not(type == 'min' or type == 'max'):
            raise Exception("Type has to be min or max!")
        else:
            self.type = type
            if self.type == 'min':
                self.objective_function = lambda x: -objective_function(x)
            else:
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
        self.time = 8

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

    def show(self):
        for i in range(0, len(self.tabu_list)):
            print(self.tabu_list[i].point)

class RecentMemory:

    def __init__(self, iterations, dimensions, initial_point):
        self.num_iterations = iterations
        self.recent_list = [0 for i in range(0, dimensions)]
        self.previous_point = initial_point

    def update(self, point):
        # if point's component is changed update list to 0 else increment
        for i in range(0, len(self.previous_point)):
            if self.previous_point[i] == point[i]:
                self.recent_list[i] += 1
            else:
                self.recent_list[i] = 0
        self.previous_point = point
        
class LongTermMemory:
    def __init__(self, initial_point):
        self.frequency_list = [[[initial_point[i], 1]] for i in range(0, len(initial_point))]
        
    def update(self, point):
        exists = False
        for i in range(0, len(point)):
            for j in range(0, len(self.frequency_list[i])):
                if self.frequency_list[i][j][0] == point[i]:
                    exists = True
                    position = j
            if not exists:
                self.frequency_list[i].append([point[i], 1])
            else:
                self.frequency_list[i][position][1] += 1
        
    def get(self, dimension, minimum_freq):
        for j in range(0, len(self.frequency_list[dimension])):
            if self.frequency_list[dimension][j][1] <= minimum_freq:
                return self.frequency_list[dimension][j][0]
        return []

class TabuSearch:
    intensify = False
    diversify = False
    diversify_iterations = 0

    def __init__(self, problem, max_iter, options):
        self.problem = problem
        self.tabu_list = TabuList()
        self.max_iter = max_iter
        self.iteration = 0
        self.tabu_list.add(self.problem.initial_point)
        if 'diversify' in options:
            self.diversify = True
            self.long_term_memory = LongTermMemory(self.problem.initial_point)
            self.diversify_iterations = options[options.index('diversify') + 1]
            self.minimum_freq = options[options.index('diversify') + 2]
            self.num_added = options[options.index('diversify') + 3]
            self.added = 0
        if 'intensify' in options:
            self.intensify = True
            self.recent_memory = RecentMemory(options[options.index('intensify') + 1], self.problem.dimension, self.problem.initial_point)

    def find_neighbourhood(self):
        neighbourhood = []
        # Find possible moves across each dimension
        changes = []
        for i in range(0, self.problem.dimension):
            if self.intensify:
                if self.recent_memory.recent_list[i] > self.recent_memory.num_iterations:
                    changes.append([self.problem.current_point[i], self.problem.current_point[i], self.problem.current_point[i]])
                else:
                    changes.append([self.problem.current_point[i] - 1, self.problem.current_point[i], self.problem.current_point[i] + 1])
            elif self.diversify and self.diversify_iterations <= self.iteration:
                    if self.long_term_memory.get(i, self.minimum_freq) != [] and self.added < self.num_added:
                        self.added += 1
                        changes.append([self.long_term_memory.get(i, self.minimum_freq), self.long_term_memory.get(i, self.minimum_freq), self.long_term_memory.get(i, self.minimum_freq)])
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
        maximum_point = []
        maximum_value = []
        for i in range(0, len(neighbourhood)):
            if not self.tabu_list.contains(neighbourhood[i]):
                if maximum_point == []:
                    maximum_point = neighbourhood[i]
                    maximum_value = self.problem.objective_function(maximum_point)
                elif self.problem.objective_function(neighbourhood[i]) > self.problem.objective_function(maximum_point):
                    maximum_point = neighbourhood[i]
                    maximum_value = self.problem.objective_function(neighbourhood[i])
        self.problem.current_point = maximum_point
        if maximum_value > self.problem.objective_function(self.problem.best_point):
            self.problem.best_point = maximum_point
        self.tabu_list.refresh()
        self.tabu_list.add(self.problem.current_point)
        if self.intensify:
            self.recent_memory.update(maximum_point)
        if self.diversify:
            self.long_term_memory.update(maximum_point)
        self.iteration += 1


    def plot(self, axis, line_weight, options):
        plt.ion()
        plt.cla()

        x_points = [i for i in range(axis[0], axis[1])]
        y_points = [i for i in range(axis[2], axis[3])]
        points = []
        for i in range(0, len(x_points)):
            for j in range(0, len(y_points)):
                points.append([x_points[i], y_points[j]])
        points = self.find_accessible_neighbourhood(points)
        a=[[1,1]]
        p = plt.plot(*zip(*points), marker='o', color='k', ls='')
        tacka = [self.problem.current_point]
        tabus = []
        for i in range(0, len(self.tabu_list.tabu_list)):
            tabus.append(self.tabu_list.tabu_list[i].point)
        plt.plot(*zip(*tabus), marker='o', color='b', markerfacecolor='none', markersize=20, ls='')
        plt.plot(*zip(*tacka), marker='o', color='r', markersize=15)
        axis[0] = axis[0] - 1;
        axis[1] = axis[1] + 1;
        axis[2] = axis[2] - 1;
        axis[3] = axis[3] + 1;
        plt.axis(axis)
        plt.draw()
        if 'delay' in options:
            time.sleep(options[options.index('delay') + 1])
        return plt

def f(x):
    return 5 * x[0] +  8 * x[1]

def c1(x):
    return x[0] + x[1] <= 6

def c2(x):
    return 5 * x[0] + 9 * x[1] <= 45

def c3(x):
    return x[0] >= 0 and x[1] >= 0

a = IntegerProblem('max', f, [0,0], [c1, c2, c3])

tabu_search = TabuSearch(a,12, [])
while tabu_search.iteration < tabu_search.max_iter:
    tabu_search.next_iteration()
    plt = tabu_search.plot([0, 9, 0, 6], 2, ['delay', 0.5])
plt.show()
print("Best solution:")
print(tabu_search.problem.best_point)
print("Objective function value:")
print(tabu_search.problem.objective_function(tabu_search.problem.best_point))

raw_input("Press ENTER to continue...")
