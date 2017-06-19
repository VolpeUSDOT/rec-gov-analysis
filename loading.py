import os, csv
import xlwt, xlrd
import sqlite3

def main():
    # Configuration
    sqlite_file="reservations.db"


    # Make database connection
    conn = sqlite3.connect(sqlite_file)
    conn.text_factory = str
    cursor = conn.cursor()



    # Create list of paths for .sql scripts to run

    # Add RecAreas
    
    tableName = 'RecAreas'
    loadPath = 'Loading/Loading_TXT_to_SQL_RecAreas.sql'
    dataPath = 'Data/RecAreas_API_v1.csv'
    colNames = ['KEYWORDS','LASTUPDATEDDATE','ORGRECAREAID','RECAREAEMAIL','RECAREAFEEDESCRIPTION','RECAREAID','RECAREALATITUDE','RECAREALONGITUDE','RECAREANAME','RECAREAPHONE','RECAREARESERVATIONURL','STAYLIMIT']
    
    addTable(tableName,loadPath,dataPath,colNames,cursor,conn)
    
    # Add Campsites
    
    tableName = 'Campsites'
    loadPath = 'Loading/Loading_TXT_to_SQL_Campsites.sql'
    dataPath = 'Data/Campsites_API_v1.csv'
    colNames = ['CAMPSITEACCESSIBLE','CAMPSITEID','CAMPSITENAME','CAMPSITETYPE','CREATEDDATE','FACILITYID','LASTUPDATEDDATE','LOOP','TYPEOFUSE']
    
    addTable(tableName,loadPath,dataPath,colNames,cursor,conn)
    
    # Add Facilities

    tableName = 'Facilities'
    loadPath = 'Loading/Loading_TXT_to_SQL_Facilities.sql'
    dataPath = 'Data/Facilities_API_v1.csv'
    colNames = ['FACILITYADAACCESS','FACILITYEMAIL','FACILITYID','FACILITYLATITUDE','FACILITYLONGITUDE','FACILITYMAPURL','FACILITYNAME','FACILITYPHONE','FACILITYRESERVATIONURL','FACILITYTYPEDESCRIPTION','FACILITYUSEFEEDESCRIPTION','KEYWORDS','LASTUPDATEDDATE','LEGACYFACILITYID','ORGFACILITYID','STAYLIMIT']
    
    addTable(tableName,loadPath,dataPath,colNames,cursor,conn)
    
    # Add RecAreaFacilities
    
    tableName = 'RecAreaFacilities'
    loadPath = 'Loading/Loading_TXT_to_SQL_RecAreaFacilities.sql'
    dataPath = 'Data/RecAreaFacilities_API_v1.csv'
    colNames = ['FACILITYID','RECAREAID']
    
    addTable(tableName,loadPath,dataPath,colNames,cursor,conn)    
    
    # Add 2015 reservations
    
    tableName = 'Recreation_2015'
    loadPath = 'Loading/Loading_TXT_to_SQL_2015.sql'
    dataPath = 'Data/Reservation/2015.csv'
    colNames = ["HistoricalReservationID","OrderNumber","Agency","OrgID","CodeHierarchy","RegionCode","RegionDescription","ParentLocationID","ParentLocation","LegacyFacilityID","Park","SiteType","UseType","ProductID","EntityType","EntityID","FacilityID","FacilityZIP","FacilityState","FacilityLongitude","FacilityLatitude","CustomerZIP","CustomerState","CustomerCountry","Tax","UseFee","TranFee","AttrFee","TotalBeforeTax","TotalPaid","StartDate","EndDate","OrderDate","NumberOfPeople","Tent","Popup","Trailer","RVMotorhome","Boat","HorseTrailer","Car","FifthWheel","Van","CanoeKayak","BoatTrailer","Motorcycle","Truck","Bus","Bicycle","Snowmobile","OffRoadlAllTerrainVehicle","PowerBoat","PickupCamper","LargeTentOver9x12","SmallTent","Marinaboat"]
    
    addTable(tableName,loadPath,dataPath,colNames,cursor,conn)    
    
    #Add 2014 reservations
    tableName = 'Recreation_2014'
    loadPath = 'Loading/Loading_TXT_to_SQL_2014.sql'
    dataPath = 'Data/Reservation/2014.csv'
    colNames = ["HistoricalReservationID","OrderNumber","Agency","OrgID","CodeHierarchy","RegionCode","RegionDescription","ParentLocationID","ParentLocation","LegacyFacilityID","Park","SiteType","UseType","ProductID","EntityType","EntityID","FacilityID","FacilityZIP","FacilityState","FacilityLongitude","FacilityLatitude","CustomerZIP","CustomerState","CustomerCountry","Tax","UseFee","TranFee","AttrFee","TotalBeforeTax","TotalPaid","StartDate","EndDate","OrderDate","NumberOfPeople","Tent","Popup","Trailer","RVMotorhome","Boat","HorseTrailer","Car","FifthWheel","Van","CanoeKayak","BoatTrailer","Motorcycle","Truck","Bus","Bicycle","Snowmobile","OffRoadlAllTerrainVehicle","PowerBoat","PickupCamper","LargeTentOver9x12","SmallTent","Marinaboat"]
    
    addTable(tableName,loadPath,dataPath,colNames,cursor,conn) 
    
    #Add 2013 reservations
    tableName = 'Recreation_2013'
    loadPath = 'Loading/Loading_TXT_to_SQL_2013.sql'
    dataPath = 'Data/Reservation/2013.csv'
    colNames = ["HistoricalReservationID","OrderNumber","Agency","OrgID","CodeHierarchy","RegionCode","RegionDescription","ParentLocationID","ParentLocation","LegacyFacilityID","Park","SiteType","UseType","ProductID","EntityType","EntityID","FacilityID","FacilityZIP","FacilityState","FacilityLongitude","FacilityLatitude","CustomerZIP","CustomerState","CustomerCountry","Tax","UseFee","TranFee","AttrFee","TotalBeforeTax","TotalPaid","StartDate","EndDate","OrderDate","NumberOfPeople","Tent","Popup","Trailer","RVMotorhome","Boat","HorseTrailer","Car","FifthWheel","Van","CanoeKayak","BoatTrailer","Motorcycle","Truck","Bus","Bicycle","Snowmobile","OffRoadlAllTerrainVehicle","PowerBoat","PickupCamper","LargeTentOver9x12","SmallTent","Marinaboat"]
    
    addTable(tableName,loadPath,dataPath,colNames,cursor,conn) 
    
    #Add 2012 reservations
    tableName = 'Recreation_2012'
    loadPath = 'Loading/Loading_TXT_to_SQL_2012.sql'
    dataPath = 'Data/Reservation/2012.csv'
    colNames = ["HistoricalReservationID","OrderNumber","Agency","OrgID","CodeHierarchy","RegionCode","RegionDescription","ParentLocationID","ParentLocation","LegacyFacilityID","Park","SiteType","UseType","ProductID","EntityType","EntityID","FacilityID","FacilityZIP","FacilityState","FacilityLongitude","FacilityLatitude","CustomerZIP","CustomerState","CustomerCountry","Tax","UseFee","TranFee","AttrFee","TotalBeforeTax","TotalPaid","StartDate","EndDate","OrderDate","NumberOfPeople","Tent","Popup","Trailer","RVMotorhome","Boat","HorseTrailer","Car","FifthWheel","Van","CanoeKayak","BoatTrailer","Motorcycle","Truck","Bus","Bicycle","Snowmobile","OffRoadlAllTerrainVehicle","PowerBoat","PickupCamper","LargeTentOver9x12","SmallTent","Marinaboat"]
    
    addTable(tableName,loadPath,dataPath,colNames,cursor,conn) 
    
    #Add 2011 reservations
    tableName = 'Recreation_2011'
    loadPath = 'Loading/Loading_TXT_to_SQL_2011.sql'
    dataPath = 'Data/Reservation/2011.csv'
    colNames = ["HistoricalReservationID","OrderNumber","Agency","OrgID","CodeHierarchy","RegionCode","RegionDescription","ParentLocationID","ParentLocation","LegacyFacilityID","Park","SiteType","UseType","ProductID","EntityType","EntityID","FacilityID","FacilityZIP","FacilityState","FacilityLongitude","FacilityLatitude","CustomerZIP","CustomerState","CustomerCountry","Tax","UseFee","TranFee","AttrFee","TotalBeforeTax","TotalPaid","StartDate","EndDate","OrderDate","NumberOfPeople","Tent","Popup","Trailer","RVMotorhome","Boat","HorseTrailer","Car","FifthWheel","Van","CanoeKayak","BoatTrailer","Motorcycle","Truck","Bus","Bicycle","Snowmobile","OffRoadlAllTerrainVehicle","PowerBoat","PickupCamper","LargeTentOver9x12","SmallTent","Marinaboat"]
    
    addTable(tableName,loadPath,dataPath,colNames,cursor,conn) 
    
    #Add 2010 reservations
    tableName = 'Recreation_2010'
    loadPath = 'Loading/Loading_TXT_to_SQL_2010.sql'
    dataPath = 'Data/Reservation/2010.csv'
    colNames = ["HistoricalReservationID","OrderNumber","Agency","OrgID","CodeHierarchy","RegionCode","RegionDescription","ParentLocationID","ParentLocation","LegacyFacilityID","Park","SiteType","UseType","ProductID","EntityType","EntityID","FacilityID","FacilityZIP","FacilityState","FacilityLongitude","FacilityLatitude","CustomerZIP","CustomerState","CustomerCountry","Tax","UseFee","TranFee","AttrFee","TotalBeforeTax","TotalPaid","StartDate","EndDate","OrderDate","NumberOfPeople","Tent","Popup","Trailer","RVMotorhome","Boat","HorseTrailer","Car","FifthWheel","Van","CanoeKayak","BoatTrailer","Motorcycle","Truck","Bus","Bicycle","Snowmobile","OffRoadlAllTerrainVehicle","PowerBoat","PickupCamper","LargeTentOver9x12","SmallTent","Marinaboat"]
    
    addTable(tableName,loadPath,dataPath,colNames,cursor,conn) 
    
    #Add 2009 reservations
    tableName = 'Recreation_2009'
    loadPath = 'Loading/Loading_TXT_to_SQL_2009.sql'
    dataPath = 'Data/Reservation/2009.csv'
    colNames = ["HistoricalReservationID","OrderNumber","Agency","OrgID","CodeHierarchy","RegionCode","RegionDescription","ParentLocationID","ParentLocation","LegacyFacilityID","Park","SiteType","UseType","ProductID","EntityType","EntityID","FacilityID","FacilityZIP","FacilityState","FacilityLongitude","FacilityLatitude","CustomerZIP","CustomerState","CustomerCountry","Tax","UseFee","TranFee","AttrFee","TotalBeforeTax","TotalPaid","StartDate","EndDate","OrderDate","NumberOfPeople","Tent","Popup","Trailer","RVMotorhome","Boat","HorseTrailer","Car","FifthWheel","Van","CanoeKayak","BoatTrailer","Motorcycle","Truck","Bus","Bicycle","Snowmobile","OffRoadlAllTerrainVehicle","PowerBoat","PickupCamper","LargeTentOver9x12","SmallTent","Marinaboat"]
    
    addTable(tableName,loadPath,dataPath,colNames,cursor,conn) 
    
    #Add 2008 reservations
    tableName = 'Recreation_2008'
    loadPath = 'Loading/Loading_TXT_to_SQL_2008.sql'
    dataPath = 'Data/Reservation/2008.csv'
    colNames = ["HistoricalReservationID","OrderNumber","Agency","OrgID","CodeHierarchy","RegionCode","RegionDescription","ParentLocationID","ParentLocation","LegacyFacilityID","Park","SiteType","UseType","ProductID","EntityType","EntityID","FacilityID","FacilityZIP","FacilityState","FacilityLongitude","FacilityLatitude","CustomerZIP","CustomerState","CustomerCountry","Tax","UseFee","TranFee","AttrFee","TotalBeforeTax","TotalPaid","StartDate","EndDate","OrderDate","NumberOfPeople","Tent","Popup","Trailer","RVMotorhome","Boat","HorseTrailer","Car","FifthWheel","Van","CanoeKayak","BoatTrailer","Motorcycle","Truck","Bus","Bicycle","Snowmobile","OffRoadlAllTerrainVehicle","PowerBoat","PickupCamper","LargeTentOver9x12","SmallTent","Marinaboat"]
    
    addTable(tableName,loadPath,dataPath,colNames,cursor,conn) 
    
    #Add 2007 reservations
    tableName = 'Recreation_2007'
    loadPath = 'Loading/Loading_TXT_to_SQL_2007.sql'
    dataPath = 'Data/Reservation/2007.csv'
    colNames = ["HistoricalReservationID","OrderNumber","Agency","OrgID","CodeHierarchy","RegionCode","RegionDescription","ParentLocationID","ParentLocation","LegacyFacilityID","Park","SiteType","UseType","ProductID","EntityType","EntityID","FacilityID","FacilityZIP","FacilityState","FacilityLongitude","FacilityLatitude","CustomerZIP","CustomerState","CustomerCountry","Tax","UseFee","TranFee","AttrFee","TotalBeforeTax","TotalPaid","StartDate","EndDate","OrderDate","NumberOfPeople","Tent","Popup","Trailer","RVMotorhome","Boat","HorseTrailer","Car","FifthWheel","Van","CanoeKayak","BoatTrailer","Motorcycle","Truck","Bus","Bicycle","Snowmobile","OffRoadlAllTerrainVehicle","PowerBoat","PickupCamper","LargeTentOver9x12","SmallTent","Marinaboat"]
    
    addTable(tableName,loadPath,dataPath,colNames,cursor,conn) 
    
    #Add 2006 reservations
    tableName = 'Recreation_2006'
    loadPath = 'Loading/Loading_TXT_to_SQL_2006.sql'
    dataPath = 'Data/Reservation/2006.csv'
    colNames = ["HistoricalReservationID","OrderNumber","Agency","OrgID","CodeHierarchy","RegionCode","RegionDescription","ParentLocationID","ParentLocation","LegacyFacilityID","Park","SiteType","UseType","ProductID","EntityType","EntityID","FacilityID","FacilityZIP","FacilityState","FacilityLongitude","FacilityLatitude","CustomerZIP","CustomerState","CustomerCountry","Tax","UseFee","TranFee","AttrFee","TotalBeforeTax","TotalPaid","StartDate","EndDate","OrderDate","NumberOfPeople","Tent","Popup","Trailer","RVMotorhome","Boat","HorseTrailer","Car","FifthWheel","Van","CanoeKayak","BoatTrailer","Motorcycle","Truck","Bus","Bicycle","Snowmobile","OffRoadlAllTerrainVehicle","PowerBoat","PickupCamper","LargeTentOver9x12","SmallTent","Marinaboat"]
    
    addTable(tableName,loadPath,dataPath,colNames,cursor,conn) 
    # Close connection
    cursor.close()
    conn.close()

def replaceBrackets(string):
    return string.replace("[","(").replace("]",")").replace("'","")
    
def addTable(tableName,loadPath,dataPath,colNames,cursor,conn):
    
    
    # Run predefined table creation
    qry = open(loadPath, 'r').read()
    try: 
        cursor.executescript(qry)
    except:
        print (tableName + ' already present')
        return

    # Prepare load query
    
    colNamesSql = replaceBrackets(str(colNames))
    
    questionMarks = []
    for i in colNames:
        questionMarks.append('?')
    questionMarksSql = replaceBrackets(str(questionMarks))
    
    loadQry = "INSERT INTO " + tableName + " " + colNamesSql + " VALUES "+ questionMarksSql + ";"
    
    # Open .csv and import row-by-row into the 
    
#    with open(dataPath,'r') as fin:
#        reader = csv.reader(fin)
#        for row in reader:
#            to_db =[]
#            for cell in row:
#                to_db.append(cell)
#            cursor.execute(loadQry, to_db)
            
    #Modified approach to deals with undedited files        
    with open(dataPath,'r') as fin:
        reader = csv.DictReader(fin) #Pulls in CSV with headers as dict fieldnames
        #names = reader.fieldnames #show field names for debug
        for row in reader:
            to_db =[]
#            print(names)   #More debugging
#            print("Heres the test")
#            print(row[names[1]])
            for i in range(0,len(colNames)): #iterate through colNames supplied in colNames for each Table
#                print("cell level testing") #debugging
#                print (i)
#                print((row[names[i]]))
                to_db.append(row[colNames[i]]) #Only columns in row that have a name specified in colNames
            cursor.execute(loadQry, to_db)

    conn.commit()
    print (tableName + ' loaded')
    
main()