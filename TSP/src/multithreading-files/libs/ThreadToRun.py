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

    # Shared list to store results from all threads
    results = []

    def __init__(self, mut_prob, population_size, cities_size, matrix_receive, true_optimal_solution):
        threading.Thread.__init__(self)
        ThreadToRun.mutationProb = mut_prob
        ThreadToRun.populationSize = population_size
        ThreadToRun.citiesNumber = cities_size
        ThreadToRun.matrix = matrix_receive
        self.true_optimal_solution = true_optimal_solution

    def run(self):
        print("thread started")
        from .TSPSolver import TSPSolver
        start_time = time.time()
        for _ in range(1, 1_000_000_000 + 1):
            TSPSolver.start(
                self.true_optimal_solution,
                ThreadToRun.mutationProb,
                ThreadToRun.populationSize,
                ThreadToRun.citiesNumber,
                ThreadToRun.matrix
            )
            if TSPSolver.best_distance <= self.true_optimal_solution:
                break

            if TSPSolver.exec_time_found >= 300:
                print("Thread timed out")
                break
        total_time = time.time() - start_time

        ThreadToRun.results.append({
            'distance': TSPSolver.best_distance,
            'path': TSPSolver.best_path,
            'iterations': TSPSolver.iterations,
            'time': total_time
        })
        print(f"Thread finished with distance: {TSPSolver.best_distance} and time: {total_time} seconds and "
              f"{TSPSolver.iterations} iterations")

    @staticmethod
    def get_best_result():
        # Find the result with the smallest distance
        best_result = min(ThreadToRun.results, key=lambda result: result['distance'])
        # If there are multiple results with the same smallest distance, find the one with the smallest time
        best_results = [result for result in ThreadToRun.results if result['distance'] == best_result['distance']]
        if len(best_results) > 1:
            best_result = min(best_results, key=lambda result: result['time'])
        return best_result
