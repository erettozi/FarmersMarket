#
# Tool to export CSV data from farmers markets to database
#
# @Author: Erick Rettozi

import sys
from CSV2DB import CSV2DB

#
# @Main
# Run Application
app = CSV2DB(sys.argv)
if(app.run() is True):
    print('The CSV file was successfully exported to database')
else:
    print('ERROR when exporting the CSV file to the database')
app.destroy()
