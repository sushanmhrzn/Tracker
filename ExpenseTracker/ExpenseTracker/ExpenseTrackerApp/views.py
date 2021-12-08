from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
def signup(req):
    return render(req,"signup.html")
def index(req):
    return render(req,"login.html")
