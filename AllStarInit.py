import sys
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, create_engine, Date
from strFuncs import *
import CSI3335Fall2021 as cfg

Base = declarative_base()


class AllStar(Base):
    __tablename__ = "AllStar"
    peopleID = Column(String(9), primary_key=True)
    year = Column(Integer, primary_key=True)
    gameNum = Column(Integer)
    teamID = Column(String(3))
    lgID = Column(String(2))
    GP = Column(Integer)
    startingPos = Column(Integer)



    def __init__(self, line):
        data = line.split(",")

        self.peopleID = emptyStrNone(data[0])
        self.year = emptyStrNone(data[1])
        self.gameNum = emptyIntNone(data[2])
        self.teamID = emptyStrNone(data[4])
        self.lgID = emptyStrNone(data[5])
        self.GP = emptyIntNone(data[6])
        self.startingPos = emptyIntNone(data[7])


def initAllStarTable():
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
    session.execute("TRUNCATE TABLE Allstar")
    session.commit()

    # open file and skip the first line
    f = open("./baseballdatabank/core/AllstarFull.csv", "r")
    next(f)

    for line in f:
        # insert the team to the table
        data = line.split(",")
        ASG = session.query(AllStar).filter_by(peopleID = data[0], year = data[1]).first()
        if not ASG:
            session.add(AllStar(line))

    # commit changes and close the connection
    session.commit()
    session.close()


initAllStarTable()
