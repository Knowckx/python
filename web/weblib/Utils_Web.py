from sys import path as sys_path  #为了加载一个Utlity~容易么我。
sys_path.insert(0,"../utils")


from libs import FileRW

import os,sqlite3,time
import requests
import datetime
from . import Cookies

ReqTimeR = datetime.datetime.now()





# 最简单的get请求
def SimpleGet (url,params = None):
    s = requests.session()
    resp = s.get(url,params=params)
    if resp.status_code != requests.codes.ok:
        print("get url return status is not 200")
        requests.Response.raise_for_status()
    return resp.text

def SaveStr (str):
    path = 'web/text/test.html'
    FileRW.Wfile(path,str)

def LoadStr ():
    path = 'web/text/test.html'
    rst = FileRW.Rfile(path)
    return rst


#最小重复的时间间隔机制
def LimitTryTimer():
    minReqTimeSpan = 3 #req之间最小间隔
    reTryTimeSpan = 0.3 #命中最小间隔内后的等待时间

    global ReqTimeR
    while(True):
        timeNow = datetime.datetime.now()
        span = (timeNow - ReqTimeR).total_seconds()
        if span>minReqTimeSpan:
            ReqTimeR = timeNow
            break
        # print("Time:" + str(span))
        time.sleep(reTryTimeSpan * 1)

def GetUrlData(s,url,encoding = 'utf-8',**kw):  
    LimitTryTimer()
    tryCnt = 0
    resp = FileRW.TryFunc(s.get,url,**kw)  #第一次请求
    while(resp.status_code != requests.codes.ok):
        if tryCnt >3: #超过三次结束 
            print("s.get没报错，但是返回的数据不对。")
            requests.Response.raise_for_status()
        tryCnt +=1
        time.sleep(tryCnt * 5)  #间隔时间
        print("第%d次重新尝试get"%tryCnt)
        resp = FileRW.TryFunc(s.get,url,**kw)  #假如访问过程中报错了，那就重复三次。
    resp.encoding = encoding
    r_data = ""
    r_data = resp.text
    try:
        r_data = resp.json()
    except Exception as e:
        # print("非json数据")
        return r_data #出错，直接返回原字符串
    return r_data  #正常返回json



def GetCookieFromChrome(cookDomain):
    return Cookies.GetCookieFromChrome(cookDomain)

#物料准备，返回一个session
def GetSession(headers,cookDomain):
    cookies = GetCookieFromChrome(cookDomain)
    s = requests.session()
    s.headers = headers
    s.cookies = requests.utils.cookiejar_from_dict(cookies)
    return s

#通用列表筛选器。带进度报告和中途错误处理
def F_List(tarlist,FuncFilter,curCnt = 0):
    FinalList = []
    maxCnt = len(tarlist) 
    FCnt = 0
    for u_id in tarlist[:]:  
        FCnt +=1
        if FCnt < curCnt:
            continue
        print("进度:" + str(FCnt) + '/' + str(maxCnt))
        try:
            _re = FuncFilter(u_id)
        except Exception as e:
            print("发生错误,中途退出",FinalList)
            raise(e)
        if _re:
            FinalList.append(u_id)
    return FinalList

__name__ = 'main'
testStr = ''
if testStr == 'GetCookieFromChrome':
    GetCookieFromChrome(typeID = 1)
if testStr == 'GetUrlData':
    url = "https://www.baidu.com/"
    payload = {
        'offset':1,
        'limit':20,
        'sort_by':'time',
        }
    data = GetUrlData(requests,url,params = payload)
    print(data)




