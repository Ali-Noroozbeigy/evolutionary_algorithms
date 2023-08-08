import random
from math import fabs

POPULATION_SIZE = 200
ITERATION = 2000
epsilon = 10e-5
mutation_prob = 0.5


class Game:
    def __init__(self):
        self.levels = levels
        self.current_level_index = -1
        self.current_level_len = 0

    def load_next_level(self):
        self.current_level_index += 1
        self.current_level_len = len(self.levels[self.current_level_index])

    def fitness_function(self, actions):
        max_step_without_lose = 0
        steps = 0
        fitness_score = 0
        map = self.levels[self.current_level_index]

        for position in range(self.current_level_len):
            if actions[position] == '1':
                fitness_score -= 0.5
            if position == self.current_level_len-1 and actions[position] == '1':
                fitness_score += 1

            if map[position] == '_':
                steps += 1
            elif map[position] == 'G' and actions[position - 1] == '1':
                steps += 1
                fitness_score += 1
            elif map[position] == 'G' and position > 2 and actions[position-2] == '1':
                steps += 1
                fitness_score += 2
            elif map[position] == 'L' and actions[position - 1] == '2':
                steps += 1
                fitness_score += 2
            elif map[position] == 'M' and actions[position - 1] != '1':
                fitness_score += 2
            else:  # agent will lose
                if steps > max_step_without_lose:
                    max_step_without_lose = steps
                    steps = 0
        if steps > max_step_without_lose:
            max_step_without_lose = steps

        fitness_score += (max_step_without_lose // self.current_level_len-1) * 5 + max_step_without_lose

        return fitness_score


class Offspring:
    def __init__(self, actions, fitness):
        self.actions = actions
        self.fitness = fitness
        self.p = 0

    def update_p(self, sum_of_fitnesses):
        self.p = self.fitness / sum_of_fitnesses


def generate_initial_population():
    available_actions = ['0', '1', '2']
    sum_fitnesses = 0

    for i in range(POPULATION_SIZE):
        actions = random.choices(available_actions, k=game.current_level_len)
        fitness_score = game.fitness_function(actions)

        o = Offspring(actions, fitness_score)
        sum_fitnesses += fitness_score
        population.append(o)

    for o in population:
        o.update_p(sum_fitnesses)


def select():
    selected = []
    for i in range(int(POPULATION_SIZE / 2)):
        r = random.random()

        sum_p = 0
        for o in population:
            if r < (sum_p + o.p):
                selected.append(o)
                break
            sum_p += o.p
    return selected


def recombination():
    offsprings = []
    i = 0
    sum_fitnesses = 0

    while i != POPULATION_SIZE/2:

        for k in range(2):

            actions = []
            for a in range(game.current_level_len):
                m = random.random()
                if m < mutation_prob:
                    actions.append(mutate())
                else:
                    r = random.choice([0, 1])
                    if i == POPULATION_SIZE / 2:
                        r = 0
                    actions.append(parents[i+r].actions[a])

            f = game.fitness_function(actions)
            sum_fitnesses += f
            offsprings.append(Offspring(actions, f))
        i += 2

    for o in offsprings:
        o.update_p(sum_fitnesses)

    return offsprings


def mutate():
    return '0'


def mate():
    global population
    population = parents + recombination()


def find_fittest():
    max_fitness = -100
    fittest_pop = None

    for p in population:
        if p.fitness > max_fitness:
            max_fitness = p.fitness
            fittest_pop = p

    return fittest_pop


def find_average_fitness():
    sum_fitness = 0
    for p in population:
        sum_fitness += p.fitness

    return sum_fitness/POPULATION_SIZE


levels = []
for i in range(1, 11):
    with open(f"level{i}.txt", "r") as level_file:
        levels.append(level_file.read())

game = Game()
solutions = []

for i in range(10):
    population = []
    game.load_next_level()
    generate_initial_population()

    j = 0
    previous_avg_fitness = 0
    while j < ITERATION:
        parents = select()
        mate()

        new_average_fitness = find_average_fitness()
        if fabs(new_average_fitness - previous_avg_fitness) < epsilon:
            #print("Break")
            break
        previous_avg_fitness = new_average_fitness
        j += 1

    solutions.append(find_fittest().actions)

for sol in solutions:
    print(sol)
