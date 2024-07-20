import multiprocessing
import time


class ProcessToRun(multiprocessing.Process):

    def __init__(self, aje, conn, mut_prob, population_size, cities_size, matrix_receive, true_optimal_solution,
                 solution_already_found):
        multiprocessing.Process.__init__(self)
        self.aje = aje
        self.conn = conn
        self.mutation_prob = mut_prob
        self.population_size = population_size
        self.cities_number = cities_size
        self.matrix = matrix_receive
        self.true_optimal_solution = true_optimal_solution

        self.timeout = False
        self.solution_already_found = solution_already_found

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
                self.solution_already_found.value = True
                break

            if time.perf_counter() - start_time >= 900:
                if not self.solution_already_found.value:
                    print("Process restarting due to timeout with no results")
                    TSPSolver.reset_tsp_solver()
                    start_time = time.perf_counter()
                else:
                    self.timeout = True
                    break

        total_time = time.perf_counter() - start_time

        if self.timeout:
            print("Process timed out")
            self.conn.send([None, None, None, None])
        else:
            self.conn.send([TSPSolver.best_distance, TSPSolver.best_path, TSPSolver.iterations, total_time])
        self.conn.close()
        print(f"Process finished with distance: {TSPSolver.best_distance} and time: {total_time} seconds and "
              f"{TSPSolver.iterations} iterations")
