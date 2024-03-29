import src.services.fare_calculator as fare_calculator
from os import environ

DB_NAME = environ["DB_NAME"] if "DB_NAME" in environ else "Fiuumber"

ETH_SHIFT = 1000000


def get_trip_fare(
    mongo_client, from_latitude, to_latitude, from_longitude, to_longitude
):
    try:
        distance_km = fare_calculator.distance(
            float(from_latitude),
            float(to_latitude),
            float(from_longitude),
            float(to_longitude),
        )
        print(f"DISTANCE: {distance_km}")
        return get_trip_fare_final(mongo_client, distance=distance_km)
    except Exception as ex:
        print(f"CANNOT CALCULATE FARE W RULES: {str(ex)}")
        fare = fare_calculator.lineal(
            float(from_latitude),
            float(to_latitude),
            float(from_longitude),
            float(to_longitude),
        )
        return fare


def get_trip_fare_final(
    mongo_client,
    passenger_id: str = "2",
    driver_id: str = "1",
    distance: float = 12,
    duration: float = 26,
):

    database = mongo_client[DB_NAME]
    fare_rule = database["fare_rules"].find_one({"selected": True})

    if fare_rule is not None:
        fare = fare_calculator.calculate_final(
            fare_rule["minimum"],
            fare_rule["duration"],
            fare_rule["distance"],
            fare_rule["dailyTripAmountDriver"],
            fare_rule["dailyTripAmountPassenger"],
            fare_rule["monthlyTripAmountDriver"],
            fare_rule["monthlyTripAmountPassenger"],
            fare_rule["seniorityDriver"],
            fare_rule["seniorityPassenger"],
            fare_rule["recentTripAmount"],
            fare_rule["nightShift"],
            duration,
            distance,
            fare_calculator.daily_trip_amount_driver(mongo_client, driver_id),
            fare_calculator.daily_trip_amount_passenger(mongo_client, passenger_id),
            fare_calculator.monthly_trip_amount_driver(mongo_client, driver_id),
            fare_calculator.monthly_trip_amount_passenger(mongo_client, passenger_id),
            fare_calculator.get_driver_seniority(mongo_client, driver_id),
            fare_calculator.get_passenger_seniority(mongo_client, passenger_id),
            fare_calculator.get_recent_trip_amount(mongo_client, passenger_id),
            fare_calculator.is_night_shift(),
        )
        return fare / ETH_SHIFT
    else:
        return None


def get_trip_fare_to_test_fare_rule(
    mongo_client,
    fare_id: str = "3f000f2c-334d-4480-8ff2-d2cf5cdd235e",
    duration: float = 20,
    distance: float = 12,
    dailyTripAmountDriver: float = 15,
    dailyTripAmountPassenger: float = 2,
    monthlyTripAmountDriver: float = 100,
    monthlyTripAmountPassenger: float = 5,
    seniorityDriver: float = 2,
    seniorityPassenger: float = 1,
    recentTripAmount: float = 2,
    nightShift: float = 1,
):
    database = mongo_client[DB_NAME]
    fare_rule = database["fare_rules"].find_one({"_id": fare_id})
    if fare_rule is not None:
        fare = fare_calculator.calculate_test(
            fare_rule["minimum"],
            fare_rule["duration"],
            fare_rule["distance"],
            fare_rule["dailyTripAmountDriver"],
            fare_rule["dailyTripAmountPassenger"],
            fare_rule["monthlyTripAmountDriver"],
            fare_rule["monthlyTripAmountPassenger"],
            fare_rule["seniorityDriver"],
            fare_rule["seniorityPassenger"],
            fare_rule["recentTripAmount"],
            fare_rule["nightShift"],
            duration,
            distance,
            dailyTripAmountDriver,
            dailyTripAmountPassenger,
            monthlyTripAmountDriver,
            monthlyTripAmountPassenger,
            seniorityDriver,
            seniorityPassenger,
            recentTripAmount,
            nightShift,
        )
        return fare
    return None


def get_trip_fare_to_test_new_fare_rule(
    minimum_fare: float = 200,
    duration_fare: float = 0.1,
    distance_fare: float = 0.1,
    dailyTripAmountDriver_fare: float = 0.81,
    dailyTripAmountPassenger_fare: float = 0.1,
    monthlyTripAmountDrive_fare: float = 0.1,
    monthlyTripAmountPassenger_fare: float = 0.1,
    seniorityDriver_fare: float = -0.6,
    seniorityPassenger_fare: float = -0.3,
    recentTripAmount_fare: float = 0.2,
    nightShift_fare: float = 0.2,
    duration: float = 20,
    distance: float = 12,
    dailyTripAmountDriver: float = 15,
    dailyTripAmountPassenger: float = 2,
    monthlyTripAmountDriver: float = 100,
    monthlyTripAmountPassenger: float = 5,
    seniorityDriver: float = 2,
    seniorityPassenger: float = 1,
    recentTripAmount: float = 2,
    nightShift: float = 1,
):

    fare = fare_calculator.calculate_test(
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
        nightShift_fare,
        duration,
        distance,
        dailyTripAmountDriver,
        dailyTripAmountPassenger,
        monthlyTripAmountDriver,
        monthlyTripAmountPassenger,
        seniorityDriver,
        seniorityPassenger,
        recentTripAmount,
        nightShift,
    )
    return fare
