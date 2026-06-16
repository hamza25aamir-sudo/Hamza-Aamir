import sys
import requests
 
if len(sys.argv) != 2:
    sys.exit("Usage: python bitcoin.py <number of bitcoins>")
 
try:
    n = float(sys.argv[1])
except ValueError:
    sys.exit("Error: input must be a numeric value.")
 
try:
    response = requests.get("https://rest.coincap.io/v3/assets/bitcoin?apiKey=YourApiKey")
    response.raise_for_status()
    data = response.json()
    price = float(data["data"]["priceUsd"])
except requests.RequestException:
    sys.exit("Error: could not retrieve Bitcoin price.")
 
total = n * price
print(f"${total:,.4f}")
 