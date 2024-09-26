import sqlite3
import csv

connection = sqlite3.connect("db.sqlite3")
cursor = connection.cursor()

# Fetch the table data
cursor.execute("SELECT * FROM preferences")
data = cursor.fetchall()

# Write data to a CSV file
with open('spreadsheet.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([description[0] for description in cursor.description])  # Write headers
    writer.writerows(data)  # Write data rows

connection.commit()
connection.close()
