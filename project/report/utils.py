import sqlite3
import csv
from pathlib import Path
import pandas as pd 
import pdfkit 
import subprocess

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

def get_wkhtmltopdf_path():
    try:
        # Run the `which wkhtmltopdf` command
        result = subprocess.run(['which', 'wkhtmltopdf'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Check if the command found the executable
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()  # Return the path of wkhtmltopdf
        else:
            return None  # wkhtmltopdf is not installed or not found in PATH
    except Exception as e:
        return f"Error occurred: {e}"

def pdfConvertor(input_file):       #put input file path as input_file
    # SAVE CSV TO HTML USING PANDAS 
    csv_file = input_file
    html_file = csv_file[:-3]+'html'    
    df = pd.read_csv(csv_file, sep=',') 
    df.to_html(html_file)
    path_wkhtmltopdf = get_wkhtmltopdf_path()
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf) 
    # CONVERT HTML FILE TO PDF WITH PDFKIT 
    output_file = csv_file[:-3]+'pdf'
    pdfkit.from_file(html_file, output_file, configuration=config) 

def dbToPDF(table_name):
    # Step 1: Convert the database table to a CSV file using the dbToCsv function
    dbToCsv(table_name)
    # Step 2: Remove spaces from the CSV (optional, based on your requirements)
    csv_file = table_name + '.csv'
    removeSpaces(csv_file)
    # Step 3: Convert the CSV file to a PDF using the pdfConvertor function
    pdfConvertor(csv_file)
    # Return the name of the generated PDF file
    output_pdf = csv_file[:-3] + 'pdf'
    return output_pdf