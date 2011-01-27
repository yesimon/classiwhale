from django.db import models
from picklefield.fields import PickledObjectField
from twitterauth.models import UserProfile, Rating
from status.models import Status 
from scikits.learn import cross_val
from scikits.learn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve, explained_variance_score
from algorithmio.interface import classifier_library
import numpy as np
import random


DEFAULT_MODEL = 'Rating'
    
def round_away(num, split=0.0):
    if num >= split: return 1
    else: return -1

def round_binary(num, split=0.0):
    if num >= split: return 1
    else: return 0

def round_proba(num):
    return (num + 1) / 2

class TrainingSet(models.Model):
    name = models.CharField(max_length=30, unique=True)
    user_profiles = models.ManyToManyField(UserProfile)
    ratings = models.ManyToManyField(Rating, blank=True, null=True)
    
    
    def setup(self):
        profs = self.user_profiles.all()
        ratings = self.ratings.all()
        status_ids = set([r.status_id for r in ratings])
        statuses = Status.objects.in_bulk(id__in=status_ids)
        training_set = {}
        for p in profs:
            data = {}
            data['user_profile'] = p
            data['ratings'] = [r for r in ratings if r.user_profile_id == p.id]
            for r in data['ratings']:
                r.status = statuses[r.status_id]
            training_set[p.id] = data
        return training_set

    def benchmark(self, classifier, n_folds=2, discrimination_bound=0.0, save=True):
        training_set = self.setup()
        probas = []
        expected = []
        for prof_id, data in training_set:
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
                classifier = classifier_library[classifier]
                c = classifier(data['user_profile']).test_train(ratings=train_ratings)
                y_pred = c.test_predict([rating.status for rating in test_ratings])
                probas.extend(map(round_proba, y_pred))
                expected.extend([rating.rating for rating in test_ratings])
        raw_data = {'y_true': expected, 'y_probas': probas}
        stats = PredictionStatistics(training_set=self,
                                     classifier=classifier,
                                     model=DEFAULT_MODEL,
                                     n_folds=n_folds,
                                     raw_data=raw_data)
        stats.calculate_statistcs()
        if save: stats.save()
        return stats

    @staticmethod
    def random_training_set(classifier=None, num_users=50, ratings_per_user=100,
                            save=False):
        """Returns a random training set for users already using the relevant
        classifier. Or else returns a random training set. The format is a dict
        where keys are user_profile_ids and values are dicts with ratings,
        clicks, and other test data"""
        random.seed()
        if classifier:
            profs = UserProfile.objects.filter(active_classifier=
                classifier).sorted_by('?').select_related('ratings')[:50]
        else:
            profs = UserProfile.objects.all().sorted_by(
                '?').select_related('ratings')[:50]
        ratings = []
        for p in profs:
            ratings.append(random.sample(p.ratings, ratings_per_user))
        success = False
        while save and not success:
            try: 
                t = TrainingSet(user_profiles=profs, ratings=ratings,
                    name='random_{0}'.format(random.randint(0, 100000000000)))
                t.save()
            except:
                continue
        return t


class PredictionStatistics(models.Model):
    """raw_data is a dict containing y_true, y_probas keys"""
    training_set = models.ForeignKey(TrainingSet)
    classifier = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    model = models.CharField(max_length=50)
    raw_data = PickledObjectField()
    discrimination_bound = models.FloatField(default=0.0)
    n_folds = models.IntegerField()
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
        y_true = np.array(self.raw_data['y_true'])
        y_pred = np.array(map(round_away, 
                              [(p, 0.5) for p in self.raw_data['y_probas']]))
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

