import streamlit as st
import yfinance as yf
import pandas as pd
import talib

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
analytical_techniques1 = st.multiselect('Aukeratu teknika bat', ['None', 'SMA20', 'SMA50', 'SMA200', 'EMA26'])

st.write('Subplot-i buruz informazioa hemen:')
st.text('https://plotly.com/python/subplots/')

# Create an analytical technique selection menu
analytical_techniques2 = st.multiselect('Aukeratu teknika bat', ['None',
    'Bollinger Bands','RSI','MACD','Volume', 'VPT', 'ADX'])

# Add a checkbox to clear all analytical technique plots
#clear_plots = st.checkbox('Clear all analytical technique plots')
    
 
# --Figurak --
import plotly.express as px 
from plotly.subplots import make_subplots
import plotly.graph_objects as go

izenburua="S&P baloreak"

fig1 = make_subplots(rows=2, cols=1,
    #subplot_titles=("Prezioak",izena2),
    shared_xaxes=True, vertical_spacing=0.01
    )

# Figure 1: Prezioak
#fig1 = px.line(x=data_close.index,y=data_close,labels={'x':'Egunak'})
#fig.data[0].name = 'Prezioak'
#st.plotly_chart(fig1)

y_min=min(data_close)*(1.-0.8)
y_max=max(data_close)*(1.+0.8)
y_min2=0
y_max2=1

fig1.add_trace(
    go.Scatter(x=data_close.index,y=data_close),
    row=1, col=1)

#if not clear_plots:
for technique in analytical_techniques1:
    if technique == 'SMA20':
    	sma20 = data_close.rolling(window=20).mean()
    	fig1.add_trace(
        go.Scatter(x=data_close.index,y=sma20),
        row=1, col=1
        )
    elif technique == 'SMA50':
        sma50 = data_close.rolling(window=50).mean()
        fig1.add_trace(
        go.Scatter(x=data_close.index,y=sma50),
        row=1, col=1
        )
    elif technique == 'SMA200':
        sma200 = data_close.rolling(window=200).mean()
        fig1.add_trace(
        go.Scatter(x=data_close.index,y=sma200),
        row=1, col=1
        )
    elif technique == 'EMA27':
        ema27 = data_close.ewm(span=27, adjust=False).mean()
        fig1.add_trace(
        go.Scatter(x=data_close.index,y=ema27),
        row=1, col=1
        )


for technique in analytical_techniques2:
    if technique == 'Volume' :
        bolumena = all_data['Volume']
        izenburua="S%P baloreak + bolumena"
        y_min2=0
        y_max2=max(bolumena)*(1.+0.1)
        fig1.add_trace(
        go.Scatter(x=data_close.index,y=bolumena,legendgroup='Bolumena'),
        row=2, col=1
        )
        
    elif technique == 'RSI' :
        izenburua="S%P baloreak + RSI"
        y_min2=0
        y_max2=100
        rsi = talib.RSI(data_close)
        fig1.add_trace(
        go.Scatter(x=data_close.index,y=rsi),
        row=2, col=1
        )
        fig1.add_hline(y=30, line_dash="dot", row=2, col=1, line_color="white", line_width=2)
        fig1.add_hline(y=70, line_dash="dot", row=2, col=1, line_color="white", line_width=2)
    
    elif technique == 'Bollinger Bands':
        # Calculate Bollinger Bands
        rolling_mean = data_close.rolling(window=20).mean()
        rolling_std = data_close.rolling(window=20).std()
        upper_band = rolling_mean + (2 * rolling_std)
        lower_band = rolling_mean - (2 * rolling_std)

        # Plot Bollinger Bands
        fig1.add_trace(
        go.Scatter(x=data_close.index,y=upper_band), color='magenta',
        row=2, col=1
        )
        fig1.add_trace(
        go.Scatter(x=data_close.index,y=lower_band), color='magenta',
        row=2, col=1
        )
                
        #ax.fill_between(upper_band.index, upper_band, lower_band, color='magenta', alpha=0.2)

    elif technique == 'MACD':
        izenburua="S%P baloreak + MACD"
        y_min2=min(data_close)*(1-0.1)
        y_max2=max(data_close)*(1+0.1)
        macd, macdsignal, macdhist = talib.MACD(data_close)
        indicator = pd.DataFrame({'MACD': macd, 'Signal': macdsignal})

        #Plot MACD
        fig1.add_trace(
        go.Scatter(x=data_close.index,y=macd),
        row=2, col=1
        )
        fig1.add_trace(
        go.Scatter(x=data_close.index,y=macdsignal),
        row=2, col=1
        )
        #ax1.fill_between(tickerDf['Close'].index, macdhist, 0, color='black', alpha=0.3)

#--Azkenik, irudiaren ezarpenak aktualizatu 
fig1.update_layout(showlegend=False, title_text=izenburua,legend_tracegroupgap=180)#,yaxis = dict(range=[y_min, y_max]),yaxis2 = dict(range=[y_min2,y_max2]))
fig1.update_layout(yaxis = dict(range=[y_min, y_max]),yaxis2 = dict(range=[y_min2,y_max2]))
fig1.update_layout(height=600, width=800)#, title_text=izenburua,legend_tracegroupgap=180,yaxis = dict(range=[y_min, y_max]),yaxis2 = dict(range=[y_min2,y_max2]))

st.plotly_chart(fig1)









