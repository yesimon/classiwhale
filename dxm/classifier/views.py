from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.core.paginator import Paginator
from twitterauth.models import *
from twitterauth.utils import get_authorized_twitter_api
from status.models import *
from classifier.models import *
from annoying.decorators import render_to
from django.core.cache import cache
from bayes.classifiers import BayesCommonData, MultinomialBayesClassifier
from bayes.extraction import SimpleExtractor
import twitter
import cPickle

@login_required
@render_to('train_bayes.html')
def train_multinomial_bayes(request):
    prof = request.user.get_profile()
    c_obj = get_multinomial_bayes_classifier(prof)
    c = c_obj.classifier
    seen_statuses = c.statuses
    ratings_list = Rating.objects.filter(user_profile=prof).exclude(
        status__id__in=seen_statuses).order_by(
        '-rated_time').select_related('status')
    train_set = []
    for rating in ratings_list:
        train_set.append((rating.status, rating.rating))
    map(c.train, train_set)
    c_obj.save()
    return {'statistics': c.most_informative_features()}

def get_multinomial_bayes_classifier(prof):
    common = cache.get('bayes_common')
    if common == None: 
        common = BayesCommonData()
        cache.set('bayes_common', common, 60 * 30)
    c_obj = prof.classifier_set.get(name='MultinomialBayesClassifier')
    try:
        c_obj = prof.classifier_set.get(name='MultinomialBayesClassifier')
        c_obj.classifier.update_common(common)
    except DoesNotExist:
        c = MultinomialBayesClassifier(common=common, extractor=SimpleExtractor)
        c_obj = Classifier(user_profile=prof, classifier=c, name='MultinomialBayesClassifier')
    except MultipleObjectsReturned:
        c_objs = prof.classifier_set.filter(name='MultinomialBayesClassifier')
        [c.delete for c in c_objs[1:]]
        c_obj = cobjs[0]
    return c_obj

@login_required
@render_to('predicted_friends_timeline.html')
def predicted_friends_timeline(request):
    prof = request.user.get_profile()
    c_obj = get_multinomial_bayes_classifier(prof)
    c = c_obj.classifier

    api = get_authorized_twitter_api(request.session['access_token'])
    statuses = api.GetFriendsTimeline()
    friends = api.GetFriends()
    ratings = map(c.predict, statuses)
    print c.most_informative_features()
    for s, r in zip(statuses, ratings):
        if r == 1:
            s.likeClass = ' active'
            s.dislikeClass = ' inactive'
        if r == -1:
            s.likeClass = ' inactive'
            s.dislikeClass = ' active'            
    return {'statuses': statuses, 'friends': friends}
    
