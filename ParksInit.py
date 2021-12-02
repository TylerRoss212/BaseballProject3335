import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, MetaData, create_engine
from strFuncs import emptyIntNone, emptyStrNone, emptyFloatNone

Base = declarative_base()

class Park(Base):
    __tablename__ = "Parks"
    parkKey = Column(String(255), primary_key=True)
    parkName = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    country = Column(String(255))

    def __init__(self, line):
        data = line.split(",")
        self.parkKey = emptyStrNone(data[0])
        self.parkName = emptyStrNone(data[1])
        self.city = emptyStrNone(data[3])
        self.state = emptyStrNone(data[4])
        self.country = emptyStrNone(data[5])


user = "root"
if len(sys.argv) == 1:
    pWord = ""
else:
    pWord = sys.argv[1]

host = "localhost"
db = "GiveUsAnADrSpeegle"

# configure engine and session
engineStr = "mysql+pymysql://" + user + ":" + pWord + "@" + host + ":3306/" + db
engine = create_engine(engineStr)
Session = sessionmaker(bind=engine)
session = Session()

# TEST: deletes all data in the table
session.execute("TRUNCATE TABLE Parks")
session.commit()

# open file and skip the first line
f = open("./baseballdatabank/core/Parks.csv", "r")
next(f)

for line in f:
    # insert the team to the table
    session.add(Park(line))

# commit changes and close the connection
session.commit()
session.close()
