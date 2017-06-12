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
RecAreas = ['25'] #['10',17','25','122'] 
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
    
    # These tasks (done using PANDAS) are setup to run at the recArea level
    #get facility IDs in rec area using Data/RecAreaFacilities_API_v1.csv
    
    print (datetime.datetime.now().time())
    
    RecArea_query='''
    select *
    from RecAreaFacilities
    where RECAREAID = ___RECIDS___
    '''
    temp_RecArea_query = RecArea_query.replace("___RECIDS___", str(recarea))
    
    
    
    FACILITYID_filtered = pd.read_sql_query(temp_RecArea_query,recreation_cnxn)
    
    
    FACILITYID_list=FACILITYID_filtered['FACILITYID'].tolist()
    print (str(len(FACILITYID_filtered)) + " facilities for RecArea " + recarea + " loaded")
    
    #Format FACILITYID_lsit for use in SQL in statement by replacing [] with ()
    FACILITYID_list = str(FACILITYID_list).replace('[','(',1)
    FACILITYID_list = FACILITYID_list.replace(']',')',1)
    
    
    #Pull Campsites that are in the list of facilities
    print("Gathering Campsite Info")
    #Setup SQL query
    campsite_query='''
    select *
    from Campsites
    where FACILITYID IN ___FACIDS___
    '''
    temp_campsite_query = campsite_query.replace("___FACIDS___", str(FACILITYID_list))
    
    #Run SQL query
    Campsites_RecArea=pd.read_sql_query(temp_campsite_query,recreation_cnxn)
    #Count sites
    campsite_count = len(Campsites_RecArea)
    
    print(str(campsite_count)+" Campsites Loaded")
    
    
    
    #setup SQL query
    
    fac_target_query = '''
    select *
    from Recreation_2015
    where FacilityID IN ___FACIDS___
    '''
    
    temp_fac_target_query = fac_target_query.replace("___FACIDS___", str(FACILITYID_list))
    # @TODO: here is what a year condition/replacement can be added for when that has to be implemented
    #Just replace year/table name in the query string before running
    
    #Make SQL query
    print('Gathering Facilities associated with RecArea')
    target_fac = pd.read_sql_query(temp_fac_target_query, recreation_cnxn)
    target_fac = target_fac.reset_index()
    
    #Run Analysis on collected facility data for RecArea
    
    #Start with pandas based sheets as those are easier to implement
   
    #Set up workbook
    new_file = os.path.join(new_folder, recarea + '.xls')
    wb = xlwt.Workbook()
    
    
    
    
     #Create RecArea basic sheet
   #RECAREANAME, RECAREAID, RECAREALATITUDE,RECAREALONGITUDE
   #Calculate Total number of campsites, average stay, average lead, Reservations 2015
   
   #@TODO look into lat/long for all sites
   
   
    print('Gathering RecArea Basic Information')
    
    #Setup SQL query
    
    RecArea_basic_query = '''
    select *
    from RecAreas
    where RECAREAID =  ___RECIDS___
    '''
    
    temp_RecArea_basic_query=RecArea_basic_query.replace("___RECIDS___", str(recarea))
    
    #Run SQL query
    RecArea_all = pd.read_sql_query(temp_RecArea_basic_query,recreation_cnxn)
    
    
    
    RecArea_target = RecArea_all.loc[RecArea_all['RECAREAID']==int(recarea)]
    
    
    
    rec_basic = wb.add_sheet('Facility_Basic')

    rec_basic.write(0,0,'RecAreaID')
    rec_basic.write(0,1,str(RecArea_target['RECAREAID'].iloc[0]))
    rec_basic.write(1,0,'RecAreaName')
    rec_basic.write(1,1,RecArea_target['RECAREANAME'].iloc[0])
    rec_basic.write(2,0,'RecAreaLatitude')
    rec_basic.write(2,1,RecArea_target['RECAREALATITUDE'].iloc[0])
    rec_basic.write(3,0,'RecAreaLongitude')
    rec_basic.write(3,1,RecArea_target['RECAREALONGITUDE'].iloc[0])
    
    #Create placeholders for items that will be filled out later
    rec_basic.write(4,0,'Number Campsites')
    rec_basic.write(4,1,campsite_count)
    rec_basic.write(5,0,'Average Stay')
    rec_basic.write(6,0,'Average Lead')
#    
#    test = RecArea_target['RECAREAID'].iloc[0]
#    
    wb.save(new_file)
    
     
    
    #Item 1: In-state/out-of-state/intl distinction
    print ("Customer Origin Analysis")
    #Count Countries where reservations come from and convert to dataframe
    country_count = target_fac['CustomerCountry'].value_counts().to_frame().reset_index()
    
    #Setup sheet where this and the other relevant info will go
    custloc_sheet = wb.add_sheet("Customer Location Breakdown")
    #custloc_sheet.write()
    custloc_sheet.write(0,0,"Reservation Breakdown by Country")
    custloc_sheet.write(1,0,"Country")
    custloc_sheet.write(1,1,"# of Reservations")
    for index, row in country_count.iterrows():
        custloc_sheet.write(int(index)+2,0,row['index'])
        custloc_sheet.write(int(index)+2,1,row['CustomerCountry'])
   
    #In State/Out of State/Out of Country distinction
    
    #Total site reservaations calcualtion
    total_res=len(target_fac)
    
    #Collect reservations made by residents of the faciliity's state
    instate_res=len(target_fac.loc[target_fac['CustomerState']==target_fac['FacilityState']])
    #outcountry_res =target_fac.loc[target_fac['CustomerState']!=target_fac['FacilityState'] & target_fac['CustomerCountry']='USA']
    
    #Collect reservations made by non-USA residents
    outcountry_res =len(target_fac.loc[target_fac['CustomerCountry']!='USA'])
    
    #Calculate residents that are out of state
    ##Total Reservations-(instate_res+outcountrye_res)=out of state residents
    outstate_res = total_res-(instate_res+outcountry_res)
    
    # Write this results to Customer Location Breakdown Sheet
    custloc_sheet.write(0,4,"Reservation Breakdown by State")
    custloc_sheet.write(1,4,"Category")
    custloc_sheet.write(1,5,"# of Reservations")
    custloc_sheet.write(2,4,"Same State as Site")
    custloc_sheet.write(2,5,instate_res)
    custloc_sheet.write(3,4,"Out of State")
    custloc_sheet.write(3,5,outstate_res)
    custloc_sheet.write(4,4,"Outside USA")
    custloc_sheet.write(4,5,outcountry_res)
    custloc_sheet.write(5,4,"Total Reservations")
    custloc_sheet.write(5,5,total_res)
    
    wb.save(new_file)
    
    
    
     #############################################################
    #Item 3 Zip code local/non-local distinction Note: Some Facilities do not have Zip
    
    #Level 1: Reservations has same zip code as site
    local_res_lev1 = len(target_fac.loc[target_fac['CustomerZIP']==target_fac['FacilityZIP']])
    #Level 2: Reservations have same 3 digit level zip as facility
    #Pull facility ZipCode (just use first row data as this should remanin the same for the filtered sheet)
    
    #set level of zip code to check i.e zip_lvl=3 for 33027 would check against 330*
    zip_lvl = 3
    fac_zip = target_fac['FacilityZIP'].iloc[0][:zip_lvl]
    #create new columns with ZipCodes as strings to use regex with
    target_fac['CustomerZIP_Str']=target_fac['CustomerZIP']
    target_fac['CustomerZIP_Str']=target_fac['CustomerZIP_Str'].apply(str)
    #form 3 digit regex expression. if handles if there is no Zip
    print ("Zip Codes Local/NonLocal Analysis")
    
    
    if fac_zip != '':
        fac_zip_regex=fac_zip+'*'
        local_res_lev2=len(target_fac['CustomerZIP'].filter(regex=fac_zip_regex))
        #write out to Breakdown sheet if data exists
        custloc_sheet.write(0,7,"Reservation Breakdown by Zip Code")
        custloc_sheet.write(1,7,"Category")
        custloc_sheet.write(1,8,"# of Reservations")
        custloc_sheet.write(2,7,"Same Zip as Site")
        custloc_sheet.write(2,8,local_res_lev1)
        custloc_sheet.write(3,7,"Within same "+str(zip_lvl)+ " Digit Level as Site")
        custloc_sheet.write(3,8,local_res_lev2)
        custloc_sheet.write(4,7,"Total Reservations")
        custloc_sheet.write(4,8,total_res)

    else:
        print('No Facility Zip Code Available in Data Set')
    
    #############################################################
    #Item 1 - Add entity type to standard report
    #get entity counts as a data frame to iterate over
    entity_count = target_fac['EntityType'].value_counts().to_frame().reset_index()
    #print (len(entity_count))
    #write to new sheet
    
    # Entity Type
    print ("Entity Type")
    
    ent_sheet = wb.add_sheet("EntityType")
    ent_sheet.write(0,0,'Entity Type')
    ent_sheet.write(0,1,'# of Reservations')
    for index, row in entity_count.iterrows():
        ent_sheet.write(int(index)+1,0,row['index'])
        ent_sheet.write(int(index)+1,1,row['EntityType'])
    wb.save(new_file)
    
    # Dates
    #Create empty df from start to end date
    
    
    # starting = "2015-01-01"
    #ending = "2015-12-31"
    
    res_year = pd.DataFrame(0,columns=['Reservations'],index=pd.date_range('20150101','20151231',freq='D'))
    
   
    
    
    #@TODO right now this only handles order date, but could be made more robust?
    res_dates= pd.DataFrame(target_fac.groupby('OrderDate').size().rename('Reservations'))
    res_dates['dates'] = pd.to_datetime(res_dates.index)
    res_dates_indexed = res_dates.set_index(['dates'],inplace=True)
    
    #fill in res_dates with reservations made
   
    for row in res_dates.iterrows():
        if row[0] in res_year.index:
            res_year.loc[row[0]]['Reservations']=row[1]
            
            
    #print out to excel sheet
   
    rec_dates = wb.add_sheet('Date Analysis')
    rec_dates.write(0,0,'Date')
    rec_dates.write(0,1,'# of Reservations')
    
   
    i = 0
    for row in res_year.iterrows():
        date = row[0].strftime('%m-%d-%Y')
        rec_dates.write(i+1,0,str(date))
        rec_dates.write(i+1,1,int(res_year.loc[row[0]]['Reservations']))
       
       
        #rec_dates.write(i+1,1,row[1]['Reservations'])
        i=i+1
        
        
    wb.save(new_file)

        
            
          
        
   
 
#Close db  connections
recreation_cursor.close()
recreation_cnxn.close()

print ("finish {}".format(datetime.datetime.now().time()))
    
    
    
