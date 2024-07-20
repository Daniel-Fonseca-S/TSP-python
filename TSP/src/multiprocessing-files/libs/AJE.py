import random
import time
import statistics
import multiprocessing

from .ProcessToRun import ProcessToRun
from ReportGenerator import ReportGenerator


class AJE:
    cities_number = 0
    matrix = []
    file_path_to_show = ""
    true_optimal_solution = 0.0

    best_distances = []
    best_times = []

    best_internal_distances = []
    best_paths = []
    iteration_list = []

    report_service = ReportGenerator()

    def reset_aje(self):
        self.cities_number = 0
        self.matrix = []
        self.best_distances = []

        self.best_times = []
        self.best_internal_distances = []
        self.best_paths = []
        self.iteration_list = []

    def reset_previous_results(self):
        self.best_times = []
        self.best_internal_distances = []
        self.best_paths = []
        self.iteration_list = []

    def read_from_file(self, file_name):
        self.file_path_to_show = "TSP/files/" + file_name
        try:
            with open(self.file_path_to_show, 'r') as file:
                lines = file.readlines()
                self.cities_number = int(lines[0].strip())
                self.matrix = [[int(num) for num in line.split()]
                               for line in lines[1:]]
                self.show_info_from_file()
        except IOError as error:
            print(f"\nError reading the file: {error}")
            exit(1)
        self.read_optimal_solution(file_name)

    def show_info_from_file(self):
        print("\n--== Information of the City ==--")
        print(f"Number of Cities: N = {self.cities_number}")
        print("\n- Matrix -")
        for row in self.matrix:
            for value in row:
                print(f"{value:04d} | ", end='')
            print()

    def read_optimal_solution(self, file_name):
        try:
            with open("TSP/files/results.txt", 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith(file_name):
                        self.true_optimal_solution = float(line.split()[1])
                        break
        except IOError as error:
            print(f"\nError reading the file: {error}")
            exit(1)

    def generate_path(self):
        if self.cities_number == 0:
            raise ValueError("Cities number is 0")
        path = list(range(self.cities_number))
        self.shuffle_array(path)
        return path

    @staticmethod
    def shuffle_array(array):
        for i in range(len(array) - 1, 0, -1):
            index = random.randint(0, i)
            array[i], array[index] = array[index], array[i]

    def calc_path(self, path):
        value_of_path = 0
        for i in range(self.cities_number):
            if i == (self.cities_number - 1):
                value_of_path += self.matrix[path[i]][path[0]]
            else:
                value_of_path += self.matrix[path[i]][path[i + 1]]
        return value_of_path

    def start(self, mutation_prob, population_number, number_of_convergences, processes_number, start_time):
        print("\n--== Calculate Paths ==--")
        for i in range(number_of_convergences):
            self.reset_previous_results()
            self.calc(i, processes_number, mutation_prob, population_number)

        smallest_number = min(self.best_distances)
        count = self.best_distances.count(smallest_number)
        average = statistics.mean(self.best_distances)
        std_dev = statistics.pstdev(self.best_times)
        std_dev_formatted = f"{std_dev / 1_000_000_000:.1f}"

        print(f"Optimal found {count} times \t Average = {average} \t Std Dev = {std_dev_formatted}")

        formatted_time_exec = f"{(time.perf_counter() - start_time):.3f}"
        print(f"\nProgram ran in {formatted_time_exec} seconds")
        print(f"Total parallel execution time: {self.report_service.calculate_total_parallel_time()} seconds")
        self.report_service.set_general_info("python-multiprocessing", self.cities_number, self.matrix,
                                             number_of_convergences, processes_number, mutation_prob, count)
        self.report_service.generate_report()

    def calc(self, test_number, processes_number, mutation_prob, population_number):
        start_time = time.perf_counter()
        processes = []
        parent_connections = []

        solution_already_found = multiprocessing.Value('b', False)

        for _ in range(processes_number):
            parent_conn, child_conn = multiprocessing.Pipe()
            process = (
                ProcessToRun(self, child_conn, mutation_prob, population_number, self.cities_number,
                             self.matrix, self.true_optimal_solution, solution_already_found))
            processes.append(process)
            parent_connections.append(parent_conn)
            process.start()

        # Wait for all processes to finish
        for process in processes:
            process.join()

        # Collect results from processes
        for parent_conn in parent_connections:
            best_distance, best_path, iterations, exec_time_found = parent_conn.recv()
            if best_distance is None:
                continue
            self.best_internal_distances.append(best_distance)
            self.best_times.append(exec_time_found)
            self.best_paths.append(best_path)
            self.iteration_list.append(iterations)

        # Process results
        exec_time_total = time.perf_counter() - start_time
        formatted_time = f"{exec_time_total:.3f}"
        best_distance = min(self.best_internal_distances)
        # índices com o valor mínimo
        min_indices = [i for i, x in enumerate(self.best_internal_distances) if x == best_distance]
        # índice com o menor tempo correspondente
        best_distance_index = min(min_indices, key=lambda index: self.best_times[index])
        self.best_distances.append(best_distance)
        best_path = self.best_paths[best_distance_index]
        iterations = self.iteration_list[best_distance_index]
        formatted_time_process = f"{self.best_times[best_distance_index]:.3f}"
        print(
            f"{test_number + 1:2d}  {self.cities_number} {self.file_path_to_show}  {processes_number}\t\t{formatted_time}\t\t{int(best_distance)}\t\t\t{iterations}\t\t{formatted_time_process}\t-{best_path}")
        self.report_service.add_converged_info(best_distance, self.best_times[best_distance_index], best_path,
                                               0, iterations)

    @staticmethod
    def count_occurrences(array, target):
        return array.count(target)

    EMPTY_ARRAY_ERROR = "Array is empty"

    @staticmethod
    def find_smallest_number(array):
        if not array:
            raise ValueError(AJE.EMPTY_ARRAY_ERROR)
        return min(array)

    @staticmethod
    def calculate_array_average_std(array):
        if not array:
            raise ValueError(AJE.EMPTY_ARRAY_ERROR)
        return statistics.pstdev(array)

    @staticmethod
    def calculate_array_average_distance(array):
        if not array:
            raise ValueError(AJE.EMPTY_ARRAY_ERROR)
        return statistics.mean(array)
