import streamlit as st
import yfinance as yf

st.title('Praktikatzeko')
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

# Create an analytical technique selection menu
analytical_techniques = st.multiselect('Aukeratu teknika bat', ['None', 'SMA20', 'SMA50', 'SMA200', 'EMA26',
    'Bollinger Bands','RSI','MACD'])

# Add a checkbox to clear all analytical technique plots
clear_plots = st.checkbox('Clear all analytical technique plots')
    

import plotly.express as px 
 
 
# Creating the Figure instance
data_guztiak=[]

data_guztiak.append(data_close)
izenak=['Prezioak']
if not clear_plots:
        for technique in analytical_techniques:
            if technique == 'SMA20':
            	sma20 = data_close.rolling(window=20).mean()
            	data_guztiak.append(sma20)
            	izenak.append('SMA20')
            elif technique == 'SMA50':
            	sma50 = data_close.rolling(window=50).mean()
            	data_guztiak.append(sma50)
            	izenak.append('SMA50')
            elif technique == 'SMA200':
            	sma200 = data_close.rolling(window=200).mean()
            	data_guztiak.append(sma200)
            	izenak.append('SMA200')
            elif technique == 'EMA26':
                ema26 = data_close.ewm(span=26, adjust=False).mean()
                data_guztiak.append(ema26)
                izenak.append('EMA26')

#--Figure 1----
# showing the plot
fig = px.line(x=data_close.index,y=data_guztiak,labels={'x':'Egunak'})

for i in range(len(data_guztiak)):
	fig.data[i].name = izenak[i]
#fig.data[0].name = "Prezioak"

st.plotly_chart(fig)



