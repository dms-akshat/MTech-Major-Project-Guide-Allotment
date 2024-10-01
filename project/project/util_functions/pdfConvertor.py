import pandas as pd 
import pdfkit 
  
# SAVE CSV TO HTML USING PANDAS 
csv_file = '/home/dms-akshat/DMS/Course/Sem5/IT303/Project/MTech-Major-Project-Guide-Allotment/project/project/util_functions/sample.csv'
html_file = csv_file[:-3]+'html'
  
df = pd.read_csv(csv_file, sep=',') 
df.to_html(html_file) 
  
# INSTALL wkhtmltopdf AND SET PATH IN CONFIGURATION 
# These two Steps could be eliminated By Installing wkhtmltopdf - 
# - and setting it's path to Environment Variables 
path_wkhtmltopdf = r'/usr/local/bin/wkhtmltopdf'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf) 
  
# CONVERT HTML FILE TO PDF WITH PDFKIT 
pdfkit.from_file(html_file, "FinalOutput.pdf", configuration=config) 