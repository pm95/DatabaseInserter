# Author: Pietro Malky
# Purpose: SST for helper functions to help importer run smoothly
# Date: July 23 2019

import csv
import json
import traceback

# pip install the following if necessary
try:
    import pyodbc
except:
    print("MUST INSTALL PYODBC BEFORE CONTINUING")


# file I/O
def readJson(jsonPath):
    with open(jsonPath, 'r') as jin:
        return json.load(jin)


def writeJson(obj, jsonPath):
    with open(jsonPath, 'w') as jout:
        json.dump(obj, jout)


# DB misc
def logIntoDatabase(credentials):
    connectionString = 'Driver={SQL Server};Server=%s;Database=%s;UID=%s;PWD=%s;' % (
        credentials['Server'], credentials['Database'], credentials['UID'], credentials['PWD'])
    connection = pyodbc.connect(connectionString)
    return connection


# Data load
def loadCSVDataToDB(fin_path, tableName, table_keys, dbCredentialsPath):
    with open(fin_path, 'r') as fin:
        fin = csv.DictReader(fin)

        # define keys for each table
        keys = table_keys[tableName]

        # read credentials json
        creds = readJson(dbCredentialsPath)
        connection = logIntoDatabase(creds)

        status = False
        try:
            # generate insertion queries
            queryInsert(connection, fin, tableName, keys)
            print("DB data load done")
            status = True
        except Exception:
            print(traceback.format_exc())
            return traceback.format_exc()
        print(status)
        # send confirmation flag to GUI when done
        return status


# Queries
def queryTableColNames(connection, tableName):
    query = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'%s';" % tableName
    cursor = connection.cursor().execute(query)
    return [row[0].lower() for row in cursor]


def queryInsert(connection, obj, tableName, tableKeys):
    vals = []
    keys = None
    for row in obj:
        data = {key: row[key]
                for key in row if key.lower() in tableKeys}
        keys = list(data.keys())
        values = list(data.values())

        keys = (", ".join(keys)).lower()
        vals.append(("('"+"','".join(values)+"'),").lower())

    vals = ''.join(vals)[:-1]  # [:-1] removes trailing comma

    query = "INSERT INTO %s (%s) VALUES %s;" % (tableName,
                                                keys, vals)
    connection.cursor().execute(query)
    connection.commit()


def queryDeleteRowsConditional(connection, tableName, condition):
    query = "DELETE FROM %s WHERE (%s);" % (tableName, condition)
    connection.cursor().execute(query)
    connection.commit()


# Data prep
def formatCSVForLoad(fin_path, fout_path, columnMappings=None, contains_dates=False):
    with open(fin_path, 'r') as fin, open(fout_path, 'w', newline='\n') as fout:
        print("Imported %s" % fin_path)

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
                    col = col.lower().replace(" ", "")
                col_names[i] = col

        fout.writerow(col_names)

        # Work on rest of data in CSV
        for row in fin:
            if contains_dates:
                for index in date_cols:
                    row[index] = row[index].replace("T00:00:00.00Z", "")
            fout.writerow(row)

        print("\nFinished writing CSV to %s" % fout_path)
