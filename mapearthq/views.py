import folium
from django.http import HttpResponse
from django.shortcuts import render, HttpResponse
from . import models
# Create your views here.

# listings = models.WorldData.objects.all()
# print(listings[0].country)

def index(request):
    listings = models.WorldData.objects.all()
    m = folium.Map([45.5236, -122.6750],zoom_start=3)
    for listing in listings:
        folium.CircleMarker([listing.lat,listing.lon],radius=2).add_to(m)    
        folium.CircleMarker([listing.lat,listing.lon],radius=4).add_to(m)    
        folium.CircleMarker([listing.lat,listing.lon],radius=8).add_to(m)    

    m=m._repr_html_()
    context = {'listings': listings,'world_map':m}
    return render(request,'index.html',context)