from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect


# Create your views here.
@login_required(login_url='/account/login')
def redirect(request):
    return HttpResponseRedirect('home/')