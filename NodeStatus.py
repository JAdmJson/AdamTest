import requests
import json
import logging
import time
from threading import Thread

# Set up logging.
logging.basicConfig(filename='NodeStatus.log', encoding='utf-8', level=logging.DEBUG, filemode='w')
logger = logging.getLogger(__name__)

# Monitor Node Status.
status = ""
txnForSigning = ""
signedTxData = ""
def monitor_status():
    global status
    try:
        while True:
            endpoint = "https://api.staked.cloud/delegations/DASH/delegator/${collateralAddress}"
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                "collateralHash": input('Enter Hash Value: '),
                "collateralIndex": input('Enter Index Value: '),
                "payoutAddress": input('Enter Address Value: ')
            }
            NodeStatus = requests.get(endpoint, headers=headers, json=params)
            # Raise exception if unsuccessful.
            NodeStatus.raise_for_status()
            # Assign Delegation_ID object.
            StatusResponse = json.loads(NodeStatus.text)
            # Log response.
            logger.info(f"NodeStatus: {NodeStatus}")
            # Get status.
            status = StatusResponse['status']
            if status == "WAITFORSIG":
                break
            # Wait for retry.
            time.sleep(30)
    except requests.exceptions.HTTPError as errh:
        logger.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        logger.error(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        logger.error(f"Timeout Error: {errt}")

    # Get txnForSigning.
    global txnForSigning
    txnForSigning = StatusResponse['txnForSigning']
    # Get signedTxData.
    global signedTxData
    signedTxData = StatusResponse['signedTxData']

t = Thread(target = monitor_status)
t.start()