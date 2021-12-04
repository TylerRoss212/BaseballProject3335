import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, MetaData, create_engine
from strFuncs import emptyIntNone, emptyStrNone, emptyFloatNone
import pymysql
import CSI3335Fall2021 as cfg

def initDivisionsTable():
    user = cfg.mysql["user"]
    pWord = cfg.mysql["password"]
    host = cfg.mysql["host"]
    db = cfg.mysql["db"]

    con = pymysql.connect(host=host, user=user, password=pWord, database=db)
    cur = con.cursor()

    # TEST: deletes all data in the table
    cur.execute("TRUNCATE TABLE Divisions")
    con.commit()

    sql = "INSERT INTO `divisions` VALUES ('E','AL','AL East','Y'),('W','AL','AL West','Y'),('C','AL','AL Central','Y'),('E','NL','NL East','Y'),('W','NL','NL West','Y'),('C','NL','NL Central','Y'),('A','AA','Sole Division','N'),('F','FL','Sole Division','N'),('N','NA','Sole Division','N'),('P','PL','Sole Division','N'),('U','UA','Sole Division','N');"

    cur.execute(sql)


    # commit changes and close the connection
    con.commit()
    con.close()

initDivisionsTable()

