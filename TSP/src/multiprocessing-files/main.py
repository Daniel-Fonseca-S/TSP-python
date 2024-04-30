import sys
import time

from libs.AJE import AJE
from libs.TSPSolver import TSPSolver

fileName = ''
processesNumber = 0
execTime = 0
populationNumber = 0
mutationProb = 0


def main():
    try:
        while True:
            if request_params() == "over":
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
            global fileName, processesNumber, execTime, populationNumber, mutationProb
            fileName = params[0]
            processesNumber = int(params[1])
            execTime = int(params[2])
            populationNumber = int(params[3])
            mutationProb = float(params[4])

            start_program()

            return "start"
    else:
        print("> <fileName> <processesNumber> <execTime> <populationNumber> <mutationProb> (max: 1 (100%))")
        return "repeat"


def reset_params():
    AJE.reset_aje()
    TSPSolver.reset_tsp_solver()


def show_info_init():
    print("\n--== General Information ==--")
    print("File: " + fileName)
    print("Number of Processes: " + str(processesNumber))
    print("(MAX) Execution Time: " + str(execTime) + " second(s)")
    print("Population: " + str(populationNumber))
    print("Mutation Probability: ( " + str(mutationProb * 100) + "% )")


def start_program():
    start_time = time.time()
    show_info_init()
    AJE.read_from_file(fileName)
    AJE.start(mutationProb, populationNumber,
              execTime, processesNumber, start_time)


if __name__ == "__main__":
    main()
