from pymongo import MongoClient
from time import time
import time
import requests
import schedule
import csv

file = open('timeData.txt', 'a')
timingData = []

schedule.clear()


def fileParser(fileName):
    file = open(fileName)
    locations = []
    for line in file:
        line = line.split(';')
        line[2] = line[2][0:-1]
        line = [float(number) for number in line]
        locations.append(line)
    #print(locations)
    return locations


def dataRequest(locations):
    headers = {
        'X-API-Key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVkZW50aWFsX2lkIjoiY3JlZGVudGlh'
                     'bHxOMHFkRzVTd1hxM2VrYzJrblFFN0g1UEdZa0ciLCJhcHBsaWNhdGlvbl9pZCI6ImFwcGxpY'
                     '2F0aW9ufE5sbDY3RE1GdkJYcHk3aUtMOVgwWVR4RUI0NEsiLCJvcmdhbml6YXRpb25faWQiOi'
                     'JkZXZlbG9wZXJ8NzNrUFgzZXUweXdxWUxGOUxET1hwaWtnbm5iWiIsImlhdCI6MTUyOTgzODE'
                     '1NH0.f43-dAkFA6VXdqoueqTUe6n9w1-TWDw3zyVJEZ86GxM'
    }

    for radius in range(250, 10001, 250):

        timingDataSingleLocation = []

        for coordinates in locations:
            query = {
                'latitude': coordinates[1],
                'longitude': coordinates[0],
                'types': 'airport',
                # 'buffer': coordinates[2] // this is for when using just the location document
                'buffer': radius
            }

            startTime = time.time()

            while True:
                try:
                    r = requests.get('https://api.airmap.com/status/v2/point', params=query, headers=headers)
                except:
                    print("working")
                    continue
                else:
                    break

            endTime = time.time()
            timingDataSingleLocation.append([radius, endTime - startTime]) # coordinates[2] replace radius with this when using location file
            request = r.json()

            airportData = {}

            for info in request['data']['advisories']:
                if 'airport_name' in info['properties']:
                    airport = info['properties']['airport_name']
                    city = info['city']
                    state = info['state']
                    country = info['country']
                    location = "{}, {}, {}".format(city, state, country)
                    phone = info['properties']['phone']
                    airportData[airport] = [location, phone]

            for airport in airportData:
                post_data = {
                    'name': airport,
                    'location': airportData[airport][0],
                    'phone': airportData[airport][1]
                }
                posts.insert_one(post_data)

        for post in posts.find():
            print(post)
        timingData.append(timingDataSingleLocation)

        analyzeTime(timingData)
        timingData.clear()


    return posts


def analyzeTime(data):
    myFile = open('timeData2.csv', 'a')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(data)


def job():
    if __name__ == "__main__":
        locationList = fileParser("locations.txt")

        # Mongo DB initialization
        client = MongoClient()
        db = client['Airports']
        global posts
        posts = db.posts
        db.posts.delete_many({})

        dataRequest(locationList)

        #analyzeTime(timingData)
        #print(timingData)
        timingData.clear()

job()
schedule.every(10).seconds.do(job)
#schedule.every(20).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(5)




