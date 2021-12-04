# BaseballProject3335
To create database: login to dbms and type "\. GiveUsAnADrSpeegle.sql" 
To initialize data: run dbInit.py (please note that this may take awhile)

To run:
	export FLASK_APP=app.py;
	flask run

	the app should be running on localhost:5000
	
Understanding basic functionality of the application:
	- Create a user by signup (this stores the User in the database)
	- Login to account after created
		- If account does not exist it will prompt you to try again or go to home page
	- On the dashboard, you can see who you are logged in as and your current favorite team
		- You can also edit your favorite team with the dropdown and pressing confirm
	- To display standings, league winners, and world series info...select a year from the drop down and press Submit
	*NOTE: To navigate back to the dashboard, just push the back arrow
	- To display roster for your favorite team, select the year you would like to see the roster for and Submit
	- To see a list of all the cheating scandals, press the "Go to Cheaters" button
	- To search for a specific batter or pitcher information, type in their name (or part of it for less specific results)

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
