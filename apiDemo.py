#importing stuff
import requests, json, math

app_id="habu7uC2upRacruDrUfu"
app_code="85_CDKXMNkoraKX54-ZS-g" 

def getMap():
    r = requests.get("https://image.maps.cit.api.here.com/mia/1.6/mapview", 
            params={'app_id':app_id, 'app_code':app_code})

    return r.content()

def getPopulatPlaces(location):
    r = requests.get("https://places.demo.api.here.com/places/v1/discover/here", 
            params={'app_id':app_id, 'app_code':app_code, 'at':'37.7942,-122.4070'})
    return r.json()

def getRouteToJson(start, end):
    waypoint0 = start
    waypoint1 = end
    mode = "fastest;car;traffic:enabled"
    departure = "now"


    r = requests.get("https://route.cit.api.here.com/routing/7.2/calculateroute.json",
            params = {
                    'app_id':app_id, 
                    'app_code':app_code,
                    'waypoint0':waypoint0,
                    'waypoint1':waypoint1,
                    'mode':mode,
                    'departure':departure
                    })

    resultJson = r.json()
    outputJson = resultJson['response']['route'][0]['waypoint']
    print len(outputJson)
    print json.dumps(outputJson, indent=4)

    #Getting the important info from the route

    return 0

def getPlaces():
    location = "37.7942,-122.4070"
    r = requests.get("https://places.demo.api.here.com/places/v1/discover/explore",
            params = {
                'app_id': app_id,
                'app_code': app_code,
                'at': location
                })

    newThing = []
    result=r.json()['results']['items']

    for item in result:
        theDict = {}
        theDict['latitude'] = item['position'][0]
        theDict['longitude'] = item['position'][1]
        theDict['title'] = item['title']
        theDict['averageRating'] = item['averageRating']
        theDict['type'] = item['category']['id']
        newThing.append(theDict)

    theResult = {'output':newThing}
    with open('result.json', 'w') as fp:
        json.dump(theResult, fp)
    return theResult



def getSetOfPoints(startLocA, startLocB, endLocA, endLocB, searchRadius):
    centerA = (startLocA + endLocA)/2.0
    centerB = (startLocB + endLocB)/2.0
    distance = math.sqrt(math.pow((startLocA - endLocA), 2) + math.pow((startLocB - endLocB), 2))

    distance = distance*60
    numbSpaces = distance/(searchRadius*2.0) + 1.0

    print numbSpaces

    deltaA = (startLocA - endLocA)/numbSpaces
    deltaB = (startLocB - endLocB)/numbSpaces

    resultList = []
    for i in range(0,int(numbSpaces)):
        lat = startLocA - deltaA*(i+1) 
        lng = startLocB - deltaB*(i+1)
        resultList.append([lat,lng])
    return resultList 

def getPoiFromSetOfPoints(setOfPoints):
    for a,b in setOfPoints:
        getPOI(a,b)

#startLoc: 
def getPoiByLocationAndRadius(startLocA, startLocB, endLocA, endLocB):
    centerA = (startLocA + endLocA)/2.0
    centerB = (startLocB + endLocB)/2.0

    thing = 15.0/60.0


    topRightA = str(centerA + thing)
    topRightB = str(centerB + thing)
    bottomLeftA = str(centerA - thing)
    bottomLeftB = str(centerB - thing)


    inParameter = topRightA + "," + topRightB + "," + bottomLeftA + "," + bottomLeftB

    r = requests.get("https://places.demo.api.here.com/places/v1/discover/explore",
            params = {
                'app_id':app_id,
                'app_code':app_code,
                'position':str(centerA) + ',' + str(centerB),
                'in': inParameter
                },

            headers = {"accept":"application/json"}
            )
    print r.json()
    return 0

def getPOI(latitude, longitude):
    r=requests.get("https://places.demo.api.here.com/places/v1/discover/here",
            params = {
                'app_id':app_id,
                'app_code':app_code,
                'at':str(latitude)+","+str(longitude)})

    #Parsing the result
    jsonResult = r.json()
    jsonResult = jsonResult['results']
    print r.json()
    for a in jsonResult['items']:
        print a['title']
        print a['position']
        print a['averageRating']
    print

#Given 3 waypoints get time to travel to all of those waypoints
#Input latitude and then longitude for the three way points as parameters
#Returns value in seconds
def getWaypointTime(latA,longA,latB,longB,latC,longC):
    #Getting the waypoints
    waypoint0 = str(latA) + "," + str(longA)
    waypoint1 = str(latB) + "," + str(longB)
    waypoint2 = str(latC) + "," + str(longC)

    #Making the request
    r=requests.get("https://route.cit.api.here.com/routing/7.2/calculateroute.json",
            params = {
                'app_id':app_id,
                'app_code':app_code,
                'waypoint0':waypoint0,
                'waypoint1':waypoint1,
                'waypoint2':waypoint2,
                'mode':'fastest;car'
                })

    #Parsing Json
    resultJson = r.json()
    outputJson = resultJson['response']['route'][0]['summary']['travelTime']
    return outputJson

#get the html code that gets a javascript
def getMapHtml(latA,longA,latB,longB,latC,longC):
    waypoint0 = str(latA) + "," + str(longA)
    waypoint1 = str(latB) + "," + str(longB)
    waypoint2 = str(latC) + "," + str(longC)

    data= open('example.html', 'r').read()
    data=data.replace('$waypoint0$', waypoint0)
    data=data.replace('$waypoint1$', waypoint1)
    data=data.replace('$waypoint2$', waypoint2)

    return data

def getLatitudeAndLongitudeByAddress(address):
    print address
    
    r=requests.get("https://geocoder.cit.api.here.com/6.2/geocode.json",
            params = {
                'app_id':app_id,
                'app_code':app_code,
                'gen':8,
                'searchtext':address
                })

    #parsing 
    result = r.json()
    if 'Response' in result:
        foobar = result['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]
        return str(foobar['Latitude']) + "," + str(foobar['Longitude'])
    else:
        print r.json().keys()
        return "Error"

#print getRouteToJson("52.5160,13.3779","52.5206,13.3862")
#loyolla (let/long), #iit (lat,long)
#print getPOI(42.000535,-87.659264,41.833040,-87.624613 )
#print getPoiByLocationAndRadius(43.0500,-87.9500,41.833040,-87.624613 )
#a = getSetOfPoints(43.0500,-87.9500,41.833040,-87.624613,3)
#print getPOI(41.833040,-87.624613)
#print getPoiFromSetOfPoints(a)
#print getRouteToJson("41.833040,-87.624613", "42.000535,-87.659264")


