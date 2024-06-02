import multiprocessing
import time


class ProcessToRun(multiprocessing.Process):
    def __init__(self, aje, conn, mut_prob, population_size, cities_size, matrix_receive, true_optimal_solution):
        multiprocessing.Process.__init__(self)
        self.aje = aje
        self.conn = conn
        self.mutation_prob = mut_prob
        self.population_size = population_size
        self.cities_number = cities_size
        self.matrix = matrix_receive
        self.true_optimal_solution = true_optimal_solution

    def run(self):
        print("Process started")
        from .TSPSolver import TSPSolver
        start_time = time.perf_counter()
        for _ in range(1, 1_000_000_000 + 1):
            TSPSolver.start(
                self.aje,
                self.true_optimal_solution,
                self.mutation_prob,
                self.population_size,
                self.cities_number,
                self.matrix
            )
            if TSPSolver.best_distance <= self.true_optimal_solution:
                break

            if TSPSolver.exec_time_found >= 300:
                print("Process timed out")
                break
        total_time = time.perf_counter() - start_time

        self.conn.send([TSPSolver.best_distance, TSPSolver.best_path, TSPSolver.iterations, total_time])
        self.conn.close()
        print(f"Process finished with distance: {TSPSolver.best_distance} and time: {total_time} seconds and "
              f"{TSPSolver.iterations} iterations")
