import random
import time
import statistics
import multiprocessing

from .ProcessToRun import ProcessToRun


class AJE:
    cities_number = 0
    matrix = []
    file_path_to_show = ""
    best_distances = []
    best_times = []

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

    @staticmethod
    def show_info_from_file():
        print("\n--== Information of the City ==--")
        print(f"Number of Cities: N = {AJE.cities_number}")
        print("\n- Matrix -")
        for row in AJE.matrix:
            for value in row:
                print(f"{value:02d} | ", end='')
            print()

    @staticmethod
    def generate_path():
        path = list(range(AJE.cities_number))
        AJE.shuffle_array(path)
        return path

    @staticmethod
    def shuffle_array(array):
        for i in range(len(array)-1, 0, -1):
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
    def start(mutation_prob, population_number, exec_time, processes_number, start_time):
        print("\n--== Calculate Paths ==--")
        for i in range(10):
            AJE.calc(i, processes_number, exec_time,
                     mutation_prob, population_number)

        smallest_number = min(AJE.best_distances)
        count = AJE.best_distances.count(smallest_number)
        average = statistics.mean(AJE.best_distances)
        std_dev = statistics.pstdev(AJE.best_times)
        std_dev_formatted = f"{std_dev / 1_000_000_000:.1f}"

        print(f"Optimal found {count} times \t Average = {average} \t Std Dev = {std_dev_formatted}")

        formatted_time_exec = f"{(time.time() - start_time):.3f}"
        print(f"\nProgram ran in {formatted_time_exec} seconds")

    @staticmethod
    def calc(test_number, processes_number, exec_time, mutation_prob, population_number):
        start_time = time.time()
        processes = []
        parent_connections = []

        # Create processes and their connections
        for _ in range(processes_number):
            parent_conn, child_conn = multiprocessing.Pipe()
            process = (
                ProcessToRun(child_conn, exec_time, mutation_prob, population_number, AJE.cities_number, AJE.matrix))
            processes.append(process)
            parent_connections.append(parent_conn)
            process.start()

        # Collect results from processes
        for parent_conn in parent_connections:
            best_distance, best_path, iterations, exec_time_found = parent_conn.recv()
            AJE.best_distances.append(best_distance)
            AJE.best_times.append(exec_time_found)

        # Wait for all processes to finish
        for process in processes:
            process.join()

        exec_time_total = time.time() - start_time
        formatted_time = f"{exec_time_total:.3f}"
        best_distance = min(AJE.best_distances)
        best_path = AJE.best_distances.index(best_distance)
        iterations = AJE.best_distances.count(best_distance)

        formatted_time_process = f"{min(AJE.best_times):.3f}"
        print(f"{test_number + 1:2d}  {AJE.cities_number} {AJE.file_path_to_show}  {processes_number}\t\t{formatted_time}\t\t{int(best_distance)}\t\t\t{iterations}\t\t{formatted_time_process}\t-{best_path}")

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
