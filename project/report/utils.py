import sqlite3
import csv,os
from pathlib import Path
import pandas as pd 
import pdfkit 
import subprocess
from django.conf import settings
from django.core.mail import EmailMessage

def dbToCsv():
    BASE_DIR = settings.BASE_DIR
    db_path = BASE_DIR / 'db.sqlite3'
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Fetch the table data
    query = """
        SELECT guide.name AS guide_name, student.name AS student_name
        FROM algo_allocatedguide AS allocatedguide
        JOIN my_admin_app_student AS student ON allocatedguide.student_id = student.id
        JOIN my_admin_app_guide AS guide ON allocatedguide.guide_id = guide.id
    """

    cursor.execute(query)
    data = cursor.fetchall()

    # Write data to a CSV file
    output_csv = 'final_report.csv'
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write headers
        writer.writerow([description[0] for description in cursor.description])
        # Write data rows
        writer.writerows(data)
    
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
    html_file = os.path.join('pdfs',csv_file[:-3]+'html')    
    df = pd.read_csv(csv_file, sep=',') 
    df.to_html(html_file)
    path_wkhtmltopdf = get_wkhtmltopdf_path()
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf) 
    # CONVERT HTML FILE TO PDF WITH PDFKIT 
    output_file = html_file[:-4]+'pdf'
    pdfkit.from_file(html_file, output_file, configuration=config) 

def dbToPDF(email):
    # Step 1: Convert the database table to a CSV file using the dbToCsv function
    dbToCsv()

    # Step 2: Remove spaces from the CSV (optional, based on your requirements)
    csv_file = 'final_report' + '.csv'
    removeSpaces(csv_file)
    # Step 3: Convert the CSV file to a PDF using the pdfConvertor function
    pdfConvertor(csv_file)
    # Return the name of the generated PDF file
    output_pdf = csv_file[:-3] + 'pdf'
    #send_pdf(email,output_pdf)

def dbToCsvGuide(guide_id):
    BASE_DIR = settings.BASE_DIR
    db_path = BASE_DIR / 'db.sqlite3'
    
    # Check if the database file exists
    if not os.path.exists(db_path):
        print(f"Database file does not exist: {db_path}")
        return
    
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Fetch the table data
        query = """
            SELECT student.name AS student_name
            FROM algo_allocatedguide AS allocatedguide
            JOIN my_admin_app_student AS student ON allocatedguide.student_id = student.id
            JOIN my_admin_app_guide AS guide ON allocatedguide.guide_id = guide.id
            WHERE guide.id = ?
        """

        
        print(f"Executing query: {query} with guide_id: {guide_id}")
        cursor.execute(query, (guide_id,))  # Use parameterized query to prevent SQL injection
        data = cursor.fetchall()

        # Check if any data was fetched
        if not data:
            print(f"No data found for guide_id: {guide_id}")
            return

        # Write data to a CSV file
        output_csv = BASE_DIR / f'final_report_{guide_id}.csv'  # Use full path for the CSV file
        with open(output_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write headers
            writer.writerow([description[0] for description in cursor.description])  # Now this should work
            # Write data rows
            writer.writerows(data)

        print(f"CSV file created successfully: {output_csv}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.commit()
        connection.close()

def dbToPDFGuide(guide_id, email):
    # Step 1: Generate CSV from the database
    dbToCsvGuide(guide_id)
    
    # Step 2: Construct the CSV file name
    csv_file = f'final_report_{guide_id}.csv'
    
    # Step 3: Check if the CSV file is empty
    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        # If not empty, proceed with removing spaces and converting to PDF
        removeSpaces(csv_file)
        
        # Step 4: Convert the CSV file to a PDF using the pdfConvertor function
        pdfConvertor(csv_file)
        
        # Return the name of the generated PDF file
        output_pdf = csv_file[:-3] + 'pdf'
        
        # Send the PDF to the provided email
        #send_pdf(email, output_pdf)
    else:
        # Optionally handle the case when no data is found
        print(f"No data found for guide ID: {guide_id}. PDF generation skipped.")


def send_pdf(email, pdf_name):
    subject = 'PDF'
    email_from = 'softwareproject68@gmail.com'
    recipient_list = [email]
    message = "PDF Sent!"
    pdf_path = Path(settings.BASE_DIR)/'pdfs'/pdf_name
    #print(pdf_name)
    # Create the email object
    emailll = EmailMessage(subject, message, email_from, recipient_list)

    try:
        # Open the PDF file in binary mode
        with open(pdf_path, 'rb') as f:
            # Attach the PDF file to the email
            emailll.attach(pdf_name, f.read(), 'application/pdf')

        # Send email
        emailll.send()
        return "PDF sent successfully!"
    
    except Exception as e:
        return f"Error sending email: {e}"