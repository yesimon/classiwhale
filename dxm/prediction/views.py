from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.core.paginator import Paginator
from twitterauth.models import *
from twitterauth.utils import get_authorized_twitter_api
from status.models import *
from annoying.decorators import render_to
from django.core.cache import cache

from algorithmio.interface import get_predictions, get_predictions_filter, force_train
from multinomialbayes.classifiers import  MultinomialBayesClassifier
from multinomialbayes.extraction import SimpleExtractor



@login_required
@render_to('train_bayes.html')
def train_multinomial_bayes(request):
    prof = request.user.get_profile()
    prof.active_classifier = 'MultinomialBayesClassifier'
    prof.classifier_version = '0.1'
    prof.save()
    force_train(prof)
    return {'success': 'works?'}

@login_required
@render_to('train_bayes.html')
def train_classifier(request):
    prof = request.user.get_profile()
    force_train(prof)
    return {'success': 'works?'}



@login_required
@render_to('predicted_friends_timeline.html')
def predicted_friends_timeline(request):
    prof = request.user.get_profile()
    api = get_authorized_twitter_api(request.session['access_token'])
    statuses = api.GetFriendsTimeline()
    friends = api.GetFriends()
    predictions = get_predictions(prof, statuses)
    for s, r in zip(statuses, predictions):
        if r > 0:
            s.likeClass = ' active'
            s.dislikeClass = ' inactive'
        if r <= 0:
            s.likeClass = ' inactive'
            s.dislikeClass = ' active'            
    return {'statuses': statuses, 'friends': friends}
    
@login_required
@render_to('timeline.html')
def filtered_friends_timeline(request):
    prof = request.user.get_profile()
    api = get_authorized_twitter_api(request.session['access_token'])
    statuses = api.GetFriendsTimeline()
    friends = api.GetFriends()
    predictions = get_predictions(prof, statuses)
    filtered_statuses = []
    for s, r in zip(statuses, predictions):
        if r >= 0: filtered_statuses.append(s)
    return {'statuses': filtered_statuses, 'friends': friends}
