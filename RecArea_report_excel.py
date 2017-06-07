# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 09:31:55 2017

@author: matthew.goodwin
"""

import datetime
import time
import os, csv#, pyodbc
import xlwt, xlrd
import sqlite3
import pandas as pd
import requests
import json

sqlite_file="reservations.db"

# Set path for output based on relative path and location of script
FileDir = os.path.dirname(__file__)
print (FileDir)
OUTDIR = os.path.join(FileDir, 'output')

# Set RecAreaIDs of objects for output. Thes come from RecAreaFacilities_API.csv
RecAreas = ['122'] #['10',17','25','122'] 
#YEARS = [2015] #[2015, 2014, 2013, 2012, 2011, 2010]
YEARS = [2015] #[2015, 2014, 2013, 2012, 2011, 2010]
YEAR_TABLE = "Recreation_2015"


recreation_cnxn = sqlite3.connect(sqlite_file)

recreation_cursor = recreation_cnxn.cursor()


#crete folder for facilities
new_folder = os.path.join(OUTDIR, "RecAreas")
if not os.path.exists(new_folder):
    os.makedirs(new_folder)
    
    
#loop through RecAreas if more than one
for recarea in RecAreas:    
    #get facility IDs in rec area using Data/RecAreaFacilities_API_v1.csv
    FACILITYID_all = pd.read_csv('Data/RecAreaFacilities_API_v1.csv', encoding="ANSI")
    FACILITYID_filtered = FACILITYID_all.loc[FACILITYID_all['RECAREAID']==int(recarea)].reset_index()
    FACILITYID_list=FACILITYID_filtered['FACILITYID'].tolist()
    print (str(len(FACILITYID_filtered)) + " facilities for RecArea " + recarea + " loaded")
    
    #Format FACILITYID_lsit for use in SQL in statement by replacing [] with ()
    FACILITYID_list = str(FACILITYID_list).replace('[','(',1)
    FACILITYID_list = FACILITYID_list.replace(']',')',1)
    
    #setup SQL query
    fac_target_query = '''
    select *
    from Recreation_2015
    where FacilityID IN ___FACIDS___
    '''
    
    temp_fac_target_query = fac_target_query.replace("___FACIDS___", str(FACILITYID_list))
    #Make SQL query
    print('Gathering Facilities associated with RecArea')
    target_fac = pd.read_sql_query(temp_fac_target_query, recreation_cnxn)
    target_fac = target_fac.reset_index()
    
    
#Close db  connections
recreation_cursor.close()
recreation_cnxn.close()

print ("finish {}".format(datetime.datetime.now().time()))
    
    
    
