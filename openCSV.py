from module import *

def getData(stockName, sdate, edate):
    title = None
    path = None
    mindate = date(2024,9,27) # minimum date
    maxdate = date(2024,9,27) # maximum datedate
    if (stockName == '삼성전자'):
        title = 'Samsung_Electornics'
        path = '^SS_2002-2024'
        mindate = date(2002,1,2)
        maxdate = date(2024,11,25)
    elif (stockName == '엔씨소프트'):
        title = 'NCsoft'
        path = '^NC_2002-2024'
        mindate = date(2002,1,2)
        maxdate = date(2024,11,22)
    elif (stockName == 'KB금융'):
        title = 'KB_Financial_Group'
        path = '^KB_2002-2024'
        mindate = date(2002,1,2)
        maxdate = date(2024,11,22)
    # format YYYY-DD-MM
    sdate = max(mindate, sdate)
    edate = min(maxdate, edate)
    if (sdate > edate): # 나중에 에러표시 필요
        edate = sdate
    return title, path, sdate, edate

def getLabel(stockName, sdate, edate):
    title = None
    code = None
    mindate = date(2024, 9, 27)  # minimum date
    maxdate = date(2024, 9, 27)  # maximum datedate
    if (stockName == '삼성전자'):
        title = '삼성전자'
        code = '005930'
        mindate = date(2016, 1, 4)
        maxdate = date(2024, 9, 30)
    elif (stockName == '엔씨소프트'):
        title = 'NCsoft'
        code = '^NC_2002-2024'
        mindate = date(2016, 1, 4)
        maxdate = date(2024, 11, 22)
    elif (stockName == 'KB금융'):
        title = 'KB_Financial_Group'
        code = '^KB_2002-2024'
        mindate = date(2016, 1, 4)
        maxdate = date(2024, 11, 22)
    # format YYYY-DD-MM
    sdate = max(mindate, sdate)
    edate = min(maxdate, edate)
    if (sdate > edate):  # 나중에 에러표시 필요
        edate = sdate
    return title, code, sdate, edate