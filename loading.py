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
	dataPath = 'Data/RecAreas_API_v1_edited.csv'
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
	dataPath = 'Data/Facilities_API_v1_edited.csv'
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
		print tableName + ' already present'
		return

	# Prepare load query
	
	colNamesSql = replaceBrackets(str(colNames))
	
	questionMarks = []
	for i in colNames:
		questionMarks.append('?')
	questionMarksSql = replaceBrackets(str(questionMarks))
	
	loadQry = "INSERT INTO " + tableName + " " + colNamesSql + " VALUES "+ questionMarksSql + ";"
	
	# Open .csv and import row-by-row into the 
	
	with open(dataPath,'r') as fin:
		reader = csv.reader(fin)
		for row in reader:
			to_db =[]
			for cell in row:
				to_db.append(cell)
			cursor.execute(loadQry, to_db)

	conn.commit()
	print tableName + ' loaded'
	
main()