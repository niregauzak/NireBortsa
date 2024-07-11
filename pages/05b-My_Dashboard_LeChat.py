import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import talib

# Add a title to the app
st.title('S&P500 Stocks')

# Define the sectors and their corresponding main tickets
sectors = {
    'Technology': ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'FB', 'NVDA', 'CSCO', 'ORCL', 'INTC', 'TSM'],
    'Finance': ['JPM', 'V', 'MA', 'C', 'BAC', 'WFC', 'AXP', 'BLK', 'CME', 'GS'],
    'Health Care': ['JNJ', 'PFE', 'ABT', 'MRK', 'AMGN', 'UNH', 'ABBV', 'MDT', 'DHR', 'ISRG'],
    'Consumer Discretionary': ['AMZN', 'HD', 'DIS', 'NKE', 'MCD', 'VZ', 'TSLA', 'PG', 'COST', 'KO'],
    'Communication Services': ['GOOGL', 'FB', 'T', 'VZ', 'DIS', 'NFLX', 'CSCO', 'TXN', 'INTC', 'AMD'],
    'Industrials': ['BA', 'CAT', 'HON', 'GE', 'DE', 'UNP', 'GD', 'RTX', 'MMM', 'CSX'],
    'Consumer Staples': ['PG', 'KO', 'PEP', 'WMT', 'COST', 'CVS', 'MO', 'PM', 'K', 'CL'],
    'Energy': ['XOM', 'CVX', 'SLB', 'COP', 'EOG', 'OXY', 'APA', 'MPC', 'DVN', 'VLO'],
    'Utilities': ['DUK', 'NEE', 'SO', 'AEP', 'EXC', 'D', 'ES', 'FE', 'XEL', 'PCG'],
    'Real Estate': ['AMT', 'PLD', 'EQR', 'SPG', 'VNO', 'DLR', 'WELL', 'BXP', 'PEAK', 'ARE'],
    'Materials': ['DOW', 'LIN', 'AIR', 'PPG', 'FCX', 'NUE', 'APD', 'DD', 'EMN', 'WRK'],
}

# Create a sector selection menu
selected_sector = st.selectbox('Select a sector', sectors.keys())

# Create a ticket selection menu based on the selected sector
selected_ticker = st.selectbox('Select a ticket', sectors[selected_sector])

##===================
##FUNCIONS
##===================


##===================
##END FUNCIONS
##===================

# Get data on the selected ticket
tickerData = yf.Ticker(selected_ticker)

# Create a time period selection menu
time_period = st.selectbox('Select time period', ['1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'max'])

# Get the historical prices for this ticket
tickerDf = tickerData.history(period=time_period)

# Create a data presentation mode selection menu
data_presentation_mode = st.selectbox('Select data presentation mode', ['Plot','Table'])

# Create an analytical technique selection menu
analytical_techniques = st.multiselect('Select analytical techniques', ['None', 'SMA20', 'SMA50', 'SMA200', 'EMA27',
    'Bollinger Bands','VWAP','RSI','MACD','Volume', 'VPT', 'ADX'])

# Add a checkbox to clear all analytical technique plots
clear_plots = st.checkbox('Clear all analytical technique plots')

if data_presentation_mode == 'Table':
    # Display the data as a table
    st.table(tickerDf)
else:
    # Plot the closing prices
    fig, ax = plt.subplots()
    ax.plot(tickerDf['Close'], label='Close')
    ax.set_title(f'{selected_ticker} Closing Prices')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')

    # Calculate and plot the selected analytical techniques
    if not clear_plots:
        for technique in analytical_techniques:
            if technique == 'SMA20':
                sma20 = tickerDf['Close'].rolling(window=20).mean()
                ax.plot(sma20, label='SMA20', color='red')
            elif technique == 'SMA50':
                sma50 = tickerDf['Close'].rolling(window=50).mean()
                ax.plot(sma50, label='SMA50', color='green')
            elif technique == 'SMA200':
                sma200 = tickerDf['Close'].rolling(window=200).mean()
                ax.plot(sma200, label='SMA200', color='blue')
            elif technique == 'EMA27':
                ema27 = tickerDf['Close'].ewm(span=27, adjust=False).mean()
                ax.plot(ema27, label='EMA27', color='orange')
            elif technique == 'Bollinger Bands':
                # Calculate Bollinger Bands
                rolling_mean = tickerDf['Close'].rolling(window=20).mean()
                rolling_std = tickerDf['Close'].rolling(window=20).std()
                upper_band = rolling_mean + (2 * rolling_std)
                lower_band = rolling_mean - (2 * rolling_std)

                # Plot Bollinger Bands
                ax.plot(upper_band, label='Upper Band', color='magenta', linestyle='--')
                ax.plot(lower_band, label='Lower Band', color='magenta', linestyle='--')
                ax.fill_between(upper_band.index, upper_band, lower_band, color='magenta', alpha=0.2)
            elif technique == 'VWAP':
                # Calculate VWAP
                vwap = (tickerDf['Volume'] * tickerDf['Close']).cumsum() / tickerDf['Volume'].cumsum()

                # Plot VWAP
                ax1 = ax.twinx()
                ax1.plot(vwap, label='VWAP', color='cyan')
                ax1.set_ylabel('VWAP')
            elif technique == 'RSI':
                rsi = talib.RSI(tickerDf['Close'])
                # Plot RSI
                ax1 = ax.twinx()
                ax1.axhline(y=30, color='red', linestyle='--')
                ax1.axhline(y=70, color='green', linestyle='--')
                ax1.set_ylim([0, 100])
                ax1.plot(rsi, label='RSI', color='darkred')
                ax1.set_ylabel('RSI')
                ax1.legend()
            elif technique == 'MACD':
                macd, macdsignal, macdhist = talib.MACD(tickerDf['Close'])
                indicator = pd.DataFrame({'MACD': macd, 'Signal': macdsignal})

                #macd, macdsignal, macdhist = talib.MACD(tickerDf['Close'], fastperiod=tickerDf[indicator]['fastperiod'], slowperiod=indicators[indicator]['slowperiod'], signalperiod=indicators[indicator]['signalperiod'])
                ax1 = ax.twinx()
                ax1.plot(tickerDf['Close'].index, macd, color='blue', label='MACD')
                ax1.plot(tickerDf['Close'].index, macdsignal, color='orange', label='Signal')
                ax1.fill_between(tickerDf['Close'].index, macdhist, 0, color='black', alpha=0.3)
                ax1.legend()
            elif technique == 'Volume' :
                bolumena = tickerDf['Volume']
                ax.plot(bolumena, label='bolumena', color='red')

            elif technique == 'VPT' :
                continue

            elif technique == 'ADX' :
                continue



    ax.legend()
    st.pyplot(fig)