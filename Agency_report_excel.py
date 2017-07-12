# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 09:31:55 2017

@author: matthew.goodwin
"""

import datetime
import sqlite3
import pandas as pd
import numpy as np
import os
import xlwt


sqlite_file="reservations.db"

# Set path for output based on relative path and location of script
FileDir = os.path.dirname(__file__)
print (FileDir)
OUTDIR = os.path.join(FileDir, 'output')

#Variable set up
#==============================================================================
# These variables will not change through the years. I initialize them as None
# so that in years beyond the first year analyzed, these values do not have to be  calculated again
#==============================================================================
FACILITYID_filtered = None
campsite_count = None



# Set Agency IDs that are present in the Reservation database
##Note: There is a '' agency for some reservations. This appears to be related to Reserve America

AgencyIDs = ['USFS'] #['NPS', 'USFS','USACE','Reserve America','NARA','BLM','FWS','BOR']


#Adjust YEARS list for each year you want analysis for
#YEAR_TABLE will be automatically updated to have the Table names for the necessary sheets based on YEARS
##Note: Make sure the years your trying to have been loaded into the datbase in loading.py

YEARS = [2015,2014] #All years [2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006]
#YEARS = [2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006]

#No need to modify once YEARS is set
YEAR_TABLE = []

#Initialize DB connections
recreation_cnxn = sqlite3.connect(sqlite_file)
recreation_cursor = recreation_cnxn.cursor()



for yr in YEARS:
    YEAR_TABLE.append("Recreation_"+str(yr))




#crete folder for facilities
new_folder = os.path.join(OUTDIR, "Agency")
if not os.path.exists(new_folder):
    os.makedirs(new_folder)
    
#loop through years. "Enumerate" also provides access to index
for agency in AgencyIDs:
    
    
    #loop through RecAreas if more than one
    for index, years in enumerate(YEARS):    
        print("Running Analysis for " + agency + " in " + str(years))
        # These tasks (done using PANDAS) are setup to run at the recArea level
        #get facility IDs in rec area using Data/RecAreaFacilities_API_v1.csv
        
        print (datetime.datetime.now().time())
        
        
        #Pull in RecArea/Facility information
        RecArea_query='''
             select *
             from RecAreaFacilities
             
             '''
        RecArea_Fac = pd.read_sql_query(RecArea_query,recreation_cnxn)
        

        #This pulls all reservation data belonging to and agency from the given years
        #reservation data
        
        #setup SQL query
        
        fac_target_query= '''
        SELECT  ___RESYEAR___.CustomerZIP,  ___RESYEAR___.FacilityID , RecAreaFacilities.FACILITYID,RecAreaFacilities.RECAREAID,
         ___RESYEAR___.EndDate,___RESYEAR___.StartDate,___RESYEAR___.OrderDate,___RESYEAR___.CustomerCountry,___RESYEAR___.CustomerState,___RESYEAR___.FacilityState,
         ___RESYEAR___.FacilityZIP,___RESYEAR___.EntityType,___RESYEAR___.OrgID
        FROM  ___RESYEAR___ LEFT JOIN RecAreaFacilities
        ON ___RESYEAR___.FacilityID = RecAreaFacilities.FACILITYID
        WHERE AGENCY = ___AGIDS___;
        '''
        
#        fac_target_query = '''
#        select *
#        from ___RESYEAR___
#        where AGENCY = ___AGIDS___
#        '''
        
        temp_fac_target_query = fac_target_query.replace("___RESYEAR___", YEAR_TABLE[index])
        temp_fac_target_query = temp_fac_target_query.replace("___AGIDS___", "'"+agency+"'")
    
        
        #Make SQL query
        print('Gathering '+agency+' Reservation Data for '+str(years))
        target_fac = pd.read_sql_query(temp_fac_target_query, recreation_cnxn)
        target_fac = target_fac.reset_index()
        
      
        
        #Run Analysis on collected facility data for RecArea
        #Convert EndDate, StateDate and OrderDate to datetime format
        target_fac['EndDate'] = pd.to_datetime(target_fac['EndDate'])
        target_fac['StartDate'] = pd.to_datetime(target_fac['StartDate'])
        target_fac['OrderDate'] = pd.to_datetime(target_fac['OrderDate'])
        
        #Calculate Time of Stay (if applicable)
        target_fac['stay_length']= np.where(target_fac['EndDate'].notnull(),(target_fac['EndDate']-target_fac['StartDate']) / np.timedelta64(1, 'D'),None)
        #Get average stay time
        Average_Stay = round(target_fac['stay_length'].mean(),2)
        
        #Get Average Lead Time
        target_fac['lead_time']= np.where(target_fac['StartDate'].notnull(),(target_fac['StartDate']-target_fac['OrderDate']) / np.timedelta64(1, 'D'),None)
        Average_Lead = round(target_fac['lead_time'].mean(),2)
        
        #Get unique facility IDS for each service
        facilities = target_fac.FacilityID.unique().tolist()
        
        #Format FACILITYID_lsit for use in SQL in statement by replacing [] with ()
        facilities = str(facilities).replace('[','(',1)
        facilities = facilities.replace(']',')',1)
        
       
        #Set up workbook
        new_file = os.path.join(new_folder, "Agency"+ agency + "_"+ str(years)+ '.xls')
        wb = xlwt.Workbook()
        
       #Calculcations for Basic Sheet
        Num_Facilities = len(target_fac['FacilityID'].value_counts())
        Num_RecAreas = len(target_fac['RECAREAID'].value_counts())
        Total_Res = len(target_fac)
        Org_ID = target_fac.iloc[1]['OrgID']
        #print (Org_ID)
        ##Grab Campsites
    
        print("Gathering Campsite Info")
        #Setup SQL query
        campsite_query='''
        select *
        from Campsites
        where FACILITYID IN ___FACIDS___
        '''
        temp_campsite_query = campsite_query.replace("___FACIDS___", str(facilities))
        
        #Run SQL query
        Campsites_RecArea=pd.read_sql_query(temp_campsite_query,recreation_cnxn)
        #Count sites
        campsite_count = len(Campsites_RecArea)
        #grab orgID off top
        
        print(str(campsite_count)+" Campsites Loaded")
       #Basic Sheet for Rec Area
        basic_sheet = wb.add_sheet("Basic Info")
        basic_sheet.write(0,0,"OrgID")
        basic_sheet.write(1,0,Org_ID)
        basic_sheet.write(0,1,"Agency Name")
        basic_sheet.write(1,1,agency)
        basic_sheet.write(0,2,"Number of RecAreas")
        basic_sheet.write(1,2,Num_RecAreas)
        basic_sheet.write(0,3,"Number of Facilities")
        basic_sheet.write(1,3,Num_Facilities)
        basic_sheet.write(0,4,"Number of Campsites")
        basic_sheet.write(1,4,campsite_count)
        basic_sheet.write(0,5,"Average Stay")
        basic_sheet.write(1,5,Average_Stay)
        basic_sheet.write(0,6,"Average Lead Time")
        basic_sheet.write(1,6, Average_Lead)
        basic_sheet.write(0,7,"Total Reservations "+ str(years))
        basic_sheet.write(1,7,Total_Res)
       
        

         
        
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
        print ("Running Zip Codes Local/NonLocal Analysis")
        
        
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
        
        
        # starting = "years-01-01"
        #ending = "years-12-31"
        
        #res_year = pd.DataFrame(0,columns=['Reservations'],index=pd.date_range('20150101','20151231',freq='D'))
        res_year = pd.DataFrame(0,columns=['Reservations'],index=pd.date_range(str(years)+'0101',str(years)+'1231',freq='D'))
       
        
        
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
        
        #Calculations for "Associated Rec Area" Sheet
        print ("Finding associated RecAreas")
        #filter out only unique RecAreas
        recAreas = np.unique(target_fac['RECAREAID'].tolist())
        #filter out NaNs
        recAreas = recAreas[~np.isnan(recAreas)]
        #Create "Associated Rec Area" Sheet    
        rec_sheet = wb.add_sheet("Associated RecAreas")
        rec_sheet.write(0,0,"RecArea ID")
        rec_sheet.write(0,1,"Number of Facilities")
        rec_sheet.write(0,2,"Average Stay (Days)")
        rec_sheet.write(0,3,"Average Lead (Days)")
        rec_sheet.write(0,4,"Total Reservations "+ str(years))
        #Debug Statement
        #print("RecArea sheet formatted")
        wb.save(new_file)
        
        for idx_rec,rec in enumerate(recAreas):
            mean_lead_rec = target_fac.loc[target_fac['RECAREAID']==rec,'lead_time'].mean()
            mean_stay_rec = target_fac.loc[target_fac['RECAREAID']==rec,'stay_length'].mean()
            rec_reserv = len(target_fac.loc[target_fac['RECAREAID']==rec])
            rec_fac = len(target_fac.loc[target_fac['RECAREAID']==rec].FacilityID.unique().tolist())
            #Debug Statment
            #print("metrics for "+ str(rec))
            rec_sheet.write(idx_rec+1,0,rec)
            rec_sheet.write(idx_rec+1,1,rec_fac)
            rec_sheet.write(idx_rec+1,2,mean_stay_rec)
            rec_sheet.write(idx_rec+1,3,mean_lead_rec)
            rec_sheet.write(idx_rec+1,4,rec_reserv)
            wb.save(new_file)
 
#Close db  connections
recreation_cursor.close()
recreation_cnxn.close()

print ("finish {}".format(datetime.datetime.now().time()))
    
    
    
