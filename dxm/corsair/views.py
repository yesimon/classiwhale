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

from algorithmio.interface import classifier_library
from corsair import conf
from corsair.models import TwitterTrainingSet, PredictionStatistics
import corsair.tasks

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
    training_sets = TwitterTrainingSet.objects.all()
    return render_to_response('corsair/training_sets.html', {
        'request': request,
        'training_sets': training_sets,
        'classifiers': classifier_library.classifiers,
    })

@login_required
def ajax_api(request, action=None):
    results = {'success': False}
    if request.is_ajax() and action:
        if action == 'start_benchmark':
            classifiers = request.POST.getlist('classifiers[]')
            training_set = request.POST[u'training_set']
            for classifier in classifiers:
                stats = benchmark_test(training_set, classifier)
#                corsair.tasks.benchmark.delay(training_set, classifier)
            results['success'] = True
            return HttpResponse(json.dumps(results))
    else:
        return HttpResponse(status=400)

def benchmark_test(training_set, classifier):
    t = TwitterTrainingSet.objects.get(name=training_set)
    stats = t.benchmark(classifier, save=True)
    return stats
   
    


@login_required
def benchmarks(request):
    benchmarks = PredictionStatistics.objects.all().select_related()
    training_sets = TwitterTrainingSet.objects.all()
    """
    latest_benchmarks = []
    for training_set in training_sets:
        for b in benchmarks:
            if b.training_set == training_set:
                latest_benchmarks.append(b)
                break
    """
    return render_to_response('corsair/benchmarks.html', {
        'benchmarks': benchmarks,
        'request': request,
        'training_sets': training_sets,
    })

@login_required
def benchmark_detail(request, benchmark):
    stats = PredictionStatistics.objects.get(id=benchmark)
    y = stats.raw_data['y_true']
    y = np.ceil(np.divide(y.astype(float), 2.0))
    probas_ = stats.raw_data['y_probas']

    # Compute ROC curve and area the curve
    fpr, tpr, thresholds = map(list, roc_curve(y, probas_))

    roc_coordinates = json.dumps(list(zip(fpr, tpr)))
    roc_auc = stats.auc

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
