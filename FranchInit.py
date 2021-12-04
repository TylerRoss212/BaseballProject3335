import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, MetaData, create_engine
from strFuncs import emptyIntNone, emptyStrNone, emptyFloatNone
import CSI3335Fall2021 as cfg

Base = declarative_base()


class Franchise(Base):
    __tablename__ = "Franchises"
    franchID = Column(String(3), primary_key=True)
    franchName = Column(String(50))
    active = Column(String(1))
    NAassoc = Column(String(3))

    def __init__(self, line):
        data = line.split(",")
        self.franchID = emptyStrNone(data[0])
        self.franchName = emptyStrNone(data[1])
        self.active = emptyStrNone(data[2])
        self.NAassoc = emptyStrNone(data[3])


def initFranchisesTable():
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
    session.execute("TRUNCATE TABLE Franchises")
    session.commit()

    # open file and skip the first line
    f = open("./baseballdatabank/core/TeamsFranchises.csv", "r")
    next(f)

    for line in f:
        # insert the team to the table
        session.add(Franchise(line))

    # commit changes and close the connection
    session.commit()
    session.close()

initFranchisesTable()
