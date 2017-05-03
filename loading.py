import os, csv
import xlwt, xlrd
import sqlite3

# Configuration
sqlite_file="reservations.db"


# Make database connection
conn = sqlite3.connect(sqlite_file)
cursor = conn.cursor()

# Create list of paths for .sql scripts to run

scripts = []
scripts.append('Loading/Loading_TXT_to_SQL_Campsites.sql')
scripts.append('Loading/Loading_TXT_to_SQL_Facilities.sql')
scripts.append('Loading/Loading_TXT_to_SQL_RecAreas.sql')
scripts.append('Loading/Loading_TXT_to_SQL_RecAreaFacilities.sql')
scripts.append('Loading/Loading_TXT_to_SQL_2015.sql')


# Run scripts

for i in scripts:
	qry = open(i, 'r').read()
	cursor.executescript(qry)
	conn.commit()
	
# Close connection
	cursor.close()
	conn.close()
