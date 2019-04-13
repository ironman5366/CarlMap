# Builtin imports
import csv
import os
import json

# External imports
import requests
from tqdm import tqdm


DATA_DIR = 'raw'
OUT_DIR = 'dist'
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'static')
CONF_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'conf.json')
CONF = json.load(open(CONF_FILE, encoding='utf-8'))
GMAPS_KEY = CONF['gmaps_key']
FIXTURE_DIR = 'fixtures'


def geocode(place_name):
    # If the place name doesn't include a comma, it's in the US
    if ',' not in place_name:
        place_name += ', USA'
    geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={place_name}&key={GMAPS_KEY}'
    return requests.get(geocode_url).json()


countries = json.load(open(os.path.join(OUT_DIR, 'countries.json'), encoding='utf-8'))

# Read the CSV files and merge them into one large file

years = {}

print("Aggregating raw CSV data...")
# Read the location data in
for data_file in os.listdir(DATA_DIR):
    if data_file.endswith('csv'):
        reader = csv.reader(open(os.path.join(DATA_DIR, data_file), encoding='utf-8'))
        for line in list(reader)[1:]:
            year = int(line[0])
            location = line[1]
            if year not in years.keys():
                years.update({year: []})
            years[year].append(location)

# Export the data out to a JSON file

out_file = os.path.join(OUT_DIR, 'data.json')

with open(out_file, 'w') as out:
    out.write(json.dumps(years, indent=4))

print("Matching countries to flags...")
country_data = []
pk = 1
# Put the flags and countries into the database
for country in countries:
    country_name_safe = country["name"].replace('"', "_")
    flag_filename = os.path.join(STATIC_DIR, f'img/flags/{country_name_safe}.png')
    if not os.path.isfile(flag_filename):
        raise FileExistsError(f"Couldn't find flag for {country}")
    country_data.append({
        "model": "CarlMap.Country",
        "pk": pk,
        "fields": {
            "name": country["name"],
            "code": country["code"],
            "flag": flag_filename
        }
    })
    pk += 1

# Export the country data in Django fixtures syntax
with open(os.path.join(FIXTURE_DIR, 'countries.json'), 'w', encoding='utf-8') as fixture_out:
    fixture_out.write(json.dumps(country_data, indent=4))

print("Running location strings through geocoding")
location_fixtures = []
pk = 1
# Try to match location data to countries in the database
for year, locations in years.items():
    print(f"Geocoding for year {year}")
    # Use the geocoding API
    for loc in tqdm(locations):
        loc_data = geocode(loc)
        # Get the long name of a place, making sure that it's either a locality or an administrative area, not a street
        found_good_type = False
        prop_comp = None
        prop_geo = None
        country_pk = None
        for result in loc_data['results']:
            addr_components = result['address_components']
            if found_good_type:
                break
            for comp in addr_components:
                types = comp['types']
                if found_good_type:
                    break
                for typ in types:
                    if typ in ['locality', 'political'] or typ.startswith('administrative_area'):
                        found_good_type = True
                        prop_comp = comp
                        prop_geo = result['geometry']
                        # Iterate through the comps again to find the country and match it to the DB
                        country_found = False
                        for comp in addr_components:
                            if 'country' in comp['types']:
                                country_abbv = comp['short_name']
                                # Find this abbreviation in the fixtures that were generated
                                for country_fixture in country_data:
                                    if country_fixture["fields"]["code"] == country_abbv:
                                        country_pk = country_fixture["pk"]
                                        country_found = True
                        if not country_found:
                            print(f"Error: Can't find country for location {loc}")
                        break
        if found_good_type:
            # Generate a fixture item
            location_fixtures.append({
                "model": "CarlMap.Location",
                "pk": pk,
                "fields": {
                    "raw_str": loc,
                    "long_name": prop_comp["long_name"],
                    "country": country_pk,
                    "year": year,
                    "lat": prop_geo['location']['lat'],
                    "lon": prop_geo["location"]["lng"]
                }
            })
            pk += 1
        else:
            print(f"Error: couldn't find good location info for location {loc}, year {year}")

with open(os.path.join(FIXTURE_DIR, 'locations.json'), 'w', encoding='utf-8') as fixture_out:
    fixture_out.write(json.dumps(location_fixtures, indent=4))