import multiprocessing as mp
import time


class ProcessToRun(mp.Process):

    def __init__(self, timePerProcess, mutProb, populSize, citSize, matrixReceive, manager):
        mp.Process.__init__(self)
        self.timePerProcess = timePerProcess
        self.shared_data = manager.dict({
            'mutationProb': mutProb,
            'populationSize': populSize,
            'citiesNumber': citSize,
            'matrix': matrixReceive,
            'bestDistanceFinal': None,
            'bestPathFinal': None,
            'iterationsFinal': None,
            'timeFinal': None
        })

    def run(self):
        from libs.TSPSolver import TSPSolver
        startTime = time.time()
        timeToExec = self.timePerProcess
        for _ in range(1, 1_000_000_000 + 1):
            TSPSolver.start(
                self.timePerProcess,
                self.shared_data['mutationProb'],
                self.shared_data['populationSize'],
                self.shared_data['citiesNumber'],
                self.shared_data['matrix']
            )
            if (time.time() - startTime) >= timeToExec:
                break

        self.shared_data['bestDistanceFinal'] = TSPSolver.bestDistance
        self.shared_data['bestPathFinal'] = TSPSolver.bestPath
        self.shared_data['iterationsFinal'] = TSPSolver.iterations
        self.shared_data['timeFinal'] = TSPSolver.execTimeFound

    def getBestDistanceFinal(self):
        return self.shared_data['bestDistanceFinal']

    def getBestPathFinal(self):
        return self.shared_data['bestPathFinal']

    def getIterationsFinal(self):
        return self.shared_data['iterationsFinal']

    def getFormattedTimeFinal(self):
        return self.shared_data['timeFinal']
