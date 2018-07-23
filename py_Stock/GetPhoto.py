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

#----------发出requests,得到HTML
def getHtml(stockCode):
    url = 'http://gpys.emoney.cn/WebSD/Handlers/SDHisHandlers.ashx'
    params = {'Type': 'S', 'Code':stockCode,'Key':'sds' }

    headers = {
         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
         'Accept-Encoding':'gzip, deflate, sdch',
         'Accept-Language':'zh-CN,zh;q=0.8', 'Cache-Control':'no-cache',
         'Connection':'keep-alive', 'Host':'gpys.emoney.cn',
         'Pragma':'no-cache', 'Upgrade-Insecure-Requests':'1', 'User-Agent':
         'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36' }  ##头部信息

    r = requests.get(url, params = params,headers = headers)
    
    r.raise_for_status()    # 如果响应状态码不是 200，就主动抛出异常
    print(r.status_code)
    return r.text


##    try:
##        reStr = getHtml(stockCode)
##    except Exception as e:
##        print('Error:', e)
##        time.sleep(3)
##        reStr = getHtml(stockCode)
####    finally:

#----------正文



o = win32com.client.Dispatch("Excel.Application") #抓到Excel进程
o.Visible = 1
sht = o.Worksheets[0]
i = 1697  #取Excel的代码值
while (i<2931):
    stockCode = sht.Cells(i,1).Value #得到000001
    print("从Excel中得到股票：" + stockCode)

    try:
        reStr = getHtml(stockCode)
    except Exception as e:
        print('Error:', e)
        time.sleep(3)
        reStr = getHtml(stockCode)
##    finally:



    try:
        re = getScore(reStr)
    except Exception as e:
        print('在分析这个时出错了：'+reStr)
    print(re)
    
    sht.Cells(i,4).Value = re[1]
    i+=1
    stime = random.uniform(0.5,1.2)
    time.sleep(stime)



##sht.Cells(2,1).Value = "Hello"

#reStr = r"([{success:1,msg:'000015,5.7,5.8,6.3,5.1,5.6,5.7,4.6,5.3,B,6,10,29%,处于上升趋势 建议持股观望,6,0,较弱,良好,该股处在29%的位置,'}])"

pass




#'http://gpys.emoney.cn/WebSD/Handlers/SDHisHandlers.ashx?Type=S&Code=000007&Key=sds'




#print(str(content))
##html = etree.HTML(content)
##stockScore = html.xpath('//*[@id="spanTestScore"]/text()')


# requests.get的参数：  allow_redirects = False  不给跳转

# r.encoding = 'ISO-8859-1'   --编码
#print(r.headers)  # 响应头内容
#print(r.history)  # 历史信息状态（是否跳转）



    
