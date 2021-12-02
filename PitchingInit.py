import sys
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, create_engine, Date
from strFuncs import *

Base = declarative_base()


class PitchingData(Base):
    __tablename__ = "PitchingStats"
    pitchingID = Column(String(23), primary_key=True)
    teamID = Column(String(3))
    W = Column(Integer)
    L = Column(Integer)
    G = Column(Integer)
    GS = Column(Integer)
    CG = Column(Integer)
    SHO = Column(Integer)
    SV = Column(Integer)
    IPouts = Column(Integer)
    H = Column(Integer)
    ER = Column(Integer)
    HR = Column(Integer)
    BB = Column(Integer)
    SO = Column(Integer)
    BAOpp = Column(Numeric)
    ERA = Column(Numeric)
    IBB = Column(Integer)
    WP = Column(Integer)
    HBP = Column(Integer)
    BK = Column(Integer)
    BFP = Column(Integer)
    GF = Column(Integer)
    R = Column(Integer)
    SH = Column(Integer)
    SF = Column(Integer)
    GIDP = Column(Integer)

    def __init__(self, line):
        data = line.split(",")

        self.pitchingID = data[0] + "P" + data[1] + "-" + data[2]
        self.teamID = emptyStrNone(data[3])
        self.W = emptyIntNone(data[5])
        self.L = emptyIntNone(data[6])
        self.G = emptyIntNone(data[7])
        self.GS = emptyIntNone(data[8])
        self.CG = emptyIntNone(data[9])
        self.SHO = emptyIntNone(data[10])
        self.SV = emptyIntNone(data[11])
        self.IPouts = emptyIntNone(data[12])
        self.H = emptyIntNone(data[13])
        self.ER = emptyIntNone(data[14])
        self.HR = emptyIntNone(data[15])
        self.BB = emptyIntNone(data[16])
        self.SO = emptyIntNone(data[17])
        self.BAOpp = emptyFloatNone(data[18])
        self.ERA = emptyFloatNone(data[19])
        self.IBB = emptyIntNone(data[20])
        self.WP = emptyIntNone(data[21])
        self.HBP = emptyIntNone(data[22])
        self.BK = emptyIntNone(data[23])
        self.BFP = emptyIntNone(data[24])
        self.GF = emptyIntNone(data[25])
        self.R = emptyIntNone(data[26])
        self.SH = emptyIntNone(data[27])
        self.SF = emptyIntNone(data[28])
        self.GIDP = emptyIntNone(data[29])







def initPitchingStatsTable():
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
    session.execute("TRUNCATE TABLE PitchingStats")
    session.commit()

    # open file and skip the first line
    f = open("./baseballdatabank/core/Pitching.csv", "r")
    next(f)

    for line in f:
        # insert the team to the table
        session.add(PitchingData(line))

    # commit changes and close the connection
    session.commit()
    session.close()


initPitchingStatsTable()
