# Description: Script for reading files from disk, saving to excel using Pandas Dataframes, then renaming of the files on disk based on the manual update in Excel file of filename mapping.
# Date: 19-09-2020
# Author: Julian Kanjere
# Usage: $python3 16_bulk_file_rename.py


### IMPORT LIBRARIES ###

from os import listdir
from os.path import isfile, join

import pandas as pd
import time
import os
import logging
import sys
import optparse


### DEFINE INITIAL CONSTANTS ###

FILEPATH_CURRENT_DIRECTORY = os.getcwd() # folder of current python script
FILE_SUBMISSION_PREFIX = 'list_of_filenames_'
FILE_EXT_XLSX = '.xlsx'

def setup_logging(options):
    try:
        loglevel = getattr(logging, options.loglevel.upper())
        logging.getLogger().setLevel(loglevel)
    except AttributeError:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.error("Unknown logging level '%s', switching to DEBUG loglevel." % options.loglevel)

def check_arguments(options):
    if options.path == '':
        logging.error('Source directory not supplied. Exiting')
        sys.exit()
    if options.mode == 'rename':
        if options.mapping_file == '':
            logging.error('Mapping not supplied. Exiting')
            sys.exit()

### READ FILE LIST ON DISK AND EXPORT TO EXCEL ###
def read_files(options):
    logging.info('Reading filenames started - ' + options.path + ' ' + options.ext)


    #  save all these variables in a single dataframe
    column_headers = ['Old Name', 'New Name']

    # check filenames:
    if (options.ext==''):
        logging.info('Extension not set, will list all files')
        old_filenames = [f for f in listdir(options.path) if isfile(join(options.path, f))]

    else:
        logging.info('Extension is set, will list all .%s files' % options.ext)
        old_filenames = [f for f in listdir(options.path) if isfile(join(options.path, f)) and  f.endswith(options.ext)]


    filename_data = pd.DataFrame({'Old Name': old_filenames,
                                  'New Name': None,
                              })[column_headers]

    timestr = time.strftime('%Y%m%d-%H%M%S')
    filename = FILE_SUBMISSION_PREFIX + timestr + FILE_EXT_XLSX
    fullfilename = os.path.join(FILEPATH_CURRENT_DIRECTORY, filename)
    logging.info('Excel filename %s' %  fullfilename)
    filename_data.to_excel(fullfilename)
    logging.info('Export to Excel complete')
    logging.info('Reading filenames finished')

### READ FILE LIST FROM EXCEL AND RENAME ON DISK ###
def rename_files(options):
    logging.info('Renaming filenames started - ' + options.path + ' ' + options.ext)
    pass
    #TODO - options.path, options.mapping_file
    #f = ''
    #g = ''
    #if isfile(join(options.path, f)):
    #    os.rename(join(options.path, f), join(options.path, g))
    #print if there are problematic files
    #commit excel file to research repos
    logging.info('Renaming filenames finished')

### DRIVER CODE ###
if __name__ == '__main__':

    args = sys.argv[1:]
    parser = optparse.OptionParser('usage: python3 %prog --path <path> --ext <ext> --filename <mapping_file> --mode <read> --loglevel <loglevel> '
                                   "e.g. python3 %prog --path '/Users/username/ResearchPaper/' --ext ''  --loglevel DEBUG")

    parser.add_option('-p', '--path', dest='path', default='', help='The top level directory to check for files')
    parser.add_option('-e', '--ext', dest='ext', default='', help='The file extension to look for')
    parser.add_option('-f', '--filename', dest='mapping_file', default='', help='The mapping file to look for')
    parser.add_option('-m', '--mode', dest='mode', default='read', help='Program mode. Options are: read, rename')
    parser.add_option('', '--loglevel', type='string', dest='loglevel', default='info',
                      help='Logging level. Options are: notset, debug, info, warn, error, fatal')

    (options, args) = parser.parse_args(args)

    setup_logging(options)

    check_arguments(options)

    if options.mode=='rename':
        rename_files(options)
    elif options.mode=='read':
        read_files(options)


