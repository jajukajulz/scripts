# Description: Sample script for reading excel file using Pandas and saving to a SQL database - SQLite, Postgres, SQL Server, MySQL
# Date: 05-01-2020
# Author: Julian Kanjere
# Usage: $python3 19_excel_to_sql.py
# Requirements: pandas ($pip3 install pandas)

### IMPORT LIBRARIES ###
import pandas as pd
import os
import time
import sys
import optparse

### DEFINE INITIAL CONSTANTS ###
DATABASE_SQLSERVER = 'sqlserver'
DATABASE_SQLITE = 'sqlite'
DATABASE_POSTGRES = 'postgres'
DATABASE_MYSQL = 'mysql'

### DEFINE TABLE AND COLUMN MAP ###
TABLE_MAP = {}
TABLE_MAP['employee'] = ('Name', 'Salary', 'Gender', 'Dept_id')


### SETUP DATABASE CONNECTIONS ###
def setup_db_sql_server():
    """ Setup SQL Server Connection """
    import pyodbc  # driver for SQL Server

    from sqlalchemy import create_engine
    conn_string = ('Driver={ODBC Driver 17 for SQL Server};'
                   'Server=%s;'
                   'Database=%s;'
                   'Trusted_Connection=yes;' % (options.computername, options.dbname))

    print("SQL Server pyodbc connection string %s" % conn_string)

    # conn = pyodbc.connect(conn_string)

    # conn_string = ('Driver={SQL Server};'
    # 'Server=%s;'
    # 'Database=%s;'
    # 'Trusted_Connection=yes;' % (options.computername, options.dbname))

    # engine = sa.create_engine('mssql+pyodbc://user:password@server/database') #SQL Authentication

    sa_conn_string = ('mssql+pyodbc://%s/%s?driver=SQL+Server' % (
    options.computername, options.dbname))  # using Windows Authentication:

    print("SQL Server SQLAlchemy connection string %s" % sa_conn_string)

    conn = create_engine(sa_conn_string)

    if conn:
        return True, conn
    else:
        return False, None


def setup_db_postgres():
    """ Setup Postgres Connection """
    import psycopg2  # driver for postgres

    # connect to the PostgreSQL database
    conn = psycopg2.connect(
        database="mydatabase", user='yourusername', password='yourpassword', host='localhost', port='5432'
    )
    if conn:
        return True, conn
    else:
        return False, None


def setup_db_sqlite():
    """ Setup SQLite Connection. If db file does not exist it will be created """
    import sqlite3  # driver for sqlite

    conn = sqlite3.connect(options.dbname)
    if conn:
        return True, conn
    else:
        return False, None


def setup_db_mysql():
    """ Setup MySQL Connection """
    import mysql.connector  # driver for MySQL

    mydb = mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword",
        database="mydatabase"
    )
    if mydb:
        return True, mydb
    else:
        return False, None


### WRITE TO DATABASE ###
def write_to_db_sqlserver(db_conn, data_list, tablename):
    """ Write to SQL Server DB """
    conn = None
    bool_write = False
    try:
        conn = db_conn
        data_list.columns = TABLE_MAP['employee']

        data_list.to_sql(tablename, conn, if_exists='append', index=False)
        print("Records inserted........")
        bool_write = True
    except (Exception) as error:
        print(error)
    finally:
        read_db_sql_server(conn, tablename)
        return bool_write


def write_to_db_mysql(db_conn, data_list, tablename):
    """ Write to MySQL DB """
    conn = None
    bool_write = False
    table_var_str = tablename
    try:
        conn = db_conn
        mycursor = conn.cursor()
        sql = "INSERT INTO tablename (TABLE_MAP['employee']) VALUES (%s, %s, %s, %s)"

        # execute the INSERT statement
        mycursor.executemany(sql, data_list)
        # Commit changes to database
        mydb.commit()
        print(mycursor.rowcount, "was inserted.")
    except (Exception) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return bool_write


def write_to_db_postgres(db_conn, data_list, tablename):
    """ Write to Postgres DB """
    sql = "INSERT INTO tablename(TABLE_MAP['employee']) VALUES(%s, %s, %s, %s)"
    conn = None
    bool_write = False
    try:
        conn = db_conn
        # create a new cursor object
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql, data_list)
        # commit changes to database
        conn.commit()
        # close communication with the database
        cur.close()
        bool_write = True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return bool_write


def write_to_db_sqlite(db_conn, data_list, tablename):
    """ Write to SQLite """
    conn = None
    bool_write = False
    try:
        conn = db_conn
        data_list.columns = TABLE_MAP['employee']

        data_list.to_sql(tablename, conn, if_exists='append', index=False)
        print("Records inserted........")
        bool_write = True
    except (Exception) as error:
        print(error)
    finally:
        read_db_sqlite(conn, tablename)
        # closing the connection
        if conn is not None:
            conn.close()
        return bool_write


### READ EXCEL OR DATABASES ###
def read_excel_file(filename, sheet_num):
    """ Read Excel file with data """
    # excel_dataframe = pd.read_excel(filename, sheet_name=int(sheet_num), index_col=None, header=None, index=False)
    excel_dataframe = pd.read_excel(filename, sheet_name=int(sheet_num), index_col=None, header=None)
    # drop index column created by pandas
    # excel_dataframe = excel_dataframe.drop(0, 1)
    return excel_dataframe


def read_db_sql_server(db_conn, tablename):
    """ Read data from SQL Server """
    with db_conn.connect() as sql_con:
        rs = sql_con.execute('SELECT * FROM %s' % tablename)

        for row in rs:
            print(row)


def read_db_mysql(db_conn, tablename):
    """ Read data from My SQL """
    conn = db_conn
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM %s' % tablename)


def read_db_postgres(db_conn, tablename):
    """ Read data from Postgres """
    conn = db_conn
    # creating a cursor object using the cursor() method
    cursor = conn.cursor()
    # Retrieving data
    cursor.execute('SELECT * from %s' % tablename)
    # closing the connection
    conn.close()


def read_db_sqlite(db_conn, tablename):
    """ Read data from sqlite """
    conn = db_conn
    # creating a cursor object using the cursor() method
    cursor = conn.cursor()
    # retrieving data
    cursor.execute('SELECT * from %s' % tablename)
    # closing the connection
    conn.close()


### DRIVER CODE ###
if __name__ == '__main__':
    print('Script execution started.')

    args = sys.argv[1:]
    parser = optparse.OptionParser(
        'usage: python3 %prog --database <dbname> --dbtable <tablename> --filename <excel_file> --sheetnumber <excel_sheet_number> --loglevel <loglevel> '
        "e.g. "
        "$python3 %prog --database sqlite --dbname '/Users/johndoe/dev/scripts/scripts/exceldb.db'  --dbtable employee --filename '/Users/johndoe/Downloads/Data1.xlsx' --sheetnumber 1 --loglevel DEBUG")

    parser = optparse.OptionParser()

    parser.add_option("-d", "--database", dest="database", default='sqlite',
                      help="database - sqlserver, mysql, postgres, sqlite}")
    parser.add_option("-c", "--computername", dest="computername", default='',
                      help="computername - COMPUTERNAME\SQLEXPRESS}")
    parser.add_option("-e", "--dbname", dest="dbname", default='sqlite',
                      help="database - sqlserver, mysql, postgres, sqlite}")
    parser.add_option("-t", "--dbtable", dest="dbtable", default='', help="database tablename}")
    parser.add_option('-f', '--filename', dest='source_file', default='',
                      help='The source excel file to look for including path')
    parser.add_option('-s', '--sheetnumber', dest='sheetnumber', default='',
                      help='zero-indexed excel sheet position to import data from')
    parser.add_option('', '--loglevel', type='string', dest='loglevel', default='info',
                      help='Logging level. Options are: notset, debug, info, warn, error, fatal')

    (options, args) = parser.parse_args(args)

    # run validations
    if not options.database:
        parser.error('no database type given e.g. sqlite')

    if options.database == 'sqlserver' and options.computername == '':
        parser.error('no database host (i.e. computername) provided  e.g. COMPUTERNAME\SQLEXPRESS')

    if not options.dbname:
        parser.error('no database name given')

    if not options.dbtable:
        parser.error('no database table given')

    if not options.source_file:
        parser.error('no source excel file given')

    if not options.sheetnumber:
        parser.error('no excel sheet number given')

    # read excel file
    print('Started reading excel sheet %s' % options.source_file)
    excel_dataframe = read_excel_file(options.source_file, options.sheetnumber)
    print('Completed reading excel sheet %s' % options.source_file)
    print('Contents of excel sheet below:')
    print(excel_dataframe)

    # write to database
    if options.database == DATABASE_SQLSERVER:
        print('Attempting to setup DB connection')
        status, conn = setup_db_sql_server()
        if status == True:
            print('DB connection successfully setup')
        if conn:
            bool_write = write_to_db_sqlserver(conn, excel_dataframe, options.dbtable)
            if bool_write:
                read_db_sql_server(conn, options.dbtable)
    elif options.database == DATABASE_MYSQL:
        conn = setup_db_mysql()
        if conn:
            bool_write = write_to_db_mysql(conn, excel_dataframe)
            if bool_write:
                read_db_mysql(conn, options.dbtable)
    elif options.database == DATABASE_POSTGRES:
        status, conn = setup_db_postgres()
        if conn:
            bool_write = write_to_db_postgres(conn, excel_dataframe)
            if bool_write:
                read_db_postgres(conn, options.dbtable)
    elif options.database == DATABASE_SQLITE:
        print('Attempting to setup DB connection')
        status, conn = setup_db_sqlite()
        if status == True:
            print('DB connection successfully setup')
        if conn:
            print('Attempting to write to DB')
            bool_write = write_to_db_sqlite(conn, excel_dataframe, options.dbtable)
            if bool_write:
                print('Attempt to write to DB complete')

    print('Script execution completed.')

