CREATE DATABASE IF NOT EXISTS `GiveUsAnADrSpeegle`;
USE `GiveUsAnADrSpeegle`;

/* Drop tables */
DROP TABLE IF EXISTS Teams;
DROP TABLE IF EXISTS People;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Parks;
DROP TABLE IF EXISTS WorldSeries;
DROP TABLE IF EXISTS Players;
DROP TABLE IF EXISTS BattingStats;
DROP TABLE IF EXISTS PitchingStats;

CREATE TABLE Teams (
	year int(11) NOT NULL,
    teamID varchar(3) NOT NULL,
    name varchar(50),
    G smallint(6),
    Ghome smallint(6),
    W smallint(6),
    L smallint(6),
    attendance int(11),
    # Caught cheating???
    primary key (year, teamID)
);

CREATE TABLE People (
    personID varchar(9) NOT NULL,
    nameFirst varchar(255),
    nameLast varchar(255),
    birthDate date,
    deathDate date,
    weight int(11),
    height int(11),
    birthCountry varchar(255),
    birthState varchar(255),
    birthCity varchar(255),
    deathCountry varchar(255),
    deathState varchar(255),
    deathCity varchar(255),
    debut date,
    finalGame date,

    primary key (personID)
);

CREATE TABLE Users (
    username varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    favoriteTeam varchar(3),

    primary key (username)
);

CREATE TABLE Parks(
    parkKey varchar(255) NOT NULL,
    parkName varchar(255),
    city varchar(255),
    state varchar(255),
    country varchar(255),

    primary key (parkKey)
);

CREATE TABLE WorldSeries(
    year int(11) NOT NULL,
    winner char(3),
    loser char(3),
    series char(3),

    primary key (year)
);

CREATE TABLE Players(
    personID varchar(9) NOT NULL,
    year smallint(6) NOT NULL,
    stint smallint(6) NOT NULL,
    battingID varchar(23),
    pitchingID varchar(23),
    fieldingID varchar(23),

    primary key (personID, year, stint)
);


CREATE TABLE BattingStats(
    battingID varchar(23) NOT NULL,
    teamID char(3),
    G smallint(6),
    AB smallint(6),
    R smallint(6),
    H smallint(6),
    twoB smallint(6),
    threeB smallint(6),
    HR smallint(6),
    RBI smallint(6),
    SB smallint(6),
    CS smallint(6),
    BB smallint(6),
    SO smallint(6),
    IBB smallint(6),
    HBP smallint(6),
    SH smallint(6),
    SF smallint(6),
    GIDP smallint(6),

    primary key (battingID)
);

CREATE TABLE PitchingStats(
    pitchingID varchar(23) NOT NULL,
    teamID char(3),
    W smallint(6),
    L smallint(6),
    G smallint(6),
    GS smallint(6),
    CG smallint(6),
    SHO smallint(6),
    SV smallint(6),
    IPouts int(11),
    H smallint(6),
    ER smallint(6),
    HR smallint(6),
    BB smallint(6),
    SO smallint(6),
    BAOpp double,
    ERA double,
    IBB  smallint(6),
    WP smallint(6),
    HBP smallint(6),
    BK smallint(6),
    BFP smallint(6),
    GF smallint(6),
    R smallint(6),
    SH smallint(6),
    SF smallint(6),
    GIDP smallint(6),

    primary key (pitchingID)
);


