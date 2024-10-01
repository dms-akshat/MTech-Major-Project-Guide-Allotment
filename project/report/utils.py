import sqlite3
import csv
from pathlib import Path

def dbToCsv(table_name):
    BASE_DIR = Path(__file__).resolve().parent.parent
    db_path = BASE_DIR / 'db.sqlite3'
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    # Fetch the table data
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    # Write data to a CSV file
    output_csv = table_name + '.csv'
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([description[0] for description in cursor.description])  # Write headers
        writer.writerows(data)  # Write data rows
    connection.commit()
    connection.close()

def removeSpaces(input_file):
    delim = ","
    with open(input_file, "r") as file:
        lines = [map(str.strip, line.split(delim)) for line in file]
    with open(input_file, "w") as file:
        for line in lines:
            file.write(",".join(line)+"\n")