import csv

def validate_csv_headers(csv_content, expected_headers):
    from io import StringIO
    # Wrap the file and read the first line
    csv_reader = csv.reader(StringIO(csv_content))
    headers = next(csv_reader, None)  # Get the first line as headers
    return headers == expected_headers