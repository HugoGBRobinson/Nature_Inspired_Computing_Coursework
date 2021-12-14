import random


class Ant:
    def __init__(self, number, current_node, iteration, items, pheremone_matrix):
        self.number = number
        self.current_node = current_node
        self.iteration = iteration
        self.items = items
        self.pheremone_matrix = pheremone_matrix
        self.path = []

    def next_node(self):
        numerators = []
        cumulative_probabilities = []
        for i in range(len(self.pheremone_matrix)):
            numerators.append(self.pheremone_matrix[self.current_node][i])

        probabilities = [b / sum(numerators) for b in numerators]
        for i in range(len(self.pheremone_matrix)):
            if i == 0:
                cumulative_probabilities.append(probabilities[i])
            else:
                cumulative_probabilities.append(cumulative_probabilities[i - 1] + probabilities[i])

        rand = random.random()
        next_node = 0
        difference = 1000000000
        for i in range(len(cumulative_probabilities)):
            if (cumulative_probabilities[i] - rand) ** 2 < difference:
                difference = (cumulative_probabilities[i] - rand) ** 2
                next_node = i

        return next_node

    def create_path(self):
        for i in range(len(self.items)):
            self.current_node = self.next_node()
            self.path.append(self.current_node)
            # Update pheromone tabel
            # Evaporate
        return self.path
