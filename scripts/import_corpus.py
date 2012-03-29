# -*- coding: utf-8 -*-
from django.core.management import setup_environ
import sys

import settings
setup_environ(settings)

############ Script ############
from nltk.corpus import movie_reviews
from classifier.models import TokenDictionary, Classifier
from django.db import transaction
words = movie_reviews.words()

words = sorted(set(words))


for word in words[:]:
    if (len(word) > 30 or
        word.find() ''): words.remove(word)

@transaction.commit_on_success
def save_instances(instances):
    for inst in instances:
        inst.save()

tokens = []

for (i, word) in enumerate(words):
    print i, word
    if len(word) > 30: print word
    t = TokenDictionary(id=i, token=word)
    t.save()
    #tokens.append(t)

#save_instances(tokens)
