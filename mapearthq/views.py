from django.http import HttpResponse
from django.shortcuts import render, HttpResponse
from . import models
# Create your views here.

# listings = models.WorldData.objects.all()
# print(listings[0].country)

def index(request):
    listings = models.WorldData.objects.all()
        
    return render(request,'index.html',{'listings': listings})