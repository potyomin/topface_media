CREATE DATABASE IF NOT EXISTS topface_media;
USE topface_media;

CREATE TABLE shipments (
  id        VARCHAR(64),
  month     CHAR(7),
  shipment  DECIMAL(15,2)
);

CREATE TABLE projects_dim (
  id         VARCHAR(64),
  month_last CHAR(7), 
  AM         VARCHAR(255),
  Account    VARCHAR(255)
);