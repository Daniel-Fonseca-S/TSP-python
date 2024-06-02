import sys
import time

from libs.AJE import AJE
from libs.TSPSolver import TSPSolver

file_name = ''
threads_number = 0
number_of_convergences = 0
population_number = 0
mutation_probability = 0


def main():
    try:
        while True:
            status = request_params()
            if status == "over" or status == "start":
                break
    except Exception as e:
        sys.stderr.write("Error: " + str(e))
        sys.exit(1)


def request_params():
    reset_params()
    print("\n(type 'exit' to leave) > ", end='')

    input_params = input()
    params = input_params.split()

    if len(params) != 0:
        if params[0].lower() == "exit":
            print("Program Finished.")
            return "over"

        if len(params) == 5 and float(params[4]) <= 1:
            global file_name, threads_number, number_of_convergences, population_number, mutation_probability
            file_name = params[0]
            threads_number = int(params[1])
            number_of_convergences = int(params[2])
            population_number = int(params[3])
            mutation_probability = float(params[4])

            start_program()

            return "start"
    else:
        print("> <fileName> <threadsNumber> <numberOfConvergences> <populationNumber> <mutationProb> (max: 1 (100%))")
        return "repeat"


def reset_params():
    AJE.reset_aje()
    TSPSolver.reset_tsp_solver()


def show_info_init():
    print("\n--== General Information ==--")
    print("File: " + file_name)
    print("Number of Threads: " + str(threads_number))
    print("Number of Convergences: " + str(number_of_convergences))
    print("Population: " + str(population_number))
    print("Mutation Probability: ( " + str(mutation_probability * 100) + "% )")


def start_program():
    start_time = time.perf_counter()
    show_info_init()
    AJE.read_from_file(file_name)
    AJE.start(mutation_probability, population_number,
              number_of_convergences, threads_number, start_time)
    exit(0)


if __name__ == "__main__":
    main()
