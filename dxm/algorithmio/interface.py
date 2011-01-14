from status.models import *
from multinomialbayes.classifiers import MultinomialBayesClassifier
from cylonbayes.classifiers import CylonBayesClassifier

def get_predictions(prof, statuses, session=None):
    """Statuses could be list of ids, list of api status objects, or list of
    django status models, inspect to decide next steps"""
    if statuses is None: return None
    if statuses[0] in (int, long):
        statuses = Status.objects.filter(id__in=statuses)
        # TODO: Do some integrity checks to make sure they are good?
    # TODO: Logic to obtain predictions from cache if at all possible
    algo = prof.active_classifier
    exec "predictions = {0}(prof).predict(statuses)\n".format(algo)
    return predictions

def get_predictions_filter(prof, statuses, session=None):
    predictions = get_predictions(prof, statuses, session)
    return [statuses[i] for i in range(len(statuses)) if predictions[i] >= 0]

def force_train(prof):
    algo, version = prof.active_classifier, prof.classifier_version
    exec "{0}(prof).force_train()\n".format(algo)
    return
