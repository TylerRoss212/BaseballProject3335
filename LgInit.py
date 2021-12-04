import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, MetaData, create_engine
from strFuncs import emptyIntNone, emptyStrNone, emptyFloatNone
import pymysql
import CSI3335Fall2021 as cfg

def initLeaguesTable():
    user = cfg.mysql["user"]
    pWord = cfg.mysql["password"]
    host = cfg.mysql["host"]
    db = cfg.mysql["db"]

    con = pymysql.connect(host=host, user=user, password=pWord, database=db)
    cur = con.cursor()

    # TEST: deletes all data in the table
    cur.execute("TRUNCATE TABLE Leagues")
    con.commit()

    sql = "INSERT INTO `leagues` VALUES ('AA','American Association','N'),('AL','American League','Y'),('FL','Federal League','N'),('ML','Major League','Y'),('NA','National Association','N'),('NL','National League','Y'),('PL','Players'' League','N'),('UA','Union Association','N');"

    cur.execute(sql)


    # commit changes and close the connection
    con.commit()
    con.close()

initLeaguesTable()

