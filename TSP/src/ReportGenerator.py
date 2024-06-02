import json
import os
from datetime import datetime


class ReportGenerator:
    def __init__(self):
        self.fileName = ""
        self.filePrefix = ""
        self.citiesNumber = 0
        self.entryMatrix = []
        self.convergedDistances = []
        self.convergedTimes = []
        self.convergedPaths = []
        self.convergedFitnesses = []
        self.convergedGenerations = []
        self.executions = 0
        self.threadsOrProcesses = 0
        self.mutationProb = 0.0
        self.optimalSolutions = 0
        self.averageConvergedTime = 0.0
        self.maxConvergedTime = 0.0
        self.minConvergedTime = 0.0

    def set_general_info(self, file_prefix, cities_number, entry_matrix, executions, threads_or_processes,
                         mutation_probability, optimal_solutions):
        self.filePrefix = file_prefix
        self.citiesNumber = cities_number
        self.entryMatrix = entry_matrix
        self.executions = executions
        self.threadsOrProcesses = threads_or_processes
        self.mutationProb = mutation_probability
        self.optimalSolutions = optimal_solutions
        self.fileName = file_prefix + "_report_" + ".txt"

    def add_converged_info(self, distance, time, path, fitness, generation):
        self.convergedDistances.append(distance)
        self.convergedTimes.append(time)
        self.convergedPaths.append(path)
        self.convergedFitnesses.append(fitness)
        self.convergedGenerations.append(generation)

    def calculate_average_max_min_converged_time(self):
        self.averageConvergedTime = sum(self.convergedTimes) / len(self.convergedTimes)
        self.maxConvergedTime = max(self.convergedTimes)
        self.minConvergedTime = min(self.convergedTimes)

    def generate_report_content_json(self):
        report_content = {
            "numberOfCities": self.citiesNumber,
            "quantityOfThreadsOrProcesses": self.threadsOrProcesses,
            "mutationProbability": self.mutationProb,
            "quantityOfExecutions": self.executions,
            "entryMatrix": self.entryMatrix,
            "convergences": [
                {
                    "distance": self.convergedDistances[i],
                    "time": self.convergedTimes[i],
                    "path": self.convergedPaths[i],
                    "fitness": self.convergedFitnesses[i],
                    "generations": self.convergedGenerations[i]
                } for i in range(len(self.convergedDistances))
            ],
            "quantityOfOptimalSolutions": self.optimalSolutions,
            "averageConvergedTime": self.averageConvergedTime,
            "maxConvergedTime": self.maxConvergedTime,
            "minConvergedTime": self.minConvergedTime,
            "totalTimeOfThreadsOrProcesses": self.calculate_total_parallel_time()
        }
        return json.dumps(report_content)

    def generate_report(self):
        today = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        reports = "reports/" + today
        if not os.path.exists(reports):
            os.makedirs(reports)
        elif self.fileName == "":
            print("Error: No data was set to generate the report.")
            return

        self.calculate_average_max_min_converged_time()
        try:
            with open("reports/" + today + "/" + self.fileName, "w") as file:
                file.write(self.generate_report_content())
            with open("reports/" + today + "/" + self.fileName.replace(".txt", ".json"), "w") as file:
                file.write(self.generate_report_content_json())
        except IOError as e:
            print(f"Error to write the report file: {e}")

    def generate_report_content(self):
        report_content = "\n".join([
            "Detailed Report of the TSP Algorithm using " + self.filePrefix + ":\n",
            "Number of Cities: " + str(self.citiesNumber),
            "Quantity of Threads/Processes: " + str(self.threadsOrProcesses),
            "Mutation Probability: " + str(self.mutationProb),
            "Quantity of Executions: " + str(self.executions),
            "Entry Matrix:",
            "\n".join([" | ".join(map(str, row)) for row in self.entryMatrix]),
            "\nTSP Results by Convergence:\n",
            "\n\n".join([
                "\n".join([
                    "Convergence " + str(i + 1),
                    "Distance: " + str(self.convergedDistances[i]),
                    "Time: " + str(self.convergedTimes[i]),
                    "Path: " + str(self.convergedPaths[i]),
                    "Fitness: " + str(self.convergedFitnesses[i]),
                    "Generations: " + str(self.convergedGenerations[i])
                ]) for i in range(len(self.convergedDistances))
            ]),
            "\nQuantity of Optimal Solutions: " + str(self.optimalSolutions),
            "Average Converged Time: " + str(self.averageConvergedTime),
            "Max Converged Time: " + str(self.maxConvergedTime),
            "Min Converged Time: " + str(self.minConvergedTime),
            "Total Time of Threads/Processes: " + str(self.calculate_total_parallel_time()),
            "\nEnd of Report"
        ])
        print("\nReport generated in the reports folder with the name: " + self.fileName)
        return report_content

    def calculate_total_parallel_time(self):
        return sum(self.convergedTimes)
