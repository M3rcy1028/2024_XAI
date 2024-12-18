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
    elif (stockname == 'SK하이닉스'):
        title = 'SK_Hynix'
        path = '^SK_2002-2024'
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
    if (stockName == 'Samsung_Electornics'):
        title = '삼성전자'
        code = '005930'
        mindate = date(2016, 1, 4)
        maxdate = date(2024, 9, 30)
    elif (stockName == 'NCsoft'):
        title = '엔씨소프트'
        code = '036570'
        mindate = date(2016, 1, 4)
        maxdate = date(2024, 9, 30)
    elif (stockName == 'KB_Financial_Group'):
        title = 'KB금융'
        code = '105560'
        mindate = date(2023, 10, 4)
        maxdate = date(2024, 9, 30)
    elif (stockName == 'SK_Hynix'):
        title = 'SK하이닉스'
        path = '000660'
        mindate = date(2016, 1, 4)
        maxdate = date(2024, 9, 30)
    # format YYYY-DD-MM
    sdate = max(mindate, sdate)
    edate = min(maxdate, edate)
    if (sdate > edate):  # 나중에 에러표시 필요
        edate = sdate
    return title, code, sdate, edate