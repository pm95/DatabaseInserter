# Author: Pietro Malky
# Purpose: Get desired table schemas
# Date: July 23 2019

from Helpers import readJson, queryTableColNames, logIntoDatabase, writeJson

# define disk file paths
tablesJsonPath = "./Config/tables.json"
dbCredentialsPath = "./Config/dbCredentials.json"

tables = readJson(tablesJsonPath)
loginCreds = readJson(dbCredentialsPath)

connection = logIntoDatabase(loginCreds)

tables["processes"] = queryTableColNames(connection, "processes")
tables["requests"] = queryTableColNames(connection, "requests")
tables["users"] = queryTableColNames(connection, "users")
tables["statuses"] = queryTableColNames(connection, "statuses")

writeJson(tables, tablesJsonPath)
