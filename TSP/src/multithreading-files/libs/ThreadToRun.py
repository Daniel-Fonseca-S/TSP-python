import threading
import time


class ThreadToRun(threading.Thread):
    mutationProb = None
    populationSize = None
    citiesNumber = None
    matrix = None
    bestDistanceFinal = None
    bestPathFinal = None
    iterationsFinal = None
    timeFinal = None

    def __init__(self, timePerThread, mutProb, populSize, citSize, matrixReceive):
        threading.Thread.__init__(self)
        self.timePerThread = timePerThread
        ThreadToRun.mutationProb = mutProb
        ThreadToRun.populationSize = populSize
        ThreadToRun.citiesNumber = citSize
        ThreadToRun.matrix = matrixReceive

    def run(self):
        from libs.TSPSolver import TSPSolver
        startTime = time.time()
        timeToExec = self.timePerThread
        for _ in range(1, 1_000_000_000 + 1):
            TSPSolver.start(
                self.timePerThread,
                ThreadToRun.mutationProb,
                ThreadToRun.populationSize,
                ThreadToRun.citiesNumber,
                ThreadToRun.matrix
            )
            if (time.time() - startTime) >= timeToExec:
                break

        ThreadToRun.setBestDistanceFinal(TSPSolver.bestDistance)
        ThreadToRun.setBestPathFinal(TSPSolver.bestPath)
        ThreadToRun.setIterationsFinal(TSPSolver.iterations)
        ThreadToRun.setFormattedTimeFinal(TSPSolver.execTimeFound)

    @staticmethod
    def setBestDistanceFinal(bDistance):
        ThreadToRun.bestDistanceFinal = bDistance

    @staticmethod
    def getBestDistanceFinal():
        return ThreadToRun.bestDistanceFinal

    @staticmethod
    def setBestPathFinal(bPath):
        ThreadToRun.bestPathFinal = bPath

    @staticmethod
    def getBestPathFinal():
        return ThreadToRun.bestPathFinal

    @staticmethod
    def setIterationsFinal(it):
        ThreadToRun.iterationsFinal = it

    @staticmethod
    def getIterationsFinal():
        return ThreadToRun.iterationsFinal

    @staticmethod
    def setFormattedTimeFinal(timeFinalInsert):
        ThreadToRun.timeFinal = timeFinalInsert

    @staticmethod
    def getFormattedTimeFinal():
        return ThreadToRun.timeFinal
