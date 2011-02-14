from celery.decorators import task, periodic_task
from celery.task.schedules import crontab
from datetime import datetime, timedelta
from django.db.models import Max
from multinomialbayes.classifiers import MultinomialBayesClassifier
from twitter.models import TwitterUserProfile

@task()
def add(x, y):
    return x + y



@periodic_task(run_every=timedelta(hours=4))
def train_all():
    """ 
    Get all profiles and first filter
    by whether the user is using MultinomialBayes.
    Afterwards, filter out all those for which
    training time is after last rated time. Runs every 4 hours.
    """

    # Annotate with most recent rated time and trained time
    profs = TwitterUserProfile.objects.filter(active_classifier=
        'MultinomialBayesClassifier').annotate(
            rated_time=Max('rating__rated_time'), 
            trained_time=Max('multinomialbayesmodel__last_modified'))
    # Check whether user needs training
    train_profs = []
    for p in profs:
        if p.rated_time is not None and \
        (p.trained_time is None or p.rated_time > p.trained_time):
            train_profs.append(p)
    for p in train_profs:
        MultinomialBayesClassifier(p).force_train()




