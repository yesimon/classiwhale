from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from tweed.accounts.models import UserProfile



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            UserProfile.objects.create(user=new_user)
            return HttpResponseRedirect("/twitter/")
    else:
        form = UserCreationForm()
    return render_to_response("register.html", {
        'form': form, 
    })
