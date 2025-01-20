# This file contains the code to fetch the data from the API

import requests
import pandas as pd
from dotenv import load_dotenv #type: ignore
import os

load_dotenv()
API_KEY = os.getenv("AlphaVantage_API_Key")
BASE_URL = "https://www.alphavantage.co/query"

def fetch_stock_data(symbol):
    params = {
        "function": "TIME_SERIES_INTRADAY", #on the same day # the api return a json object where each key is a timestamp and the corresponding value is the stock data for that minute
        "symbol": symbol,
        "interval": "1min",
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if "Time Series (1min)" in data:
            time_series = data["Time Series (1min)"] #this value contains actual stock data for each minute
            df = pd.DataFrame.from_dict(time_series, orient="index") # we get data in dictionary form #orient="index" means that the keys(each timestamps) are the index(rows) of the dataframe and values are columns
            df = df.rename(columns={
                "1. open": "Open",
                "2. high": "High",
                "3. low": "Low",
                "4. close": "Close",
                "5. volume": "Volume"
            })
            df.index = pd.to_datetime(df.index) #convert the index(each row) to datetime object allows for more efficient time based operations
            print (df.head())
            return df.sort_index() #for ascending order
        else:
            print("Data not found for this symbol")
            return pd.DataFrame()

    else:
        print(f"Error fetching data from API: {response.status_code}")
        return pd.DataFrame()

