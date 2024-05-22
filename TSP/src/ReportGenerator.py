import os
from datetime import datetime


# Class that generates a detailed report in the reports folder of the execution and results of the TSP algorithm
# used for threading and processing versions of the TSP algorithm
class ReportGenerator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ReportGenerator, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.file_prefix = ""
        self.file_prefix = ""
        self.cities_number = 0
        self.entry_matrix = []
        self.converged_distances = []
        self.converged_times = []
        self.converged_paths = []
        self.converged_fitness = []
        self.converged_generations = []
        self.quantity_of_executions = 0
        self.quantity_of_threads_or_processes = 0
        self.mutation_probability = 0.0
        self.quantity_of_optimal_solutions = 0
        self.file_name = ""
        self.average_converged_time = 0.0
        self.max_converged_time = 0.0
        self.min_converged_time = 0.0

    # Method to set the general information of the report
    def set_general_info(self, file_prefix, cities_number, entry_matrix, quantity_of_executions,
                         quantity_of_threads_or_processes, mutation_probability, quantity_of_optimal_solutions):
        self.file_prefix = file_prefix
        self.cities_number = cities_number
        self.entry_matrix = entry_matrix
        self.quantity_of_executions = quantity_of_executions
        self.quantity_of_threads_or_processes = quantity_of_threads_or_processes
        self.mutation_probability = mutation_probability
        self.quantity_of_optimal_solutions = quantity_of_optimal_solutions
        self.file_name = f"{file_prefix}_report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    # Method for include process/thread related information in the report
    def include_process_thread_info(self, converged_distance, converged_time, converged_path, converged_fitness,
                                    converged_generation):
        self.converged_distances.append(converged_distance)
        self.converged_times.append(converged_time)
        self.converged_paths.append(converged_path)
        self.converged_fitness.append(converged_fitness)
        self.converged_generations.append(converged_generation)

    # Method to calculate the average, maximum and minimum time of the converged paths
    def calculate_average_max_min_time(self):
        self.average_converged_time = sum(self.converged_times) / len(self.converged_times)
        self.max_converged_time = max(self.converged_times)
        self.min_converged_time = min(self.converged_times)

    # Method to reset the parameters of the report
    def reset_params(self):
        self.file_prefix = ""
        self.cities_number = 0
        self.entry_matrix = []
        self.converged_distances = []
        self.converged_times = []
        self.converged_paths = []
        self.converged_fitness = []
        self.converged_generations = []
        self.quantity_of_executions = 0
        self.quantity_of_threads_or_processes = 0
        self.mutation_probability = 0.0
        self.quantity_of_optimal_solutions = 0
        self.file_name = ""
        self.average_converged_time = 0.0
        self.max_converged_time = 0.0
        self.min_converged_time = 0.0

    # Method to generate the report in the reports folder (create the folder if it does not exist)
    def generate_report(self):
        if not os.path.exists("reports"):
            os.makedirs("reports")
        if self.file_prefix == "":
            print("No report data to generate file")
            return
        self.calculate_average_max_min_time()
        with open("reports/" + self.file_name, "w") as file:
            file.write("Detailed Report of the TSP Algorithm using " + self.file_prefix + "\n")
            file.write("Number of Cities: " + str(self.cities_number) + "\n")
            file.write("Quantity of Threads/Processes: " + str(self.quantity_of_threads_or_processes) + "\n")
            file.write("Mutation Probability: " + str(self.mutation_probability) + "\n")
            file.write("Quantity of Executions: " + str(self.quantity_of_executions) + "\n")
            file.write("\n")
            file.write("Entry Matrix:\n")
            for row in self.entry_matrix:
                for value in row:
                    file.write(f"{value:02d} | ")
                file.write("\n")
            file.write("\n")
            file.write("TSP Results by Convergence:\n")
            for i in range(len(self.converged_distances)):
                file.write(f"Convergence {i + 1}:\n")
                file.write("Distance: " + str(self.converged_distances[i]) + "\n")
                file.write("Time: " + str(self.converged_times[i]) + "\n")
                file.write("Path: " + str(self.converged_paths[i]) + "\n")
                file.write("Fitness: " + str(self.converged_fitness[i]) + "\n")
                file.write("Generations: " + str(self.converged_generations[i]) + "\n")
                file.write("\n")
            file.write("Quantity of Optimal Solutions: " + str(self.quantity_of_optimal_solutions) + "\n")
            file.write("\n")
            file.write("Average Converged Time: " + str(self.average_converged_time) + "\n")
            file.write("Max Converged Time: " + str(self.max_converged_time) + "\n")
            file.write("Min Converged Time: " + str(self.min_converged_time) + "\n")
            file.write("\n")
            file.write("End of Report")
            file.close()
        print(f"Report generated in the reports folder with the name: {self.file_name}")
        self.reset_params()
