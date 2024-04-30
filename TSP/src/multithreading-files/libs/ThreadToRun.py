import threading
import time


class ThreadToRun(threading.Thread):
    mutationProb = 0
    populationSize = 0
    citiesNumber = 0
    matrix = []
    bestDistanceFinal = 0
    bestPathFinal = []
    iterationsFinal = 0
    timeFinal = 0

    def __init__(self, time_per_thread, mut_prob, population_size, cities_size, matrix_receive):
        threading.Thread.__init__(self)
        self.timePerThread = time_per_thread
        ThreadToRun.mutationProb = mut_prob
        ThreadToRun.populationSize = population_size
        ThreadToRun.citiesNumber = cities_size
        ThreadToRun.matrix = matrix_receive

    def run(self):
        from .TSPSolver import TSPSolver
        start_time = time.time()
        time_to_exec = self.timePerThread
        for _ in range(1, 1_000_000_000 + 1):
            TSPSolver.start(
                self.timePerThread,
                ThreadToRun.mutationProb,
                ThreadToRun.populationSize,
                ThreadToRun.citiesNumber,
                ThreadToRun.matrix
            )
            if (time.time() - start_time) >= time_to_exec:
                break

        ThreadToRun.set_best_distance_final(TSPSolver.best_distance)
        ThreadToRun.set_best_path_final(TSPSolver.best_path)
        ThreadToRun.set_iterations_final(TSPSolver.iterations)
        ThreadToRun.set_formatted_time_final(TSPSolver.exec_time_found)

    @staticmethod
    def set_best_distance_final(b_distance):
        ThreadToRun.bestDistanceFinal = b_distance

    @staticmethod
    def get_best_distance_final():
        return ThreadToRun.bestDistanceFinal

    @staticmethod
    def set_best_path_final(b_path):
        ThreadToRun.bestPathFinal = b_path

    @staticmethod
    def get_best_path_final():
        return ThreadToRun.bestPathFinal

    @staticmethod
    def set_iterations_final(it):
        ThreadToRun.iterationsFinal = it

    @staticmethod
    def get_iterations_final():
        return ThreadToRun.iterationsFinal

    @staticmethod
    def set_formatted_time_final(time_final_insert):
        ThreadToRun.timeFinal = time_final_insert

    @staticmethod
    def get_formatted_time_final():
        return ThreadToRun.timeFinal
