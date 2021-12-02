import datetime

def emptyIntNone(dataStr):
    if dataStr == "" or dataStr == "\n":
        return None
    else:
        return int(dataStr)


def emptyStrNone(dataStr):
    if dataStr == "" or dataStr == "\n":
        return None
    else:
        return dataStr


def emptyFloatNone(dataStr):
    if dataStr == "" or dataStr == "\n":
        return None
    else:
        return float(dataStr)


def emptyDateNone(year, month, day):
    if year == "":
        return None
    elif month == "" and day == "":
        return datetime.datetime.strptime(year, '%Y')
    elif day == "":
        myStr = year + "-" + month
        return datetime.datetime.strptime(myStr, '%Y-%m')
    else:
        myStr = year + "-" + month + "-" + day
        return datetime.datetime.strptime(myStr, '%Y-%m-%d')
