import csv
import sqlite3

connection=sqlite3.connect("pushkar.db")
cursor=connection.cursor()

table_info = """
CREATE TABLE IF NOT EXISTS PUSHKAR(NUM1 INT, NUM2 INT);
"""

cursor.execute(table_info)

with open('placement.csv') as file_obj:
    reader_obj = csv.reader(file_obj)
    
    # print(cursor)
    firstrow=next(reader_obj)
    print(firstrow)

    next(reader_obj)
    for row in reader_obj:
        cursor.execute(r'''INSERT INTO PUSHKAR VALUES ({},{})'''.format(row[0], row[1]))

data = cursor.execute('''SELECT * FROM pushkar''')
for row in data:
    print(row)


connection.commit()
connection.close()

