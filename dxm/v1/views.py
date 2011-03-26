# Create your views here.

from django.template import Context, loader
from django.http import HttpResponse
from v1.utils import rendered_template


def index(request):
    return rendered_template('v1/base/basenav.html', {}, request)

def asdf(request):
    return "asdf"