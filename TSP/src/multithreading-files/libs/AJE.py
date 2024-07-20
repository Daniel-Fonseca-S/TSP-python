import random
import time
import statistics

from .ThreadToRun import ThreadToRun
from ReportGenerator import ReportGenerator


class AJE:
    cities_number = 0
    matrix = []
    file_path_to_show = ""
    true_optimal_solution = 0.0

    best_distances = []
    best_times = []

    report_service = ReportGenerator()

    @staticmethod
    def reset_aje():
        AJE.cities_number = 0
        AJE.matrix = []
        AJE.best_distances = []
        AJE.best_times = []

    @staticmethod
    def read_from_file(file_name):
        AJE.file_path_to_show = "TSP/files/" + file_name
        try:
            with open(AJE.file_path_to_show, 'r') as file:
                lines = file.readlines()
                AJE.cities_number = int(lines[0].strip())
                AJE.matrix = [[int(num) for num in line.split()]
                              for line in lines[1:]]
                AJE.show_info_from_file()
        except IOError as error:
            print(f"\nError reading the file: {error}")
        AJE.read_optimal_solution(file_name)

    @staticmethod
    def show_info_from_file():
        print("\n--== Information of the City ==--")
        print(f"Number of Cities: N = {AJE.cities_number}")
        print("\n- Matrix -")
        for row in AJE.matrix:
            for value in row:
                print(f"{value:04d} | ", end='')
            print()

    @staticmethod
    def read_optimal_solution(file_name):
        try:
            with open("TSP/files/results.txt", 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith(file_name):
                        AJE.true_optimal_solution = float(line.split()[1])
                        break
        except IOError as error:
            print(f"\nError reading the file: {error}")
            exit(1)

    @staticmethod
    def generate_path():
        path = list(range(AJE.cities_number))
        AJE.shuffle_array(path)
        return path

    @staticmethod
    def shuffle_array(array):
        for i in range(len(array) - 1, 0, -1):
            index = random.randint(0, i)
            array[i], array[index] = array[index], array[i]

    @staticmethod
    def calc_path(path):
        value_of_path = 0
        for i in range(AJE.cities_number):
            if i == (AJE.cities_number - 1):
                value_of_path += AJE.matrix[path[i]][path[0]]
            else:
                value_of_path += AJE.matrix[path[i]][path[i + 1]]
        return value_of_path

    @staticmethod
    def start(mutation_prob, population_number, number_of_convergences, threads_number, start_time):
        print("\n--== Calculate Paths ==--")
        for i in range(number_of_convergences):
            AJE.calc(i, threads_number, mutation_prob, population_number)

        smallest_number = min(AJE.best_distances)
        count = AJE.best_distances.count(smallest_number)
        average = statistics.mean(AJE.best_distances)
        std_dev = statistics.pstdev(AJE.best_times)
        std_dev_formatted = f"{std_dev / 1_000_000_000:.1f}"

        print(f"Optimal found {count} times \t Average = {average} \t Std Dev = {std_dev_formatted}")

        formatted_time_exec = f"{(time.perf_counter() - start_time):.3f}"
        print(f"\nProgram ran in {formatted_time_exec} seconds")
        print(f"Total concurrent execution time: {AJE.report_service.calculate_total_parallel_time()} seconds")
        AJE.report_service.set_general_info("python-multithreading", AJE.cities_number, AJE.matrix,
                                            number_of_convergences, threads_number, mutation_prob, count)
        AJE.report_service.generate_report()

    @staticmethod
    def calc(test_number, threads_number, mutation_prob, population_number):
        ThreadToRun.results.clear()
        start_time = time.perf_counter()
        threads = [ThreadToRun(mutation_prob, population_number, AJE.cities_number, AJE.matrix,
                               AJE.true_optimal_solution) for _ in range(threads_number)]
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        best_result = ThreadToRun.get_best_result()

        exec_time_total = time.perf_counter() - start_time
        formatted_time = f"{exec_time_total:.3f}"
        best_distance = best_result['distance']

        AJE.best_distances.append(best_distance)
        AJE.best_times.append(exec_time_total)

        formatted_time_thread = f"{best_result['time']:.3f}"
        print(
            f"{test_number + 1:2d}  {AJE.cities_number} {AJE.file_path_to_show}  {threads_number}\t\t{formatted_time}\t\t{int(best_distance)}\t\t\t{best_result['iterations']}\t\t{formatted_time_thread}\t-{best_result['path']}")
        AJE.report_service.add_converged_info(best_distance, best_result['time'], best_result['path'],
                                              0, best_result['iterations'])

    @staticmethod
    def count_occurrences(array, target):
        return array.count(target)

    @staticmethod
    def find_smallest_number(array):
        if not array:
            raise ValueError("Array is empty")
        return min(array)

    @staticmethod
    def calculate_array_average_std(array):
        if not array:
            raise ValueError("Array is empty")
        return statistics.pstdev(array)

    @staticmethod
    def calculate_array_average_distance(array):
        if not array:
            raise ValueError("Array is empty")
        return statistics.mean(array)
