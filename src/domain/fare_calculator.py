from math import radians, cos, sin, asin, sqrt


def calculate(from_latitude, to_latitude, from_longitude, to_longitude):
    distance_km = __distance(from_latitude, to_latitude, from_longitude, to_longitude)
    base_price = 250  # TODO add to database
    price_per_km = 40  # TODO add to database
    return round(base_price + (distance_km * price_per_km), 2)


def calculate_test_without_driver(
    minimum_fare,
    duration_fare,
    distance_fare,
    dailyTripAmountPassenger_fare,
    monthlyTripAmountPassenger_fare,
    seniorityDriver_fare,
    seniorityPassenger_fare,
    recentTripAmount_fare,
    duration,
    distance,
    dailyTripAmountPassenger,
    monthlyTripAmountPassenger,
    seniorityDriver,
    seniorityPassenger,
    recentTripAmount,
):
    return (
        minimum_fare
        + duration_fare * duration
        + distance_fare * distance
        + dailyTripAmountPassenger_fare * dailyTripAmountPassenger
        + monthlyTripAmountPassenger_fare * monthlyTripAmountPassenger
        + seniorityDriver_fare * seniorityDriver
        + seniorityPassenger_fare * seniorityPassenger
        + recentTripAmount_fare * recentTripAmount
    )


def calculate_test(
    minimum_fare,
    duration_fare,
    distance_fare,
    dailyTripAmountDriver_fare,
    dailyTripAmountPassenger_fare,
    monthlyTripAmountDrive_fare,
    monthlyTripAmountPassenger_fare,
    seniorityDriver_fare,
    seniorityPassenger_fare,
    recentTripAmount_fare,
    duration,
    distance,
    dailyTripAmountDriver,
    dailyTripAmountPassenger,
    monthlyTripAmountDrive,
    monthlyTripAmountPassenger,
    seniorityDriver,
    seniorityPassenger,
    recentTripAmount,
):

    return (
        minimum_fare
        + duration_fare * duration
        + distance_fare * distance
        + dailyTripAmountDriver_fare * dailyTripAmountDriver
        + dailyTripAmountPassenger_fare * dailyTripAmountPassenger
        + monthlyTripAmountDrive_fare * monthlyTripAmountDrive
        + monthlyTripAmountPassenger_fare * monthlyTripAmountPassenger
        + seniorityDriver_fare * seniorityDriver
        + seniorityPassenger_fare * seniorityPassenger
        + recentTripAmount_fare * recentTripAmount
    )


def lineal(from_latitude, to_latitude, from_longitude, to_longitude):
    # trip["from_latitude"], trip["to_latitude"], trip["from_longitude"], trip["to_longitude"]
    distance_km = __distance(from_latitude, to_latitude, from_longitude, to_longitude)
    base_price = 250  # TODO add to database
    price_per_km = 40  # TODO add to database
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
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return c * r
