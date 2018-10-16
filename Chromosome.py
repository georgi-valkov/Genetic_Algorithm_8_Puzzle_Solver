import random


class Chromosome:
    """
    Constructor
    """
    def __init__(self, state):
        self.state = state
        self.fitness_score = 0

    '''
    Crossover function for creating offspring
    Preconditions: Needs a Chromosome type object with valid state and another Chromosome type object
    with also a valid state
    Post conditions: Takes n number of elements, based on randomly generated pivot point, and merges them
    with m+k elements. The m elements come from the second Chromosome and the k elements are the remaining
    elements that complete the set [0-8]
    In other words, it returns a new Chromosome type object as a children
    '''
    def crossover(self, second_chromosome):

        pivot = random.randint(0, len(self.state)) # Randomly selecting middle point
        # Take elements from first array up to the randomly generated pivot point
        # and merge them with unique numbers from second array and also add what's missing from 0-8 sequence
        offspring = self.state[0:pivot] + [i for i in second_chromosome.state if i not in self.state[0:pivot]]
        return Chromosome(offspring)
    '''
    Mutate function - there is a certain % chance for mutation
    Preconditions: Needs a Chromosome type object with a valid state and mutation rate as float
    Post conditions: Swaps randomly two elements of the chromosome state
    '''
    def mutate(self, mutation_rate):
        for i in range(len(self.state)):
            if random.random() < mutation_rate:
                temp = random.randint(0, len(self.state) - 1)
                self.state[i], self.state[temp] = self.state[temp], self.state[i]