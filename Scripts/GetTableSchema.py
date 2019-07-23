# Author: Pietro Malky
# Purpose: Get desired table schemas
# Date: July 23 2019

from Helpers import readJson, queryTableColNames, logIntoDatabase, writeJson

# define disk file paths
tablesJsonPath = "./tables.json"
dbCredentialsPath = "./dbCredentials.json"

tables = readJson(tablesJsonPath)
loginCreds = readJson(dbCredentialsPath)

connection = logIntoDatabase(loginCreds)
cursor = connection.cursor()

tables["processes"] = queryTableColNames(cursor, "processes")
tables["requests"] = queryTableColNames(cursor, "requests")
tables["users"] = queryTableColNames(cursor, "users")
tables["statuses"] = queryTableColNames(cursor, "statuses")

writeJson(tables, tablesJsonPath)
