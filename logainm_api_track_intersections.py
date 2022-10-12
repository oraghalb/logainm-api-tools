# -*- coding: utf-8 -*-

"""
This module takes a track in GPX format and prints out the list of Logainm townlands the track intersects in a specified county.
"""

import gpxpy
import json
import os
import requests
from shapely.geometry import shape, Point, Polygon, MultiPolygon
import time

# Get list of townland IDs from the Logainm API (See: docs.gaois.ie) for a specific county:

api_key = '' # Get key here: https://www.gaois.ie/en/technology/developers/registration/
place_id = '100018' # EDIT (i.e. 100000 to 100031)
category_id = 'BF'

# Run API query and cache (i.e. save to file), if not already cached:
if not os.path.isfile('logainm_'+place_id+'_'+category_id+'.json'):
    json_payload = requests.get('https://www.logainm.ie/api/v1.0/?PlaceID='+place_id+'&CategoryID='+category_id+'&apiKey='+api_key).text
    with open('logainm_'+place_id+'_'+category_id+'.json', 'w', encoding='utf-8') as f:
        f.write(json_payload)

# Read cached data:
with open('logainm_'+place_id+'_'+category_id+'.json', 'r', encoding='utf-8') as fi:
    json_payload = fi.read()

# Convert from JSON to Python (Object to dict, Array to list, etc.):
results_data = json.loads(json_payload) # dict
results = results_data['results'] # list

townland_ids = []
for place in results:
	townland_ids.append(place['id'])

# Load townland boundary data:
with open('Townlands_-_OSi_National_Statutory_Boundaries_-_2019_-_Generalised_20m.geojson', 'r', encoding='utf-8') as f: # Boundary data © Ordnance Survey Ireland. Retrieved from data.gov.ie.
	townland_data = json.loads(f.read())
all_townlands = townland_data['features'] # list of dicts
townlands = []
for townland in all_townlands:
	properties = townland['properties']
	if properties['LOGAINM_ID']:
		if int(properties['LOGAINM_ID']) in townland_ids:
			townlands.append(townland) # list of dicts

# Load track points:
with open('track.gpx', 'r', encoding='utf-8') as gpx_file: # https://en.wikipedia.org/wiki/GPS_Exchange_Format
	gpx = gpxpy.parse(gpx_file)
	track_points = []
	for track in gpx.tracks:
		for segment in track.segments:
			for point in segment.points:
				track_points.append(point)

# Check which townlands are intersected by the track:
intersected_townlands = []
for townland in townlands:
	td_geometry_type = townland['geometry']['type']
	geo = townland['geometry'] # dict
	if td_geometry_type == 'Polygon':
		boundary = shape(geo) # Polygon
		for point in track_points:
			if Polygon(boundary).contains(Point(point.longitude, point.latitude)):
				print(townland['properties']['LOGAINM_ID'] + ': ' + townland['properties']['ENGLISH'])
				intersected_townlands.append(townland['properties']['LOGAINM_ID'])
				break
	elif td_geometry_type == 'MultiPolygon':
		boundaries = shape(geo) # MultiPolygon
		for boundary in boundaries.geoms:
			for point in track_points:
				if Polygon(boundary).contains(Point(point.longitude, point.latitude)):
					print(townland['properties']['LOGAINM_ID'] + ': ' + townland['properties']['ENGLISH'])
					intersected_townlands.append(townland['properties']['LOGAINM_ID'])
					break
			else:
				continue
			break

# Sort results:
intersected_townlands.sort()

# Print results to TXT file as list of hyperlinks to Logainm:
timestr = time.strftime("%y%m%d%H%M%S")
with open(timestr+'-intersected-townlands.txt', 'w', encoding='utf-8') as outf:
	for townland_id in intersected_townlands:
		outf.write('https://www.logainm.ie/en/'+townland_id+'\n')
