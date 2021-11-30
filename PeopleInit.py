import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, MetaData, create_engine
from strFuncs import emptyIntNone, emptyStrNone, emptyFloatNone

Base = declarative_base()


class Person(Base):
    __tablename__ = "People"

    personID = Column(String(9), primary_key=True)
    nameFirst = Column(String(255))
    nameLast = Column(String(255))
    birthYear = Column(Integer)
    birthMonth = Column(Integer)
    birthDay = Column(Integer)
    deathYear = Column(Integer)
    deathMonth = Column(Integer)
    deathDay = Column(Integer)
    weight = Column(Integer)
    height = Column(Integer)
    birthCountry = Column(String(255))
    birthState = Column(String(255))
    birthCity = Column(String(255))
    deathCountry = Column(String(255))
    deathState = Column(String(255))
    deathCity = Column(String(255))
    #salary = Column(Numeric)


    def __init__(self, line):
        data = line.split(",")

        self.personID = emptyStrNone(data[0])
        self.nameFirst = emptyStrNone(data[13])
        self.nameLast = emptyStrNone(data[14])
        self.birthYear = emptyIntNone(data[1])
        self.birthMonth = emptyIntNone(data[2])
        self.birthDay = emptyIntNone(data[3])
        self.deathYear = emptyIntNone(data[7])
        self.deathMonth = emptyIntNone(data[8])
        self.deathDay = emptyIntNone(data[9])
        self.weight = emptyIntNone(data[16])
        self.height = emptyIntNone(data[17])
        self.birthCountry = emptyStrNone(data[4])
        self.birthState = emptyStrNone(data[5])
        self.birthCity = emptyStrNone(data[6])
        self.deathCountry = emptyStrNone(data[10])
        self.deathState = emptyStrNone(data[11])
        self.deathCity = emptyStrNone(data[12])
        #self.salary = emptyStrNone(data[])


user = "root"
pWord = sys.argv[1]
host = "localhost"
db = "GiveUsAnADrSpeegle"

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
