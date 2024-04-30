import random


class PMX:
    @staticmethod
    def generate_child(number_of_cities, path1, path2, mutation_prob):
        n = number_of_cities
        off_spring1 = [0] * n
        off_spring2 = [0] * n

        PMX.pmx_crossover(path1, path2, off_spring1, off_spring2, n)
        PMX.mutate(off_spring1, mutation_prob)
        PMX.mutate(off_spring2, mutation_prob)

        return off_spring1, off_spring2

    @staticmethod
    def pmx_crossover(parent1, parent2, off_spring1, off_spring2, n):
        replacement1 = [-1] * (n + 1)
        replacement2 = [-1] * (n + 1)

        cutting_point1 = random.randint(0, n - 1)
        cutting_point2 = random.randint(0, n - 1)

        while cutting_point1 == cutting_point2:
            cutting_point2 = random.randint(0, n - 1)
        if cutting_point1 > cutting_point2:
            cutting_point1, cutting_point2 = cutting_point2, cutting_point1

        for i in range(cutting_point1, cutting_point2 + 1):
            off_spring1[i] = parent2[i]
            off_spring2[i] = parent1[i]
            replacement1[parent2[i]] = parent1[i]
            replacement2[parent1[i]] = parent2[i]

        for i in range(n):
            if i < cutting_point1 or i > cutting_point2:
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
                off_spring1[i] = n1
                off_spring2[i] = n2

    @staticmethod
    def mutate(offspring, mutation_probability):
        n = len(offspring)

        for _ in range(n):
            if random.random() < mutation_probability:
                mutation_index1 = random.randint(0, n - 1)
                mutation_index2 = random.randint(0, n - 1)

                offspring[mutation_index1], offspring[mutation_index2] = (offspring[mutation_index2],
                                                                          offspring[mutation_index1])
