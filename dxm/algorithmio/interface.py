from exceptions import NotImplementedError
from status.models import *
import abc

class Classifier(object):
    """
    Abstract interface that an algorithm absolutely must implement.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, version):
        self.version = version

    @abc.abstractmethod
    def force_train(self, prof):
        """Force a train on a user immediately"""
        return NotImplementedError

    @abc.abstractmethod
    def predict(self, statuses, prof):
        """Predict ratings using algorithm, returns list of float from [-1 1]"""
        return NotImplementedError

def get_predictions(prof, statuses, session=None):
    """Statuses could be list of ids, list of api status objects, or list of
    django status models, inspect to decide next steps"""
    if statuses is None: return None
    if statuses[0] in (int, long):
        statuses = Status.objects.filter(id__in=statuses)
        # TODO: Do some integrity checks to make sure they are good?
    # TODO: Logic to obtain predictions from cache if at all possible
    algo, version = prof.active_algorithm, prof.classifier_version
    exec "predictions = {0}({1}).predict(statuses, prof)".format(algo, version)
    return predictions

def get_predictions_filter(prof, statuses, session=None):
    predictions = get_predictions(prof, statuses, session)
    return [statuses[i] for i in range(len(statuses)) if predictions[i] >= 0]

