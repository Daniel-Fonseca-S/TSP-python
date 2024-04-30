import multiprocessing
import time


class ProcessToRun(multiprocessing.Process):
    def __init__(self, conn, time_per_process, mut_prob, population_size, cities_size, matrix_receive):
        multiprocessing.Process.__init__(self)
        self.conn = conn
        self.timePerProcess = time_per_process
        self.mutationProb = mut_prob
        self.populationSize = population_size
        self.citiesNumber = cities_size
        self.matrix = matrix_receive

    def run(self):
        from .TSPSolver import TSPSolver
        start_time = time.time()
        time_to_exec = self.timePerProcess
        for _ in range(1, 1_000_000_000 + 1):
            TSPSolver.start(
                self.timePerProcess,
                self.mutationProb,
                self.populationSize,
                self.citiesNumber,
                self.matrix
            )
            if (time.time() - start_time) >= time_to_exec:
                break

        self.conn.send([TSPSolver.best_distance, TSPSolver.best_path, TSPSolver.iterations, TSPSolver.exec_time_found])
        self.conn.close()
