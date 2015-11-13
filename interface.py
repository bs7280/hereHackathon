#Meant to be a command line interface for the python script that interacts with the
#Here api

#importing
import sys
import apiDemo as module

def main(params):
    if params[0] == "getWaypointTime" and len(params)==7:
        print module.getWaypointTime(params[1], params[2], params[3], params[4], params[5],params[6])
    elif params[0] == "getLatitudeLongitude" and len(params)>=2:
        print module.getLatitudeAndLongitudeByAddress(" ".join(params[1:]))
    elif params[0] == "getPlaces":
        print module.getPlaces()
    elif params[0] == "getWaypointHTML" and len(params)==7:
        results = module.getMapHtml(params[1], params[2], params[3], params[4], params[5], params[6])

        if results == "Error":
            print "Error"
        else:
            print results
    else:
        print "Go fuck your self"

if __name__ == "__main__":
    main(sys.argv[1:])
