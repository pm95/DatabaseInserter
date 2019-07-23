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


def readJson(jsonPath):
    with open(jsonPath, 'r') as jin:
        return json.load(jin)


def writeJson(obj, jsonPath):
    with open(jsonPath, 'w') as jout:
        json.dump(obj, jout)


def queryTableColNames(connection, tableName):
    query = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'%s';" % tableName
    cursor = connection.cursor().execute(query)
    return [row[0] for row in cursor]


def logIntoDatabase(credentials):
    connectionString = 'Driver={SQL Server};Server=%s;Database=%s;UID=%s;PWD=%s;' % (
        credentials['Server'], credentials['Database'], credentials['UID'], credentials['PWD'])
    connection = pyodbc.connect(connectionString)
    return connection


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


def formatCSVForLoad(fin_path, fout_path, modify_headers):
    with open(fin_path, 'r') as fin, open(fout_path, 'w', newline='\n') as fout:
        print("Imported %s" % fin_path)

        # Read in the CSV file
        fin = csv.reader(fin, delimiter=',')

        # Call writable object to write CSV
        fout = csv.writer(fout, delimiter=',')

        # Extract first row in CSV (headers)
        col_names = next(fin)

        # Extract the indeces for all columns containing "date" information
        date_cols = [index for (index, col) in enumerate(
            col_names) if "Date" in col or "date" in col]

        # Mofidy headers to make import into DB easier
        for i in range(len(col_names)):
            col = col_names[i]
            if col.lower() in modify_headers:
                col = modify_headers[col.lower()]
            else:
                col = col.lower().replace(" ", "")
            col_names[i] = col

        fout.writerow(col_names)

        # Work on rest of data in CSV
        for row in fin:
            for index in date_cols:
                row[index] = row[index].replace("T00:00:00.00Z", "")
            fout.writerow(row)

        print("\nFinished writing CSV to %s" % fout_path)
