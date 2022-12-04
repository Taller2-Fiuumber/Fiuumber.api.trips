import requests

URL_PAYMENTS = "https://fiuumber-api-users.herokuapp.com/api/users-service"
URL_USERS = "https://fiuumber-api-payments.herokuapp.com/api/wallets-service"
MAX_ETH_TEST = 0.00000001

def get_wallet_address(userId):
    try:
        url = format("{URL_USERS}/user/{userId}", URL_USERS, str(userId))
        print(url)
        r = requests.get(url)
        r_user = r.json()
        address = r_user["walletAddress"]
        return address
    except Exception as ex:
        print("[ERROR] Error in get_wallet_address: " + str(ex))
        raise ex

def process_payment_from_passenger(trip):
    try:
        passenger_wallet_address = get_wallet_address(trip.passengerId)
        hash = deposit_from_sender(passenger_wallet_address, trip.finalPrice)
        return hash
    except Exception as ex:
        print("[ERROR] Error in process_payment_from_passenger: " + str(ex))
        raise ex

def process_payment_to_driver(trip):
    try:
        driver_wallet_address = get_wallet_address(trip.driverId)
        # TODO: descontar comisión de Fiuumber ;)
        deposit_to_receiver(driver_wallet_address, trip.finalPrice)
    except Exception as ex:
        print("[ERROR] Error in process_payment_to_driver: " + str(ex))
        raise ex

# Realiza un depósito desde la wallet provista en sender_address a la wallet de Fiuumber (owner)
# Retorna el hash de la transaccion
def deposit_from_sender(sender_address, ammount):
    if (ammount > MAX_ETH_TEST): raise Exception("ETH value provided is too large for testing purposes")
    try:
        url = format("{URL_PAYMENTS}/depositFromSender")
        req_body = {'senderAddress': sender_address, 'amountInEthers': ammount}
        r = requests.post(url, req_body)
        r_deposit = r.json()
        return r_deposit["hash"]
    except Exception as ex:
        print("[ERROR] Error in deposit_from_sender: " + str(ex))
        raise ex

# Realiza un depósito desde la wallet de Fiuumber (owner) a la sender_address provista
# Retorna el hash de la transaccion
def deposit_to_receiver(receiver_address, ammount):
    if (ammount > MAX_ETH_TEST): raise Exception("ETH value provided is too large for testing purposes")
    try:
        url = format("{URL_PAYMENTS}/depositToReceiver")
        req_body = {'receiverAddress': receiver_address, 'amountInEthers': ammount}
        r = requests.post(url, req_body)
        r_deposit = r.json()
        return r_deposit["hash"]
    except Exception as ex:
        print("[ERROR] Error in deposit_to_receiver: " + str(ex))
        raise ex
