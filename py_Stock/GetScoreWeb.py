#-*- coding:utf-8 -*-
import win32com.client
import requests
import time
import random
from lxml import etree


#----------HTML得到的字符串处理
def getScore(reStr):
    Str1 = ''
    Str2 = ''
    InxAnchor = 0
    inxSign = 0
    while((reStr.index(',',InxAnchor)) != -1): #还存在，号呢
        inxSign = reStr.index(',',InxAnchor)
        if (not reStr[inxSign-7].isalnum() and reStr[inxSign-6:inxSign].isdigit()):
            Str1 = reStr[inxSign-6:inxSign]
            print('发现股票代码：' + Str1)
        elif reStr[inxSign+1].isalpha():
            print('，后面发现一个字母 '+ reStr[inxSign+1])
            InxAnchor = reStr.index(',',inxSign+1)
            if InxAnchor - inxSign <= 3:
                Str2 = reStr[inxSign+1:InxAnchor]
                print('发现评级：' + Str2)
        if Str1 != '' and Str2 != '':
            print('处理字符串最后返回：' + Str1 + ' '+Str2)
            return Str1,Str2
        InxAnchor = inxSign + 1
        pass

#----------发出requests,得到HTML页面
def getHtml(stockCode):
    url = 'http://gpys.emoney.cn/WebSD/Handlers/SDHisHandlers.ashx'
    params = {'Type': 'S', 'Code':stockCode,'Key':'sds' }
    retryCnt = 5
    headers = {
         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
         'Accept-Encoding':'gzip, deflate, sdch',
         'Accept-Language':'zh-CN,zh;q=0.8', 'Cache-Control':'no-cache',
         'Connection':'keep-alive', 'Host':'gpys.emoney.cn',
         'Pragma':'no-cache', 'Upgrade-Insecure-Requests':'1', 'User-Agent':
         'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36' }  ##头部信息
    for i in range(1,retryCnt+1):
        try:
            r = requests.get(url, params = params,headers = headers)
            break
        except Exception as e:
            print('requests出错,次数：',i, e)
            if i == retryCnt:
                raise SystemExit
            else:
                print('requests出错,次数：',i, e)
                stime = random.uniform(0.3,0.9)
                time.sleep(stime)
                continue
            
    r.raise_for_status()    # 如果响应状态码不是 200，就主动抛出异常
    print('status_code',r.status_code)
    return r.text




#----------正文



o = win32com.client.Dispatch("Excel.Application") #抓到Excel进程
o.Visible = 1
sht = o.Worksheets[0]
i = 2  #取Excel的代码值
while (i<2932):
    stockCode = sht.Cells(i,1).Value #得到000001
    print("从Excel中得到股票：" + stockCode)

    reStr = getHtml(stockCode)

    try:
        re = getScore(reStr)
    except Exception as e:
        print('在分析这个时出错了：'+reStr)
    print(re)
    
    sht.Cells(i,4).Value = re[1]
    i+=1
    stime = random.uniform(0.3,0.6)
    time.sleep(stime)



    
