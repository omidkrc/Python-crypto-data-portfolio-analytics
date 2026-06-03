# Cryptocurrency data analysis project
# Extracted from the original Jupyter notebook.

# %% Cell 0
## installing packages

#pip install alphavantage
#pip install matplotlib.pyplot
#pip install pandas
#pip install numpy
#pip install datetime
#pip install requests
#pip install math
#pip install yahoo-finance
#pip install pandas_datareader
#pip install plotly
#pip install statsmodels
#pip install yfinance

# %% Cell 1
## importing packages

import numpy as np
import pandas_datareader
from pandas_datareader import data as wb
from pandas_datareader import yahoo
import pandas as pd
import requests
from datetime import datetime
import math
import plotly
import plotly.graph_objects as go
import yfinance as yf
import matplotlib.pyplot as plt

# %% Cell 2
## Question 1, part a

# %% Cell 3
# Define tickers
tickers = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'XRP-USD', 'ADA-USD']

# download data
data1 = pd.DataFrame()

for t in tickers:
    data1[t] = yf.download(t, start="2022-01-01", end="2022-12-31")['Close']

# renaming the data frame columns, showing the data frame
data1 = data1.rename(columns={ 'BTC-USD': 'Bitcoin', 'ETH-USD': 'Ethereum', 'BNB-USD': 'Binance coin', 'XRP-USD': 'Ripple', 'ADA-USD': 'Cardano'})
data1

# %% Cell 4
# calculating mean and standard deviation of price data of cryptos

data1_mean = data1.mean()
data1_std = data1.std()

# %% Cell 5
# scaling the price data of cryptos, showing the price trend for which based on a scaled diagram that each one starts form price=100

data1_scaled = (data1 - data1_mean) / data1_std
(data1_scaled / data1_scaled.iloc[0] * 100).plot(figsize = (15, 6));
plt.show()

# %% Cell 6
# calculating the cumulative return for each crypto

data1_returns = (data1 / data1.shift(1)) - 1
cumulative_return = (1 + data1_returns).product() - 1
cumulative_return

# %% Cell 7
## Question 1, part b

# %% Cell 8
# Define the tickers
tickers = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'XRP-USD', 'ADA-USD', 'DOGE-USD', 'SOL-USD', 'MATIC-USD', 'TRX-USD', 'LTC-USD']

# download data for the last year
data2 = pd.DataFrame()

for t in tickers:
    data2[t] = yf.download(t, start="2022-12-26", end="2023-06-26")['Close']

# renaming the data frame columns, showing the data frame
data2 = data2.rename(columns={ 'BTC-USD': 'Bitcoin', 'ETH-USD': 'Ethereum', 'BNB-USD': 'Binance coin', 'XRP-USD': 'Ripple', 'ADA-USD': 'Cardano',
 'DOGE-USD': 'Dogecoin', 'SOL-USD': 'Solana', 'MATIC-USD': 'Polygon', 'TRX-USD': 'Tronix', 'LTC-USD': 'Litecoin'})

data2

# %% Cell 9
# calculating the daily returns for cryptos
data2_returns = (data2 / data2.shift(1)) - 1
data2_returns

# define the tickers
tickers2 = ['Bitcoin', 'Ethereum', 'Binance coin', 'Ripple', 'Cardano', 'Dogecoin', 'Solana', 'Polygon', 'Tronix', 'Litecoin']

# calculating number of days with positive and negative returns for each cryptocurrency, printing the results
for crypto in tickers2:
    positive_days = (data2_returns[crypto] > 0).sum()
    negative_days = (data2_returns[crypto] < 0).sum()
    print(f'{crypto} has positive daily return for {positive_days} days and negative daily return for {negative_days} days')

# %% Cell 10
# calculating cumulative return for altcoins when bitcoin daily return is negative or positive using ∏(1 + returns𝑖) formula, printing the results
btc_returns = data2_returns['Bitcoin']
alt_returns_when_btc_positive = (1 + data2_returns[btc_returns > 0]).prod() - 1
alt_returns_when_btc_negative = (1 + data2_returns[btc_returns < 0]).prod() - 1

print('\nCumulative return for altcoins when bitcoin daily return is positive:')
print(alt_returns_when_btc_positive)
print('\nCumulative return for altcoins when bitcoin daily return is negative:')
print(alt_returns_when_btc_negative)

# %% Cell 11
## Question 2, part a

# %% Cell 12
# Define the tickers
tickers = ['BTC-USD', 'ETH-USD', 'XRP-USD']

# download the data for the last year
data3 = pd.DataFrame()

for t in tickers:
    data3[t] = yf.download(t, start="2022-01-01", end="2022-12-31")['Close']

# renaming the data frame columns, showing the data frame
data3 = data3.rename(columns={ 'BTC-USD': 'Bitcoin', 'ETH-USD': 'Ethereum', 'XRP-USD': 'Ripple' })

data3

# %% Cell 13
# calculate daily returns
log_returns3 = np.log(data3 / data3.shift(1))
log_returns3

# calculate annual returns
annual_returns3 = log_returns3.mean() * 363
annual_returns3

# define the weights
weights = np.arange(0, 1.05, 0.05)

# calculate portfolio return and volatility for each possible composition
portfolio_returns = []
portfolio_volatilities = []
portfolio_weights = []

for i in range(len(weights)):
    for j in range(len(weights)):
        for k in range(len(weights)):
            if weights[i] + weights[j] + weights[k] == 1:
                new_weights = [weights[i], weights[j], weights[k]]
                portfolio_return = np.sum(annual_returns3* new_weights)
                portfolio_variance = np.dot(np.array(new_weights).T, np.dot(log_returns3.cov() * 363, new_weights))
                portfolio_volatility = np.sqrt(portfolio_variance)
                portfolio_weights.append(new_weights)
                portfolio_returns.append(portfolio_return)
                portfolio_volatilities.append(portfolio_volatility)

# Print the results
# Consider that first element in every matrix relates to Bitcoin, second relates to Ethereum and third one relates to Ripple
for i in range(len(portfolio_returns)):
    print('Weights:', np.round(portfolio_weights[i], 4))
    print('Portfolio Return:', round(portfolio_returns[i], 4))
    print('Portfolio Volatility:', round(portfolio_volatilities[i], 4))
    print()

# %% Cell 14
## Question 2, part b

# %% Cell 15
# plot all possible sharpe ratios that could be obtained by chosen portfolios
risk_free_rate = 0

# method 1 for ploting
fig = go.Figure()
fig.add_trace(go.Scatter(x=list(portfolio_volatilities), 
                         y=list(portfolio_returns), 
                      #- Add color scale for sharpe ratio   
                      marker=dict(color=(np.array(portfolio_returns)-risk_free_rate)/(np.array(portfolio_volatilities)), 
                                  showscale=True, 
                                  size=7,
                                  line=dict(width=1),
                                  colorscale="RdBu",
                                  colorbar=dict(title="Sharpe<br>Ratio")
                                 ), 
                      mode='markers'))
# Add title/labels
fig.update_layout(template='plotly_white',
                  xaxis=dict(title='Annualised Risk (Volatility)'),
                  yaxis=dict(title='Annualised Return'),
                  title='Sample of chosen Portfolios',
                  coloraxis_colorbar=dict(title="Sharpe Ratio"))

# %% Cell 16
# method 2 for ploting
x2 = portfolio_volatilities
y2 = portfolio_returns

plt.scatter(x2, y2)
plt.show()

# %% Cell 17
# creating csv file containing portfolios of three cryptos, returns and variances for each combination of weights
portfolios_data_frame = pd.DataFrame(0,index=range(len(portfolio_weights)), columns=['Bitcoin-weight','Ethereum-weight','Ripple-weight','return','volatility','sharpe ratio' ])

for i in range(len(portfolio_weights)):
    portfolios_data_frame['Bitcoin-weight'].loc[i]=portfolio_weights[i][0]
    portfolios_data_frame['Ethereum-weight'].loc[i]=portfolio_weights[i][1]
    portfolios_data_frame['Ripple-weight'].loc[i]=portfolio_weights[i][2]
    portfolios_data_frame['return'].loc[i]=portfolio_returns[i]
    portfolios_data_frame['volatility'].loc[i]=portfolio_volatilities[i]
    portfolios_data_frame['sharpe ratio'].loc[i]=portfolio_returns[i]/portfolio_volatilities[i]

portfolios_data_frame.to_csv('portfolios.csv')

# %% Cell 18
# calculating the best weights which give us the highest possible sharpe ratio, printing the results

sharpe_ratio = (np.array(portfolio_returns) - risk_free_rate)/(np.array(portfolio_volatilities))
sharpe_ratio

M = max(sharpe_ratio)
for i in range(0, np.array(sharpe_ratio.shape)[0]) :
     if sharpe_ratio[i] == M :
          print('Optimal weights to gain highest sharpe ratio are:', np.round(portfolio_weights[i], 4))

# %% Cell 19
# Question 3

# %% Cell 20
# download the data for the last year
data4= pd.DataFrame()
data4= yf.download('BTC-USD', start="2021-09-01", end="2023-01-01")['Adj Close']

# %% Cell 21
data=[]
for i in range(10,101,5):
    for j in range(5,i,5):

        #i is number of days of long moving average and j is number of days of short moving average
        sell= 0
        buy= 0
        wealth= 1
        wealth_transactioned= 1
        first_day= np.where(data4==data4.loc['2022-01-01'])[0][0]
        last_day= np.where(data4==data4.loc['2022-12-31'])[0][0]
        for t in range(first_day , last_day):

            #if short moving average is bigger than long moving average we have buy signal
            if sum(data4[t-j:t])/j > sum(data4[t-i:t])/i:
                buy+= 1
                wealth*= data4[t] / data4[t-1]
                wealth_transactioned*= 1 + 0.95*(data4[t] / data4[t-1] -1)
            
            #if long moving average is bigger than short moving average we have sell signal
            elif sum(data4[t-i:t])/i > sum(data4[t-j:t])/j:
                sell+= 1
        data.append([i,j,buy,sell,wealth,wealth_transactioned])    
        

# %% Cell 22
#finding maximum possible wealth
max_wealth=0
for i in range(np.shape(data)[0]):
    if data[i][4] > max_wealth:
        max_wealth= data[i][4]

#finding index of trading strategy which makes maximum possible wealth
for i in range(np.shape(data)[0]):
    if data[i][4] == max_wealth:
        max_index=i

# %% Cell 23
#finding maximum possible transactioned wealth
max_transactioned_wealth=0
for i in range(np.shape(data)[0]):
    if data[i][5] > max_transactioned_wealth:
        max_transactioned_wealth= data[i][5]

#finding index of trading strategy which makes maximum possible transactioned wealth
for i in range(np.shape(data)[0]):
    if data[i][5] == max_transactioned_wealth:
        max_transactioned_index=i

# %% Cell 24
# printing the results for part a
print("best trading strategy without transaction:")
print("long moving average days:  ",data[max_index][0])
print("short moving average days:  ",data[max_index][1])
print("buy signals:  ",data[max_index][2])
print("sell signals:  ",data[max_index][3])
print("ratio of wealth change:  ",data[max_index][4])

# %% Cell 25
# printing the results for part b
print("best trading strategy with transaction:")
print("long moving average days:  ",data[max_transactioned_index][0])
print("short moving average days:  ",data[max_transactioned_index][1])
print("buy signals:  ",data[max_transactioned_index][2])
print("sell signals:  ",data[max_transactioned_index][3])
print("ratio of wealth change:  ",data[max_transactioned_index][5])

