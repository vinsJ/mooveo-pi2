# Import the matrix of via per country (based on the passport)

import pandas as pd 
import requests

# Will be used to compute the distance from GPS Coordinates
from math import sin, cos, sqrt, atan2, radians

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
USE_GMAP = os.getenv('USE_GMAP')

passportIndex = pd.read_csv('./DB/passport-index-matrix.csv', index_col = 'Passport')

# The coordinates must only contains {'latitude': X, 'longitude': Y}
def RawDistance(userCoord, offerCoord):
    """ Compute distance from GPS coordinates

    :param: userCoord: user's coordinates : {'latitude': X, 'longitude': Y} 
    :param: offerCoord: offer's coordinates : {'latitude': X, 'longitude': Y} 

    :return: distance: distance in km
    :return: underRange: indicator to know if we should use Gmap API
    """
    underRange = False
    R = 6373.0 # Approcimate radius of earth, in km

    lat1 = radians(userCoord['latitude'])
    lon1 = radians(userCoord['longitude'])

    lat2 = radians(offerCoord['latitude'])
    lon2 = radians(offerCoord['longitude'])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    if(distance < 80):
        underRange = True
    return distance, underRange

def DistanceAPIGMap(userCoord, offerCoord, distance):
    """ Compute time travel from GPS coordinates

    :param: userCoord: user's coordinates : {'latitude': X, 'longitude': Y} 
    :param: offerCoord: offer's coordinates : {'latitude': X, 'longitude': Y} 
    :param: distance in km

    If distance <= 50km : compute transit and car time travel.
    Else, compute car time travel

    :return: drivingTime in minutes
    :return: transitTime in minutes 
    """
    try:
        drivingTime = None
        transitTime = None

        api_url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(userCoord['latitude']) + "," + str(userCoord['longitude']) + "&destinations=" + str(offerCoord['latitude']) + "," + str(offerCoord['longitude']) + "&key=" + str(API_KEY)
        if(distance <= 50):
            #Make car and transit request
            car_req = requests.get(api_url + "&mode=driving").json()
            transit_req = requests.get(api_url + "&mode=transit").json()

            if(car_req['rows'][0]['elements'][0]['status'] == "OK"):
                drivingTime = float(car_req['rows'][0]['elements'][0]['duration']['value']/60) #Get result in minutes
            if(transit_req['rows'][0]['elements'][0]['status'] == "OK"):
                transitTime = float(transit_req['rows'][0]['elements'][0]['duration']['value']/60)
        else:
            #Make car request only
            car_req = requests.get(api_url + "&mode=driving")
            if(car_req['rows'][0]['elements'][0]['status'] == "OK"):
                drivingTime = float(car_req['rows'][0]['elements'][0]['duration']['value']/60)

        return drivingTime, transitTime
    except:
        return None, None


def VisaType(userCountry, offerCountry):
    """ Look for visa type given countries

    :param: userCountry
    :param: offerCountry

    :return: visaType based on the two inputs countries

    """
    visaType = 'NA'
    try:
        visaType = passportIndex.at[userCountry,offerCountry]
    except:
        pass
    return visaType

def scaleHeuristic(heuristic):
    """ Scale function

    f(x) = 1 - (x/(1+x))
    We remove from 1, the penalties of the heuristic (if a distance is great, we will remove more from 1)

    :param: heuristic

    :return: scaled heuristic

    """
    return 1 - ((heuristic / (1 + heuristic)))

# The Location must contains {'coordinates': {'latitude': X, 'longitude': Y}, 'country': 'X'}
def Heuristic(userLocation, offerLocation):
    """ Main function to compute heurisitc

    Decide wich heuristic we need to compute

    :param: userLocation : {'coordinates': {'latitude': X, 'longitude': Y}, 'country': 'X'}
    :param: offerLocation : {'coordinates': {'latitude': X, 'longitude': Y}, 'country': 'X'}

    :return: Heuristic object : {'gmapH' : {'driving': drivingH, 'transit': transitH}, 'insideCountry' : heuristicInsideCoutry, 'countryH' : heuristicCountry}

    """
    try:
        rawDist, useGMap = RawDistance(userLocation['coordinates'], offerLocation['coordinates'])
        visaType = 'NA'
        
        heuristicInsideCoutry = None
        heuristicCountry = None
        drivingH = None
        transitH = None

        if(useGMap):
            if(USE_GMAP == "True"): 
                drivingH, transitH = DistanceAPIGMap(userLocation['coordinates'], offerLocation['coordinates'], rawDist)
                if(drivingH):
                    drivingH = scaleHeuristic(drivingH)
                if(transitH):
                    transitH = scaleHeuristic(transitH)
            else:
                heuristicInsideCoutry = scaleHeuristic(rawDist)
        elif (userLocation['country'] == offerLocation['country']):
            heuristicInsideCoutry = scaleHeuristic(rawDist)
        else:
            earthCircHalf = 20000
            visaType = VisaType(userLocation['country'], offerLocation['country'])
            coeffVisa = {'NA' : 0, 'VR' : 0.1, 'ETA' : 0.1, 'VF' : 1, 'VOA' : 0.9, '15' : 0.2, '21' : 0.3, '90' : 0.5, '120' : 0.6, '180' : 0.7, '360' : 0.8}
            heuristicCountry = (1 - (rawDist)/earthCircHalf) * coeffVisa[visaType]


        heuristic = {'gmapH' : {'driving': drivingH, 'transit': transitH}, 'insideCountry' : heuristicInsideCoutry, 'countryH' : heuristicCountry}
        return heuristic
    except Exception as e:
        return {'gmapH' : {'driving': None, 'transit': None}, 'insideCountry' : None, 'countryH' : None, 'error' : e.args}