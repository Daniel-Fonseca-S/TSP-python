import random


class PMX:
    @staticmethod
    def generate_child(numberOfCities, path1, path2, mutationProb):
        n = numberOfCities
        offSpring1 = [0]*n
        offSpring2 = [0]*n

        PMX.pmxCrossover(path1, path2, offSpring1, offSpring2, n)
        PMX.mutate(offSpring1, mutationProb)
        PMX.mutate(offSpring2, mutationProb)

        return offSpring1, offSpring2

    @staticmethod
    def pmxCrossover(parent1, parent2, offSpring1, offSpring2, n):
        replacement1 = [-1]*(n+1)
        replacement2 = [-1]*(n+1)

        cuttingPoint1 = random.randint(0, n-1)
        cuttingPoint2 = random.randint(0, n-1)

        while cuttingPoint1 == cuttingPoint2:
            cuttingPoint2 = random.randint(0, n-1)
        if cuttingPoint1 > cuttingPoint2:
            cuttingPoint1, cuttingPoint2 = cuttingPoint2, cuttingPoint1

        for i in range(cuttingPoint1, cuttingPoint2+1):
            offSpring1[i] = parent2[i]
            offSpring2[i] = parent1[i]
            replacement1[parent2[i]] = parent1[i]
            replacement2[parent1[i]] = parent2[i]

        for i in range(n):
            if i < cuttingPoint1 or i > cuttingPoint2:
                n1 = parent1[i]
                m1 = replacement1[n1]
                n2 = parent2[i]
                m2 = replacement2[n2]
                while m1 != -1:
                    n1 = m1
                    m1 = replacement1[m1]
                while m2 != -1:
                    n2 = m2
                    m2 = replacement2[m2]
                offSpring1[i] = n1
                offSpring2[i] = n2

    @staticmethod
    def mutate(offspring, mutationProbability):
        n = len(offspring)

        for i in range(n):
            if random.random() < mutationProbability:
                mutationIndex1 = random.randint(0, n-1)
                mutationIndex2 = random.randint(0, n-1)

                offspring[mutationIndex1], offspring[mutationIndex2] = offspring[mutationIndex2], offspring[mutationIndex1]
