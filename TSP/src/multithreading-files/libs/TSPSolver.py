import time

from .AJE import AJE
from .PMX import PMX


class TSPSolver:
    mutation_prob = 0.0
    population_size = 0
    cities_number = 0
    matrix = None

    best_distance = 0.0
    best_path = None
    iterations = 0
    exec_time_found = 0

    @staticmethod
    def reset_tsp_solver():
        TSPSolver.mutation_prob = 0.0
        TSPSolver.population_size = 0
        TSPSolver.cities_number = 0
        TSPSolver.matrix = None
        TSPSolver.best_distance = 0.0
        TSPSolver.best_path = None
        TSPSolver.iterations = 0
        TSPSolver.exec_time_found = 0

    class Tour:
        def __init__(self, path):
            self.path = path
            self.fitness = 0
            for i in range(TSPSolver.cities_number - 1):
                self.fitness += TSPSolver.matrix[self.path[i]][self.path[i + 1]]
            self.fitness += TSPSolver.matrix[self.path[TSPSolver.cities_number - 1]][self.path[0]]

    @staticmethod
    def init_population():
        population = [TSPSolver.Tour(AJE.generate_path())
                      for _ in range(TSPSolver.population_size)]
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
        for _ in range(TSPSolver.population_size):
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
    def start(true_optimal_solution, mut_prob, population_size, cit_size, matrix_receive):
        TSPSolver.mutation_prob = mut_prob
        TSPSolver.population_size = population_size
        TSPSolver.cities_number = cit_size
        TSPSolver.matrix = matrix_receive

        TSPSolver.iterations = 0
        best_distance_found = 0
        best_path_found = [0] * TSPSolver.cities_number

        population = TSPSolver.init_population()
        start_time = time.perf_counter()
        iterations_total = 0
        exec_time_found = 0
        for i in range(1, 1_000_000_000):
            if (i - 1) == TSPSolver.population_size:
                i = 1

            final_worst_tour1 = TSPSolver.get_worst_tour(population)
            population = TSPSolver.select_second_worst(
                population, final_worst_tour1)
            final_worst_tour2 = TSPSolver.get_worst_tour(population)
            paths_pmx = PMX.generate_child(
                TSPSolver.cities_number, final_worst_tour1.path, final_worst_tour2.path, TSPSolver.mutation_prob)

            fitness_pmx1 = AJE.calc_path(paths_pmx[0])
            fitness_pmx2 = AJE.calc_path(paths_pmx[1])

            if (fitness_pmx1 < TSPSolver.get_worst_fitness(population) or
                    fitness_pmx2 < TSPSolver.get_worst_fitness(population)):
                population = TSPSolver.remove_worse_paths(population)
                population = TSPSolver.add_new_paths(population, TSPSolver.Tour(
                    paths_pmx[0]), TSPSolver.Tour(paths_pmx[1]))

            for tour in population:
                if best_distance_found > tour.fitness or best_distance_found == 0:
                    best_distance_found = tour.fitness
                    best_path_found = tour.path
                    population = TSPSolver.change_population_to_best(
                        best_path_found)
                    exec_time_found = time.perf_counter() - start_time
                    iterations_total += 1

            if best_distance_found <= true_optimal_solution:
                break

            if time.perf_counter() - start_time >= 900:
                print("TSP solver timed out")
                break

        TSPSolver.iterations = iterations_total
        TSPSolver.best_distance = best_distance_found
        TSPSolver.best_path = best_path_found
        TSPSolver.exec_time_found = exec_time_found
