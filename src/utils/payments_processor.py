import requests

from src.domain.payment import Payment
import src.services.trips_provider as trips_provider
import src.services.payments as payments

URL_USERS = "https://fiuumber-api-users.herokuapp.com/api/users-service"
URL_PAYMENTS = "https://fiuumber-api-payments.herokuapp.com/api/wallets-service"
MAX_ETH_TEST = 0.0005
HEADERS = {"Content-type": "application/json", "Accept": "application/json"}


def process_payments(mongo_client):
    try:
        pending_payments = payments.get_pending_payments(mongo_client)
        for payment in pending_payments:
            try:
                print("[INFO] processing payment: " + payment["_id"])
                payments.mark_payment_as_processing(payment["_id"])
                hash = process_payment(payment)
                payments.mark_payment_as_processed(payment["_id"], hash)
            except Exception as ex:
                print(
                    "[INFO] error processing payment: "
                    + payment["_id"]
                    + ": "
                    + str(ex)
                )
                continue

        return pending_payments
    except Exception as ex:
        raise ex


def get_wallet_address(userId):
    try:
        url = format("{URL_USERS}/user/{userId}", URL_USERS, str(userId))
        r = requests.get(url)
        r_user = r.json()
        address = r_user["walletAddress"]
        return address
    except Exception as ex:
        print("[ERROR] Error in get_wallet_address: " + str(ex))
        raise ex


def process_payment(payment):
    try:
        hash = None
        if payment["type"] == "FROM_SENDER":
            hash = deposit_from_sender(payment["wallet_address"], payment["amount"])

        if payment["type"] == "TO_RECEIVER":
            # TODO: descontar comisión de Fiuumber ;)
            hash = deposit_to_receiver(payment["wallet_address"], payment["amount"])

        return hash
    except Exception as ex:
        print("[ERROR] Error in process_payment_from_passenger: " + str(ex))
        raise ex


# Realiza un depósito desde la wallet provista en sender_address a la wallet de Fiuumber (owner)
# Retorna el hash de la transaccion
def deposit_from_sender(sender_address, amount):
    if amount > MAX_ETH_TEST:
        raise Exception("ETH value provided is too large for testing purposes")
    try:
        url = f"{URL_PAYMENTS}/depositFromSender"
        formatted_amount = "{:.10f}".format(amount)
        req_body = {
            "senderAddress": sender_address,
            "amountInEthers": formatted_amount,
        }
        print(
            f"[INFO] deposit_from_sender {url} -> ETH: {formatted_amount} sender: {sender_address}"
        )

        r = requests.post(url, json=req_body)

        if r.status_code != 200:
            raise Exception(r.json()["message"])

        r_deposit = r.json()

        return r_deposit["hash"]
    except Exception as ex:
        print("[ERROR] Error in deposit_from_sender: " + str(ex))
        raise ex


# Realiza un depósito desde la wallet de Fiuumber (owner) a la sender_address provista
# Retorna el hash de la transaccion
def deposit_to_receiver(receiver_address, amount):
    if amount > MAX_ETH_TEST:
        raise Exception("ETH value provided is too large for testing purposes")
    try:
        url = f"{URL_PAYMENTS}/depositToReceiver"
        formatted_amount = "{:.10f}".format(amount)
        req_body = {
            "receiverAddress": receiver_address,
            "amountInEthers": formatted_amount,
        }

        print(
            f"[INFO] deposit_from_sender {url} -> ETH: {formatted_amount} sender: {receiver_address}"
        )

        r = requests.post(url, json=req_body)

        if r.status_code != 200:
            raise Exception(r.json()["message"])

        r_deposit = r.json()

        return r_deposit["hash"]
    except Exception as ex:
        print("[ERROR] Error in deposit_to_receiver: " + str(ex))
        raise ex


def get_user_wallet(user_id):
    try:
        url = f"{URL_USERS}/user/{user_id}"

        r = requests.get(url)

        if r.status_code != 200:
            raise Exception(r.json())

        user = r.json()

        return user["walletAddress"]
    except Exception as ex:
        print("[ERROR] Error in get_user_wallet: " + str(ex))
        raise ex


def create_trip_payments(mongo_client, trip_id):

    print("____________trip_id", trip_id)
    try:
        trip = trips_provider.get_trip_by_id(mongo_client, trip_id)
        if trip is None:
            raise Exception(f"Trip with id={trip_id} was not found")

        wallet_passenger = get_user_wallet(trip["passengerId"])
        if wallet_passenger is None:
            raise Exception("Passenger has not a wallet")

        wallet_driver = get_user_wallet(trip["driverId"])
        if wallet_driver is None:
            raise Exception("Driver has not a wallet")

        passenger_payment = create_payment(
            trip["_id"],
            "FROM_SENDER",
            trip["finalPrice"],
            wallet_passenger,
            1,
            mongo_client,
        )
        driver_payment = create_payment(
            trip["_id"],
            "TO_RECEIVER",
            trip["finalPrice"],
            wallet_driver,
            2,
            mongo_client,
        )
        return (passenger_payment, driver_payment)
    except Exception as ex:
        print("[ERROR] Error in create_trip_payments: " + str(ex))
        raise ex


def create_payment(trip_id, type, amount, wallet_address, order, mongo_client):
    payment = Payment.parse_obj(
        {
            "tripId": trip_id,
            "type": type,
            "amount": amount,
            "wallet_address": wallet_address,
            "order": order,
        }
    )
    return payments.create_payment(payment, mongo_client)


def create_and_process_trip_payments(trip_id, mongo_client):
    try:
        (passenger_payment, driver_payment) = create_trip_payments(
            mongo_client, trip_id
        )
        process_payment(passenger_payment)
        process_payment(driver_payment)
    except Exception as ex:
        print(
            f"[ERROR] cannot create or process payments for trip {trip_id} reason: {str(ex)}"
        )
        raise ex
