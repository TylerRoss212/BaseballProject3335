# BaseballProject3335
To create database: login to dbms and type "\. GiveUsAnADrSpeegle.sql" 
To initialize data: run dbInit.py (please note that this may take awhile)

To run:
	export FLASK_APP=app.py;
	flask run

	the app should be running on localhost:5000

Python modules imported:
	pymysql
	sqlalchemy
	hashlib
	sys
	datetime

Data files are located in the baseballdatabank directory
	added data files: caughtCheating.csv, WorldSeries.csv

additional work done: 
	created a cheaters page 
	series score for every world series
	added a search for batters and pitchers