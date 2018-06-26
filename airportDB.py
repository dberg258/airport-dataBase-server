from pymongo import MongoClient
from time import time
import requests

timingData = []

def fileParser(fileName):
    file = open(fileName)
    locations = []
    for line in file:
        line = line.split(';')
        line[2] = line[2][0:-1]
        line = [float(number) for number in line]
        locations.append(line)
    # print(locations)
    return locations


def dataRequest(locations):
    headers = {
        'X-API-Key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVkZW50aWFsX2lkIjoiY3JlZGVudGlh'
                     'bHxOMHFkRzVTd1hxM2VrYzJrblFFN0g1UEdZa0ciLCJhcHBsaWNhdGlvbl9pZCI6ImFwcGxpY'
                     '2F0aW9ufE5sbDY3RE1GdkJYcHk3aUtMOVgwWVR4RUI0NEsiLCJvcmdhbml6YXRpb25faWQiOi'
                     'JkZXZlbG9wZXJ8NzNrUFgzZXUweXdxWUxGOUxET1hwaWtnbm5iWiIsImlhdCI6MTUyOTgzODE'
                     '1NH0.f43-dAkFA6VXdqoueqTUe6n9w1-TWDw3zyVJEZ86GxM'
    }

    for coordinates in locations:
        query = {
            'latitude': coordinates[1],
            'longitude': coordinates[0],
            'types': 'airport',
            'buffer': coordinates[2]
        }

        startTime = time()
        r = requests.get('https://api.airmap.com/status/v2/point', params=query, headers=headers)
        endTime = time()
        timingData.append((coordinates[2], endTime - startTime))
        request = r.json()