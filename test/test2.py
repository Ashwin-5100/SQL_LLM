import csv
import sqlite3



import pandas as pd
from sqlalchemy import create_engine

# Path to your CSV file
csv_file = 'test/placement.csv'

# Path to your SQLite database file
db_file = 'data.db'

# Create a SQLAlchemy engine to connect to the SQLite database
engine = create_engine(f'sqlite:///{db_file}')

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file)

# Write the DataFrame to the SQLite database table
df.to_sql('data', engine, if_exists='replace', index=False)

connection=sqlite3.connect(db_file)
cursor=connection.cursor()


query_output = cursor.execute('''SELECT * FROM data where cgpa<6''')
for row in query_output:
    print(row)


connection.commit()
connection.close()

