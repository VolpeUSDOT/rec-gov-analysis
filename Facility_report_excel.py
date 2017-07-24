import datetime
import time
import os, csv#, pyodbc
import xlwt, xlrd
import sqlite3
import pandas as pd

sqlite_file="reservations.db"

# Set path for output based on relative path and location of script
FileDir = os.path.dirname(__file__)
print (FileDir)
OUTDIR = os.path.join(FileDir, 'output')

# Set IDs of objects for output
FACILITYIDS = ['233262'] #['233396','233262','233266','233260','232250','232769','233261','234735','232254','231980'] 


#Adjust YEARS list for each year you want analysis for
#YEAR_TABLE will be automatically updated to have the Table names for the necessary sheets based on YEARS
YEARS = [2015] #[2015, 2014, 2013, 2012, 2011, 2010]

#No need to modify once YEARS is set
YEAR_TABLE = []
for yr in YEARS:
    YEAR_TABLE.append("Recreation_"+str(yr))
    
#YEAR_TABLE = "Recreation_2015"


recreation_cnxn = sqlite3.connect(sqlite_file)

recreation_cursor = recreation_cnxn.cursor()


#crete folder for facilities
new_folder = os.path.join(OUTDIR, "Facilities")
if not os.path.exists(new_folder):
    os.makedirs(new_folder)


#location of facility, average length stay, average lead time, number of campsites


fac_basic_query = '''
select p.facilityid as facitlyid, facilityname, facilitylatitude, facilitylongitude, recareaid, recareaname, count(p.facilityid) as num_campsites
from(
                        select f.facilityid, f.FACILITYNAME, f.facilitylatitude, f.facilitylongitude, raf.recareaid, ra.RECAREANAME
                        from facilities f
                        left outer join RecAreaFacilities raf on f.FACILITYID = raf.FACILITYID
                        left outer join RecAreas ra on raf.recareaid = ra.recareaid
                        where f.facilityid = '___FACID___'
)p
left outer join Campsites q on p.FACILITYID = q.FACILITYID
group by p.facilityid,facilityname, facilitylatitude, facilitylongitude, recareaid, RECAREANAME
'''



time_query ='''select facilityid, avg(cast(stay as float)) as avg_stay, avg(cast(lead as float)) as avg_lead, count(m.facilityid)
from(
    select x.facilityid, (julianday(EndDate) - julianday(StartDate)) as stay, (julianday(StartDate) - julianday(OrderDate)) as lead
    from(
        select facilityid from facilities where facilityid = '___FACID___'
    )x
    left outer join Recreation____YEAR___ a on x.FACILITYID = a.facilityid
)m
group by m.FACILITYID
'''


fac_info_query = '''select facilityid, FACILITYNAME from facilities where facilityid in (___FACID___)'''

year_compare_query = '''select x.facilityid, FACILITYNAME, count(a.facilityid) as reservations
from(
    select facilityid, FACILITYNAME from facilities where facilityid in (___FACID___)
)x
left outer join Recreation____YEAR___ a on x.FACILITYID = a.facilityid
group by x.FACILITYID, FACILITYNAME, a.FacilityID
'''

date_query = '''select FacilityID, StartDate, EndDate from Recreation____YEAR___ where FacilityID in ('___FACID___')'''


# create new sheet fac_basic for each facility in facid add run query and create new line
for run_years in YEARS:
    print("Running Facility Analysis for " + str(run_years))
    
    for facid in FACILITYIDS:
    
        print (datetime.datetime.now().time())
        
        new_file = os.path.join(new_folder, "Fac"+facid+"_"+str(run_years) + '.xls')
        wb = xlwt.Workbook()
        
        print ("running basic facility information {}".format(facid))
    
        fac_basic = wb.add_sheet('Facility_Basic')
    
        fac_basic.write(0,0,'FacilityID')
        fac_basic.write(0,1,'FacilityName')
        fac_basic.write(0,2,'FacilityLatitude')
        fac_basic.write(0,3,'FacilityLongitude')
        fac_basic.write(0,4,'RecAreaID')
        fac_basic.write(0,5,'RecAreaName')
        fac_basic.write(0,6,'Number Campsites')
        fac_basic.write(0,7,'Average Stay')
        fac_basic.write(0,8,'Average Lead')
                
        col_res = 9
        
        for index, year in enumerate(YEARS):
            fac_basic.write(0, col_res, "Reservations " + str(year))
            
            col_res = col_res + 1    
        
        i=1
    
        temp_fac_basic_query = fac_basic_query.replace("___FACID___", str(facid))
        temp_fac_basic_query2 = temp_fac_basic_query.replace("___YEAR___", YEAR_TABLE[index])
    
    
    
       
        rows = recreation_cursor.execute(temp_fac_basic_query2)
            
        for x in rows:
            fac_basic.write(i, 0, x[0])
            fac_basic.write(i, 1, x[1])
            fac_basic.write(i, 4, x[4])
            fac_basic.write(i, 5, x[5])
            fac_basic.write(i, 6, x[6])
            
            if x[2] == None:
                fac_basic.write(i, 2, 0)
                fac_basic.write(i, 3, 0)
            else:
                fac_basic.write(i, 2, x[2])
                fac_basic.write(i, 3, x[3])
        
        avg_stay = []
        avg_lead = []
        
        col_res = 9
        
        for year in YEARS:
            temp_time_query = time_query.replace("___YEAR___", str(year))
            temp_time_query2 = temp_time_query.replace("___FACID___", str(facid))
            
            year_exe = recreation_cursor.execute(temp_time_query2)
            
            for x in year_exe: 
                if x[1] == '':
                    x[1] = None
                if x[2] == '':
                    x[2] = None
                if x[1] == None and x[2] == None:
                    fac_basic.write(i, col_res, 0)
                else:
                    fac_basic.write(i, col_res, x[3])            
                
                col_res = col_res + 1
                
                if x[1] != None and x[2] != None:
                    avg_stay.append(x[1])
                    avg_lead.append(x[2])                    
                elif x[1] != None and x[2] == None:
                    avg_stay.append(x[1])
                elif x[1] == None and x[2] != None:
                    avg_lead.append(x[2])
                else:
                    continue
                
        if len(avg_stay) == 0 and len(avg_lead) == 0:
            fac_basic.write(i, 7, 0)
            fac_basic.write(i, 8, 0)
            
        elif len(avg_stay) > 0 and len(avg_lead) == 0:
            true_avg_stay = sum(avg_stay) / float(len(avg_stay))
            fac_basic.write(i, 7, round(true_avg_stay,2))
            fac_basic.write(i, 8, 0)
            
        elif len(avg_stay) == 0 and len(avg_lead) > 0:
            fac_basic.write(i, 7, 0)
            true_avg_lead = sum(avg_lead) / float(len(avg_lead))
            fac_basic.write(i, 8, round(true_avg_lead,2))
                
        else:     
            true_avg_stay = sum(avg_stay) / float(len(avg_stay))
            true_avg_lead = sum(avg_lead) / float(len(avg_lead))
    
            fac_basic.write(i,7, round(true_avg_stay,2))
            fac_basic.write(i,8, round(true_avg_lead,2))
    
        i = i + 1
        wb.save(new_file)
            
            
        # Growth
        print ("year by year growth")
        fac_growth = wb.add_sheet("Growth")
            
        fac_growth.write(0,0,"Year")
        fac_growth.write(0,1,"Number Reservations")
        fac_growth.write(0,2,"Growth Rate")
    
        i = 1
    
        for year in YEARS: 
    
            temp_year_compare_query = year_compare_query.replace("___FACID___", str(facid))
            temp_year_compare_query2 = temp_year_compare_query.replace("___YEAR___", str(year))
            
            fac_growth_run = recreation_cursor.execute(temp_year_compare_query2)
            
            for x in fac_growth_run:
                            
                fac_growth.write(i,0,str(year))
                fac_growth.write(i,1, x[2])
                
                i = i + 1
                
     
    
        wb.save(new_file)
        
        wbr = xlrd.open_workbook(new_file)
    
        growth_wbr = wbr.sheet_by_index(1)
    
        start_cell = len(YEARS)
    
        while start_cell > 1:    
            new = growth_wbr.cell(start_cell-1, 1).value
            
            old = growth_wbr.cell(start_cell, 1).value
            if     old == 0:
                change = "no previous data"
                fac_growth.write(start_cell-1, 2, change)
            else:     
                change = ((new-old)/old)*100
                fac_growth.write(start_cell-1, 2, round(change,2))            
            
            start_cell = start_cell-1
    
        wb.save(new_file)
            
        #calendar dates    
        print ("reservations by date")
        fac_agg = wb.add_sheet("Date Analysis")
    
        fac_agg.write(0,0,"Date")
        fac_agg.write(0,1,"Number Reservations")
    
        temp_date_query = date_query.replace("___FACID___", str(facid))
        
        fac_date_counter = {}
        
    
        starting = "2015-01-01"
        ending = "2015-12-31"
    
    
        start_year_as_int = int(starting[:4])
        start_month_as_int = int(starting[5:-3])
        start_day_as_int = int(starting[-2:])
        end_year_as_int = int(ending[:4])
        end_month_as_int = int(ending[5:-3])
        end_day_as_int = int(ending[-2:])
                
    
        start_date = datetime.datetime(start_year_as_int, start_month_as_int, start_day_as_int)
        end_date = datetime.datetime(end_year_as_int, end_month_as_int, end_day_as_int)
            
        total_days = (end_date - start_date).days + 1
        
        for day_number in range(total_days):        
                
            current_date = (start_date + datetime.timedelta(days = day_number)).date()
            
            day_m = str(current_date)[-5:]
            
            if not day_m in fac_date_counter:
                fac_date_counter[day_m] = 0
            else: 
                fac_date_counter[day_m] += 1
                
        for index,year in enumerate(YEARS):
            
                        
            temp_year_query = temp_date_query.replace("___YEAR___", str(year))
            
            
            date = recreation_cursor.execute(temp_year_query)
            
            date_counter = {}
            for record in date:
                
                start = record[1]
                end = record[2]
                
                if start != None and end != None and end != '' and start != '':
                
                    start_year_as_int = int(start[:4])
                    start_month_as_int = int(start[5:-3])
                    start_day_as_int = int(start[-2:])
                    end_year_as_int = int(end[:4])
                    end_month_as_int = int(end[5:-3])
                    end_day_as_int = int(end[-2:])
                    
                    start_date = datetime.datetime(start_year_as_int, start_month_as_int, start_day_as_int)
                    end_date = datetime.datetime(end_year_as_int, end_month_as_int, end_day_as_int)
                        
                    total_days = (end_date - start_date).days + 1
                        
                    for day_number in range(total_days):        
                            
                        current_date = (start_date + datetime.timedelta(days = day_number)).date()
                        day_m = str(current_date)[-5:]
                        
                        # if not str(current_date) in date_counter:
                            # date_counter[str(current_date)] = 1
                        
                        # else: 
                            # date_counter[str(current_date)] += 1
                        
                        if not day_m in fac_date_counter:
                            fac_date_counter[day_m] = 1
                        else: 
                            fac_date_counter[day_m] += 1
                
                # Handles reservations with only a start-date. Typical for one-day events such as tours, but not typical for campgrounds. 
                elif start != None and start != '' and (end == None or end == ''):
                    
                    # Seperate out year, month, and day
                    start_year_as_int = int(start[:4])
                    start_month_as_int = int(start[5:-3])
                    start_day_as_int = int(start[-2:])
                    
                    # Input into common time format
                    start_date = datetime.datetime(start_year_as_int, start_month_as_int, start_day_as_int)
                    
                    # Convert date/time format to just date
                    start_date = start_date.date()
                    
                    day_m = str(start_date)[-5:]
                
                    if not day_m in fac_date_counter:
                        fac_date_counter[day_m] = 1
                    else: 
                        fac_date_counter[day_m] += 1
                
                else:
                    continue
                    
                    
        i = 1
    
        for k,v in fac_date_counter.items():
            fac_agg.write(i, 0, k)
            fac_agg.write(i, 1, v)
            
            i = i + 1
            
        wb.save(new_file)
       
        #Todo List items using pandas
        
        ##########################################################
        
        #Query Recreation table for all reservation in facility   
        fac_target_query = '''
        select *
        from Recreation_2015
        where FacilityID=___FACID___
        '''
        temp_fac_target_query = fac_target_query.replace("___RESYEAR___", YEAR_TABLE[index])
        temp_fac_target_query = temp_fac_target_query.replace("___FACID___", str(facid))
        
        target_fac = pd.read_sql_query(temp_fac_target_query, recreation_cnxn)
        target_fac = target_fac.reset_index()
        
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
            
            
        # Add top 5 zip codes    
        #zip_count = target_fac['CustomerZIP_Str'].value_counts().to_frame()
        zip_digit = target_fac['CustomerZIP_Str'].str[0:3]
        zip_count = zip_digit.value_counts().to_frame().reset_index()
        zip_top5 = zip_count.head(5)
        zip_top5 = zip_top5.rename(columns = {'index':'ZIP'})
        custloc_sheet.write (0,11,"Top 5 Zip Codes by Reservation")
       
        for index,row in zip_top5.iterrows():
           
            custloc_sheet.write(index+1,11,row['ZIP']+"XX")
            custloc_sheet.write(index+1,12,row['CustomerZIP_Str'])
        wb.save(new_file)
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
    
    

    
    #End Pandas Implementation 
        
    
    
#Close connections
recreation_cursor.close()
recreation_cnxn.close()

    
    
  
print ("finish {}".format(datetime.datetime.now().time()))






