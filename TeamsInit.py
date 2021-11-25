import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, MetaData, create_engine

Base = declarative_base()

class Team(Base):
    __tablename__ = "Teams"
    yearID = Column(Integer, primary_key=True)
    lgID = Column(String(2))
    teamID = Column(String(3), primary_key=True)
    franchID = Column(String(3))
    divID = Column(String(1))  # may need to be an integer to correspond with div_ID
    Rank = Column(Integer)
    G = Column(Integer)
    Ghome = Column(Integer)
    W = Column(Integer)
    L = Column(Integer)
    DivWin = Column(String(1))
    WCWin = Column(String(1))
    LgWin = Column(String(1))
    WSWin = Column(String(1))
    R = Column(Integer)
    AB = Column(Integer)
    H = Column(Integer)
    twoB = Column(Integer)
    threeB = Column(Integer)
    HR = Column(Integer)
    BB = Column(Integer)
    SO = Column(Integer)
    SB = Column(Integer)
    CS = Column(Integer)
    HBP = Column(Integer)
    SF = Column(Integer)
    RA = Column(Integer)
    ER = Column(Integer)
    ERA = Column(Numeric)
    CG = Column(Integer)
    SHO = Column(Integer)
    SV = Column(Integer)
    IPouts = Column(Integer)
    HA = Column(Integer)
    HRA = Column(Integer)
    BBA = Column(Integer)
    SOA = Column(Integer)
    E = Column(Integer)
    DP = Column(Integer)
    FP = Column(Numeric)
    name = Column(String(50))
    park = Column(String(255))
    attendance = Column(Integer)
    BPF = Column(Integer)
    PPF = Column(Integer)
    teamIDBR = Column(String(3))
    teamIDlahman45 = Column(String(3))
    teamIDretro = Column(String(3))

    def __init__(self, line):
        data = line.split(",")
        self.yearID = emptyIntNone(data[0])
        self.lgID = emptyStrNone(data[1])
        self.teamID = emptyStrNone(data[2])
        self.franchID = emptyStrNone(data[3])
        self.divID = emptyStrNone(data[4])  # may need to be an integer to correspond with div_ID
        self.Rank = emptyIntNone(data[5])
        self.G = emptyIntNone(data[6])
        self.Ghome = emptyIntNone(data[7])
        self.W = emptyIntNone(data[8])
        self.L = emptyIntNone(data[9])
        self.DivWin = emptyStrNone(data[10])
        self.WCWin = emptyStrNone(data[11])
        self.LgWin = emptyStrNone(data[12])
        self.WSWin = emptyStrNone(data[13])
        self.R = emptyIntNone(data[14])
        self.AB = emptyIntNone(data[15])
        self.H = emptyIntNone(data[16])
        self.twoB = emptyIntNone(data[17])
        self.threeB = emptyIntNone(data[18])
        self.HR = emptyIntNone(data[19])
        self.BB = emptyIntNone(data[20])
        self.SO = emptyIntNone(data[21])
        self.SB = emptyIntNone(data[22])
        self.CS = emptyIntNone(data[23])
        self.HBP = emptyIntNone(data[24])
        self.SF = emptyIntNone(data[25])
        self.RA = emptyIntNone(data[26])
        self.ER = emptyIntNone(data[27])
        self.ERA = emptyFloatNone(data[28])
        self.CG = emptyIntNone(data[29])
        self.SHO = emptyIntNone(data[30])
        self.SV = emptyIntNone(data[31])
        self.IPouts = emptyIntNone(data[32])
        self.HA = emptyIntNone(data[33])
        self.HRA = emptyIntNone(data[34])
        self.BBA = emptyIntNone(data[35])
        self.SOA = emptyIntNone(data[36])
        self.E = emptyIntNone(data[37])
        self.DP = emptyIntNone(data[38])
        self.FP = emptyFloatNone(data[39])
        self.name = emptyStrNone(data[40])
        self.park = emptyStrNone(data[41])
        self.attendance = emptyIntNone(data[42])
        self.BPF = emptyIntNone(data[43])
        self.PPF = emptyIntNone(data[44])
        self.teamIDBR = emptyStrNone(data[45])
        self.teamIDlahman45 = emptyStrNone(data[46])
        self.teamIDretro = emptyStrNone(data[47])


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
db = "baseball2"

# configure engine
engineStr = "mysql+pymysql://" + user + ":" + pWord + "@" + host + ":3306/" + db
engine = create_engine(engineStr)

# drop all instances of the Teams table, this is only for testing purposes
Base.metadata.drop_all(engine)

# create an instance of the Teams table
Base.metadata.create_all(engine)

# configure session
Session = sessionmaker(bind=engine)
session = Session()

# open file and skip the first line
f = open("./baseballdatabank/core/Teams.csv", "r")
next(f)

for line in f:
    # insert the team to the table
    session.add(Team(line))

# commit changes and close the connection
session.commit()
session.close()
