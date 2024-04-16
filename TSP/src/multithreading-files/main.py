import sys
import time

from libs.AJE import AJE
from libs.TSPSolver import TSPSolver

fileName = None
threadsNumber = None
execTime = None
populationNumber = None
mutationProb = None


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
            global fileName, threadsNumber, execTime, populationNumber, mutationProb
            fileName = params[0]
            threadsNumber = int(params[1])
            execTime = int(params[2])
            populationNumber = int(params[3])
            mutationProb = float(params[4])

            start_program()

            return "start"
    else:
        print("> <fileName> <threadsNumber> <execTime> <populationNumber> <mutationProb> (max: 1 (100%))")
        return "repeat"


def reset_params():
    AJE.reset_AJE()
    TSPSolver.reset_TSPSolver()


def show_info_init():
    print("\n--== General Informations ==--")
    print("File: " + fileName)
    print("Number of Threads: " + str(threadsNumber))
    print("(MAX) Execution Time: " + str(execTime) + " second(s)")
    print("Population: " + str(populationNumber))
    print("Mutation Probability: ( " + str(mutationProb * 100) + "% )")


def start_program():
    start_time = time.time()
    show_info_init()
    AJE.read_From_File(fileName)
    AJE.start(mutationProb, populationNumber,
              execTime, threadsNumber, start_time)


if __name__ == "__main__":
    main()
