## Setup
1. Ensure you have Sqlite3 installed and available to your python scripts. Python 3.6 with the PANDAS v0.20 package is also needed to run these scripts
2. Download RIDB and Recreation.gov reservations csv files from https://ridb.recreation.gov/?action=datadownload and place into a "Data" folder alongside repo code.
3. Run loading.py to create the SQLite database from the downloaded data files. As is, loading.py is set up to load all Reservation files from 2006 until 2015. If you want to only load certain years, comment out the "addTable" line in the section for unwanted years. Note: To add additional years Loading.py must be modified to add a new table based to the reservation csv file (e.g. "2015.csv", "2014.csv" etc). A loading path must also be added (e.g. "Loading_TXT_to_SQL_2014.sql)

## Running the Analysis
1. Based on the level you want to run the analysis on, open the appropriate file:
  -Agency Level Report (e.g. USFS, NPS, etc) -> Agency_report_excel.py
  -Recreation Area Level Report -> RecArea_report_excel.py
  -Facility Level Report (most granular level of report) -> Facility_report_excel.py
2. Within a given script you can change the specifics how the analysis is run in terms of year(s) and IDs of specific agencies, recareas, and facililties you want to run the analysis on
3. Once the parameters have been set, run the script and an excel workbook will be created within a directory of the "output" folder with various sheets of analysis
