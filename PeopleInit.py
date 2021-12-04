import sys
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, create_engine, Date
from strFuncs import *
import CSI3335Fall2021 as cfg

Base = declarative_base()


class Person(Base):
    __tablename__ = "People"
    personID = Column(String(9), primary_key=True)
    nameFirst = Column(String(255))
    nameLast = Column(String(255))
    birthDate = Column(Date)
    deathDate = Column(Date)
    #birthYear = Column(Integer)
    #birthMonth = Column(Integer)
    #birthDay = Column(Integer)
    #deathYear = Column(Integer)
    #deathMonth = Column(Integer)
    #deathDay = Column(Integer)
    weight = Column(Integer)
    height = Column(Integer)
    birthCountry = Column(String(255))
    birthState = Column(String(255))
    birthCity = Column(String(255))
    deathCountry = Column(String(255))
    deathState = Column(String(255))
    deathCity = Column(String(255))
    #salary = Column(Numeric)
    debut = Column(Date)
    finalGame = Column(Date)



    def __init__(self, line):
        data = line.split(",")

        self.personID = emptyStrNone(data[0])
        self.nameFirst = emptyStrNone(data[13])
        self.nameLast = emptyStrNone(data[14])
        self.birthDate = emptyDateNone(data[1], data[2], data[3])
        self.deathDate = emptyDateNone(data[7], data[8], data[9])
        #self.birthYear = emptyIntNone(data[1])
        #self.birthMonth = emptyIntNone(data[2])
        #self.birthDay = emptyIntNone(data[3])
        #self.deathYear = emptyIntNone(data[7])
        #self.deathMonth = emptyIntNone(data[8])
        #self.deathDay = emptyIntNone(data[9])
        self.weight = emptyIntNone(data[16])
        self.height = emptyIntNone(data[17])
        self.birthCountry = emptyStrNone(data[4])
        self.birthState = emptyStrNone(data[5])
        self.birthCity = emptyStrNone(data[6])
        self.deathCountry = emptyStrNone(data[10])
        self.deathState = emptyStrNone(data[11])
        self.deathCity = emptyStrNone(data[12])
        dateStr = data[20].split('-')
        try:
            self.debut = emptyDateNone(dateStr[0], dateStr[1], dateStr[2])
        except Exception:
            self.debut = None

        dateStr = data[21].split('-')
        try:
            self.finalGame = emptyDateNone(dateStr[0], dateStr[1], dateStr[2])
        except Exception:
            self.finalGame = None
        #self.salary = emptyStrNone(data[])

def initPeopleTable():
    user = cfg.mysql["user"]
    pWord = cfg.mysql["password"]
    host = cfg.mysql["host"]
    db = cfg.mysql["db"]

    # configure engine and session
    engineStr = "mysql+pymysql://" + user + ":" + pWord + "@" + host + ":3306/" + db
    engine = create_engine(engineStr)
    Session = sessionmaker(bind=engine)
    session = Session()

    # TEST: deletes all data in the table
    session.execute("TRUNCATE TABLE People")
    session.commit()

    # open file and skip the first line
    f = open("./baseballdatabank/core/People.csv", "r")
    next(f)

    for line in f:
        # insert the team to the table
        session.add(Person(line))

    # commit changes and close the connection
    session.commit()
    session.close()


initPeopleTable()
