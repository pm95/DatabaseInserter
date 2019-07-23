# Author: Pietro Malky
# Purpose: Get desired table schemas
# Date: July 23 2019

import Helpers

# define disk file paths
tablesJsonPath = "./Config/tables.json"
dbCredentialsPath = "./Config/dbCredentials.json"

tables = Helpers.readJson(tablesJsonPath)
loginCreds = Helpers.readJson(dbCredentialsPath)

connection = Helpers.logIntoDatabase(loginCreds)

tables["processes"] = Helpers.queryTableColNames(connection, "processes")
tables["requests"] = Helpers.queryTableColNames(connection, "requests")
tables["users"] = Helpers.queryTableColNames(connection, "users")
tables["statuses"] = Helpers.queryTableColNames(connection, "statuses")

Helpers.writeJson(tables, tablesJsonPath)
