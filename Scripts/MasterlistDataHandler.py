# Author: Pietro Malky
# Purpose: Manipulate Masterlist data prior to importing it to DB
# Date: July 17 2019

import csv
import json
import traceback

# pip install the following if necessary
try:
    import pyodbc
except:
    print("MUST INSTALL PYODBC BEFORE CONTINUING")


class MasterlistDataLoader:
    def __init__(self, fin_path, header_map_path, table_keys_path, fout_path):
        self.fin_path = fin_path
        self.header_map_path = header_map_path
        self.table_keys_path = table_keys_path
        self.fout_path = fout_path

        self.modify_headers = None
        self.table_keys = None

    def defineModifyHeaders(self):
        with open(self.header_map_path, 'r') as fin:
            self.modify_headers = json.load(fin)

    def defineTableKeys(self):
        with open(self.table_keys_path, 'r') as fin:
            self.table_keys = json.load(fin)

    def formatCSVForLoad(self):
        with open(self.fin_path, 'r') as fin, open(self.fout_path, 'w', newline='\n') as fout:
            print("Imported %s" % self.fin_path)

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
                if col.lower() in self.modify_headers:
                    col = self.modify_headers[col.lower()]
                else:
                    col = col.lower().replace(" ", "")
                col_names[i] = col

            fout.writerow(col_names)

            # Work on rest of data in CSV
            for row in fin:
                for index in date_cols:
                    row[index] = row[index].replace("T00:00:00.00Z", "")
                fout.writerow(row)

            print("\nFinished writing CSV to %s" % self.fout_path)

    def loadBulkDataToDB(self):
         # DB Insertion Steps
        with open(self.fout_path, 'r') as fin, open("./db_credentials.json", 'r') as jin:
            fin = csv.DictReader(fin)

            # define keys for each table
            processes_keys = self.table_keys["processes"]

            # read credentials json
            creds = json.load(jin)
            connectionString = 'Driver={SQL Server};Server=%s;Database=%s;UID=%s;PWD=%s;' % (
                creds['Server'], creds['Database'], creds['UID'], creds['PWD'])

            # open connection to DB
            connection = pyodbc.connect(connectionString)

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

            vals = ''.join(vals)[:-1]  # [:-1] removes trailing comma

            query = "INSERT INTO dbo.Processes (%s) VALUES %s;" % (
                keys, vals)

            try:
                cursor.execute(query)
                connection.commit()
                print("DB data load done")
                return True
            except Exception:
                print(traceback.format_exc())
                return traceback.format_exc()

    def run(self):
        self.defineModifyHeaders()
        self.defineTableKeys()
        self.formatCSVForLoad()
        return self.loadBulkDataToDB()
