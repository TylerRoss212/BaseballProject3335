import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, MetaData, create_engine
from strFuncs import emptyIntNone, emptyStrNone, emptyFloatNone
import pymysql

def initLeaguesTable():
    con = pymysql.connect(host='localhost', user='root', password='', database='GiveUsAnADrSpeegle')
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

