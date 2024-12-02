from module import *

def getData(stockname, sdate, edate):
    title = None
    path = None
    mindate = date(2024,9,27) # minimum date
    maxdate = date(2024,9,27) # maximum datedate
    if (stockname == '삼성전자'):
        title = 'Samsung_Electornics'
        path = '^SS_2002-2024'
        mindate = date(2002,1,2)
        maxdate = date(2024,11,25)
    elif (stockname == '엔씨소프트'):
        title = 'NCsoft'
        path = '^NC_2002-2024'
        mindate = date(2002,1,2)
        maxdate = date(2024,11,22)
    elif (stockname == 'KB금융'):
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