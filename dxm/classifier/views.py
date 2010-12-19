from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.core.paginator import Paginator
from twitterauth.models import *
from twitterauth.utils import get_authorized_twitter_api
from status.models import *
from classifier.models import *
from datetime import datetime
from email.utils import parsedate
from time import mktime
from annoying.decorators import render_to
from django.core.cache import cache
from bayes.classifier import BayesCommonData, MultinomialBayesClassifier
from bayes.extraction import SimpleExtractor
import twitter
import json

@login_required
@render_to('sds.html')
def train_multinomial_bayes(request):
    prof = request.user.get_profile()
    c_obj = get_multinomial_bayes_classifier
    c = c_obj.classifier
    ratings_list = Rating.objects.filter(user_profile=prof).order_by(
        '-rated_time').selected_related('status')
    train_set = []
    for rating in ratings_list:
        train_set.append((rating.status, rating.rating))
    map(c.train, train_set)
    


def get_multinomial_bayes_classifier(prof):
    try: common = cache.get('bayes_common')
    except: 
        common = BayesCommonData()
        cache.set('bayes_common', common)
    try:
        c_obj = prof.classifer_set.get(name__equals='MultinomialBayesClassifier')
        c_obj.classifier.update_common(common)
    except:
        c = MultinomialBayesClassifier(common=common, extractor=SimpleExtractor)
        c_obj = Classifier(classifier=c, name=c.__class__.__name__)
    return c_obj
