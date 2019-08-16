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
def formatCSVForLoad(fin_path, fout_path, columnMappings=None):
    with open(fin_path, 'r') as fin, open(fout_path, 'w', newline='\n') as fout:
            # Read in the CSV file
        fin = csv.reader(fin, delimiter=',')

        # Call writable object to write CSV
        fout = csv.writer(fout, delimiter=',')

        # Extract first row in CSV (headers)
        col_names = next(fin)

        # Mofidy headers to make import into DB easier
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
            for i in range(len(row)):
                if row[i] == 'Yes' or row[i] == 'yes':
                    row[i] = True
                elif row[i] == 'No' or row[i] == 'no':
                    row[i] = False

            fout.writerow(row)


def readCSVDictList(fin_path):
    with open(fin_path, 'r') as fin:
        return [dict(row) for row in csv.DictReader(fin)]


# ORM-based functions
def logIntoDatabase(dbLoginCredsPath):
    # dialect+driver://username:password@host:port/db?driver=SQL+Server
    dbLoginCreds = readJson(dbLoginCredsPath)

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


def runMainHelper(tablesPath, csvNoFormatPath, csvFormattedPath, dbCredentialsPath, columnMappingsPath):
    tables = list(readJson(tablesPath).keys())

    result = []
    for table in tables:
        print("Loading data for %s table" % table)
        formatCSVForLoad(
            csvNoFormatPath,
            csvFormattedPath,
            columnMappings=readJson(columnMappingsPath)[table]
        )

        currResult = queryInsertORM(
            tableName=table,
            csvDataPath=csvFormattedPath,
            dbCredentialsPath=dbCredentialsPath,
        )

        currResult = True

        result.append(currResult)

        print("Insert query status: %s\n\n" % currResult)

    return result


def queryGetTableSchema(tablesJsonPath, dbCredentialsPath):
    tables = readJson(tablesJsonPath)
    engine = logIntoDatabase(dbCredentialsPath)
    connection = engine.connect()
    metadata = db.MetaData()

    for tableName in tables:
        table = db.Table(
            tableName,
            metadata,
            autoload=True,
            autoload_with=engine)

        tables[tableName] = table.columns.keys()

    writeJson(tables, tablesJsonPath)


def getUniqueValues(csvDataPath, uniqueCol, colsToRead=None, writeOutPath=None):
    data_in = readCSVDictList(csvDataPath)
    uniqueRows = []
    uniqueKeys = []
    for row in data_in:
        if colsToRead:
            row = {key: row[key] for key in row if key in colsToRead}
        if row[uniqueCol] not in uniqueKeys:
            uniqueKeys.append(row[uniqueCol])
            uniqueRows.append(row)

    if colsToRead:
        fieldnames = colsToRead
    else:
        fieldnames = data_in[0].keys()

    if writeOutPath:
        with open(writeOutPath, 'w', newline='\n') as fout:
            fout = csv.DictWriter(
                fout, fieldnames=fieldnames, delimiter=',')
            fout.writeheader()
            for row in uniqueRows:
                fout.writerow(row)
    print(len(data_in), len(uniqueRows))


def test():
    cols = ["Requester", "Date Created", "Last Updated", ]
    uniqueCol = "Requester"
    getUniqueValues(
        csvDataPath="C:/Users/pum001f/Desktop/DataloaderInfo/BulkData.csv",
        uniqueCol=uniqueCol,
        colsToRead=cols,
        writeOutPath="C:/Users/pum001f/Desktop/testchump.csv"
    )

    csvIn = readCSVDictList("C:/Users/pum001f/Desktop/BulkData.csv")
    refVector = readCSVDictList("C:/Users/pum001f/Desktop/testchump.csv")

    fieldnames = csvIn[0].keys()

    modifyCol = "Last Updated"
    vlookupCol = "Requester"

    for i in range(len(csvIn)):
        row = csvIn[i]
        for ref in refVector:
            if row[vlookupCol] == ref[vlookupCol]:
                row[modifyCol] = ref[modifyCol]
                break
        csvIn[i] = row
