# import requests

# from src.domain.payment import Payment
import src.services.trips_provider as trips_provider

# import src.dal.payments_provider as payments_provider
import src.domain.status as trip_status

import src.services.trips_status as services

from pymongo import MongoClient

from os import environ

MONGODB_URL = environ["MONGODB_URL"]

URL_USERS = "https://fiuumber-api-users.herokuapp.com/api/users-service"
URL_PAYMENTS = "https://fiuumber-api-payments.herokuapp.com/api/wallets-service"
MAX_ETH_TEST = 0.0005
HEADERS = {"Content-type": "application/json", "Accept": "application/json"}

mongo_client = MongoClient(MONGODB_URL, connect=False)


def cancel_from_passenger(trip_id, latitude=None, longitude=None):
    try:
        trip = trips_provider.get_trip_by_id(trip_id)
        if trip is None:
            raise Exception(f"Trip with id = {trip_id} was not found")

        status = trip.get("STATUS")

        print(f"trip prev status: {status}")

        # if status == trip_status.Requested.name():
        #     # Caso trivial, no se hace nada, solo se setea el estado

        if (
            status == trip_status.DriverAssigned.name()
            or status == trip_status.DriverArrived.name()
        ):
            # Se cobra el viaje a favor del chofer a modo de penalidad para el pasajero
            return

        if status == trip_status.InProgress.name():
            # Se cobra la distancia recorrida hasta el momento
            # Recalcular la tarifa con la posición de cancelación
            print(latitude)
            print(longitude)
            return

        # setear el viaje en cancelado
        return services.update_trip_status(
            id, mongo_client, trip_status.Canceled.name()
        )

    except Exception as ex:
        raise ex


def cancel_from_driver(trip_id, latitude=None, longitude=None):
    try:
        trip = trips_provider.get_trip_by_id(trip_id)
        if trip is None:
            raise Exception(f"Trip with id = {trip_id} was not found")

        status = trip.get("STATUS")

        print(f"trip prev status: {status}")

        if (
            status == trip_status.DriverAssigned.name()
            or status == trip_status.DriverArrived.name()
        ):
            # No se hace nada, el pasajero conserva su dinero
            return

        if status == trip_status.InProgress.name():
            # Se le reembolsa el total del viaje al pasajero
            return

        # setear el viaje en cancelado

    except Exception as ex:
        raise ex
