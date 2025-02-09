
#Import modules
import pandas as pd # Manage CSV-file and database
import sqlite3 # Connect to SQLite-database
import logging # Manage events
import pytest # Not used

# Loggfil
File = "logfile.log"

logging.basicConfig(
    filename=File,
    level=logging.INFO,  
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt='%y-%m-%d %H:%M'  
)


# connecting to database "Salaries_Norway".
try:
    con = sqlite3.connect("Salaries_Norway2.db")
    logging.info("[Success] Your database has been connected") # Send message "Success"
except Exception as e:
    logging.exception("[Error] Database failed to connect") # Send a message "Failed"


# Read CSV-file
try:
    df_oslo = pd.read_csv("salaries.csv", index_col=False)
    df2_Nordland = pd.read_csv("salaries.csv", index_col=False)
    logging.info("[Success] CSV read")
except FileNotFoundError as e:
    logging.error(e)
    logging.error("Can't find CSV")

# Checking if "arbeidssted" exist otherwise raise the problem
df_columns = df_oslo.columns.tolist()
df_columns2 = df2_Nordland.columns.tolist()
if 'arbeidssted' not in df_columns or 'arbeidssted' not in df_columns2:
    logging.error("[Error] Column 'arbeidssted' not found in CSV")
    raise SystemExit("Column 'arbeidssted' not found in CSV")

df_oslo = df_oslo[df_oslo['arbeidssted'].str.contains("Oslo", na=False)]
df2_Nordland = df2_Nordland[df2_Nordland['arbeidssted'].str.contains("Nordland", na=False)]
print(df_oslo.head())
print(df2_Nordland.head())

df_oslo.to_sql('arbeidssted', con, if_exists='append', index=False)
df2_Nordland.to_sql('arbeidssted', con, if_exists='append', index=False)
logging.info('Data saved in database')

con.close()
logging.info ("Connection closed")

