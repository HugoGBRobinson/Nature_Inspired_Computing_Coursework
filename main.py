import matplotlib.pyplot as plt
import numpy
import numpy as np
import time


def bin_packing_problem():
    """
    This is the primary function of the algorithm where initial variables are set and the primary iteration runs
    """
    # All preset variables
    num_bins = 10
    num_items = 500
    items = np.arange(0, num_items)
    # Uncomment for BPP2 Experiments
    # items = square(items)
    num_ants = 100
    fitness_evaluations = 100
    iterations = 5
    total_fitness = []
    x = []
    y = []

    for iteration in range(iterations):
        # Distribute pheromone
        pheromone_matrix = np.random.rand(num_bins, num_items)
        for fitness_evaluation in range(fitness_evaluations):
            # A large best fitness to compare each ant to for each fitness evaluation
            best_fitness = 100000000
            for j in range(num_ants):
                # Generate set of p ant paths from S to E
                path = generate_path(pheromone_matrix, num_items, num_bins)
                fit = fitness(path, items, num_bins)
                # If the fitness is zero then it is a perfect solution and the loop ends
                if fit == 0:
                    best_fitness = fit
                    break
                elif fit < best_fitness:
                    best_fitness = fit
                # Update pheromone in the pheromone table for each ant's path according to fitness
                pheromone_matrix = update_pheromone(pheromone_matrix, fit, path)
            x.append(fitness_evaluation + 1)
            y.append(best_fitness)
            # Evaporate pheromone for all links in graph
            pheromone_matrix = evaporate_pheromone(pheromone_matrix)
        # A plot to produce the graphs
        plt.plot(x, y, label="Iteration" + str(iteration + 1))
        x = []
        y = []
        # Termination criteria met
        print(best_fitness)
        total_fitness.append(best_fitness)
    plt.title("Experiment 2 BPP 4")
    plt.xlabel("Fitness Evaluation")
    plt.ylabel("Best Fitness")
    plt.legend()
    plt.show()


def square(x):
    """
    A function that takes in a value and squares it.
    :param x: A number
    :return: The number x squared
    """
    return x ** 2


def generate_path(pheromone_matrix, num_items, num_bins):
    """
    This function produces the ants' path through the problem
    :param pheromone_matrix: The pheromone matrix that guides the ants' path
    :param num_items: The number of items set in bin_packing_problem()
    :param num_bins: The number of bins set in bin_packing_problem()
    :return: A 1D numpy array of integers that is the ants' path
    """
    path = np.zeros([num_items, 1], dtype=numpy.int8).flatten()
    # For each element in the path generate a node
    for i in range(num_items):
        path[i] = next_node(pheromone_matrix, i, num_bins)

    return path


def next_node(pheromone_matrix, at_item, num_bins):
    """
    A function that decides the next node in the ants' path
    :param pheromone_matrix: The pheromone matrix that guides the ants' path
    :param at_item: The item that the ant is currently at
    :param num_bins: The number of bins set in bin_packing_problem()
    :return: An integer representing the next node in the path
    """
    bins = np.zeros([num_bins, 1]).flatten()

    # For the number of bins, add their pheromone value to bins
    for i in range(num_bins):
        bins[i] = pheromone_matrix[i][at_item]

    cumulative_probabilities = generate_cumulative_probabilities(bins)

    return get_node_from_cumulative_probabilities(cumulative_probabilities)


def generate_cumulative_probabilities(bins):
    """
    A function that generates the cumulative probabilities of each of the next bins
    :param bins: A numpy array containing all the pheromone values for the next bins in the path
    :return: A numpy array of the cumulative probabilities of each bin
    """
    Sum = np.sum(bins)
    cumulative_probilities = np.zeros(shape=(len(bins)))
    divided = divide_by_sum(bins, Sum)
    acumlator = 0
    # For the number of bins, add the new value to all the previous and append it to cumulative_probilities
    for i in range(len(bins)):
        acumlator = acumlator + divided[i]
        cumulative_probilities[i] = acumlator
    return cumulative_probilities


def divide_by_sum(x, sum):
    """
    A function that divides a value by another number
    :param x: The value
    :param sum: The sum of the bins
    :return: A float of the divided value
    """
    return x / sum


def get_node_from_cumulative_probabilities(cumulative_probabilities):
    """
    Produces the next node from the cumulative probabilities by creating a random number between 0 and 1 and getting the
    index of the number it is closest to
    :param cumulative_probabilities: A numpy array of the cumulative probabilities of each bin
    :return: An integer that is the next bin
    """
    # Generate a random number between 0 and 1
    rand = np.random.rand()
    cumulative_probabilities = np.asarray(cumulative_probabilities)
    # Find the closest index to the random number
    idx = (np.abs(cumulative_probabilities - rand)).argmin()

    return idx


def fitness(path, items, num_bins):
    """
    A function that generates the fitness of a path
    :param path: A numpy array containing the path taken by the ant
    :param items: A numpy array of all the items
    :param num_bins: The number of bins
    :return: Returns the max number bin - the min number bin to provide a fitness value
    """
    # Create an array of bins to exact size to allow for O(1) insertion
    bins = [0] * num_bins
    for i in range(len(path)):
        bins[path[i]] += items[i]
    # Find the largest difference between bins, this is fitness
    return max(bins) - min(bins)


def update_pheromone(pheromone_matrix, fit, path):
    """
    A function to update the pheromone matrix based on the fitness of a path
    :param pheromone_matrix: The pheromone matrix that guides the ants' path
    :param fit: The fitness of the path
    :param path: A numpy array containing the path taken by the ant
    :return: The updated pheromone matrix is returned
    """
    # Ant Deposit
    for i in range(len(path)):
        if i < len(path) - 1:
            # Deposit 100 divided by the fitness to each node in the ants' path
            pheromone_matrix[path[i]][path[i + 1]] += 100 / fit
    return pheromone_matrix


def evaporate_pheromone(pheromone_matrix):
    """
    A function to evaporate the pheremones based on rho
    :param pheromone_matrix: The pheromone matrix that guides the ants' path
    :return: The updated pheromone matrix is returned
    """
    # Evaporation
    pheromone_matrix = add_rho(pheromone_matrix)
    return pheromone_matrix


def add_rho(x):
    """
    A function that takes in a value and multiplies it by (1-rho)
    :param x: The input value from the pheromone matrix
    :return: Returns the updated value
    """
    # rho can be changed here for each experiment
    rho = 0.1
    return x * (1 - rho)


if __name__ == '__main__':
    bin_packing_problem()
