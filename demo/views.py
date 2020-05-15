from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import os

APPNAME='demo'
# Create your views here.
def index(request):
    return render(request, 'index.html')


