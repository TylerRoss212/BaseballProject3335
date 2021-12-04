import sys
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, create_engine, Date
from strFuncs import *
import CSI3335Fall2021 as cfg

Base = declarative_base()


class BattingData(Base):
    __tablename__ = "BattingStats"
    battingID = Column(String(23), primary_key=True)
    teamID = Column(String(3))
    G = Column(Integer)
    AB = Column(Integer)
    R = Column(Integer)
    H = Column(Integer)
    twoB = Column(Integer)
    threeB = Column(Integer)
    HR = Column(Integer)
    RBI = Column(Integer)
    SB = Column(Integer)
    CS = Column(Integer)
    BB = Column(Integer)
    SO = Column(Integer)
    IBB = Column(Integer)
    HBP = Column(Integer)
    SH = Column(Integer)
    SF = Column(Integer)
    GIDP = Column(Integer)

    def __init__(self, line):
        data = line.split(",")

        self.battingID = data[0] + "B" + data[1] + "-" + data[2]
        self.teamID = emptyStrNone(data[3])
        self.G = emptyIntNone(data[5])
        self.AB = emptyIntNone(data[6])
        self.R = emptyIntNone(data[7])
        self.H = emptyIntNone(data[7])
        self.twoB = emptyIntNone(data[9])
        self.threeB = emptyIntNone(data[10])
        self.HR = emptyIntNone(data[11])
        self.RBI = emptyIntNone(data[12])
        self.SB = emptyIntNone(data[13])
        self.CS = emptyIntNone(data[14])
        self.BB = emptyIntNone(data[15])
        self.SO = emptyIntNone(data[16])
        self.IBB = emptyIntNone(data[17])
        self.HBP = emptyIntNone(data[18])
        self.SH = emptyIntNone(data[19])
        self.SF = emptyIntNone(data[20])
        self.GIDP = emptyIntNone(data[21])





def initBattingStatsTable():
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
    session.execute("TRUNCATE TABLE BattingStats")
    session.commit()

    # open file and skip the first line
    f = open("./baseballdatabank/core/Batting.csv", "r")
    next(f)

    for line in f:
        # insert the team to the table
        session.add(BattingData(line))

    # commit changes and close the connection
    session.commit()
    session.close()


initBattingStatsTable()
