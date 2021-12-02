import sys
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, create_engine, Date
from strFuncs import *

Base = declarative_base()


class Player(Base):
    __tablename__ = "Players"
    personID = Column(String(9), primary_key=True)
    year = Column(Integer, primary_key=True)
    stint = Column(Integer, primary_key=True)
    battingID = Column(String(22))
    pitchingID = Column(String(22))
    fieldingID = Column(String(22))

    def __init__(self, line):
        data = line.split(",")

        self.personID = data[0]
        self.year = data[1]
        self.stint = data[2]
        self.battingID = self.personID + "B" + self.year + "-" + self.stint
        self.pitchingID = self.personID + "P" + self.year + "-" + self.stint
        self.fieldingID = self.personID + "F" + self.year + "-" + self.stint






def initPlayersTable():
    user = "root"
    pWord = ""
    host = "localhost"
    db = "GiveUsAnADrSpeegle"

    # configure engine and session
    engineStr = "mysql+pymysql://" + user + ":" + pWord + "@" + host + ":3306/" + db
    engine = create_engine(engineStr)
    Session = sessionmaker(bind=engine)
    session = Session()

    # TEST: deletes all data in the table
    session.execute("TRUNCATE TABLE Players")
    session.commit()

    # open file and skip the first line
    f = open("./baseballdatabank/core/Batting.csv", "r")
    next(f)

    for line in f:
        # insert the team to the table
        session.add(Player(line))

    # commit changes and close the connection
    session.commit()
    session.close()


initPeopleTable()
