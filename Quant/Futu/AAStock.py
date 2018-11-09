import datetime
import requests
import pandas as pd
from web.weblib import http 
from lxml import etree
from pyquery import PyQuery as pq


def GetFirstPage (SID = '08611'):
    url = 'http://www.aastocks.com/sc/stocks/analysis/transaction.aspx'
    payload = {
    'symbol': SID
    }
    pageText = http.SimpleGet(url,params=payload)
    return pageText

def GetStockTradeDay(text):
    d = pq(text)
    date = d('#ddlDate > option:nth-child(1)').attr("value")
    return date

# 取tick的请求必须带上第一次请求的时间和参数
def GetTickUrl(text):
    date = GetStockTradeDay(text) #先拿到上一个交易日

    tar1 =r'function GetTsData() {'
    atInt = text.find(tar1)
    at11 = text.find("\"",atInt)
    at12 = text.find("\"",at11+1)
    at21 = text.find("\"",at12+1)
    at22 = text.find("\"",at21+1)
    # http://tldata.aastocks.com/TradeLogServlet/getTradeLog?id=01801.HK
    str1 = text[at11+1:at12]
    # &u=13&t=20181104181451&d=2B2F2B2E
    str2 = text[at21+1:at22]

    tickUrl = str1+date+str2
    return  tickUrl

def GetTickResp(tickUrl):
    pageText = http.SimpleGet(tickUrl)
    return pageText

# 拿一下每手股数 LotSize
def GetStockLotSize(SID = '08611'):
    url = 'http://www.aastocks.com/sc/stocks/analysis/company-fundamental/basic-information'
    payload = {
    'symbol': SID
    }
    text = http.SimpleGet(url,params=payload)
    # 文本： ...买卖单位</td> <td class="mcFont cls">100</td>
    atInt = text.find('买卖单位')
    atcls = text.find('cls',atInt)
    attd = text.find('</td>',atcls)
    resStr = text[atcls+5:attd].replace(',','') #千分位
    LotSize = int(resStr)
    return LotSize


#处理网页上那堆纯文本
def HandTickData(text,size=1):
    # text = http.LoadStr()
    text = text[text.find("#")+1:]
    texts = text.split("|")
    texts = texts[:-1] #转成粗数组

    #四个tick列
    timel = []
    lotsl = []
    pricel = []
    ordertypel = []

    for text in texts:
        ls = text.split(";")

        timeS = ls[0]
        timeS = timeS[0:2] + ':'+timeS[2:4]+':'+timeS[4:6]
        timel.append(timeS) # 时间列

        lots = int(ls[1])/size
        lotsl.append(lots) #手数

        pricel.append(ls[3]) #价格列

        ordertypel.append(TypeFormat(ls[4])) #方向列
    
    time = pd.Series(timel)
    lots = pd.Series(lotsl)
    price = pd.Series(pricel)
    ordertype = pd.Series(ordertypel)
    df = pd.DataFrame({ 'time': time, 'lots': lots, 'price': price, 'type': ordertype})
    return df

def TypeFormat(Tstr):
    if Tstr == "A":
        return "buy"
    elif Tstr == "B":
        return "sell"
    else:
        return "auto"

# 顺序流
def GetTickDataFrame(SID):
    text = GetFirstPage(SID)  #访问第一页
    tickUrl = GetTickUrl(text) #拼出url
    tickT = GetTickResp(tickUrl) #访问URL，拿到原始数据
    size = GetStockLotSize(SID)  #拿一下每手多少股数
    df = HandTickData(tickT,size) #处理数据
    return df


def main(SID):
    df = GetTickDataFrame(SID)
    print(df)
    fPath = 'Docs/' + SID + '.xlsx'
    df.to_excel(fPath,sheet_name=SID)    

SID = '08259'
print(SID)
# main(SID)