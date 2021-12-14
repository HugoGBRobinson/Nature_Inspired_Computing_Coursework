import random

import ant


def bin_packing_problem():
    num_bins = 10
    num_items = 500
    items = generate_items(num_items)
    num_ants = 100
    iterations = 100
    total_all_fits = []

    # Distribute pheromone

    # Generate set of p ant paths from S to E
    for iteration in range(iterations):
        all_fits = []
        pheromone_matrix = ([([random.random() for i in range(num_items)]) for j in range(num_bins)])
        for i in range(num_ants):
            path = generate_path(pheromone_matrix, num_items, num_bins)
            fit = fitness(path, items, num_bins)
            all_fits.append(fit)
            if fit == 0:
                return fit
            # Update pheromone in the pheromone table for each ant's path according to fitness
            pheromone_matrix = update_pheromone(pheromone_matrix, fit, path)

            # Evaporate pheromone for all links in graph
        pheromone_matrix = evaporate_pheromone(pheromone_matrix)
        total_all_fits.append(min(all_fits))
    # Termination criteria met
    print(total_all_fits)
    return total_all_fits


def generate_path(pheromone_matrix, num_items, num_bins):
    path = []
    for i in range(num_items):
        path.append(next_node(pheromone_matrix, i, num_bins))
    return path


def next_node(pheromone_matrix, at_item, num_bins):
    bins = []
    for i in range(num_bins):
        bins.append(pheromone_matrix[i][at_item])
    cumulative_probabilities = generate__cumulative_probabilitys(bins)
    return get_node_from_cumulative_probabilities(cumulative_probabilities)


def generate__cumulative_probabilitys(bins):
    Sum = sum(bins)
    cumulative_probabilities = []
    for i in range(len(bins)):
        if i == 0:
            cumulative_probabilities.append(bins[i] / Sum)
        else:
            cumulative_probabilities.append(cumulative_probabilities[i - 1] + bins[i] / Sum)
    return cumulative_probabilities


def get_node_from_cumulative_probabilities(cumulative_probabilities):
    rand = random.random()
    difference = 1000000000
    for i in range(len(cumulative_probabilities)):
        if (cumulative_probabilities[i] - rand) ** 2 < difference:
            difference = (cumulative_probabilities[i] - rand) ** 2
            next_node = i
    return next_node


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
    rho = 0.1
    for i in range(len(pheromone_matrix)):
        for j in range(len(pheromone_matrix[i])):
            pheromone_matrix[i][j] = pheromone_matrix[i][j] * (1 - rho)
    return pheromone_matrix


def generate_items(num_items):
    return [i + 1 for i in range(num_items)]


#     num_bins = 10
#     num_items = 500
#     items = generate_items(num_items)
#     print(items)
#     num_ants = 100
#     best_difference = 10000000
#     for i in range(5):
#         pheromone_matrix = ([([random.random() for i in range(len(items))]) for j in range(num_bins)])
#         smallest_path = []
#         smallest_difference = 10000000
#         iteration = 0
#         while iteration != 10000:
#             print(iteration)
#             for i in range(num_ants):
#                 path = ant.Ant(number=i, current_node=0, iteration=1, items=items,
#                                pheremone_matrix=pheromone_matrix).create_path()
#                 fit = fitness(path, items, num_bins)
#                 if fit == 0:
#                     smallest_path = path
#                     print(smallest_path)
#                     smallest_difference = fit
#                     print(smallest_difference)
#                     return smallest_path
#                 if fit < smallest_difference:
#                     smallest_path = path
#                     print(smallest_path)
#                     smallest_difference = fit
#                     print(smallest_difference)
#                 pheromone_matrix = update_pheromones(pheromone_matrix, path, fit)
#                 # print(pheromone_matrix)
#             iteration += 1
#
#         print(smallest_path)
#         print(smallest_difference)
#         if smallest_difference < best_difference:
#             best_difference = smallest_difference
#     print(best_difference)
#
#
# def fitness(path, items, num_bins):
#     bins = [0] * num_bins
#     for i in range(len(path)):
#         bins[path[i]] += items[i]
#     return max(bins) - min(bins)
#     # Find the largest difference between bins, this is fitness
#
#
# def generate_items(num_items):
#     return [i + 1 for i in range(num_items)]
#
#
# def update_pheromones(pheromone_matrix, path, fit):
#     # Evaporation
#     rho = 0.1
#     for i in range(len(pheromone_matrix)):
#         for j in range(len(pheromone_matrix[i])):
#             pheromone_matrix[i][j] = pheromone_matrix[i][j] * (1 - rho)
#     # Ant Deposit
#     for i in range(len(path)):
#         if i < len(path) - 1:
#             pheromone_matrix[path[i]][path[i + 1]] += 100 / fit
#     return pheromone_matrix
#
#
# def termination(num_bins, num_items):
#     return num_bins * num_items
#

if __name__ == '__main__':
    bin_packing_problem()
