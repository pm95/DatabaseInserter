# Author: Pietro Malky
# Purpose: Manipulate Masterlist data prior to importing it to DB
# Date: July 17 2019

import csv
import json

# pip install the following if necessary
import pyodbc

# file and json paths
fin_path = "./DatabasePullTestPlugin.csv"
fout_path = "./DatabasePullTestPlugin_NEW.csv"
header_map_path = "./header_map.json"
table_keys_path = "./table_keys.json"

# load json objects to memory
with open(header_map_path, 'r') as fin:
    modify_headers = json.load(fin)

with open(table_keys_path, 'r') as fin:
    table_keys = json.load(fin)


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


# DB Insertion Steps
with open(fout_path, 'r') as fin:
    fin = csv.DictReader(fin)

    # define keys for each table
    processes_keys = table_keys["processes"]

    # open connection to DB
    connection = pyodbc.connect('Driver={SQL Server};'
                                'Server=chont55862usb;'
                                'Database=controltower;'
                                'UID=uipathadmin;'
                                'PWD=Sql@2017;'
                                )

    cursor = connection.cursor()

    vals = []
    keys = None
    for row in fin:
        data = {key: row[key]
                for key in row if key.lower() in processes_keys}
        keys = list(data.keys())
        values = list(data.values())

        keys = (", ".join(keys)).lower()
        vals.append(("('"+"','".join(values)+"'),").lower())

    vals = ''.join(vals)[:-1]

    query = "INSERT INTO dbo.Processes (%s) VALUES %s;" % (
        keys, vals)

    print(query)

    cursor.execute(query)
    connection.commit()
