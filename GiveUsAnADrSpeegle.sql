CREATE DATABASE IF NOT EXISTS `GiveUsAnADrSpeegle`;
USE `GiveUsAnADrSpeegle`;

/* Drop tables */
DROP TABLE IF EXISTS Teams;
DROP TABLE IF EXISTS People;

CREATE TABLE Teams (
	year int(11) NOT NULL,
    teamID varchar(3) NOT NULL,
    name varchar(50),
    G smallint(6),
    Ghome smallint(6),
    W smallint(6),
    L smallint(6),
    # Caught cheating???
    primary key (year, teamID)
);

CREATE TABLE People (
    personID varchar(9) NOT NULL,
    nameFirst varchar(255),
    nameLast varchar(255),
    birthYear int(11),
    birthMonth int(11),
    birthDay int(11),
    deathYear int(11),
    deathMonth int(11),
    deathDay int(11),
    weight int(11),
    height int(11),
    birthCountry varchar(255),
    birthState varchar(255),
    birthCity varchar(255),
    deathCountry varchar(255),
    deathState varchar(255),
    deathCity varchar(255),
    #salary double,

    primary key (personID)
);
