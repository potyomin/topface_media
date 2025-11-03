USE topface_media;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/chipments.csv'
INTO TABLE chipments
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','  ENCLOSED BY '"'
LINES  TERMINATED BY '\n'
IGNORE 1 LINES
(id, month, shipment);
