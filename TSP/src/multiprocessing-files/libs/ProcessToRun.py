import multiprocessing
import time


class ProcessToRun(multiprocessing.Process):
    def __init__(self, aje, conn, time_per_process, mut_prob, population_size, cities_size, matrix_receive):
        multiprocessing.Process.__init__(self)
        self.aje = aje
        self.conn = conn
        self.time_per_process = time_per_process
        self.mutation_prob = mut_prob
        self.population_size = population_size
        self.cities_number = cities_size
        self.matrix = matrix_receive

    def run(self):
        print("Process started")
        from .TSPSolver import TSPSolver
        start_time = time.time()
        time_to_exec = self.time_per_process
        for _ in range(1, 1_000_000_000 + 1):
            TSPSolver.start(
                self.aje,
                self.time_per_process,
                self.mutation_prob,
                self.population_size,
                self.cities_number,
                self.matrix
            )
            if (time.time() - start_time) >= time_to_exec:
                break

        self.conn.send([TSPSolver.best_distance, TSPSolver.best_path, TSPSolver.iterations, TSPSolver.exec_time_found])
        self.conn.close()
        print("Process finished - " + str(TSPSolver.exec_time_found) + " seconds - " + str(TSPSolver.best_distance))
