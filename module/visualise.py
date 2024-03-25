# Import necessary libraries
import matplotlib.pyplot as plt


class __str__(object):
    def __str__(self):
        return self.__class__.__name__


class VisualiseSimilarity:
    def __init__(self, diff1: list, diff2: list):
        """Initialise the instance attributes"""
        self.diff1 = diff1
        self.diff2 = diff2

    def visualise_similarity(self) -> None:
        """
        Visualise the output of similarity of two distributions
        :return: A histogram of the absolute differences in seniority
        """
        # Set X axis as the range of the maximum absolute difference in seniority
        # and Y axis as the probability density to compare the distributions
        # of the absolute differences in seniority between all reverts and AB-BA sequences
        # Probability density is used to compare the distributions of samples as the number of samples is different

        # Plot the histograms
        fig, ax = plt.subplots()
        plt.hist(self.diff2, alpha=0.5, label="Other reverts", density=True, color="red")
        plt.hist(self.diff1, alpha=0.5, label="Mutual reverts", density=True, color="green")
        plt.title("Distribution of absolute differences in seniority")
        plt.xlim(0, max(max(self.diff1), max(self.diff2)))
        plt.ylim(0, 0.6)
        plt.xlabel("Absolute difference in seniority")
        plt.ylabel("Probability density")
        plt.legend(loc="upper right")

        return plt.show()
