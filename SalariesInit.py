from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, create_engine, Date
from strFuncs import *

Base = declarative_base()


class Salary(Base):
    __tablename__ = "Salaries"
    personID = Column(String(9), primary_key=True)
    year = Column(Integer, primary_key=True)
    teamID = Column(String(3), primary_key=True)
    Salary = Column(Numeric)

    def __init__(self, line):
        data = line.split(",")

        self.personID = emptyStrNone(data[3])
        self.year = emptyIntNone(data[0])
        self.teamID = emptyStrNone(data[1])
        self.Salary = emptyFloatNone(data[4])


def initSalariesTable():
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
    session.execute("TRUNCATE TABLE Salaries")
    session.commit()

    # open file and skip the first line
    f = open("./baseballdatabank/core/Salaries.csv", "r")
    next(f)

    for line in f:
        # insert the team to the table
        session.add(Salary(line))

    # commit changes and close the connection
    session.commit()
    session.close()


initSalariesTable()
