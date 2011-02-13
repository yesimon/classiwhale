from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.core.paginator import Paginator
from annoying.decorators import render_to
from django.core.cache import cache
from twitter.models import *
from twitter.utils import get_authorized_twython
from twython import Twython, TwythonError


from algorithmio.interface import get_predictions, get_predictions_filter, force_train
from multinomialbayes.classifiers import  MultinomialBayesClassifier
from multinomialbayes.extraction import SimpleExtractor



@login_required
@render_to('train_bayes.html')
def train_multinomial_bayes(request):
    prof = request.user.get_profile()
    tp = TwitterUserProfile.objects.get(user=prof)
    tp.active_classifier = 'MultinomialBayesClassifier'
    tp.classifier_version = '0.1'
    tp.save()
    force_train(tp)
    return {'success': 'works?'}

@login_required
@render_to('train_bayes.html')
def train_classifier(request):
    prof = request.user.get_profile()
    tp = TwitterUserProfile.objects.get(user=prof)
    force_train(tp)
    return {'success': 'works?'}



@login_required
@render_to('predicted_friends_timeline.html')
def predicted_friends_timeline(request):
    prof = request.user.get_profile()
    tp = TwitterUserProfile.objects.get(user=prof)
    twitter_tokens = request.session['twitter_tokens']
    api = get_authorized_twython(twitter_tokens)
    statuses = Status.construct_from_dicts(api.getFriendsTimeline())
    friends = api.getFriendsStatus()
    predictions = get_predictions(tp, statuses)
    for s, r in zip(statuses, predictions):
        if r >= 0:
            s.likeClass = ' active'
            s.dislikeClass = ' inactive'
        if r < 0:
            s.likeClass = ' inactive'
            s.dislikeClass = ' active'            
    return {'statuses': statuses, 'friends': friends}
    
@login_required
@render_to('twitter/timeline.html')
def filtered_friends_timeline(request):
    prof = request.user.get_profile()
    tp = TwitterUserProfile.objects.get(user=prof)
    twitter_tokens = request.session['twitter_tokens']
    api = get_authorized_twython(twitter_tokens)
    statuses = Status.construct_from_dicts(api.getFriendsTimeline())
    friends = api.getFriendsStatus()
    predictions = get_predictions(tp, statuses)
    filtered_statuses = []
    for s, r in zip(statuses, predictions):
        if r >= 0: filtered_statuses.append(s)
    return {'statuses': filtered_statuses, 'friends': friends}
