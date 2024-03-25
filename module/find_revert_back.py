# Import necessary libraries
from datetime import timedelta


class __str__(object):
    def __str__(self):
        return self.__class__.__name__


class FindRevertBack:
    def __init__(self, network: list):
        """Initialise the instance attributes"""
        # Initialise the network
        self.network = network[::-1]
        # Initialise an empty list for the event sequence
        self.event_sequence = []

    def within_24_hours(self, time1, time2):
        """Check if two times are within 24 hours"""
        return abs((time1 - time2).total_seconds()) <= 24 * 60 * 60

    # For each edge in the network find the revert back to the original editor
    # if it is within 24 hours, go to the next step
    def create_revert_event(self):
        for i in range(len(self.network) - 1):
            for j in range(i + 1, len(self.network)):
                if (
                    self.network[i][0] == self.network[j][1]
                    and self.network[i][1] == self.network[j][0]
                    and self.within_24_hours(self.network[i][2], self.network[j][2])
                ):
                    self.event_sequence.append(self.network[i])
                    self.event_sequence.append(self.network[j])

        return self.event_sequence
