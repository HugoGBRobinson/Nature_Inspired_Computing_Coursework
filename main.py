import random

import ant


def bin_packing_problem():
    num_bins = 10
    num_items = 500
    items = generate_items(num_items)
    print(items)
    num_ants = 100
    best_difference = 10000000
    for i in range(5):
        pheromone_matrix = ([([random.random() for i in range(len(items))]) for j in range(num_bins)])
        smallest_path = []
        smallest_difference = 10000000
        iteration = 0
        while iteration != 10000:
            print(iteration)
            for i in range(num_ants):
                path = ant.Ant(number=i, current_node=0, iteration=1, items=items,
                               pheremone_matrix=pheromone_matrix).create_path()
                fit = fitness(path, items, num_bins)
                if fit == 0:
                    smallest_path = path
                    print(smallest_path)
                    smallest_difference = fit
                    print(smallest_difference)
                    return smallest_path
                if fit < smallest_difference:
                    smallest_path = path
                    print(smallest_path)
                    smallest_difference = fit
                    print(smallest_difference)
                pheromone_matrix = update_pheromones(pheromone_matrix, path, fit)
                # print(pheromone_matrix)
            iteration += 1

        print(smallest_path)
        print(smallest_difference)
        if smallest_difference < best_difference:
            best_difference = smallest_difference
    print(best_difference)


def fitness(path, items, num_bins):
    bins = [0] * num_bins
    for i in range(len(path)):
        bins[path[i]] += items[i]
    return max(bins) - min(bins)
    # Find the largest difference between bins, this is fitness


def generate_items(num_items):
    return [i + 1 for i in range(num_items)]


def update_pheromones(pheromone_matrix, path, fit):
    # Evaporation
    rho = 0.1
    for i in range(len(pheromone_matrix)):
        for j in range(len(pheromone_matrix[i])):
            pheromone_matrix[i][j] = pheromone_matrix[i][j] * (1 - rho)
    # Ant Deposit
    for i in range(len(path)):
        if i < len(path) - 1:
            pheromone_matrix[path[i]][path[i + 1]] += 100 / fit
    return pheromone_matrix


def termination(num_bins, num_items):
    return num_bins * num_items


if __name__ == '__main__':
    bin_packing_problem()
