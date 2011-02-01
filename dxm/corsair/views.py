from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt

import numpy as np
import random
import json
from scikits.learn import svm, datasets
from scikits.learn.metrics import roc_curve, auc
from corsair import conf
from corsair.models import TrainingSet, PredictionStatistics

def login_required(func):
    def wrapped(request, *args, **kwargs):
        if not conf.PUBLIC:
            if not request.user.is_authenticated():
                return HttpResponseRedirect(reverse('corsair-login'))
            if not request.user.has_perm('corsair_trainingset.can_view'):
                return HttpResponseRedirect(reverse('corsair-login'))
        return func(request, *args, **kwargs)
    wrapped.__doc__ = func.__doc__
    wrapped.__name__ = func.__name__
    return wrapped

@csrf_protect
def login(request):
    from django.contrib.auth import login as login_
    from django.contrib.auth.forms import AuthenticationForm
    
    if request.POST:
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login_(request, form.get_user())
            return HttpResponseRedirect(request.POST.get('next') or reverse('corsair'))
        else:
            request.session.set_test_cookie()
    else:
        form = AuthenticationForm(request)
        request.session.set_test_cookie()

    context = locals()
    context.update(csrf(request))
    return render_to_response('corsair/login.html', context)

def logout(request):
    from django.contrib.auth import logout
    logout(request)
    return HttpResponseRedirect(reverse('corsair'))


@login_required
def training_sets(request):
    training_sets = TrainingSet.objects.all()
    return render_to_response('corsair/training_sets.html', {
        'request': request,
        'training_sets': training_sets,
    })

@login_required
def benchmarks(request):
    benchmarks = PredictionStatistics.objects.all()
    return render_to_response('corsair/benchmarks.html', {
        'benchmarks': benchmarks,
        'request': request,
    })

@login_required
def benchmark_detail(request, benchmark):
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    X, y = X[y!=2], y[y!=2]
    n_samples, n_features = X.shape
    p = range(n_samples)
    random.seed(0)
    random.shuffle(p)
    X, y = X[p], y[p]
    half = int(n_samples/2)
    
    # Add noisy features
    X = np.c_[X,np.random.randn(n_samples, 200*n_features)]

    # Run classifier
    classifier = svm.SVC(kernel='linear', probability=True)
    probas_ = classifier.fit(X[:half],y[:half]).predict_proba(X[half:])

    # Compute ROC curve and area the curve
    fpr, tpr, thresholds = roc_curve(y[half:], probas_[:,1])
    print fpr
    print tpr
    print thresholds

    fpr = list(fpr)
    tpr = list(tpr)
    roc_coordinates = json.dumps(list(zip(fpr, tpr)))
    print roc_coordinates
    print
    roc_auc = auc(fpr, tpr)
    return render_to_response('corsair/benchmark_detail.html', {
        'request': request,
        'roc_coordinates': roc_coordinates,
        'roc_auc': roc_auc,
    })

@login_required
def index(request):
    return render_to_response('corsair/base.html', {
        'request': request,
    })
