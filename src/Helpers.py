# Author: Pietro Malky
# Purpose: SST for helper functions to help importer run smoothly
# Date: July 23 2019

import csv
import json
import traceback
import urllib.parse

# pip install the following if necessary
try:
    import pyodbc
except:
    print("MUST INSTALL PYODBC BEFORE CONTINUING")
try:
    import sqlalchemy as db
except:
    print("MUST INSTALL SQL ALCHEMY BEFORE CONTINUING")


# file I/O
def readJson(jsonPath):
    with open(jsonPath, 'r') as jin:
        return json.load(jin)


def writeJson(obj, jsonPath):
    with open(jsonPath, 'w') as jout:
        json.dump(obj, jout)


# Data prep
def formatCSVForLoad(fin_path, fout_path, columnMappings=None, contains_dates=False):
    with open(fin_path, 'r') as fin, open(fout_path, 'w', newline='\n') as fout:
        # Read in the CSV file
        fin = csv.reader(fin, delimiter=',')

        # Call writable object to write CSV
        fout = csv.writer(fout, delimiter=',')

        # Extract first row in CSV (headers)
        col_names = next(fin)

        # Extract the indeces for all columns containing "date" information
        if contains_dates:
            date_cols = [index for (index, col) in enumerate(
                col_names) if "Date" in col or "date" in col]

        # Mofidy headers to make import into DB easier
        if columnMappings:
            for i in range(len(col_names)):
                col = col_names[i]
                if col.lower() in columnMappings:
                    col = columnMappings[col.lower()]
                else:
                    col = col.replace(" ", "")
                    col = col[0].lower() + col[1:]
                col_names[i] = col

        fout.writerow(col_names)

        # Work on rest of data in CSV
        for row in fin:
            if contains_dates:
                for index in date_cols:
                    row[index] = row[index].replace("T00:00:00.00Z", "")
            fout.writerow(row)


def readCSVDictList(fin_path):
    with open(fin_path, 'r') as fin:
        return [dict(row) for row in csv.DictReader(fin)]


# ORM-based functions
def logIntoDatabase(dbLoginCredsPath):
    # dialect+driver://username:password@host:port/db?driver=SQL+Server
    dbLoginCreds = readJson("./config/dbCredentials.json")

    connectionString = 'mssql+pyodbc://%s:%s@%s/%s?driver=SQL+Server' % (
        dbLoginCreds['UID'],
        urllib.parse.quote_plus(dbLoginCreds['PWD']),
        dbLoginCreds['Server'],
        dbLoginCreds['Database']
    )

    try:
        return db.create_engine(connectionString)
    except Exception:
        exception = traceback.format_exc()
        print(exception)
        return exception


def queryInsertORM(tableName, csvDataPath, dbCredentialsPath):
    engine = logIntoDatabase(dbCredentialsPath)
    connection = engine.connect()
    metadata = db.MetaData()

    table = db.Table(
        tableName,
        metadata,
        autoload=True,
        autoload_with=engine,
    )

    values_list = readCSVDictList(csvDataPath)

    try:
        query = db.insert(table)
        connection.execute(query, values_list)
        return True
    except Exception:
        exception = traceback.format_exc()
        print(exception)
        return exception


def queryUpdateORM(tableName, colName, newVal, matchCol, matchVal, dbCredentialsPath):
    engine = logIntoDatabase(dbCredentialsPath)
    connection = engine.connect()
    metadata = db.MetaData()

    table = db.Table(
        tableName,
        metadata,
        autoload=True,
        autoload_with=engine,
    )

    query = db.update(table).where(
        table.columns[matchCol] == matchVal).values({table.columns[colName]: newVal})
    connection.execute(query)


def querySelectWhereORM(tableName, colName, matchCol, matchVal, dbCredentialsPath):
    engine = logIntoDatabase(dbCredentialsPath)
    connection = engine.connect()
    metadata = db.MetaData()

    table = db.Table(
        tableName,
        metadata,
        autoload=True,
        autoload_with=engine,
    )

    query = db.select([table.columns[colName]]).where(
        table.columns[matchCol] == matchVal)

    return connection.execute(query).fetchall()


# testing
def runMainHelper(tablesPath, csvNoFormatPath, csvFormattedPath, dbCredentialsPath, columnMappingsPath):
    tables = list(readJson(tablesPath).keys())
    for table in tables:
        print("Loading data for %s table" % table)
        formatCSVForLoad(
            csvNoFormatPath,
            csvFormattedPath,
            columnMappings=readJson(columnMappingsPath)[table],
            contains_dates=True
        )

        print("Insert query status: %s\n\n" % queryInsertORM(
            tableName=table,
            csvDataPath=csvFormattedPath,
            dbCredentialsPath=dbCredentialsPath,
        ))
    return True

# statusCodes = [x[0] for x in querySelectWhereORM(
#     "statuses",
#     "statusCode",
#     "updatedAt",
#     "2019-05-21",
#     "./config/dbCredentials.json"
# )]

# for x in statusCodes:
#     queryUpdateORM(
#         tableName="requests",
#         colName="overallStatusCode",
#         newVal=x,
#         matchCol="overallStatusCode",
#         matchVal=None,
#         dbCredentialsPath='./config/dbCredentials.json'
#     )
