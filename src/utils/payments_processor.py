import requests

from src.domain.payment import Payment

URL_USERS = "https://fiuumber-api-users.herokuapp.com/api/users-service"
URL_PAYMENTS = "https://fiuumber-api-payments.herokuapp.com/api/wallets-service"
MAX_ETH_TEST = 0.00000001
HEADERS = {'Content-type': 'application/json', 'Accept': 'application/json'}

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

def process_payment(payment):
    try:
        hash = None
        if (payment["type"] == "FROM_SENDER"):
            hash = deposit_from_sender(payment["wallet_address"], payment["ammount"])

        if (payment["type"] == "TO_RECEIVER"):
            # TODO: descontar comisión de Fiuumber ;)
            hash = deposit_to_receiver(payment["wallet_address"], payment["ammount"])

        return hash
    except Exception as ex:
        print("[ERROR] Error in process_payment_from_passenger: " + str(ex))
        raise ex

# Realiza un depósito desde la wallet provista en sender_address a la wallet de Fiuumber (owner)
# Retorna el hash de la transaccion
def deposit_from_sender(sender_address, ammount):
    if (ammount > MAX_ETH_TEST): raise Exception("ETH value provided is too large for testing purposes")
    try:
        url = f'{URL_PAYMENTS}/depositFromSender'
        req_body = {'senderAddress': sender_address, 'amountInEthers': '{:f}'.format(ammount)}
        
        print(f'[INFO] deposit_from_sender {url} -> ETH: {ammount} sender: {sender_address}')

        r = requests.post(url, json=req_body)

        if (r.status_code != 200): raise Exception(r.json()["message"])

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
        url = format("{URL_PAYMENTS}/depositToReceiver", URL_PAYMENTS)
        req_body = {'receiverAddress': receiver_address, 'amountInEthers': '{:f}'.format(ammount)}

        print(f'[INFO] deposit_from_sender {url} -> ETH: {ammount} sender: {receiver_address}')

        r = requests.post(url, json=req_body)

        if (r.status_code != 200): raise Exception(r.json()["message"])

        r_deposit = r.json()
        
        return r_deposit["hash"]
    except Exception as ex:
        print("[ERROR] Error in deposit_to_receiver: " + str(ex))
        raise ex
