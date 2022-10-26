from math import radians, cos, sin, asin, sqrt
from src.domain.trip import Trip


def lineal(trip: Trip):
    distance_km = __distance(trip["from_latitude"], trip["to_latitude"], trip["from_longitude"], trip["to_longitude"])
    base_price = 250 # TODO add to database
    price_per_km = 40 # TODO add to database
    return round(base_price + (distance_km * price_per_km), 2)


def __distance(lat1, lat2, lon1, lon2):
     
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    return(c * r)

