# Import nesessay libraries
import math
import pickle
from datetime import datetime


class __str__(object):
    def __str__(self):
        return self.__class__.__name__


class Text2Data:
    """
    A class that transforms text data into a list of fields.

    Attributes:
        input_text (str): The path to the input text file.
        raw_data (list): A list to store the transformed data.

    Methods:
        __init__(self, input_text: str): Initializes the instance attributes.
        text_to_data(self) -> list: Transforms the text data into a list.

    """

    def __init__(self, input_text: str):
        """Initialise the instance attributes"""
        # Initialise the input text
        self.input_text = input_text
        # Initialise an empty list for the transformed data
        self.raw_data = []

    def text_to_data(self) -> list:
        """
        Transform text data into a list

        Returns:
            list: A list containing the transformed data.

        """
        # Open the file and iterate over the lines
        with open(self.input_text, "r") as file:
            # Skip the header line
            next(file)
            # Iterate over the lines in reverse order
            for line in reversed(list(file)):
                # Split the line into fields
                title, time, revert, version, user = line.strip().split("\t")
                # Convert revert and version to integers
                time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                revert = int(revert)
                version = int(version)
                # Add the fields to the list
                self.raw_data.append([title, time, revert, version, user])
        return self.raw_data


class CreateEditHistory:
    def __init__(self, data: Text2Data):
        """Initialise the instance attributes"""
        self.data = data
        self.edit_history = {}

    def create_edit_history(self):
        """
        Create a dictionary of edit history which keys are user and values are time
        """
        # Iterate over the data and create a dictionary of edit history
        for data in self.data:
            _, time, _, _, user = data
            if user not in self.edit_history:
                self.edit_history[user] = [time]
            else:
                self.edit_history[user].append(time)
        return self.edit_history


class EstimateSeniority:
    def __init__(self, edit_history: dict):
        """Initialise the instance attributes"""
        self.edit_history = edit_history
        self.edit_counts = {user: len(times) for user, times in edit_history.items()}

    def estimate_seniority(self, user, revert_time):
        """
        Count the number of edits for each user before a specific revert time and
        estimate the seniority of an editor based on the number of edits
        """
        edit_count = sum(time < revert_time for time in self.edit_history[user])
        if edit_count == 0:
            edit_count += 1
        seniority = math.log10(edit_count)
        return seniority


class CreateNetwork:
    def __init__(self, data: Text2Data, edit_history: CreateEditHistory):
        """Initialise the instance attributes"""
        # Initialise the transformed data from text
        self.data = data
        # Initialise an empty list for the edges
        self.network = []
        # Initialise an empty dictionary for the last version before each revert
        self.last_version = {}
        # Initialise an empty dictionary for the last title before each revert
        self.last_title = None
        # Initialise the edit history
        self.edit_history = edit_history
        # Initialise an instance of EstimateSeniority
        self.es = EstimateSeniority(self.edit_history)

    def create_network(self):
        for data in self.data:
            title, time, revert, version, user = data

            # Update the last version and title for non-revert edits
            if revert == 0:
                self.last_version = (user, version)
                self.last_title = title

            # Process revert edits
            elif revert == 1 and self.last_version:
                if user == self.last_version[0]:
                    continue
                elif version < self.last_version[1]:
                    # Calculate the seniority of the reverter and the reverted
                    seniority_reverter = self.es.estimate_seniority(user, time)
                    seniority_reverted = self.es.estimate_seniority(self.last_version[0], time)
                    # Create a new network element
                    network_elements = [
                        user,
                        self.last_version[0],
                        time,
                        seniority_reverter,
                        seniority_reverted,
                    ]
                    self.network.append(network_elements)

        # Sort the network in reverse order
        self.network = self.network[::-1]

        return self.network


class CreateNode:
    def __init__(self, network: CreateNetwork):
        """Initialise the instance attributes"""
        # Initialise the network
        self.network = network

    def create_node(self) -> list:
        """
        Create nodes from a network
        :return: The nodes
        """
        nodes = set([element[0] for element in self.network] + [element[1] for element in self.network])
        return nodes
