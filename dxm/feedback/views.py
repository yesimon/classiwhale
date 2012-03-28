# Create your views here.
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.utils.encoding import force_unicode
from django.core.mail import send_mail, mail_admins, send_mass_mail
from django.conf import settings

import json
from feedback import forms

#import appsettings
#settings = appsettings.settings.feedback

feedback_recipients = [admin[1] for admin in settings.ADMINS]


def sanitize(errors):
    dct = dict((str(k),list(force_unicode(a) for a in v)) for k,v in errors.items())
    return dct

def handle_ajax(request, url):
    if not request.POST:
        return HttpResponse(json.dumps({'error':'no post recieved'}))
    else:
        post = {}
        for k in request.POST:
            post[k] = request.POST[k]
        post['url'] = url
        post['site'] = Site.objects.get_current().id
        form = forms.FeedbackForm(post)
        if form.is_valid():
            form.save()
            try:
                feedback_message = ('[Feedback] ' + form.cleaned_data['subject'],
                                form.cleaned_data['text'],
                                form.cleaned_data['email'],
                                feedback_recipients)
                send_mass_mail((feedback_message,), fail_silently=False)
            except:
                return HttpResponse(json.dumps({'error':'Failed to send email'}))
            return HttpResponse(json.dumps({}))
        else:
            return HttpResponse(json.dumps({'errors':sanitize(form.errors)}))
