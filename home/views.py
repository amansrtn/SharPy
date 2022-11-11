from django.shortcuts import render
from django.http import HttpResponse
from subprocess import run,PIPE,sys
from .sharpy import open_cv
# Create your views here.
def index(request):
    return render(request,'index.html')

def open_cv_view(request):
    print(">>>>>>>>>>>>>>open cv")
    open_cv()
    
