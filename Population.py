from Chromosome import Chromosome
import random
import numpy as np


class Population:
    """
    Constructor
    """
    def __init__(self, initial_state, goal_state, initial_population, mutation_rate, shape):
        self.initial_state = initial_state              # It is used to create the initial population
        self.goal_state = goal_state                    # State that needs to be reached
        self.initial_population = initial_population    # Number of initial population
        self.mutation_rate = mutation_rate              # Specified mutation rate (float 0.01 = 1%)
        self.members = []                               # Array that will hold all of the population or Chromosomes
        self.generation = 0                             # Generation counter
        self.goal_reached = False                       # Boolean indicator for reaching the goal
        self.darwin_pool = []                           # "Darwin pool" array that will hold multiplications of
                                                        # Chromosome objects based on their fitness
        self.shape = shape                              # Shape of the square ex. 3x3,4x4
        self.avg_fitness = 0                            # Population's average fitness

        self.elite_chromosome = Chromosome(initial_state) # Elite Chromosome - closest to the goal
        # Calculate fitness score of the elite chromosome
        self.elite_chromosome.fitness_score = count_sim_elements(initial_state, goal_state)
        # Create initial population by shuffling the elements of the initial sate
        for i in range(self.initial_population):
            self.members.append(Chromosome(state=random.sample(self.initial_state, len(self.initial_state))))

    '''
    Calculate fitness score
    Preconditions: Needs a Population type object with members container filled with Chromosomes
    Post conditions: Calculates fitness for ever Chromosome in members and also
    the average fitness for the whole population. It fills the Darwin pool as well with multiplications of
    Chromosomes based on their fitness score. For example, if Chromosome x has 7 fitness score and y has 5,
    the function adds x to Darwin pool 7 times and y only 5 times. Thus fittest Chromosomes has the best chance
    to be picked up and create offspring.
    '''
    def calculate_fitness(self):
        average_fitness = 0
        self.darwin_pool = []
        for chromosome in self.members:
            chromosome.fitness_score = count_sim_elements(chromosome.state, self.goal_state)
            average_fitness += chromosome.fitness_score
            # Update darwin_pool based on fitness scores
            for i in range(chromosome.fitness_score):
                self.darwin_pool.append(chromosome)
        self.avg_fitness = average_fitness / len(self.members)

    '''
    Preconditions: Needs a Population type object with members container filled with Chromosomes
    Post conditions: Creates a new generation of Chromosomes and replaces the old ones. For each iteration,
    two parents are randomly picked from the Darwin pool to create a child. A mutation function is applied
    and the child replaces a current member of the population. As a result the whole population gets
    replaced by new members.
    It also increments the generation counter 
    '''
    def produce_new_generation(self):
        for i in range(len(self.members)):
            # Pick parent A from the pool
            parent_a = self.darwin_pool[random.randint(0, len(self.darwin_pool) - 1)]
            # Pick parent B from pool
            parent_b = self.darwin_pool[random.randint(0, len(self.darwin_pool) - 1)]
            # Create offspring
            offspring = parent_a.crossover(parent_b)
            # Apply mutation j% chance
            offspring.mutate(mutation_rate=self.mutation_rate)
            # Replace an old member of the population with new
            self.members[i] = offspring
        # Increment the number of generations
        self.generation += 1

    """ Criterion for evaluating each of the chromosomes """
    # There must be a valid tile move comparing to the state of the previous elite chromosome
    #   - valid moves are move to left, right, up and down if at the target position resides
    #     0 which denotes an empty cell
    '''
    Evaluates every Chromosome in search for a valid move
    Preconditions: Needs a Population type object with members container filled with Chromosomes as well as
    an elite chromosome
    Post conditions: Compares every member in the population with the elite Chromosome and if their states
    have only two differences it also checks whether those differences result in a valid move based on the
    position of the zero.
    Returns a composed string that is used to update GUI
    '''
    def evaluate(self):

        for chromosome in self.members:
            # Validate chromosomes
            # 1. Check if there is only two different positions
            # 2. CHeck for valid move depending on the position of the zero

            current_chromosome_zero_index = chromosome.state.index(0)
            elite_chromosome_zero_index = self.elite_chromosome.state.index(0)

            difference = (np.array(self.elite_chromosome.state) != np.array(chromosome.state)).sum()
            if difference == 2:
                # Possible moves based on the position of the zero
                if current_chromosome_zero_index == 0:
                    if elite_chromosome_zero_index - current_chromosome_zero_index == 1 \
                            or current_chromosome_zero_index - elite_chromosome_zero_index == 3:
                        self.elite_chromosome = chromosome
                        return " Valid Move -" + ' '.join(str(e) for e in chromosome.state) + '-' + str(
                            self.generation) + '-' + str(self.avg_fitness)
                elif current_chromosome_zero_index == 1:
                    if elite_chromosome_zero_index - current_chromosome_zero_index == 1\
                            or elite_chromosome_zero_index - current_chromosome_zero_index == -1\
                            or elite_chromosome_zero_index - current_chromosome_zero_index == 3:
                        self.elite_chromosome = chromosome
                        return " Valid Move -" + ' '.join(str(e) for e in chromosome.state) + '-' + str(
                            self.generation) + '-' + str(self.avg_fitness)
                elif current_chromosome_zero_index == 2:
                    if elite_chromosome_zero_index - current_chromosome_zero_index == -1 \
                            or current_chromosome_zero_index - elite_chromosome_zero_index == 3:
                        self.elite_chromosome = chromosome
                        return " Valid Move -" + ' '.join(str(e) for e in chromosome.state) + '-' + str(
                            self.generation) + '-' + str(self.avg_fitness)
                elif current_chromosome_zero_index == 3:
                    if elite_chromosome_zero_index - current_chromosome_zero_index == 1\
                            or elite_chromosome_zero_index - current_chromosome_zero_index == 3\
                            or elite_chromosome_zero_index - current_chromosome_zero_index == -3:
                        self.elite_chromosome = chromosome
                        return " Valid Move -" + ' '.join(str(e) for e in chromosome.state) + '-' + str(
                            self.generation) + '-' + str(self.avg_fitness)
                elif current_chromosome_zero_index == 4:
                    if elite_chromosome_zero_index - current_chromosome_zero_index == 1 \
                            or elite_chromosome_zero_index - current_chromosome_zero_index == -1 \
                            or elite_chromosome_zero_index - current_chromosome_zero_index == 3 \
                            or elite_chromosome_zero_index - current_chromosome_zero_index == -3:
                        self.elite_chromosome = chromosome
                        return " Valid Move -" + ' '.join(str(e) for e in chromosome.state) + '-' + str(
                            self.generation) + '-' + str(self.avg_fitness)
                elif current_chromosome_zero_index == 5:
                    if elite_chromosome_zero_index - current_chromosome_zero_index == -1 \
                            or elite_chromosome_zero_index - current_chromosome_zero_index == 3 \
                            or elite_chromosome_zero_index - current_chromosome_zero_index == -3:
                        self.elite_chromosome = chromosome
                        return " Valid Move -" + ' '.join(str(e) for e in chromosome.state) + '-' + str(
                            self.generation) + '-' + str(self.avg_fitness)
                elif current_chromosome_zero_index == 6:
                    if elite_chromosome_zero_index - current_chromosome_zero_index == 1 \
                            or elite_chromosome_zero_index - current_chromosome_zero_index == -3:
                        self.elite_chromosome = chromosome
                        return " Valid Move -" + ' '.join(str(e) for e in chromosome.state) + '-' + str(
                            self.generation) + '-' + str(self.avg_fitness)
                elif current_chromosome_zero_index == 7:
                    if elite_chromosome_zero_index - current_chromosome_zero_index == 1 \
                            or elite_chromosome_zero_index - current_chromosome_zero_index == -1 \
                            or elite_chromosome_zero_index - current_chromosome_zero_index == -3:
                        self.elite_chromosome = chromosome
                        return " Valid Move -" + ' '.join(str(e) for e in chromosome.state) + '-' + str(
                            self.generation) + '-' + str(self.avg_fitness)
                elif current_chromosome_zero_index == 8:
                    if elite_chromosome_zero_index - current_chromosome_zero_index == -1 \
                            or elite_chromosome_zero_index - current_chromosome_zero_index == -3:
                        self.elite_chromosome = chromosome
                        return " Valid Move -" + ' '.join(str(e) for e in chromosome.state) + '-' + str(
                            self.generation) + '-' + str(self.avg_fitness)


'''
A Static function
Preconditions: Two int arrays of the same length
Post Conditions: Counts the similar elements in array a and b
and returns that count
'''
def count_sim_elements(a, b):
    count = 0
    for i in range(len(a)):
        if a[i] == b[i]:
            count += 1
    return count
