import sys
import time

from libs.AJE import AJE
from libs.TSPSolver import TSPSolver

fileName = ''
processesNumber = 0
numberOfConvergences = 0
populationNumber = 0
mutationProb = 0
aje = AJE()


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
            global fileName, processesNumber, numberOfConvergences, populationNumber, mutationProb
            fileName = params[0]
            processesNumber = int(params[1])
            numberOfConvergences = int(params[2])
            populationNumber = int(params[3])
            mutationProb = float(params[4])

            start_program()

            return "start"
    else:
        print("> <fileName> <processesNumber> <numberOfConvergences> <populationNumber> <mutationProb> (max: 1 (100%))")
        return "repeat"


def reset_params():
    aje.reset_aje()
    TSPSolver.reset_tsp_solver()


def show_info_init():
    print("\n--== General Information ==--")
    print("File: " + fileName)
    print("Number of Processes: " + str(processesNumber))
    print("Number of Convergences: " + str(numberOfConvergences))
    print("Population: " + str(populationNumber))
    print("Mutation Probability: ( " + str(mutationProb * 100) + "% )")


def start_program():
    start_time = time.time()
    show_info_init()
    aje.read_from_file(fileName)
    aje.start(mutationProb, populationNumber,
              numberOfConvergences, processesNumber, start_time)
    exit(0)


if __name__ == "__main__":
    main()
