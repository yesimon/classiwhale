from django.test import TestCase
from django.utils import unittest
from twitterauth.models import UserProfile, Rating
from django.contrib.auth.models import User
from twitteroauth import DEFAULT_CLASSIFIER, DEFAULT_CLASSIFIER_VERSION

from multinomialbayes.classifiers import MultinomialBayesClassifier
from cylonbayes.classifiers import CylonBayesClassifier

class UserProfileTestCase(unittest.TestCase):
    def setUp(self):
        s = User(username=73)
        s.set_password('42')
        self.simon = UserProfile.objects.create(user=s, 
                               active_classifier=DEFAULT_CLASSIFIER,
                               classifier_version=DEFAULT_CLASSIFIER_VERSION
                                                )

    def test_classifier_exists(self):
        prof = self.simon
        algo = prof.active_classifier
        exec "classifier = {0}(prof)\n".format(algo)





class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)



