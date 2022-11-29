from django.shortcuts import render, HttpResponse
from sharpy import*
# Create your views here.
def index(request):
    return render(request,'index.html')
    # return HttpResponse("HELLO WORLD IT'S AMAN HERE")
def python(request):
    return render(request,'index.html',open())

