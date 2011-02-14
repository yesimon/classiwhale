from __future__ import division
from django.db import models
from picklefield.fields import PickledObjectField
from scikits.learn import cross_val
from scikits.learn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve, explained_variance_score
from algorithmio.interface import classifier_library
import numpy as np
import random

from twitter.models import *
from profile.models import *

DEFAULT_MODEL = 'Rating'
    
def round_away(tup):
    num, split = tup[0], tup[1]
    if num >= split: return 1
    else: return -1

def round_np_away(array, split):
    rounded = np.copy(array)
    for i, num in enumerate(rounded):
        if num >= split: rounded[i] = 1
        else: rounded[i] = -1
    return rounded

def round_binary(tup):
    num, split = tup[0], tup[1]
    if num >= split: return 1
    else: return 0

def round_proba(num):
    return (num + 1) / 2

class TwitterTrainingSet(models.Model):
    name = models.CharField(max_length=30, unique=True)
    users = models.ManyToManyField(TwitterUserProfile)
    ratings = models.ManyToManyField(Rating, blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
    def setup(self):
        profs = self.users.all()
        ratings = self.ratings.all()
        status_ids = set([r.status_id for r in ratings])
        statuses = Status.objects.in_bulk(status_ids)
        training_set = {}
        for p in profs:
            data = {}
            data['user'] = p
            data['ratings'] = [r for r in ratings if r.user_id == p.user_id]
            for r in data['ratings']:
                r.status = statuses[r.status_id]
            training_set[p.user_id] = data
        return training_set

    def benchmark(self, classifier_name, n_folds=2, discrimination_bound=0.0, save=True):
        training_set = self.setup()
        probas = []
        expected = []
        for prof_id, data in training_set.iteritems():
            n = len(data['ratings'])
            if n_folds >= n:
                continue
            kf = cross_val.KFold(n, n_folds)
            for train_index, test_index in kf:
                train_ratings = [data['ratings'][i] for i in range(n) if 
                                train_index[i]]
                test_ratings = [data['ratings'][i] for i in range(n) if
                                test_index[i]]
                if len(train_ratings) < 1 or len(test_ratings) < 1: continue
                classifier = classifier_library.classifiers[classifier_name]
                c = classifier(data['user']).test_train(ratings=train_ratings)
                y_pred = c.test_predict([rating.status for rating in test_ratings])
#                print y_pred
                probas.extend(map(round_proba, y_pred))
#                print map(round_proba, y_pred)
                expected.extend([rating.rating for rating in test_ratings])
        raw_data = {'y_true': np.array(expected), 'y_probas': np.array(probas)}
#        print raw_data['y_probas']
#        print raw_data
        stats = PredictionStatistics(training_set=self,
                                     classifier=classifier_name,
                                     model=DEFAULT_MODEL,
                                     n_folds=n_folds,
                                     raw_data=raw_data)
        stats.calculate_statistics()
        if save: stats.save()
        return stats

    @staticmethod
    def random_training_set(classifier=None, num_users=50, ratings_per_user=100,
                            save=False):
        """Returns a random training set for users already using the relevant
        classifier. Or else returns a random training set. The format is a dict
        where keys are twitter user_profile_ids and values are dicts with ratings,
        clicks, and other test data"""
        random.seed()
        if classifier:
            profs = TwitterUserProfile.objects.filter(active_classifier=
                classifier).sorted_by('?').select_related('ratings')[:50]
        else:
            profs = TwitterUserProfile.objects.all().sorted_by(
                '?').select_related('ratings')[:50]
        ratings = []
        for p in profs:
            ratings.append(random.sample(p.ratings, ratings_per_user))
        success = False
        while save and not success:
            try: 
                t = TwitterTrainingSet(users=profs, ratings=ratings,
                    name='random_{0}'.format(random.randint(0, 100000000000)))
                t.save()
            except:
                continue
        return t


class PredictionStatistics(models.Model):
    """raw_data is a dict containing y_true, y_probas keys"""
    training_set = models.ForeignKey(TwitterTrainingSet)
    classifier = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    model = models.CharField(max_length=50)
    raw_data = PickledObjectField()
    discrimination_bound = models.FloatField(default=0.0)
    n_folds = models.IntegerField()
    auc = models.FloatField()
    ppv = models.FloatField()
    npv = models.FloatField()
    tpr = models.FloatField()
    tnr = models.FloatField()
    acc = models.FloatField()
    mcc = models.FloatField()
    tp = models.IntegerField()
    fp = models.IntegerField()
    tn = models.IntegerField()
    fn = models.IntegerField()

    class Meta:
        ordering = ["-created"]
        verbose_name_plural = "prediction statistics"

    def calculate_statistics(self):
        """Rely on labels being [-1 1] for array labels"""
        y_true = self.raw_data['y_true']
        y_pred = round_np_away(self.raw_data['y_probas'], 0.5)


        # Compute ROC curve and area the curve
        y = np.ceil(np.divide(y_true.astype(float), 2.0))
        probas_ = self.raw_data['y_probas']
        fpr, tpr, thresholds = roc_curve(y, probas_)
        roc_auc = auc(fpr, tpr)
        self.auc = roc_auc

        cm = confusion_matrix(y_true, y_pred, labels=[-1, 1])
        self.tn = cm[0, 0]
        self.tp = cm[1, 1]
        self.fn = cm[1, 0]
        self.fp = cm[0, 1]
        p = self.tp + self.fn
        p_prime = self.tp + self.fp
        n = self.fp + self.tn
        n_prime = self.fn + self.tn
        self.ppv = self.tp / (self.tp + self.fp)
        self.npv = self.tn / (self.tn + self.fn)
        self.tpr = self.tp / p
        self.tnr = self.tn / n
        self.acc = (self.tp + self.tn) / (p + n)
        self.mcc = (self.tp*self.tn - self.fp*self.fn)/pow(p*n*p_prime*n_prime, 0.5)


