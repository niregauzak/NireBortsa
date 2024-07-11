import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import talib

# Add a title to the app
st.title('New York Stock Exchange (NYSE)')

# Define the sectors and their corresponding main tickets
sectors = {
    'Technology': ['AAPL', 'MSFT', 'CSCO', 'ORCL'],
    'Finance': ['JPM', 'C', 'BAC', 'GS'],
    'Health Care': ['JNJ', 'PFE', 'UNH', 'MRK'],
    'Consumer Discretionary': ['DIS', 'NKE', 'MCD', 'HD'],
    'Communication Services': ['VZ', 'T', 'TXN', 'CSCO'],
    'Industrials': ['BA', 'GE', 'HON', 'CAT'],
    'Consumer Staples': ['PG', 'KO', 'PEP', 'WMT'],
    'Energy': ['XOM', 'CVX', 'SLB', 'COP'],
    'Utilities': ['DUK', 'NEE', 'SO', 'AEP'],
    'Real Estate': ['VNO', 'DLR', 'SPG', 'PLD'],
    'Materials': ['DOW', 'FCX', 'NUE', 'APD'],
}

# Create a sector selection menu
selected_sector = st.selectbox('Select a sector', sectors.keys())

# Create a ticket selection menu based on the selected sector
selected_ticker = st.selectbox('Select a ticket', sectors[selected_sector])

# Get data on the selected ticket
tickerData = yf.Ticker(selected_ticker)

# Create a time period selection menu
time_period = st.selectbox('Select time period', ['1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'max'])

# Get the historical prices for this ticket
tickerDf = tickerData.history(period=time_period)
#print(tickerDf)
#aurrerako aukeratu nik datak
#all_data = yf.download(selected_ticker, start=start_date, end=end_date)

data_close = tickerDf['Close']

# Create an analytical technique selection menu
analytical_technique1 = st.multiselect('Aukeratu bat:', ['None', 'SMA20', 'SMA50', 'SMA200', 'EMA27','Candle',
    'Bollinger Bands'])

analytical_technique2 = st.multiselect('Aukeratu bat:', ['None','Volume','RSI','MACD','VPT', 'ADX'])


 

# Figure 1: Plot the closing prices and tendencies
fig1, ax1 = plt.subplots()
ax1.plot(data_close.index,data_close, label='Close')
ax1.set_title(f'{selected_ticker} Closing Prices')
ax1.set_xlabel('Date')
ax1.set_ylabel('Price')
ax1.tick_params(axis='x', rotation=90)#,labelsize=labeltamaina)
#start, end = ax1.get_xlim()
#ax1.xaxis.set_ticks(np.arange(start, end, zenbatero))


# Figure 2: momentum indicators
fig2, ax2 = plt.subplots()
#ax2.plot(tickerDf['Close'], label='Close')
ax2.set_title(f'{selected_ticker} Indicators')
ax2.set_xlabel('Date')
ax2.set_ylabel('Price')
ax2.tick_params(axis='x', rotation=90)

    # Calculate and plot the selected analytical techniques
#if not clear_plots:
for technique in analytical_technique1:
            if technique == 'SMA20':
                sma20 = tickerDf['Close'].rolling(window=20).mean()
                ax1.plot(sma20, label='SMA20', color='red')
            elif technique == 'SMA50':
                sma50 = tickerDf['Close'].rolling(window=50).mean()
                ax1.plot(sma50, label='SMA50', color='green')
            elif technique == 'SMA200':
                sma200 = tickerDf['Close'].rolling(window=200).mean()
                ax1.plot(sma200, label='SMA200', color='blue')
            elif technique == 'EMA27':
                ema27 = tickerDf['Close'].ewm(span=27, adjust=False).mean()
                ax1.plot(ema27, label='EMA27', color='orange')
            elif technique == 'Bollinger Bands':
                # Calculate Bollinger Bands
                rolling_mean = tickerDf['Close'].rolling(window=20).mean()
                rolling_std = tickerDf['Close'].rolling(window=20).std()
                upper_band = rolling_mean + (2 * rolling_std)
                lower_band = rolling_mean - (2 * rolling_std)

                # Plot Bollinger Bands
                ax1.plot(upper_band, label='Upper Band', color='magenta', linestyle='--')
                ax1.plot(lower_band, label='Lower Band', color='magenta', linestyle='--')
                ax1.fill_between(upper_band.index, upper_band, lower_band, color='magenta', alpha=0.2)

            elif technique == 'Candle':
                #Hemendik hartuta: https://www.geeksforgeeks.org/how-to-create-a-candlestick-chart-in-matplotlib/
                up = tickerDf[tickerDf.Close >= tickerDf.Open] 
                down = tickerDf[tickerDf.Close < tickerDf.Open] 
  
                col1 = 'blue'
                col2 = 'green'
  
# Setting width of candlestick elements 
                width = .3
                width2 = .03
  
# Plotting up prices of the stock 
                ax1.bar(up.index, up.Close-up.Open, width, bottom=up.Open, color=col1) 
                ax1.bar(up.index, up.High-up.Close, width2, bottom=up.Close, color=col1) 
                ax1.bar(up.index, up.Low-up.Open, width2, bottom=up.Open, color=col1) 
  
# Plotting down prices of the stock 
                ax1.bar(down.index, down.Close-down.Open, width, bottom=down.Open, color=col2) 
                ax1.bar(down.index, down.High-down.Open, width2, bottom=down.Open, color=col2) 
                ax1.bar(down.index, down.Low-down.Close, width2, bottom=down.Close, color=col2) 
 

for technique in analytical_technique2:
    if technique == 'Volume' :
                bolumena = tickerDf['Volume']
                ax2.plot(bolumena, label='bolumena', color='red')

    elif technique == 'RSI':
                rsi = talib.RSI(tickerDf['Close'])
                # Plot RSI
                #ax2 = ax.twinx()
                ax2.axhline(y=30, color='red', linestyle='--')
                ax2.axhline(y=70, color='green', linestyle='--')
                ax2.set_ylim([0, 100])
                ax2.plot(rsi, label='RSI', color='darkred')
                ax2.set_ylabel('RSI')
                ax2.legend()
    elif technique == 'MACD':
                macd, macdsignal, macdhist = talib.MACD(tickerDf['Close'])
                indicator = pd.DataFrame({'MACD': macd, 'Signal': macdsignal})

                #macd, macdsignal, macdhist = talib.MACD(tickerDf['Close'], fastperiod=tickerDf[indicator]['fastperiod'], slowperiod=indicators[indicator]['slowperiod'], signalperiod=indicators[indicator]['signalperiod'])
                #ax2 = ax.twinx()
                ax2.plot(tickerDf['Close'].index, macd, color='blue', label='MACD')
                ax2.plot(tickerDf['Close'].index, macdsignal, color='orange', label='Signal')
                ax2.fill_between(tickerDf['Close'].index, macdhist, 0, color='black', alpha=0.3)
                ax2.legend()
            

    

    elif technique == 'ADX' :
        # Check if the stock data was downloaded successfully
        if isinstance(tickerDf, pd.DataFrame):
            n_lerro = len(tickerDf)
            kenduazkena = tickerDf.iloc[:-2]
            print("Azkena:")
            print(tickerDf.iloc[-1])
        #adx, adx_di_plus, adx_di_minus = talib.ADX(tickerDf['High'], tickerDf['Low'], tickerDf['Close'], timeperiod=14)
        #adx, di_plus, di_minus, _ = talib.ADX(tickerDf['High'], tickerDf['Low'], tickerDf['Close'], timeperiod=14)
            adx = talib.ADX(kenduazkena['High'],kenduazkena['Low'], kenduazkena['Close'], timeperiod=14)
            ax2.plot(adx, label='ADX')

    elif technique == 'VPT' :
        #vpt = talib.VPT(tickerDf['High'], tickerDf['Low'], tickerDf['Close'], tickerDf['Volume'])
        

#Assuming tickerDf is your DataFrame and it has columns 'Close' and 'Volume'
# Calculate the percentage change
        Price_Change = tickerDf['Close'].pct_change()

# Multiply the volume by the percentage change
        VPT_Change = tickerDf['Volume'] * Price_Change

# Calculate the cumulative sum of VPT_Change to get the VPT
        vpt = VPT_Change.cumsum()

# Drop the unnecessary columns
        #tickerDf = tickerDf.drop(['Price_Change', 'VPT_Change'], axis=1)
        ax2.plot(vpt, label='VPT', color='purple')
        ax2.set_ylabel('VPT')

ax1.legend()
st.pyplot(fig1)
ax2.legend()
st.pyplot(fig2)