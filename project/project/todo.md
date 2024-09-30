* Replace placeholders in /util_functions/pdfConvertor.py for input file path and output file directory with env variables

Steps to do stuff

    csv to db
        https://www.geeksforgeeks.org/import-a-csv-file-into-an-sqlite-table/
    sqlite3 db.sqlite3
    .mode csv
    .import <csv_path> <table_name>

    db to csv
    
    sqlite3 db.sqlite3
    .mode column
    .mode csv
    .header on
    .output <output file name>
    SQL Query
