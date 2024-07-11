import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import talib

st.title('Matplotlib-ekin sortuta')
st.write('Jarri hasierako eta bukaerako data')

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
selected_sector = st.selectbox('Sektore bat aukeratu', sectors.keys())

# Create a ticket selection menu based on the selected sector
selected_ticker = st.selectbox('Akzioa aukeratu', sectors[selected_sector])


selected_hasi_urtea = st.selectbox('Hasierako urte bat aukeratu', ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022','2023','2024'])
selected_buk_urtea = st.selectbox('Bukaerako urte bat aukeratu', ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022','2023','2024'])

start_date = selected_hasi_urtea +'-01-01'
end_date = selected_buk_urtea + '-12-31'

all_data = yf.download(selected_ticker, start=start_date, end=end_date)

data_close = all_data['Close']
#st.table(all_data)

#--> Figure 1
#fig, (ax1, ax2) = plt.subplots(2, sharex=True)
#fig.suptitle('Baloreak')
#ax1.plot(data_close.index,data_close,label='Close Price')
#ax1.set_xlabel('Data',color='lightgreen')
#ax1.set_ylabel('Prezioa',color='lightgreen')

#for ax in fig.get_axes():
    #ax.label_outer()

fig1, ax1 = plt.subplots()
ax1.plot(data_close, label='Close')
ax1.set_title(f'{selected_ticker} Closing Prices')
ax1.set_xlabel('Date')
ax1.set_ylabel('Price')


# Create an analytical technique selection menu
analytical_techniques1 = st.multiselect('Aukeratu teknika bat', ['None', 'SMA20', 'SMA50', 'SMA200', 'EMA26'])

# Add a checkbox to clear all analytical technique plots
clear_plot1 = st.checkbox('Garbitu grafika')

#hemen esan zer egin aukera bakoitzarekin
if not clear_plot1:
    for technique in analytical_techniques1:
        if technique == 'SMA20':
            sma20 = data_close.rolling(window=20).mean()
            ax1.plot(sma20, label='SMA20', color='red')
        elif technique == 'SMA50':
            sma50 = data_close.rolling(window=50).mean()
            ax1.plot(sma50, label='SMA50', color='green')
        elif technique == 'SMA200':
            sma200 = data_close.rolling(window=200).mean()
            ax1.plot(sma200, label='SMA200', color='blue')
        elif technique == 'EMA27':
            ema27 = data_close.ewm(span=27, adjust=False).mean()
            ax1.plot(ema27, label='EMA27', color='orange')

ax1.legend()
st.plotly_chart(fig1)

#--Figure 2
fig2, ax2 = plt.subplots()
ax2.set_xlabel('Date')
ax2.set_ylabel('Price')

# Create an analytical technique selection menu
analytical_techniques2 = st.multiselect('Aukeratu teknika bat', ['None',
    'Bollinger Bands','RSI','MACD','Volume', 'VPT', 'ADX'])

# Add a checkbox to clear all analytical technique plots
#clear_plots = st.checkbox('Clear all analytical technique plots')


for technique in analytical_techniques2:
    if technique == 'Volume' :
        bolumena = all_data['Volume']
    elif technique == 'RSI':
        rsi = talib.RSI(data_close)
        # Plot RSI
        ax2.set_ylim([0, 100])
        ax2.plot(rsi, label='RSI', color='yellow')
        ax2.set_ylabel('RSI')
        ax2.axhline(y=30, color='r')
        ax2.axhline(y=70, color='white', linestyle='--')
        ax2.legend()

ax2.legend()
st.plotly_chart(fig2)









