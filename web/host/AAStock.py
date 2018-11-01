import datetime
import requests
from web.weblib import http 


def GetFirstPage (SID = '08611'):
    url = 'http://www.aastocks.com/sc/stocks/analysis/transaction.aspx'
    payload = {
    'symbol': SID
    }
    pageText = http.SimpleGet(url,params=payload)
    return pageText

def GetTickUrl(text):
    tar1 =r'function GetTsData() {'
    atInt = text.find(tar1)
    at11 = text.find("\"",atInt)
    at12 = text.find("\"",at11+1)
    at21 = text.find("\"",at12+1)
    at22 = text.find("\"",at21+1)
    str1 = text[at11+1:at12]
    str2 = text[at21+1:at22]
    day1 = datetime.date.today().strftime('%Y%m%d') 
    tickUrl = str1+day1+str2
    return  tickUrl

def GetTickContent(tickUrl):
    pageText = http.SimpleGet(tickUrl)
    return pageText

def HandTickData():
    pass


def start():
    text = GetFirstPage()
    tickUrl = GetTickUrl(text)
    print(tickUrl)
    tickT = GetTickContent(tickUrl)
    # http.SavePage(tickT)


# start()
text = http.LoadStr()
text = text[text.find("#")+1:]


# str = #
texts = text.split("|")
texts = texts[:-1]
timel = []
volumel = []
pricel = []
ordertypel = []

for text in texts:
    ls = text.split(";")
    timeS = ls[0]
    timeS = timeS[0:2] + ':'+timeS[2:4]+':'+timeS[4:6]
    timel.append(timeS)

    volumel.append(ls[1])
    pricel.append(ls[3])
    ordertypel.append(ls[4])

print(timel[:5])



				# population = pd.Series([852469, 1015785, 485199])
