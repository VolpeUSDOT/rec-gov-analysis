CREATE TABLE Campsites(
  "CAMPSITEACCESSIBLE" varchar(1024) NULL,
  "CAMPSITEID" INTEGER NULL,
  "CAMPSITENAME" varchar(1024) NULL,
  "CAMPSITETYPE" varchar(1024) NULL,
  "CREATEDDATE" varchar(1024) NULL,
  "FACILITYID" INTEGER NULL,
  "LASTUPDATEDDATE" varchar(1024) NULL,
  "LOOP" varchar(1024) NULL,
  "TYPEOFUSE" varchar(1024) NULL
);

.mode csv ,
.import Data/Campsites_API_v1_edited.csv Campsites