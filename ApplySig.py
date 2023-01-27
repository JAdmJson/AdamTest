import requests
import logging

# Set up logging.
logging.basicConfig(filename='ApplySig.log', encoding='utf-8', level=logging.DEBUG, filemode='w')
logger = logging.getLogger(__name__)

# Apply signature.
try:
    endpoint = "https://api.staked.cloud/delegations/DASH/delegator/${collateralAddress}"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "signedTxData": Signature
    }
    ApplySig = requests.put(endpoint, headers=headers, json=params)
    # Raise exception if unsuccessful.
    ApplySig.raise_for_status()
    # Log Response
    logger.info(f"ApplySig: {ApplySig}")
except requests.exceptions.HTTPError as errh:
    logger.error(f"HTTP Error: {errh}")
except requests.exceptions.ConnectionError as errc:
    logger.error(f"Error Connecting: {errc}")
except requests.exceptions.Timeout as errt:
    logger.error(f"Timeout Error: {errt}")