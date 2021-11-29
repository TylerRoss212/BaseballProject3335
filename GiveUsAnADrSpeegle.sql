CREATE DATABASE IF NOT EXISTS `GiveUsAnADrSpeegle`;
USE `GiveUsAnADrSpeegle`;

/* Drop tables */
DROP TABLE IF EXISTS Teams;

CREATE TABLE Teams (
	year int(11) NOT NULL,
    teamID varchar(3) NOT NULL,
    name varchar(50),
    G smallint(6),
    Ghome smallint(6),
    W smallint(6),
    L smallint(6),
   
    primary key (year, teamID)
)