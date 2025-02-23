import pyodbc


conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=master;Trusted_Connection=yes;'
try:
    conn = pyodbc.connect(conn_str)
    print("Connection successful!")
except Exception as e:
    print("Error:", e)

try:
    with pyodbc.connect(conn_str) as conn:
        print("Connection successful!")
except Exception as e:
    print("Error:", e)



from sqlalchemy import create_engine
from sqlalchemy.engine import reflection

import urllib
params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=master;Trusted_Connection=yes")
# Proper SQLAlchemy connection string using pyodbc
conn_str = f"mssql+pyodbc:///?odbc_connect={params}"

# Create an engine that the Session will use for connection resources
engine = create_engine(conn_str)

# Create an inspector object to explore the database
inspector = reflection.Inspector.from_engine(engine)

# Retrieve the list of all table names in the default schema
tables = inspector.get_table_names()
print("List of tables:")
for table in tables:
    print(table)


params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=master;Trusted_Connection=yes")
# Define SQLAlchemy connection string
SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
import yfinance as yf
def fetch_and_store_stock_data(symbols):
    for symbol in symbols:
        # Fetch stock data from yfinance
        data = yf.download(symbol, period="1d")
        # Store data in SQL Server
        data.reset_index(inplace=True)
        print(data)