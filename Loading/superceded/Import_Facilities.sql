--find way to pull fields from csv, maybe using python??
--sqlcmd -S CLAYMANB41301\SQLEXPRESS -i C:\Work\2016_01_14_Brazil_Data\SQL\Basic_Select_All_Years.sql -o output if needed
.mode csv ,
.import Facilities_API_v1_edited.csv Facilities
