import time

from libs.AJE import AJE
from libs.PMX import PMX


class TSPSolver:
    mutationProb = 0.0
    populationSize = 0
    citiesNumber = 0
    matrix = None

    bestDistance = 0.0
    bestPath = None
    iterations = 0
    execTimeFound = 0

    @staticmethod
    def reset_TSPSolver():
        TSPSolver.mutationProb = 0.0
        TSPSolver.populationSize = 0
        TSPSolver.citiesNumber = 0
        TSPSolver.matrix = None
        TSPSolver.bestDistance = 0.0
        TSPSolver.bestPath = None
        TSPSolver.iterations = 0
        TSPSolver.execTimeFound = 0

    class Tour:
        def __init__(self, path):
            self.path = path
            self.fitness = 0
            for i in range(TSPSolver.citiesNumber - 1):
                self.fitness += TSPSolver.matrix[self.path[i]
                                                 ][self.path[i + 1]]
            self.fitness += TSPSolver.matrix[self.path[TSPSolver.citiesNumber - 1]][self.path[0]]

    @staticmethod
    def init_population():
        population = [TSPSolver.Tour(AJE.generate_path())
                      for _ in range(TSPSolver.populationSize)]
        return population

    @staticmethod
    def get_worst_tour(population):
        return max(population, key=lambda tour: tour.fitness)

    @staticmethod
    def select_second_worst(population, best_tour1):
        new_population = population.copy()
        worst_tour = TSPSolver.get_worst_tour(population)
        second_worst_tour = max((tour for tour in population if tour != best_tour1 and tour !=
                                worst_tour), key=lambda tour: tour.fitness, default=None)
        if second_worst_tour is not None:
            new_population[new_population.index(
                worst_tour)] = second_worst_tour
        return new_population

    @staticmethod
    def change_population_to_best(best_path_found):
        new_population = []
        for _ in range(TSPSolver.populationSize):
            path = best_path_found.copy()  # create a copy of the best path
            AJE.shuffle_array(path)  # shuffle the path
            # create a new Tour with the shuffled path
            new_population.append(TSPSolver.Tour(path))
        return new_population

    @staticmethod
    def get_worst_fitness(population):
        return max(tour.fitness for tour in population)

    @staticmethod
    def remove_worse_paths(population):
        for tour in population:
            tour.fitness = AJE.calc_path(tour.path)
        population.sort(key=lambda tour: tour.fitness)
        return population[:-2]

    @staticmethod
    def add_new_paths(population, new_path1, new_path2):
        return population + [new_path1, new_path2]

    @staticmethod
    def start(exec_time, mut_prob, popul_size, cit_size, matrix_receive):
        TSPSolver.mutationProb = mut_prob
        TSPSolver.populationSize = popul_size
        TSPSolver.citiesNumber = cit_size
        TSPSolver.matrix = matrix_receive

        TSPSolver.iterations = 0
        best_distance_found = 0
        best_path_found = [0] * TSPSolver.citiesNumber

        population = TSPSolver.init_population()
        start_time = time.time()
        iterations_total = 0
        time_to_exec = exec_time
        exec_time_found = 0
        for i in range(1, 1_000_000_000):
            if (i - 1) == TSPSolver.populationSize:
                i = 1

            final_worst_tour1 = TSPSolver.get_worst_tour(population)
            population = TSPSolver.select_second_worst(
                population, final_worst_tour1)
            final_worst_tour2 = TSPSolver.get_worst_tour(population)
            paths_PMX = PMX.generate_child(
                TSPSolver.citiesNumber, final_worst_tour1.path, final_worst_tour2.path, TSPSolver.mutationProb)

            fitness_PMX1 = AJE.calc_path(paths_PMX[0])
            fitness_PMX2 = AJE.calc_path(paths_PMX[1])

            if fitness_PMX1 < TSPSolver.get_worst_fitness(population) or fitness_PMX2 < TSPSolver.get_worst_fitness(population):
                population = TSPSolver.remove_worse_paths(population)
                population = TSPSolver.add_new_paths(population, TSPSolver.Tour(
                    paths_PMX[0]), TSPSolver.Tour(paths_PMX[1]))

            for tour in population:
                if best_distance_found > tour.fitness or best_distance_found == 0:
                    best_distance_found = tour.fitness
                    best_path_found = tour.path
                    population = TSPSolver.change_population_to_best(
                        best_path_found)
                    exec_time_found = time.time() - start_time
                    iterations_total += 1

            if (time.time() - start_time) >= time_to_exec:
                break

        TSPSolver.iterations = iterations_total
        TSPSolver.bestDistance = best_distance_found
        TSPSolver.bestPath = best_path_found
        TSPSolver.execTimeFound = exec_time_found
