# dxm/v1/utils.py

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.template import RequestContext

def rendered_template(template, dictionary, request):
    return render_to_response(template, dictionary, context_instance=RequestContext(request))
