import sys
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, create_engine, Date
from strFuncs import *
import CSI3335Fall2021 as cfg

Base = declarative_base()


class Manager(Base):
    __tablename__ = "Managers"
    personID = Column(String(9), primary_key=True)
    year = Column(Integer, primary_key=True)
    teamID = Column(String(3), primary_key=True)
    lgID = Column(String(2))
    inseason = Column(Integer)
    G = Column(Integer)
    W = Column(Integer)
    L = Column(Integer)
    rank = Column(Integer)
    plyrMgr = Column(String(1))

    def __init__(self, line):
        data = line.split(",")

        self.personID = emptyStrNone(data[0])
        self.year = emptyIntNone(data[1])
        self.teamID = emptyStrNone(data[2])
        self.lgID = emptyStrNone(data[3])
        self.inseason = emptyIntNone(data[4])
        self.G = emptyIntNone(data[5])
        self.W = emptyIntNone(data[6])
        self.L = emptyIntNone(data[7])
        self.rank = emptyIntNone(data[8])
        self.plyrMgr = emptyStrNone(data[9])






def initManagersTable():
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
    session.execute("TRUNCATE TABLE Managers")
    session.commit()

    # open file and skip the first line
    f = open("./baseballdatabank/core/Managers.csv", "r")
    next(f)

    for line in f:
        # insert the team to the table
        data = line.split(",")
        man = session.query(Manager).filter_by(personID = data[0], year = data[1], teamID = data[2]).first()
        if not man:
            session.add(Manager(line))

    # commit changes and close the connection
    session.commit()
    session.close()


initManagersTable()
