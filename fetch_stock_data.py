import yfinance as yf
from sqlalchemy import create_engine, select, Table, MetaData
import pandas as pd
import urllib
import time

params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=master;Trusted_Connection=yes")
# Define SQLAlchemy connection string
SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
metadata = MetaData(bind=engine)
stock_data_table = Table('stock_data', metadata, autoload=True, autoload_with=engine)

def check_and_append_data(data, engine):
    with engine.connect() as conn:
        for index, row in data.iterrows():
            # Check if the record exists
            stmt = select([stock_data_table]).where(stock_data_table.c.Date == row['Date']).where(stock_data_table.c.Symbol == row['Symbol'])
            result = conn.execute(stmt).fetchall()
            if not result:
                # Record does not exist, insert new record
                row_df = pd.DataFrame([row])
                row_df.to_sql('stock_data', con=engine, if_exists='append', index=False)

def calculate_RSI(data, periods = 14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    RS = gain / loss
    return 100 - (100 / (1 + RS))

def fetch_financials(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    return {
        'Dividend': info.get('dividendRate', 0),
        'EPS': info.get('trailingEps', 0),
        'PE Ratio': info.get('trailingPE', 0),
        'Beta': info.get('beta', 0)
    }

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
def calculate_additional_metrics(data, symbol):
    # Basic calculations
    data['Daily Price Range'] = data['High'] - data['Low']
    data['Daily Price Change'] = data['Close'] - data['Open']
    data['Daily Price Change Percentage'] = (data['Daily Price Change'] / data['Open']) * 100
    data['Total Dollar Volume'] = data['Volume'] * data['Close']
    data['Volume Weighted Average Price (VWAP)'] = data['Total Dollar Volume'] / data['Volume']
    data['Price Range Percentage'] = ((data['High'] - data['Low']) / data['Open']) * 100
    data['Daily Return'] = data['Close'].pct_change()
    financials = fetch_financials(symbol)
    data['Dividend'] = financials['Dividend']
    data['EPS'] = financials['EPS']
    data['PE Ratio'] = financials['PE Ratio']
    data['Beta'] = financials['Beta']
    data['Adjusted Close'] = data['Adj Close']

    # Moving Averages and other complex metrics
    data['50-day SMA'] = data['Close'].rolling(window=50).mean()
    data['200-day SMA'] = data['Close'].rolling(window=200).mean()
    # EMA calculations (with smoothing factor)
    smoothing_factor_12 = 2 / (12 + 1)
    smoothing_factor_26 = 2 / (26 + 1)
    data['12-day EMA'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['26-day EMA'] = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD Line'] = data['12-day EMA'] - data['26-day EMA']
    data['9-day EMA of MACD'] = data['MACD Line'].ewm(span=9, adjust=False).mean()
    data['MACD Histogram'] = data['MACD Line'] - data['9-day EMA of MACD']

    # Volatility and RSI (placeholders for actual calculations which require more detailed time-series data)
    data['Volatility'] = data['Daily Return'].rolling(window=30).std()
    data['RSI'] = calculate_RSI(data)
    # Placeholder for RSI (real calculation requires more complex logic)
    return data

def fetch_and_store_stock_data(symbols):
    for symbol in symbols:
        data = yf.download(symbol, period="5mo", interval="1d")
        data.reset_index(inplace=True)
        data = calculate_additional_metrics(data, symbol)
        data['Symbol'] = symbol
        check_and_append_data(data, engine)
        print(f"Data stored for {symbol}")

# Define list of company symbols
symbols = ["ACN", "AAPL", "CTSH", "IBM", "INFY"]

interval_hours = 1  

while True:
    fetch_and_store_stock_data(symbols)
    print(f"Waiting {interval_hours} hour(s) to fetch data again...")
    time.sleep(interval_hours * 3600)