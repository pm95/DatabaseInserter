# Author: Pietro Malky
# Purpose: Manipulate Masterlist data prior to importing it to DB
# Date: July 17 2019

import csv
import json
import traceback

import Helpers

# pip install the following if necessary
try:
    import pyodbc
except:
    print("MUST INSTALL PYODBC BEFORE CONTINUING")


class MasterlistDataLoader:
    def __init__(self, fin_path, fout_path, header_map_path, table_keys_path, dbCredentialsPath):
        self.fin_path = fin_path
        self.header_map_path = header_map_path
        self.table_keys_path = table_keys_path
        self.fout_path = fout_path

        self.modify_headers = None
        self.table_keys = None

        self.dbCredentialsPath = dbCredentialsPath

    def defineModifyHeaders(self):
        self.modify_headers = Helpers.readJson(self.header_map_path)

    def defineTableKeys(self):
        self.table_keys = Helpers.readJson(self.table_keys_path)

    def formatCSVForLoad(self):
        Helpers.formatCSVForLoad(
            self.fin_path,
            self.fout_path,
            self.modify_headers
        )

    def loadBulkDataToDB(self, tableName):
         # DB Insertion Steps
        with open(self.fout_path, 'r') as fin:
            fin = csv.DictReader(fin)

            # define keys for each table
            processes_keys = self.table_keys[tableName]

            # read credentials json
            creds = Helpers.readJson(self.dbCredentialsPath)
            connection = Helpers.logIntoDatabase(creds)

            status = False
            try:
                # generate insertion queries
                Helpers.queryInsert(
                    connection, fin, tableName, processes_keys)
                print("DB data load done")
                status = True
            except Exception:
                print(traceback.format_exc())
                return traceback.format_exc()

            # send confirmation flag to GUI when done
            return status

    def run(self):
        self.defineModifyHeaders()
        self.defineTableKeys()
        self.formatCSVForLoad()
        return self.loadBulkDataToDB("processes")
