import random
import time
import statistics

from libs.ThreadToRun import ThreadToRun


class AJE:
    citiesNumber = None
    matrix = None
    filePathToShow = None
    bestDistances = []
    bestTimes = []

    @staticmethod
    def reset_AJE():
        AJE.citiesNumber = None
        AJE.matrix = None
        AJE.bestDistances = []
        AJE.bestTimes = []

    @staticmethod
    def read_From_File(fileName):
        AJE.filePathToShow = "TSP/files/" + fileName
        try:
            with open(AJE.filePathToShow, 'r') as file:
                lines = file.readlines()
                AJE.citiesNumber = int(lines[0].strip())
                AJE.matrix = [[int(num) for num in line.split()]
                              for line in lines[1:]]
                AJE.show_Info_From_File()
        except IOError as error:
            print(f"\nError reading the file: {error}")

    @staticmethod
    def show_Info_From_File():
        print("\n--== Informations of the City ==--")
        print(f"Number of Cities: N = {AJE.citiesNumber}")
        print("\n- Matrix -")
        for row in AJE.matrix:
            for value in row:
                print(f"{value:02d} | ", end='')
            print()

    @staticmethod
    def generate_path():
        path = list(range(AJE.citiesNumber))
        AJE.shuffle_array(path)
        return path

    @staticmethod
    def shuffle_array(array):
        for i in range(len(array)-1, 0, -1):
            index = random.randint(0, i)
            array[i], array[index] = array[index], array[i]

    @staticmethod
    def calc_path(path):
        valueOfPath = 0
        for i in range(AJE.citiesNumber):
            if i == (AJE.citiesNumber - 1):
                valueOfPath += AJE.matrix[path[i]][path[0]]
            else:
                valueOfPath += AJE.matrix[path[i]][path[i + 1]]
        return valueOfPath

    @staticmethod
    def start(mutationProb, populationNumber, execTime, threadsNumber, startTime):
        print("\n--== Calculate Paths ==--")
        for i in range(10):
            AJE.calc(i, threadsNumber, execTime,
                     mutationProb, populationNumber)

        smallestNumber = min(AJE.bestDistances)
        count = AJE.bestDistances.count(smallestNumber)
        average = statistics.mean(AJE.bestDistances)
        stdDev = statistics.pstdev(AJE.bestTimes)
        stdDevFormatted = f"{stdDev / 1_000_000_000:.1f}"

        print(
            f"Optimal found {count} times \t Average = {average} \t Std Dev = {stdDevFormatted}")

        formattedTimeExec = f"{(time.time() - startTime):.3f}"
        print(f"\nProgram runned in {formattedTimeExec} seconds")

    @staticmethod
    def calc(testNumber, threadsNumber, execTime, mutationProb, populationNumber):
        startTime = time.time()
        bestDistance = float('inf')
        threads = [ThreadToRun(execTime, mutationProb, populationNumber,
                               AJE.citiesNumber, AJE.matrix) for _ in range(threadsNumber)]
        for thread in threads:
            thread.start()

        while any(thread.is_alive() for thread in threads):
            time.sleep(0.01)

        execTimeTotal = time.time() - startTime
        formattedTime = f"{execTimeTotal:.3f}"
        bestDistance = min(thread.getBestDistanceFinal() for thread in threads)

        AJE.bestDistances.append(bestDistance)
        AJE.bestTimes.append(execTimeTotal)

        formattedTimeThread = f"{ThreadToRun.getFormattedTimeFinal():.3f}"
        print(f"{testNumber + 1:2d}  {AJE.citiesNumber} {AJE.filePathToShow}  {threadsNumber}\t\t{formattedTime}  {int(bestDistance)}\t\t\t {ThreadToRun.getIterationsFinal()}\t\t{formattedTimeThread}\t- {ThreadToRun.getBestPathFinal()}")

        for thread in threads:
            if thread.is_alive():
                thread.interrupt()

    @staticmethod
    def count_occurrences(array, target):
        return array.count(target)

    @staticmethod
    def find_smallest_number(array):
        if not array:
            raise ValueError("Array is empty")
        return min(array)

    @staticmethod
    def calculate_array_average_STD(array):
        if not array:
            raise ValueError("Array is empty")
        return statistics.pstdev(array)

    @staticmethod
    def calculate_array_average_distance(array):
        if not array:
            raise ValueError("Array is empty")
        return statistics.mean(array)
