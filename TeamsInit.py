import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, MetaData, create_engine

Base = declarative_base()

class Team(Base):
    __tablename__ = "Teams"
    year = Column(Integer, primary_key=True)
    teamID = Column(String(3), primary_key=True)
    name = Column(String(50))
    G = Column(Integer)
    Ghome = Column(Integer)
    W = Column(Integer)
    L = Column(Integer)


    def __init__(self, line):
        data = line.split(",")
        self.year = emptyIntNone(data[0])
        self.teamID = emptyStrNone(data[2])
        self.G = emptyIntNone(data[6])
        self.Ghome = emptyIntNone(data[7])
        self.W = emptyIntNone(data[8])
        self.L = emptyIntNone(data[9])

        # kept in so i dont have to count column names if we want to reuse this lol
        # self.LgWin = emptyStrNone(data[12])
        # self.WSWin = emptyStrNone(data[13])
        # self.R = emptyIntNone(data[14])
        # self.AB = emptyIntNone(data[15])
        # self.H = emptyIntNone(data[16])
        # self.twoB = emptyIntNone(data[17])
        # self.threeB = emptyIntNone(data[18])
        # self.HR = emptyIntNone(data[19])
        # self.BB = emptyIntNone(data[20])
        # self.SO = emptyIntNone(data[21])
        # self.SB = emptyIntNone(data[22])
        # self.CS = emptyIntNone(data[23])
        # self.HBP = emptyIntNone(data[24])
        # self.SF = emptyIntNone(data[25])
        # self.RA = emptyIntNone(data[26])
        # self.ER = emptyIntNone(data[27])
        # self.ERA = emptyFloatNone(data[28])
        # self.CG = emptyIntNone(data[29])
        # self.SHO = emptyIntNone(data[30])
        # self.SV = emptyIntNone(data[31])
        # self.IPouts = emptyIntNone(data[32])
        # self.HA = emptyIntNone(data[33])
        # self.HRA = emptyIntNone(data[34])
        # self.BBA = emptyIntNone(data[35])
        # self.SOA = emptyIntNone(data[36])
        # self.E = emptyIntNone(data[37])
        # self.DP = emptyIntNone(data[38])
        # self.FP = emptyFloatNone(data[39])
        self.name = emptyStrNone(data[40])
        # self.park = emptyStrNone(data[41])
        # self.attendance = emptyIntNone(data[42])
        # self.BPF = emptyIntNone(data[43])
        # self.PPF = emptyIntNone(data[44])
        # self.teamIDBR = emptyStrNone(data[45])
        # self.teamIDlahman45 = emptyStrNone(data[46])
        # self.teamIDretro = emptyStrNone(data[47])


def emptyIntNone(dataStr):
    if dataStr == "":
        return None
    else:
        return int(dataStr)


def emptyStrNone(dataStr):
    if dataStr == "":
        return None
    else:
        return dataStr


def emptyFloatNone(dataStr):
    if dataStr == "":
        return None
    else:
        return float(dataStr)


# get database login info
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
session.execute("TRUNCATE TABLE Teams")
session.commit()

# open file and skip the first line
f = open("./baseballdatabank/core/Teams.csv", "r")
next(f)

for line in f:
    # insert the team to the table
    session.add(Team(line))

# commit changes and close the connection
session.commit()
session.close()
