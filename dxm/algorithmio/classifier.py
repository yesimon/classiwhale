from exceptions import NotImplementedError

import abc

class Classifier(object):
    """
    Abstract interface that an algorithm absolutely must implement.
    """

    __metaclass__ = abc.ABCMeta

    # Be careful of race condition when asynch tasking on this. Essentially, 
    # don't save prof model in a task without refetching
    def __init__(self, prof):
        self.prof = prof

    @abc.abstractmethod
    def force_train(self):
        """Force a train on a user immediately"""
        return NotImplementedError

    @abc.abstractmethod
    def predict(self, statuses):
        """Predict ratings using algorithm, returns list of float from [-1 1]"""
        return NotImplementedError
