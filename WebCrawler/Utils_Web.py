from sys import path as sys_path  #为了加载一个Utlity~容易么我。
sys_path.insert(0,"../utils")
import FileRW

from win32.win32crypt import CryptUnprotectData
import os,sqlite3,time
import requests
import datetime


ReqTimeR = datetime.datetime.now()

#给定站点，找出相应的Cookies
def getcookiefromchrome(host='.zhihu.com',typeID = 1):
    #C:\Users\Eniru\AppData\Local\Google\Chrome\User Data\Default\Cookies
    cookiepath=os.environ['LOCALAPPDATA']+r"\Google\Chrome\User Data\Default\Cookies"
    
    with sqlite3.connect(cookiepath) as conn:
        cu=conn.cursor()     
        if (typeID == 1) :
            sql="select host_key,name,encrypted_value from cookies where host_key='%s'" % host  #只拿到这几项
            cookies={name:CryptUnprotectData(encrypted_value)[1].decode() for host_key,name,encrypted_value in cu.execute(sql).fetchall()}
        elif (typeID == 2) :
            sql="select * from cookies where host_key='%s'" % host 
            a  = cu.execute(sql).fetchall()
            cookies={name:CryptUnprotectData(encrypted_value)[1].decode() for host_key,name,encrypted_value in cu.execute(sql).fetchall()}            
            pass
    return cookies




#最小重复的时间间隔机制
def LimitTryTimer():
    minReqTimeSpan = 0.5 #req之间最小间隔
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


#物料准备，返回一个session
def GetSession(headers,cookDomain):
    cookies = getcookiefromchrome(cookDomain)
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
if testStr == 'getcookiefromchrome':
    getcookiefromchrome(typeID = 1)
if testStr == 'GetUrlData':
    url = "https://www.baidu.com/"
    payload = {
        'offset':1,
        'limit':20,
        'sort_by':'time',
        }
    data = GetUrlData(requests,url,params = payload)
    print(data)


