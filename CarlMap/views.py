# Internal/Django imports
from django.views.generic import TemplateView
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from CarlMap.models import *
from django.core.cache import cache
from django.conf import settings

# External imports
import wikipedia
import requests


class Index(TemplateView):
    template_name = "index.html"
    

def expand_country(request, abbv, *args, **kwargs):
    # Check if the abbreviation is 3 characters (ISO alpha-3), and if it is, chop one of the end
    # to convert it to ISO alpha-2
    if len(abbv) >= 3:
        abbv = abbv[:2]
    country = get_object_or_404(Country, code=abbv)
    cache_sum = cache.get(f"{abbv}_country_summary")
    if cache_sum:
        summary = cache_sum
    else:
        summary = wikipedia.summary(country.name, sentences=2)
        # Cache the summary for 30 minutes
        cache.set(f"{abbv}_country_summary", summary, 60*30)
    points_cache = cache.get(f"{abbv}_country_points")
    if points_cache:
        points = points_cache
    else:
        # Get the lats and lons
        country_students = Location.objects.filter(country=country)
        # Weight the locations by the number of attendees, down to the second decimal point
        points = []
        for student in country_students:
            lat = round(student.lat, 1)
            lon = round(student.lon, 1)
            found = False
            for idx in range(len(points)-1):
                e_p = points[idx]
                if e_p["lat"] == lat and e_p["lon"] == lon:
                    points[idx]["weight"] += 1
                    found = True
            if not found:
                # Different parts of the client libraries check for both 'lat' and 'latitude'
                points.append({"lat": lat, "lon": lon, "weight": 1, "name": student.long_name,
                               'latitude': lat, 'longitude': lon})
        cache.set(f"{abbv}_country_points", points)
    bubbles = []
    for point in points:
        weight = point["weight"]
        if weight * 2.5 < 10:
            radius = weight*2.5
        else:
            radius = 10
        point.update({"radius": radius})
        bubbles.append(point)
    # Get the viewport
    cached_viewport = cache.get(f"{abbv}_country_viewport")

    if cached_viewport:
        viewport = cached_viewport
    else:
        geocoded = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={country.name},"
                                f"{country.code}&key={settings.CONF['gmaps_key']}").json()['results']
        viewport = {
            "lat": sum([lat for lat in [geocoded[0]["geometry"]["viewport"]["northeast"]["lat"],
                                        geocoded[0]["geometry"]["viewport"]["southwest"]["lat"]]])/2,
            "lon": sum([lon for lon in [geocoded[0]["geometry"]["viewport"]["northeast"]["lng"],
                                        geocoded[0]["geometry"]["viewport"]["southwest"]["lng"]]])/2
        }

        cache.set(f'{abbv}_country_viewport', viewport)
    return JsonResponse({
        "name": country.name,
        "code": country.code,
        "flag": country.flag.name,
        "summary": summary,
        "bubbles": bubbles,
        "lat": viewport["lat"],
        "lon": viewport["lon"]
    })