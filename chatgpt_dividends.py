import requests
import json


# Specify the stock ticker and the ex-dividend date
ticker = "AAPL"
ex_dividend_date = "2022-01-01"
headers = {'Authorization': 'Bearer 6_I3juoqn42n_W7Tgc6ikNrfdlP8ry29'}

# Use the /v2/aggs/ticker endpoint to retrieve the stock price before the ex-dividend date
url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/2021-12-30/2022-01-01"
response = requests.get(url, headers=headers)

# Check for errors
if response.status_code != 200:
    raise Exception("Error: API request unsuccessful.")

# Parse the response
data = response.json()

# Print the stock price before the ex-dividend date
print(f"Stock price before ex-dividend date: {data['results'][0]['c']}")

# Use the /v2/aggs/ticker endpoint to retrieve the stock price on the ex-dividend date
url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{ex_dividend_date}/{ex_dividend_date}"
response = requests.get(url)

# Check for errors
if response.status_code != 200:
    raise Exception("Error: API request unsuccessful.")

# Parse the response
data = response.json()

# Print the stock price on the ex-dividend date
print(f"Stock price on ex-dividend date ({data['results'][0][{'ticker'}]}): {data['results'][0]['close']}")

# Use the /v2/aggs/grouped/locale/us/options/ticker endpoint to retrieve options prices for each day
url = f"https://api.polygon.io/v2/aggs/grouped/locale/us/options/{ticker}/range/1/day/{ex_dividend_date}/{ex_dividend_date}"
response = requests.get(url)

# Check for errors
if response.status_code != 200:
    raise Exception("Error: API request unsuccessful.")

# Parse the response
data = response.json()

# Print the options prices for each day
for day in data['results']:
    print(f"Options prices for {day['date']}:")
    for option in day['options']:
        print(f"  {option['cid']}: {option['lastTradePrice']}")
