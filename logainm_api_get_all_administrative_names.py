# -*- coding: utf-8 -*-

"""
This module gets all administrative divisions in Ireland

from the Logainm API (See: docs.gaois.ie)

and prints placenames and metadata to a TSV and an XLSX file.
"""

import csv
import json
import os
from pathlib import Path
import requests
from xlsxwriter.workbook import Workbook

class Place:
    def __init__(self, logainm_id, lat, lon, county, barony, parish, cats, names_en, names_ga, names_ga_genitive):
        self.logainm_id = logainm_id
        self.lat = lat
        self.lon = lon
        self.county = county
        self.barony = barony
        self.parish = parish
        self.cats = cats
        self.names_en = names_en
        self.names_ga = names_ga
        self.names_ga_genitive = names_ga_genitive

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
    names_ga_genitive = []
    for placename in placenames:
        if placename['language'] == 'en':
            names_en.append(placename['wording'])
        if placename['language'] == 'ga':
            names_ga.append(placename['wording'])
            try:
                names_ga_genitive.append(placename['genitive'])
            except:
                continue

    p = Place(str(logainm_id), str(lat), str(lon), county, barony, parish, ', '.join(cats), ', '.join(names_en), ', '.join(names_ga), ', '.join(names_ga_genitive))
    return p

api_key = 'xx' # Get key here: https://www.gaois.ie/en/technology/developers/registration/

output_dir = r'cached_files'
Path(output_dir).mkdir(parents=True, exist_ok=True)

# Get provinces and counties:
# Run API query and cache (i.e. save to file), if not already cached:
if not os.path.isfile(os.path.join(output_dir, f'logainm_01_CUIGE.json')):
    json_payload = requests.get(f'https://www.logainm.ie/api/v1.0/?CategoryID=CUIGE&apiKey={api_key}').text
    results_data = json.loads(json_payload)
    with open(os.path.join(output_dir, f'logainm_01_CUIGE.json'), 'w', encoding='utf-8') as f:
        f.write(json_payload)
if not os.path.isfile(os.path.join(output_dir, f'logainm_02_CON.json')):
    json_payload = requests.get(f'https://www.logainm.ie/api/v1.0/?CategoryID=CON&apiKey={api_key}').text
    results_data = json.loads(json_payload)
    with open(os.path.join(output_dir, f'logainm_02_CON.json'), 'w', encoding='utf-8') as f:
        f.write(json_payload)

place_ids = [i for i in range(100000, 100031+1)] # All COUNTIES in Logainm
category_ids = ['B', 'BAR', 'BF', 'CBA', 'CBU', 'CCA', 'CR', 'CTH', 'PAR', 'TR'] # Sub-county-level administrative place CATEGORIES in Logainm.

# Get sub-county-level administrative places:
for place_id in place_ids:
    for category_id in category_ids:
        current_page = 1
        total_pages = 20
        while current_page <= total_pages:
            # Run API query and cache (i.e. save to file), if not already cached:
            if not os.path.isfile(os.path.join(output_dir, f'logainm_{str(place_id)}_{category_id}_{str(current_page)}.json')):
                json_payload = requests.get(f'https://www.logainm.ie/api/v1.0/?PlaceID={str(place_id)}&CategoryID={category_id}&apiKey={api_key}&Page={str(current_page)}').text # See: docs.gaois.ie
                results_data = json.loads(json_payload)
                total_pages = int(results_data['totalPages'])
                with open(os.path.join(output_dir, f'logainm_{str(place_id)}_{category_id}_{str(current_page)}.json'), 'w', encoding='utf-8') as f:
                    f.write(json_payload)
                current_page += 1
            else:
                break

fo = open('logainm_administrative_names.tsv', 'w', encoding='utf-8') # output file (TSV can be pasted into Excel)
fo = open(fo.name, 'a', encoding='utf-8')
fo.write('LOGAINM_ID\tLAT\tLON\tCOUNTY\tCATS\tNAMES_EN\tNAMES_GA\tNAMES_GA_GENITIVE\tLINK\n') # write header

for filename in os.listdir(output_dir):
    # Read cached data:
    with open(os.path.join(output_dir, filename), 'r', encoding='utf-8') as fi:
        json_payload = fi.read()

    # Convert from JSON to Python (Object to dict, Array to list, etc.):
    results_data = json.loads(json_payload) # dict
    results = results_data['results'] # list

    # Write places to TSV file, one per line:
    for place in results:
        p = parse_place(place)
        if p.logainm_id not in ['67240', '67270', '1421794', '1403321', '1403318', '1383740', '1403314', '1403311', '1403313', '1383768', '1403335', '1403323', '1403324', '1403319', '1403315', '1403312', '1403322', '1403325', '1403320', '1403326', '1403353', '1403368']: # Places that do not exist anymore (Property of existence is not currently exposed via the API)
            log_link = f'=HYPERLINK("https://www.logainm.ie/en/{p.logainm_id}","{p.logainm_id}")'
            fo.write(f'{p.logainm_id}\t{p.lat}\t{p.lon}\t{p.county}\t{p.cats}\t{p.names_en}\t{p.names_ga}\t{p.names_ga_genitive}\t{log_link}\n')

fo.close()

# Save TSV as XLSX:
workbook = Workbook('logainm_administrative_names.xlsx')
worksheet = workbook.add_worksheet()
with open('logainm_administrative_names.tsv', 'rt', encoding='utf8') as f:
    reader = csv.reader(f, delimiter='\t')
    for r, row in enumerate(reader):
        for c, col in enumerate(row):
            worksheet.write(r, c, col)
workbook.close()
