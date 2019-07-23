# Author: Pietro Malky
# Purpose: Manipulate Masterlist data prior to importing it to DB
# Date: July 17 2019


import Helpers

# Obtain tables' schemas from DB
import GetTableSchema


class MasterlistDataLoader:
    def __init__(self, fin_path, fout_path, header_map_path, table_keys_path, dbCredentialsPath):
        self.fin_path = fin_path
        self.header_map_path = header_map_path
        self.table_keys_path = table_keys_path
        self.fout_path = fout_path

        self.columnMappings = None
        self.table_keys = None

        self.dbCredentialsPath = dbCredentialsPath

    def defineModifyHeaders(self):
        self.columnMappings = Helpers.readJson(self.header_map_path)

    def defineTableKeys(self):
        self.table_keys = Helpers.readJson(self.table_keys_path)

    def formatCSVForLoad(self, columnMappings):
        Helpers.formatCSVForLoad(
            self.fin_path,
            self.fout_path,
            columnMappings=columnMappings,
            contains_dates=True
        )

    def loadBulkDataToDB(self, tableName):
        return Helpers.loadCSVDataToDB(
            self.fout_path,
            tableName,
            self.table_keys,
            self.dbCredentialsPath
        )

    def run(self):
        self.defineModifyHeaders()
        self.defineTableKeys()

        # processes table
        self.formatCSVForLoad(columnMappings=self.columnMappings["processes"])
        self.loadBulkDataToDB(tableName="processes")

        # requests table
        self.formatCSVForLoad(columnMappings=self.columnMappings["requests"])
        self.loadBulkDataToDB(tableName="requests")
