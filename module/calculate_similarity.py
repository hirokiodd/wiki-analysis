# Import necessary libraries
import numpy as np


class __str__(object):
    def __str__(self):
        return self.__class__.__name__


class CreateComparisonNetwork:
    def __init__(self, sequence: list, network: list):
        """
        Initialise the instance attributes
        sequence (list): A list of sequences to be added to the existing_sequences set.
        network (list): A list of edges to be appended to the comparison_network list.
        """
        # Initialise the sequence and network
        self.sequence = sequence
        self.network = network
        # Initialise an empty list for the comparison network
        self.comparison_network = []
        # Initialise a set to keep track of the existing sequences
        self.existing_sequences = set()

    def create_comparison_network(self) -> list:
        """
        Creates a comparison network from a network
        :return: The comparison network list after adding the sequences and edges.
        """
        for seq in self.sequence:
            # Add the sequence to the set of existing sequences
            self.existing_sequences.add((seq[0], seq[1]))

        for edge in self.network:
            if (edge[0], edge[1]) not in self.existing_sequences:
                # Append the edge to the comparison network
                self.comparison_network.append(list(edge))

        return self.comparison_network


class CalculateSimilarity:
    def __init__(self):
        """Initialise the instance attributes"""
        # Initialise lists to store the absolute differences in seniority
        self.differences = []
        # Initialise an empty list for the comparison network
        self.comparison_network = []

    def calc_abs_difference(self, sequences: list) -> list:
        """
        Calculate the absolute difference between two edges
        :param sequences: The list of event sequences
        :return: The absolute difference between the two edges
        """
        # Iterate over the event sequences
        for seq in sequences:
            # Calculate the absolute difference in seniority for the AB-BA sequence
            difference = abs(seq[-2] - seq[-1])
            self.differences.append(difference)

        return self.differences

    def calc_mean_similarity(self, diff: list) -> float:
        """
        Calculate the mean similarity between two edges
        :param diff: The list of absolute differences in seniority
        :return: The mean similarity between the two edges
        """
        # Calculate the mean similarity
        mean_differences = np.mean(diff)

        return mean_differences
