import subprocess # Import subprocess module
import os # We will use the exists() function from this module to know if the file was created.
def convert_file_to_pdf(file_path, output_dir):
    subprocess.run(
        f'/usr/bin/libreoffice \
        --headless \
        --convert-to pdf \
        --outdir {output_dir} {file_path}', shell=True)
    
    pdf_file_path = f'{output_dir}{file_path.rsplit("/", 1)[1].split(".")[0]}.pdf'
    
    if os.path.exists(pdf_file_path):
        return pdf_file_path
    else:
        return None
    
file_path = 'spreadsheet.csv'
output_dir = '.'
file = convert_file_to_pdf(file_path, output_dir)
if file:
    print(f'File converted to {file}.')
else:
    print('Unable to convert the file.')