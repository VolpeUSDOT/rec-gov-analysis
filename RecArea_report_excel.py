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
    FACILITYID_filtered = FACILITYID_all.loc[FACILITYID_all['RECAREAID']==int(recarea)]
    print (str(len(FACILITYID_filtered)) + " facilities for RecArea " + recarea + " loaded")
    
    
    
    