# Create a new virtual environment
python -m venv "D:\Qriocity\Apache Superset\.venv"

# Activate the new environment
"D:\Qriocity\Apache Superset\.venv\Scripts\activate"

# Install Superset
pip install apache-superset

# Initialize the database
superset db upgrade
superset fab create-admin
superset init

$env:FLASK_APP = "superset"

$env:SUPERSET_CONFIG_PATH = "D:\Qriocity\Apache Superset\superset_config.py"


superset db init
superset db upgrade
SQLALCHEMY_DATABASE_URI = 'sqlite:///D:\\Qriocity\\Apache Superset\\stock_data.db'

SQLALCHEMY_DATABASE_URI = r'mssql+pyodbc://@localhost/master?driver=ODBC Driver 17 for SQL Server;Trusted_Connection=yes;'



CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);


ERROR [flask_migrate] Error: Online migration expected to match one row when updating 'bb51420eaf83' to 'b4456560d4f3' in 'alembic_version'; 0 found

insert_query = "INSERT INTO alembic_version (version_num) VALUES ('bb51420eaf83');"


git clone https://github.com/coleifer/peewee.git
cd peewee
python setup.py install

ALTER TABLE stock_data
ADD Dividend FLOAT;

ALTER TABLE stock_data
ADD EPS FLOAT;

ALTER TABLE stock_data
ADD [PE Ratio] FLOAT;

ALTER TABLE stock_data
ADD Beta FLOAT;

ALTER TABLE stock_data
ADD [Adjusted Close] FLOAT;

ALTER TABLE stock_data
ADD [Daily Price Range] FLOAT,
    [Daily Price Change] FLOAT,
    [Daily Price Change Percentage] FLOAT,
    [Total Dollar Volume] FLOAT,
    [Volume Weighted Average Price (VWAP)] FLOAT,
    [Price Range Percentage] FLOAT,
    [Daily Return] FLOAT,
    [50-day SMA] FLOAT,
    [200-day SMA] FLOAT,
    [12-day EMA] FLOAT,
    [26-day EMA] FLOAT,
    [MACD Line] FLOAT,
    [9-day EMA of MACD] FLOAT,
    [MACD Histogram] FLOAT,
    [Volatility] FLOAT;

