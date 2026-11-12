import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the project folder
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("ETHERSCAN_API_KEY")

def get_transactions(wallet_address):

    if not API_KEY:
        print("ERROR: API key not found.")
        return []

    url = "https://api.etherscan.io/v2/api"

    params = {
        "chainid": 1,
        "module": "account",
        "action": "txlist",
        "address": wallet_address,
        "startblock": 0,
        "endblock": 99999999,
        "page": 1,
        "offset": 100,
        "sort": "asc",
        "apikey": API_KEY
    }

    try:
        response = requests.get(
            url, params=params, timeout=20
        )
        data = response.json()

        if data.get("status") == "1":
            print("Blockchain connection successful!")
            return data.get("result", [])

        print("API Error:", data.get("result"))
        print("Message:", data.get("message"))
        return []

    except requests.RequestException as error:
        print("Network error:", error)
        return []

    except ValueError:
        print("Invalid API response.")
        return []

print("API key loaded:",bool(API_KEY))
