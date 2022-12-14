import requests

import src.dal.trips_provider as trips_provider
from src.utils.payments_processor import URL_USERS

URL_EXPO = "https://api.expo.dev/v2"
HEADERS = {
    "Content-type": "application/json",
    "Accept": "application/json",
    "Accept-encoding": "gzip, deflate",
}


def send_notification(title, body, expo_token):

    try:
        url = f"{URL_EXPO}/push/send"
        req_body = {"body": body, "title": title, "to": expo_token}

        r = requests.post(url, json=req_body)

        if r.status_code != 200:
            raise Exception(r.json()["message"])

        # {"data":[{"id":"183835e4-1e05-46de-9015-f2f687a4a7d6","status":"ok"}]}
        response = r.json()

        return response
    except Exception as ex:
        print("[ERROR] Error in send_notification: " + str(ex))
        raise ex


def get_notification_token(user_id):
    try:
        url = f"{URL_USERS}/user/{str(user_id)}"
        r = requests.get(url)
        r_user = r.json()
        notifications_token = r_user["notificationsToken"]
        return notifications_token
    except Exception as ex:
        print("[ERROR] Error in get_wallet_address: " + str(ex))
        raise ex


def notify_for_assigned_driver(trip_id):
    try:
        trip = trips_provider.get_trip_by_id(trip_id)
        passenger_id = trip.get("passengerId")
        notifications_token = get_notification_token(passenger_id)
        if notifications_token is None:
            raise Exception(
                f"Passenger with id={passenger_id} has not setted notifications token"
            )
        send_notification(
            "Assigned driver", "Your Fiuumber is on the way ;)", notifications_token
        )
    except Exception as ex:
        print("[ERROR] Error in notify_for_assigned_driver: " + str(ex))
        raise ex
