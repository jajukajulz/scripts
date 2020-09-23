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
import shutil


### DEFINE INITIAL CONSTANTS ###

FILEPATH_CURRENT_DIRECTORY = os.getcwd() # folder of current python script
FILE_SUBMISSION_PREFIX = 'list_of_filenames_'
FILE_EXT_XLSX = '.xlsx'
EXCEL_SHEET_NAME = 'FilenameSheet'
COLUMN_HEADERS = ['Old Name', 'New Name', 'LastName1', 'LastName2', 'YYYY', 'ShortTitle', 'Journal']
FILES_TO_IGNORE = ['.DS_Store'] #ignore list
BACKUP_SUFFIX = '_backup'
TIMESTR = time.strftime('%Y%m%d-%H%M%S')
#FORMAT = 'LastName1LastName2_YYYY_ShortTitle-Journal.pdf' e.g. gansscottstern_2018_entrepreneurialstrategy-hbr

### SETUP LOGGING ###
def setup_logging(options):
    try:
        loglevel = getattr(logging, options.loglevel.upper())
        logging.getLogger().setLevel(loglevel)
    except AttributeError:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.error("Unknown logging level '%s', switching to DEBUG loglevel." % options.loglevel)

### CONFIRM ARGUMENTS ARE SET CORRECTLY ###
def check_arguments(options):
    if options.path == '':
        logging.error('Source directory not supplied. Exiting')
        sys.exit()
    if not os.path.isdir(options.path):
        logging.error('Source directory (%s) does not exist or is invalid. Exiting' % options.path)
        sys.exit()
    if options.mode == 'rename':
        if options.mapping_file == '':
            logging.error('Mapping not supplied. Exiting')
            sys.exit()

### BACKUP FOLDER BEFORE RENAMING ###
def backup_folder(options):
    logging.info('Backing up folder (%s) before renaming files.' % options.path)
    bool_success = True
    # Split the path in head and tail pair
    head_tail = os.path.split(options.path)
    backup_path = os.path.abspath(os.path.join(options.path,"../"))
    backup_name = head_tail[1] + BACKUP_SUFFIX + "_" + TIMESTR
    backup_location = os.path.join(backup_path, backup_name)
    logging.info('Backup location %s ' % backup_location)
    try:
        shutil.copytree(options.path, backup_location)
        logging.info('Backing up folder (%s) successful.' % options.path)
        return bool_success
    except:
        logging.error("An exception occurred")
        return not bool_success

### READ FILE LIST ON DISK AND EXPORT TO EXCEL ###
def read_files(options):
    logging.info('Reading filenames started - ' + options.path + ' ' + options.ext)

    # check filenames:
    if (options.ext==''):
        logging.info('Extension not set, will list all files')
        old_filenames = [f for f in listdir(options.path) if isfile(join(options.path, f)) and f not in FILES_TO_IGNORE]
    else:
        logging.info('Extension is set, will list all .%s files' % options.ext)
        old_filenames = [f for f in listdir(options.path) if isfile(join(options.path, f)) and f.endswith(options.ext)
                         and f not in FILES_TO_IGNORE]

    # sort the filenames in ascending order
    old_filenames.sort()

    # convert to lowercase
    old_filenames = [x.lower() for x in old_filenames]

    # suggested list of filenames - replace blanks with underscore and split once on dot.
    suggested_filenames = [x.replace(" ", "_").rsplit('.', 1)[0] for x in old_filenames]

    filename_data = pd.DataFrame({COLUMN_HEADERS[0]: old_filenames,
                                  COLUMN_HEADERS[1]: '',
                                  COLUMN_HEADERS[2]: '',
                                  COLUMN_HEADERS[3]: '',
                                  COLUMN_HEADERS[4]: '',
                                  COLUMN_HEADERS[5]: suggested_filenames,
                                  COLUMN_HEADERS[6]: '',
                              })[COLUMN_HEADERS]


    filename = FILE_SUBMISSION_PREFIX + TIMESTR + FILE_EXT_XLSX
    fullfilename = os.path.join(FILEPATH_CURRENT_DIRECTORY, filename)
    logging.info('Excel filename %s' %  fullfilename)
    filename_data.to_excel(fullfilename, sheet_name=EXCEL_SHEET_NAME)
    logging.info('Export to Excel complete')
    logging.info('Reading filenames finished')

### READ FILE LIST FROM EXCEL AND RENAME ON DISK ###
def rename_files(options):
    logging.info('Renaming filenames initialising - ' + options.path + ' ' + options.mapping_file)
    full_filename = join(options.path, options.mapping_file)
    if isfile(full_filename):

        excel_data_df = pd.read_excel(full_filename, sheet_name=EXCEL_SHEET_NAME)

        # print whole sheet data
        logging.debug('Excel data below:')
        logging.debug(excel_data_df)

        # list of column names in Excel
        excel_data_df_columns = excel_data_df.columns.ravel()
        logging.debug('Excel data columns below:')
        logging.debug(excel_data_df_columns)

        # original filenames
        excel_data_df_orig_filenames = excel_data_df[COLUMN_HEADERS[0]].tolist()
        logging.debug('List of old filenames %s' % excel_data_df_orig_filenames)

        # new filenames
        excel_data_df_new_filenames = excel_data_df[COLUMN_HEADERS[1]].tolist()
        logging.debug('List of new filenames %s' % excel_data_df_new_filenames)

       # sanity check - column lengths
        len_excel_data_df_orig_filenames = len(excel_data_df_orig_filenames)
        len_excel_data_df_new_filenames = len(excel_data_df_new_filenames)

        logging.info('# of old filenames %s' % len_excel_data_df_orig_filenames)
        logging.info('# of new filenames %s' % len_excel_data_df_new_filenames)

        if len_excel_data_df_new_filenames != len_excel_data_df_orig_filenames:
            logging.error('Number of new filenames (%s) does not match number of old filenames (%s). Exiting' %
                          (len_excel_data_df_new_filenames, len_excel_data_df_orig_filenames))
            sys.exit()

        # sanity check - null values
        if excel_data_df[COLUMN_HEADERS[1]].isnull().values.any():
            logging.error('The new filenames contain some null values (%s entries). Exiting' %
                          (excel_data_df[COLUMN_HEADERS[1]].isnull().sum()))
            sys.exit()

        # backup folder before renaming files
        backup_status = backup_folder(options)

        if backup_status:
            logging.info('Renaming filenames starting - ' + options.path + ' ' + options.mapping_file)

            for count, new_name_entry in enumerate(excel_data_df_new_filenames):
                old_name_entry = excel_data_df_orig_filenames[count]
                old_name_fullpath = join(options.path, old_name_entry)
                if isfile(old_name_fullpath):
                    os.rename(old_name_fullpath, join(options.path, new_name_entry))
                else:
                    logging.info('Skipping %s as it is not a valid file' % old_name_fullpath)
            logging.info('Renaming filenames finished')
        else:
            logging.info('Backup was unsuccessful. Exiting')
    else:
        logging.error('Invalid file or file does not exist - %s. Exiting' % full_filename)
        sys.exit()

### DRIVER CODE ###
if __name__ == '__main__':
    args = sys.argv[1:]
    parser = optparse.OptionParser('usage: python3 %prog --path <path> --ext <ext> --filename <mapping_file> --mode <read> --loglevel <loglevel> '
                                   "e.g. "
                                   "read $python3 %prog --path '/Users/username/ResearchPaper/' --ext '' --mode 'read' --loglevel DEBUG"
                                   "rename $python3 %prog --path '/Users/username/ResearchPapers1' --ext '' --filename '/Users/username/list_of_filenames_20200922-221324.xlsx' --mode 'rename' --loglevel DEBUG")

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

    logging.info('File Operations complete. Goodbye')
    sys.exit()


