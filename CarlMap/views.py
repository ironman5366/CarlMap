# Internal/Django imports
from django.views.generic import TemplateView
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from CarlMap.models import *
from django.core.cache import cache

# External imports
import wikipedia


class Index(TemplateView):
    template_name = "index.html"
    

def expand_country(request, abbv, *args, **kwargs):
    country = get_object_or_404(Country, code=abbv)
    cache_sum = cache.get(f"{abbv}_country_summary")
    if cache_sum:
        summary = cache_sum
    else:
        summary = wikipedia.summary(country.name, sentences=1)
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
            lat = round(student.lat, 2)
            lon = round(student.lon, 2)
            found = False
            for idx in range(len(points)-1):
                e_p = points[idx]
                if e_p["lat"] == lat and e_p["lon"] == lon:
                    found = True
                    points[idx]["weight"] += 1
                    break
            if not found:
                points.append([{"lat": lat, "lon": lon, "weight": 1, "name": student.long_name}])
        cache.set(f"{abbv}_country_points", points)
    return JsonResponse({
        "name": country.name,
        "code": country.code,
        "flag": country.flag,
        "summary": summary,
        "points": points
    })