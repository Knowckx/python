import requests
from lxml import etree
import math,codecs,json
import Utils_Web,FileRW
import WeiBo as WB

#---------------------------------------------------------单位函数
#---------0 从一个问题里得到答主列表 ---------测试可以，能正确返回目标性别的列表。
def get_question(questionID):
    print('问题的ID为：'+str(questionID))  
    idList = []   #存放用户ID
    url = 'https://www.zhihu.com/api/v4/questions/' + str(questionID) + '/answers' 
    payload = {
            'offset':1,
            'limit':20,
            'sort_by':'created',
            }
    jsonData = Utils_Web.GetUrlData(s,url, params = payload)
    totals = jsonData['paging']['totals']
    limit = 20  #每次数量
    cnt = math.ceil(totals/limit)
    print("问题回答的总条数："+ str(totals),"总共页数："+ str(cnt))
    for i in range (0,cnt):  #请求几页
        print("开始遍历页："+ str(i+1))
        payload = {
                'offset':i*limit,
                'limit':limit,
                'sort_by':'created',
                }
        jsonData = Utils_Web.GetUrlData(s,url,params = payload)
        print("本页目标数量："+ str(len(jsonData['data'])))
        for k in jsonData['data']:  #每一页
        # -1 无性别 0 女 1 男
            if (k['author']['name'] == '匿名用户') or (k['author']['gender'] != 0):
                continue
            # print(k['author']['name'])
            userid =  k['author']['url_token']
            idList.append(userid)
    print('处理后有效名单长度：' + str(len(idList)))
    return idList

#---------1返回用户的信息，没有接口，直接解析页面.返回一个清洗过的infoDic.
def get_userInfo(peopleID):
    infoDic = {}   #存放用户数据
    url = 'https://www.zhihu.com/people/' + str(peopleID) + '/collections' 
    data = Utils_Web.GetUrlData(s,url)
    dataTree = etree.HTML(data)  #取出用户数据的DIV
    tardiv = dataTree.xpath('//div[@id="data"]') 
    try:
        strData = tardiv[0].attrib['data-state'] #目标字符串
        strData= strData.replace("&quot;","\"")
        jsonData = json.loads(strData)  #json get
        users = jsonData['entities']['users']  #用户信息在这里
    except Exception as e:
        print("解析用户信息出错：" + str(peopleID))
        raise(e)
    tarUserinfo = None
    for k,v in users.items():
        if k != "Knowckx":
            print("JSON目标用户名：" + k)
            tarUserinfo = v
            infoDic['ID'] = k
    if not(tarUserinfo) or len(users) != 2:
        print("Json里没有获得目标用户信息")
        raise(Exception)
    #-----------------------上面保证用户信息是正确的
    infoDic['gender'] = tarUserinfo['gender'] #1 = 男  0 = 女 
    if len(tarUserinfo['locations']) == 0:
        infoDic['loc'] = None
    else:
        infoDic['loc'] = tarUserinfo['locations'][0]['name']
    infoDic['Weibo'] = tarUserinfo.get('sinaWeiboUrl')
    return infoDic

#---------2先拿到用户的信息 再判断是否是目标用户
def F_UserID(userID):
    infoDic = get_userInfo(userID)
    if infoDic['gender'] == "男":
        print("非目标性别,PASS")
        return False      #一定是正确性别
    strLoc = infoDic['loc']
    if strLoc != None and strLoc.find('广州') != -1:
        print("------------目标通过_知乎------------")
        return True
    #微博
    weiboUrl = infoDic['Weibo']
    if weiboUrl == None:
        print("地址不通过 and 无微博,PASS")
        return False
    else:
        weiboUserID = weiboUrl.partition("/u/")[2]
        info = WB.get_userInfo(weiboUserID)
        if info !=None:
            strLoc = str(info['area'])
            if (strLoc.find('广州') != -1 ):
                print("------------目标通过_微博------------")
                return True
    print("地址不通过 and 微博不通过,PASS")
    return False
    
#---------是否是已经查过的。那就引发异常。  | 记录到JSON
def ToJsonData_Q(Q_ID,mode = "R"):
    dataPath = "../WebCrawler/Data/Zhihu_GZ_Q.json"
    jsonData = json.loads(FileRW.Rfile(dataPath))
    is_inData = str(Q_ID) in jsonData
    if is_inData :
        print(str(Q_ID) + " 发现重复项")
        return False
    if mode == "W":
        jsonData[str(Q_ID)] = 1
        strJSON = json.dumps(jsonData,ensure_ascii = False)
        if strJSON:
            FileRW.Wfile(dataPath,strJSON)
    return True   #表示通过，没有发现相同项

def ToJsonData_U(L_U_ID):
    dataPath = "../WebCrawler/Data/Zhihu_GZ_U.json"
    jsonData = json.loads(FileRW.Rfile(dataPath))

    for U_ID in L_U_ID[:]:
        is_inData = str(U_ID) in jsonData
        if is_inData :
            print(str(U_ID) + " 是重复项")
            L_U_ID.remove(U_ID)
            continue
    
    if not L_U_ID: return L_U_ID
    for U_ID in L_U_ID[:]: #增加进去
        jsonData[str(U_ID)] = 1
        strJSON = json.dumps(jsonData,ensure_ascii = False)
        if strJSON:
            FileRW.Wfile(dataPath,strJSON)
    return L_U_ID

    # a = ["knowckx","excited-vczh",'1']
#---------------------------------------------------------

def main(questionID = 30739577 , midCnt = 540):
    tarlist = []  #保存最后的结果
    if (not ToJsonData_Q(questionID)):  #先判断是否存在已经
        return
    IDlist = get_question(questionID) #回答者列表
    tarlist = Utils_Web.F_List(IDlist,F_UserID,curCnt = midCnt)
    print("---1 问题晒选结果",tarlist)
    ToJsonData_Q(questionID,mode = "W")  
    tarlist = ToJsonData_U(tarlist)
    print("---2 最后结果",tarlist)
    

#---------------------------------------------------------


#---------------------------------------------------------
#先设置一下request的配置
headers = {
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
        "Host": "www.zhihu.com",
    }
cookDomain = '.zhihu.com'
s = Utils_Web.GetSession(headers,cookDomain)
if __name__ == '__main__':  #本地启动，debug用
    testStr = 'main'
    if testStr == 'get_question':
        list1 = get_question(24062988)
        print(list1)
    if testStr == 'get_userInfo':
        userID = 'ru-ru-19-5'
        info = get_userInfo(userID)
        print(info)

    if testStr == 'F_UserID':
        userID = 'tang-xiao-lu-37'
        print(F_UserID(userID))
    if testStr == 'main':
        main()
    
    
