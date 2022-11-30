import random

import_pygame = [[0, 1, 8, 8, 2, 3, 6, 2, 2, 8],
                 [1, 0, 1, 5, 7, 3, 2, 1, 5, 7],
                 [8, 1, 0, 2, 5, 7, 4, 1, 2, 6],
                 [8, 5, 2, 0, 1, 7, 2, 4, 3, 9],
                 [2, 7, 5, 1, 0, 9, 2, 2, 1, 8],
                 [3, 3, 7, 7, 9, 0, 9, 6, 9, 3],
                 [6, 2, 4, 2, 2, 9, 0, 7, 2, 1],
                 [2, 1, 1, 4, 2, 6, 7, 0, 5, 2],
                 [2, 5, 2, 3, 1, 9, 2, 5, 0, 2],
                 [8, 7, 6, 9, 8, 3, 1, 2, 2, 0]]

chance_daun = 0.1

population_size = 500
population = []


class Parent:
    def __init__(self, chromosome, path):
        self.chromosome = chromosome
        self.path = path


def start_population():
    def shuffle_chromosome():
        chromosome = [1]
        start = [2, 3, 4, 5, 6, 7, 8, 9, 10]
        random.shuffle(start)
        chromosome += start
        chromosome.append(1)
        return chromosome


    for x in range(population_size):
        chromosome = shuffle_chromosome()
        while chromosome in population:
            chromosome = shuffle_chromosome()
        population.append(chromosome)

    parents = []

    for chromosome in population:
        parents.append(Parent(chromosome, sum_path(chromosome)))

    return parents


def sum_path(chromosome):
    path = 0
    for i in range(len(chromosome) - 1):
        start = chromosome[i] - 1
        end = chromosome[i + 1] - 1
        path += import_pygame[start][end]
    return path


parents = start_population()
print("Сформировали стартовую популяцию")
for i in parents: print(i.chromosome)


min_parent = parents[0]
min_era_parent = 0

for era in range(1, 5001):
    parents_pool = []

    def min_path(list_parents):
        min_parent = list_parents[0]
        for parent in list_parents:
            if min_parent.path > parent.path:
                min_parent = parent
        return min_parent


    while len(parents_pool) != population_size:
        list_loxov = []
        for i in range(5):
            index = random.randint(0, population_size-1)
            while index in list_loxov:
                index = random.randint(0, population_size-1)
            list_loxov.append(parents[index])
        parents_pool.append(min_path(list_loxov))

    # print("Отобрали родителей")
    # for i in parents_pool: print(i.chromosome)

    #  Скрещивание
    def cyclic_crossing(parents):
        def mutate(child_chromosome):
            gene1 = 0
            gene2 = 0
            while gene1 != gene2:
                gene1 = random.randint(1, 9)
                gene2 = random.randint(1, 9)
            child_chromosome[gene1], child_chromosome[gene2] = child_chromosome[gene2], child_chromosome[gene1]
            return child_chromosome

        def sex(mama, papa):
            child_chromosome = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
            i = 1
            j = len(papa) - 2
            while 0 in child_chromosome:
                if mama[i] not in child_chromosome:
                    for x in range(len(child_chromosome)):
                        if child_chromosome[x] == 0:
                            child_chromosome[x] = mama[i]
                            break
                    i += 1
                else:
                    i += 1

                if papa[j] not in child_chromosome:
                    for y in range(len(child_chromosome)-1, 0, -1):
                        if child_chromosome[y] == 0:
                            child_chromosome[y] = papa[j]
                            break
                    j -= 1
                else:
                    j -= 1

            if random.random() < chance_daun:
                return mutate(child_chromosome)
            return child_chromosome

        population = []
        for index_parent in range(0, len(parents) - 1, 2):
            mama = parents[index_parent].chromosome
            papa = parents[index_parent + 1].chromosome
            child_chromosome1 = sex(mama, papa)
            child_chromosome2 = sex(papa, mama)
            population.append(Parent(child_chromosome1, sum_path(child_chromosome1)))
            population.append(Parent(child_chromosome2, sum_path(child_chromosome2)))

        return population

    population = cyclic_crossing(parents_pool)

    print(f"Формирование {era} эпохи")
    # for i in population:
    #     print(i.chromosome, i.path)

    min_current_era_parent = min_path(population)
    print("Минимальный путь: " + str(min_current_era_parent.path))

    if min_parent.path > min_current_era_parent.path:
        min_parent = min_current_era_parent
        min_era_parent = era


print(f"ПОБЕДИТЕЛЬ ЭТОЙ ЖИЗНИ: {min_parent.chromosome} ПУТЬ: {min_parent.path}")
print(f"ЭРА ЭТОГО СЧАСТЛИВЧИКА {min_era_parent}")
