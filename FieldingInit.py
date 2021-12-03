import sys
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, create_engine, Date
from strFuncs import *

Base = declarative_base()


class FieldingData(Base):
    __tablename__ = "FieldingStats"
    fieldingID = Column(String(23), primary_key=True)
    teamID = Column(String(3))
    POS = Column(String(2))
    G = Column(Integer)
    GS = Column(Integer)
    InnOuts = Column(Integer)
    PO = Column(Integer)
    A = Column(Integer)
    E = Column(Integer)
    DP = Column(Integer)
    PB = Column(Integer)
    WP = Column(Integer)
    SB = Column(Integer)
    CS = Column(Integer)
    ZR = Column(Numeric)

    def __init__(self, line):
        data = line.split(",")

        self.fieldingID = self.pitchingID = data[0] + "F" + data[1] + "-" + data[5] + "-" + data[2]
        self.teamID = emptyStrNone(data[3])
        self.POS = emptyStrNone(data[5])
        self.G = emptyIntNone(data[6])
        self.GS = emptyIntNone(data[7])
        self.InnOuts = emptyIntNone(data[8])
        self.PO = emptyIntNone(data[9])
        self.A = emptyIntNone(data[10])
        self.E = emptyIntNone(data[11])
        self.DP = emptyIntNone(data[12])
        self.PB = emptyIntNone(data[13])
        self.WP = emptyIntNone(data[14])
        self.SB = emptyIntNone(data[15])
        self.CS = emptyIntNone(data[16])
        self.ZR = emptyFloatNone(data[17])


def initFieldingStatsTable():
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
    session.execute("TRUNCATE TABLE FieldingStats")
    session.commit()

    # open file and skip the first line
    f = open("./baseballdatabank/core/Fielding.csv", "r")
    next(f)

    for line in f:
        # insert the team to the table
        session.add(FieldingData(line))

    # commit changes and close the connection
    session.commit()
    session.close()


initFieldingStatsTable()
