import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class VolatilityExtractor:
    def __init__(self, ticker):
        ticker = ticker.lower()
        ticker_map = {"wheat" : "ZW=F", "corn" : "ZC=F", "soy" : "ZS=F"}
        self.ticker = ticker_map[ticker]
        self.volatlity = self.__get_volatility()
    
    def __get_volatility(self, period=30):
        data = yf.download(self.ticker, start="2012-12-01", end="2023-01-01")
        returns = np.log(data['Close']/data['Close'].shift(1))
        returns.fillna(0, inplace=True)
        volatility = returns.rolling(window=period).std() * np.sqrt(252)
        volatility = self.__vol_monthly_avg(volatility.dropna())

        return volatility
    
    def __vol_monthly_avg(self, data):
        output = {}
        months = ["January", "February", "March", "April", "May", "June", 
                "July", "August", "September", "October", "November", "December"]

        sorted_data = sorted(data.items(), key=lambda x: x[0])  # sort data by date

        prev_month = sorted_data[0][0].month
        prev_year = sorted_data[0][0].year
        rolling = [0, 0]

        for date, value in sorted_data:
            if date.month != prev_month:
                output[f"{months[int(prev_month) - 1]}_{prev_year}"] = [prev_month, round(rolling[0] / rolling[1], 4)]
                prev_month = date.month
                prev_year = date.year
                rolling = [value, 1]
            else:
                rolling[0] += value
                rolling[1] += 1

        # handle last month's data
        output[f"{months[int(prev_month) - 1]}_{prev_year}"] = [prev_month, round(rolling[0] / rolling[1], 4)]

        return output


    def plot_volatility(self):
        fig, ax1 = plt.subplots(figsize=(14, 7))
        ax1.plot(self.volatlity, color="red", label="1-Month Volatility")
        ax1.set_ylabel('Volatility', color='red')
        ax1.tick_params(axis='y', labelcolor='red')
        plt.title('Close Price and 12-Month Volatility')
        plt.show()
    
    def get_volatility(self):
        return self.volatlity


wheat_vol = VolatilityExtractor("wheat")
# print(wheat_vol.get_volatility())