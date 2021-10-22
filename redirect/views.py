from django.shortcuts import render, HttpResponseRedirect


# Create your views here.
def redirect(request):
    return HttpResponseRedirect('blog/')
