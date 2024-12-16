# -*- coding: utf-8 -*-

"""
This module gets a list of places of a specified type from a specified county in Ireland

from the Logainm API (See: docs.gaois.ie) and prints place metadata to a TSV formatted file.
"""

import json
import os
import requests

class Place:
    def __init__(self, logainm_id, lat, lon, county, barony, parish, cats, names_en, names_ga):
        self.logainm_id = logainm_id
        self.lat = lat
        self.lon = lon
        self.county = county
        self.barony = barony
        self.parish = parish
        self.cats = cats
        self.names_en = names_en
        self.names_ga = names_ga

def parse_place(place_data):

    # Get place ID:
    logainm_id = place_data['id']
    
    # Get place coordinates:
    lat = ''
    lon = ''
    if 'geography' in place_data:
        geography = place_data['geography']
        coordinates = geography['coordinates'] # list of coordinates
        if coordinates:
            lat = coordinates[0]['latitude']
            lon = coordinates[0]['longitude']

    # Get place parents (county, barony and parish parents):
    parents = place_data['includedIn'] # list of dicts
    county = ''
    barony = ''
    parish = ''
    for parent in parents:
        if parent['category']['id'] == 'CON':
            county = str(parent['id']) + ' ' + parent['nameEN']
        if parent['category']['id'] == 'BAR':
            barony = str(parent['id']) + ' ' + parent['nameEN']
        if parent['category']['id'] == 'PAR':
            parish = str(parent['id']) + ' ' + parent['nameEN']

    # Get place categories:
    categories = place_data['categories'] # list of dicts
    cats = []
    for category in categories:
        cats.append(category['nameEN'])

    # Get place names:
    placenames = place_data['placenames'] # list of dicts
    names_en = []
    names_ga = []
    for placename in placenames:
        if placename['language'] == 'en':
            names_en.append(placename['wording'])
        if placename['language'] == 'ga':
            names_ga.append(placename['wording'])

    print(str(logainm_id))
    p = Place(str(logainm_id), str(lat), str(lon), county, barony, parish, ', '.join(cats), ', '.join(names_en), ', '.join(names_ga))
    return p

api_key = '' # Get key here: https://www.gaois.ie/en/technology/developers/registration/
place_id = '100004' # EDIT (i.e. 100000 to 100031)
category_id = 'BF' # EDIT (e.g. CON, BAR, PAR, BF, TR, B)

# Run API query and cache (i.e. save to file), if not already cached:
if not os.path.isfile('logainm_'+place_id+'_'+category_id+'.json'):
    json_payload = requests.get('https://www.logainm.ie/api/v1.0/?PlaceID='+place_id+'&CategoryID='+category_id+'&apiKey='+api_key).text # See: docs.gaois.ie
    with open('logainm_'+place_id+'_'+category_id+'.json', 'w', encoding='utf-8') as f:
        f.write(json_payload)

# Read cached data:
with open('logainm_'+place_id+'_'+category_id+'.json', 'r', encoding='utf-8') as fi:
    json_payload = fi.read()

# Convert from JSON to Python (Object to dict, Array to list, etc.):
results_data = json.loads(json_payload) # dict
results = results_data['results'] # list

fo = open('logainm_'+place_id+'_'+category_id+'.tsv', 'w', encoding='utf-8') # output file (TSV can be pasted into Excel)
fo.write('LOGAINM_ID\tLAT\tLON\tCOUNTY\tBARONY\tPARISH\tCATS\tNAMES_EN\tNAMES_GA\n') # write header

# Write places to TSV file, one per line:
for place in results:
    p = parse_place(place)
    fo.write(p.logainm_id + '\t' + p.lat + '\t' + p.lon + '\t' + p.county + '\t' + p.barony + '\t' + p.parish + '\t' + p.cats + '\t' + p.names_en + '\t' + p.names_ga + '\n')

fo.close()
