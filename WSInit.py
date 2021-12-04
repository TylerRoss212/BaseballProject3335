import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, MetaData, create_engine
from strFuncs import emptyIntNone, emptyStrNone, emptyFloatNone
import CSI3335Fall2021 as cfg

Base = declarative_base()


class WorldSeries(Base):
    __tablename__ = "WorldSeries"
    year = Column(Integer, primary_key=True)
    winner = Column(String(3))
    loser = Column(String(3))
    series = Column(String(3))







    def __init__(self, line):
        data = line.split(",")

        self.year = emptyIntNone(data[0])
        self.winner = emptyStrNone(data[1])
        self.loser = emptyStrNone(data[2])
        self.series = emptyStrNone(data[3])

def initWorldSeriesTable():
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
    session.execute("TRUNCATE TABLE WorldSeries")
    session.commit()

    # open file and skip the first line
    f = open("./baseballdatabank/core/WorldSeries.csv", "r")
    next(f)

    for line in f:
        # insert the team to the table
        session.add(WorldSeries(line))

    # commit changes and close the connection
    session.commit()
    session.close()


initWorldSeriesTable()
