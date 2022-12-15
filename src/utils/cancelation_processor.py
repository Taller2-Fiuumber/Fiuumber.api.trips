# import requests

# from src.domain.payment import Payment
import src.services.trips_provider as trips_provider

# import src.dal.payments_provider as payments_provider
import src.domain.status as trip_status

import src.services.trips_status as trip_status_service
import src.services.fare as fare_service
import src.services.trips as trips_service

from pymongo import MongoClient

from os import environ

from src.utils.payments_processor import (
    create_and_process_trip_payments,
)

MONGODB_URL = environ["MONGODB_URL"]

URL_USERS = "https://fiuumber-api-users.herokuapp.com/api/users-service"
URL_PAYMENTS = "https://fiuumber-api-payments.herokuapp.com/api/wallets-service"
MAX_ETH_TEST = 0.0005
HEADERS = {"Content-type": "application/json", "Accept": "application/json"}

mongo_client = MongoClient(MONGODB_URL, connect=False)


def cancel_from_passenger(trip_id, latitude=None, longitude=None):
    try:
        trip = trips_provider.get_trip_by_id(mongo_client, trip_id)
        if trip is None:
            raise Exception(f"Trip with id = {trip_id} was not found")

        status = trip_status.InProgress().name()

        if (
            status == trip_status.DriverAssigned().name()
            or status == trip_status.DriverArrived().name()
        ):
            # Se cobra la totalidad del viaje a favor del chofer a modo de
            # penalidad para el pasajero (asi lo pide la US)
            create_and_process_trip_payments(trip_id, mongo_client)

        if status == trip_status.InProgress().name():
            # Se cobra la distancia recorrida hasta el momento
            # Se recalcula la tarifa con la posición de cancelación
            try:
                new_final_price = fare_service.get_trip_fare(
                    trip.get("from_latitude"),
                    latitude,
                    trip.get("from_longitude"),
                    longitude,
                )
                print(f"PREV FARE: {trip.get('finalPrice')}")
                trip = trips_service.update_trip_fare(
                    trip_id, new_final_price, mongo_client
                )
                print(f"NEW FARE: {trip.get('finalPrice')}")
                create_and_process_trip_payments(trip_id, mongo_client)
            except Exception as ex:
                raise ex

        # setear el viaje en cancelado
        return trip_status_service.update_trip_status(
            trip_id, mongo_client, trip_status.Canceled().name()
        )

    except Exception as ex:
        raise ex


def cancel_from_driver(trip_id, latitude=None, longitude=None):
    try:
        trip = trips_provider.get_trip_by_id(mongo_client, trip_id)
        if trip is None:
            raise Exception(f"Trip with id = {trip_id} was not found")

        # No hay reembolsos que hacer, ya que el viaje se cobra al final
        return trip_status_service.update_trip_status(
            trip_id, mongo_client, trip_status.Canceled().name()
        )

    except Exception as ex:
        raise ex
