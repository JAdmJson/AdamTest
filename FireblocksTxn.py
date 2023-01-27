import requests
import logging
import time
from threading import Thread

# Set up logging.
logging.basicConfig(filename='FireblocksTxn.log', encoding='utf-8', level=logging.DEBUG, filemode='w')
logger = logging.getLogger(__name__)

FireblocksKey = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
FireblocksToken = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"

def sign_transaction():
    global status
    global txnForSigning
    global Signature
    while status != "WAITFORSIG":
        time.sleep(1)
    # Perform transaction.
    try:
        endpoint = "https://api.fireblocks.io/v1/transactions/"
        headers = {
            "X-API-Key": FireblocksKey,
            "Authorization": "Bearer " + FireblocksToken
        }
        params = {
            "asset_ID": "DASH",
            "amount": "1000",
            "source": "TransferPeerPath(VAULT_ACCOUNT, from_vault_account_id)",
            "destination": "DestinationTransferPeerPath(VAULT_ACCOUNT, to_vault_account_id)",
            "externalTxID": txnForSigning
        }
        FireblocksTxn = requests.post(endpoint, headers=headers, json=params)
        # Raise exception if unsuccessful.
        FireblocksTxn.raise_for_status()
        # Log response.
        logger.info(f"FireblocksTxn: {FireblocksTxn}")
        txId = FireblocksTxn['id']
    except requests.exceptions.HTTPError as errh:
        logger.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        logger.error(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        logger.error(f"Timeout Error: {errt}")

    # Get transaction details.
    try:
        endpoint = "https://api.fireblocks.io/v1/transactions/"
        headers = {
            "X-API-Key": FireblocksKey,
            "Authorization": "Bearer " + FireblocksToken
        }
        params = {
            "txId": txId
        }
        TxDetails = requests.get(endpoint, headers=headers, json=params)
        # Raise exception if unsuccessful.
        TxDetails.raise_for_status()
        # Log response.
        logger.info(f"TxDetails: {TxDetails}")
        global Signature
        Signature = TxDetails['SignedMessage'['content']]
    except requests.exceptions.HTTPError as errh:
        logger.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        logger.error(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        logger.error(f"Timeout Error: {errt}")

t = Thread(target = sign_transaction)
t.start()