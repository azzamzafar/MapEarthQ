import folium
from django.shortcuts import render
from mapearthq.models import WorldData, WeeklyCsvFile

# Create your views here.

# listings = models.WorldData.objects.all()
# print(listings[0].country)


def index(request):
    listings = WorldData.objects.order_by("-time")[:30]
    weekly_data = WeeklyCsvFile.objects.last()
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
    context = {"listings": listings, "world_map": m, "csv_obj": weekly_data}
    return render(request, "index.html", context)
