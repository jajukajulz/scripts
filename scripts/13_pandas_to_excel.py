# Description: Sample script for saving to excel using Pandas Dataframes
# Date: 01-05-2020
# Author: Julian Kanjere
# Usage: $python3 13_pandas_to_excel.py
# Requirements: pandas ($pip3 install pandas), openpyxl ($pip3 install openpyxl)


### IMPORT LIBRARIES ###

import pandas as pd
import os
import time

### DEFINE INITIAL CONSTANTS ###

FILEPATH_CURRENT_DIRECTORY = os.getcwd() # folder of current python script
FILE_SUBMISSION_PREFIX = 'pandas_to_excel_'
FILE_EXT_XLSX = '.xlsx'



### EXPORT TO EXCEL ###

# setting up the lists that will form our dataframe with all the results
country = ['South Africa', 'Namibia', 'Zimbabwe']
capital_city = ['Pretoria', 'Windhoek', 'Harare']
calling_code = ['+27','+264', '+263']

#  save all these variables in a single dataframe
column_headers = ['Country', 'Capital City', 'Calling Code']



country_data = pd.DataFrame({'Country': country,
                          'Capital City': capital_city,
                          'Calling Code': calling_code
                          })[column_headers]

timestr = time.strftime("%Y%m%d-%H%M%S")
filename = FILE_SUBMISSION_PREFIX + timestr + FILE_EXT_XLSX
fullfilename = os.path.join(FILEPATH_CURRENT_DIRECTORY, filename)

country_data.to_excel(fullfilename)
print('Export to Excel complete')