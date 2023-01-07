import folium
from django.shortcuts import render
from django.http import HttpResponse
from mapearthq.models import WorldData, WeeklyCsvFile

# Create your views here.

# listings = models.WorldData.objects.all()
# print(listings[0].country)
def download_csv(request):
    weekly_data = WeeklyCsvFile.objects.last()
    file = weekly_data.csv_file.file
    data = file.read().decode()
    response = HttpResponse(data,content_type='text/plain')
    response['Content-Disposition']='attachment; filename="last_week.csv"'
    return response

def index(request):
    listings = WorldData.objects.order_by("-time")[:30]
    m = folium.Map(location=[listings[0].lat, listings[0].lon], zoom_start=2)
    for listing in listings:
        popupstr = f"{listing.country}\nMagnitude:{listing.Mag}"
        if listing.Mag >= 6:
            folium.CircleMarker(
                [listing.lat, listing.lon],
                radius=10,
                fill=True,
                color="red",
                opacity=0.6,
            ).add_to(m)
            folium.CircleMarker(
                [listing.lat, listing.lon],
                radius=20,
                fill=True,
                color="red",
                opacity=0.6,
            ).add_to(m)
            folium.CircleMarker(
                [listing.lat, listing.lon],
                radius=30,
                fill=True,
                color="red",
                opacity=0.6,
                popup=popupstr,
            ).add_to(m)
        else:
            folium.CircleMarker(
                [listing.lat, listing.lon],
                radius=10,
                fill=True,
                color="blue",
                opacity=0.6,
            ).add_to(m)
            folium.CircleMarker(
                [listing.lat, listing.lon],
                radius=20,
                fill=True,
                color="blue",
                opacity=0.6,
                popup=popupstr,
            ).add_to(m)

    m = m._repr_html_()
    WeeklyCsvFile
    context = {"listings": listings, "world_map": m}
    return render(request, "index.html", context)
