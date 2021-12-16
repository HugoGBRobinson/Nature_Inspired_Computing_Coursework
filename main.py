import matplotlib.pyplot as plt
import numpy
import numpy as np
import time


def bin_packing_problem():
    """
    This is the primary function of the algorithm where
    :return:
    """
    num_bins = 10
    num_items = 500
    items = np.arange(0, num_items)
    num_ants = 100
    fitness_evaluations = 10
    iterations = 5
    total_fitness = []
    x = []
    y = []

    for iteration in range(iterations):
        # Distribute pheromone
        pheromone_matrix = np.random.rand(num_bins, num_items)
        start = time.time()
        for fitness_evaluation in range(fitness_evaluations):

            best_fitness = 100000000
            best_path = []

            for j in range(num_ants):

                # Generate set of p ant paths from S to E

                path = generate_path(pheromone_matrix, num_items, num_bins)

                fit = fitness(path, items, num_bins)

                if fit == 0:
                    best_path = path
                    best_fitness = fit
                    break
                elif fit < best_fitness:
                    best_path = path
                    best_fitness = fit
                # Update pheromone in the pheromone table for each ant's path according to fitness

                pheromone_matrix = update_pheromone(pheromone_matrix, fit, path)

            x.append(fitness_evaluation + 1)
            y.append(best_fitness)
            # Evaporate pheromone for all links in graph
            pheromone_matrix = evaporate_pheromone(pheromone_matrix)
        end = time.time()
        print((end - start) * 1)
        plt.plot(x, y, label="Iteration" + str(iteration + 1))
        x = []
        y = []
        # Termination criteria met
        print(best_fitness)
        total_fitness.append(best_fitness)
    plt.legend()
    plt.show()
    return total_fitness


def generate_path(pheromone_matrix, num_items, num_bins):
    path = np.zeros([num_items, 1], dtype=numpy.int8).flatten()

    for i in range(num_items):
        path[i] = next_node(pheromone_matrix, i, num_bins)

    return path


def next_node(pheromone_matrix, at_item, num_bins):
    bins = np.zeros([num_bins, 1]).flatten()

    for i in range(num_bins):
        bins[i] = pheromone_matrix[i][at_item]

    cumulative_probabilities = generate_cumulative_probabilities(bins)

    return get_node_from_cumulative_probabilities(cumulative_probabilities)


def generate_cumulative_probabilities(bins):
    # Half the time taken up here?
    Sum = np.sum(bins)
    cumulative_probilities = np.zeros(shape=(len(bins)))
    divided = divide_by_sum(bins, Sum)
    acumlator = 0
    for i in range(len(bins)):
        acumlator = acumlator + divided[i]
        cumulative_probilities[i] = acumlator
    return divided


def divide_by_sum(x, sum):
    return x / sum


def get_node_from_cumulative_probabilities(cumulative_probabilities):
    rand = np.random.rand()
    cumulative_probabilities = np.asarray(cumulative_probabilities)
    idx = (np.abs(cumulative_probabilities - rand)).argmin()

    return idx


def fitness(path, items, num_bins):
    # Create an array of bins to exact size to allow for O(1) insertion
    bins = [0] * num_bins
    for i in range(len(path)):
        bins[path[i]] += items[i]
    # Find the largest difference between bins, this is fitness
    return max(bins) - min(bins)


def update_pheromone(pheromone_matrix, fit, path):
    # Ant Deposit
    for i in range(len(path)):
        if i < len(path) - 1:
            pheromone_matrix[path[i]][path[i + 1]] += 100 / fit
    return pheromone_matrix


def evaporate_pheromone(pheromone_matrix):
    # Evaporation
    pheromone_matrix = add_rho(pheromone_matrix)
    return pheromone_matrix


def add_rho(x):
    rho = 0.1
    return x * rho


if __name__ == '__main__':
    bin_packing_problem()
