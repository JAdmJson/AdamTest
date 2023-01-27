import requests
import json
import logging

# Set up logging.
logging.basicConfig(filename='MasternodeRequest.log', encoding='utf-8', level=logging.DEBUG, filemode='w')
logger = logging.getLogger(__name__)

# Request Masternode.
try:
    global Delegation_ID
    endpoint = "https://api.staked.cloud/delegations/DASH/delegator/${collateralAddress}"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "collateralHash": input('Enter Hash Value: '),
        "collateralIndex": input('Enter Index Value: '),
        "payoutAddress": input('Enter Address Value: ')
    }
    MasternodeRequest = requests.post(endpoint, headers=headers, json=params)
    # Raise exception if unsuccessful.
    MasternodeRequest.raise_for_status()
    # Assign Delegation_ID
    Delegation_ID = MasternodeRequest.text
    # Log Response
    logger.info(f"MasternodeRequest: {MasternodeRequest}")
except requests.exceptions.HTTPError as errh:
    logger.error(f"HTTP Error: {errh}")
except requests.exceptions.ConnectionError as errc:
    logger.error(f"Error Connecting: {errc}")
except requests.exceptions.Timeout as errt:
    logger.error(f"Timeout Error: {errt}")