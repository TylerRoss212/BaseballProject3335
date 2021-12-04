import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, MetaData, create_engine
from strFuncs import emptyIntNone, emptyStrNone, emptyFloatNone
import CSI3335Fall2021 as cfg

Base = declarative_base()


class CaughtCheating(Base):
    __tablename__ = "CaughtCheating"
    teamID = Column(String(9), primary_key=True)
    year = Column(Integer, primary_key=True)
    description = Column(String(255))

    def __init__(self, line):
        data = line.split(",")
        self.teamID = data[0]
        self.year = data[1]
        self.description = data[2]


def initCaughtCheatingTable():
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
    session.execute("TRUNCATE TABLE CaughtCheating")
    session.commit()

    # open file and skip the first line
    f = open("./baseballdatabank/core/caughtCheating.csv", "r")
    next(f)

    for line in f:
        # insert the team to the table
        session.add(CaughtCheating(line))

    # commit changes and close the connection
    session.commit()
    session.close()

initCaughtCheatingTable()
