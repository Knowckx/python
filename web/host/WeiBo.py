# from sys import path as sys_path  #为了加载一个Utlity~容易么我。
# sys_path.insert(0,"../Utlity")

import requests
from lxml import etree
import math,codecs,json
import web.weblib.Utils_Web as Utils_Web



#A1 获得一条微博下的评论，转发和点赞名单

def get_commetList(weiboID,mode=111):
    # PC端的微博地址需要目标博主的ID。
    # 而移动端微博地址为：http://m.weibo.cn/status/EFH5lqCHj  | 后面的字符串换成数字也是可以的
    print('微博的ID为：'+weiboID)  
    if (not weiboID.isdigit()):
        weiboID = murl_to_mid(weiboID)
    print('微博的数字ID为：'+weiboID)  

    
    idList = []   #存放用户ID

    comment_url = 'http://m.weibo.cn/api/comments/show'
    ResL = getIDList(comment_url,weiboID) #求评论数据的用户
    if ResL!= None:
        idList.extend(ResL)

    repost_url = 'http://m.weibo.cn/api/statuses/repostTimeline'
    ResL = getIDList(repost_url,weiboID)  #转发用户
    if ResL!= None:
        idList.extend(ResL)

    zan_url = 'http://m.weibo.cn/api/attitudes/show'
    ResL = getIDList_Att(zan_url,weiboID)
    if ResL!= None:
        idList.extend(ResL)

    print("相加总数：%s"%len(idList))
    idList = list(set(idList))
    print("最后取得用户列表长度：%s"%len(idList))
    return idList

#B1 从一个Url(评论，转发)中获得IDList  感觉可以用下面点赞的逻辑来合并成一个呢。
def getIDList(url,weiboID):
    idList = []
    print('访问评论的URL：' + url)
    pageCnt = 1
    payload = {
            'id': str(weiboID),
            'page':str(pageCnt), 
            }
    jsonData = Utils_Web.GetUrlData(s,url, params = payload)
    if jsonData['ok'] == 0 :
        print(".......数量为0哦……")
        return idList
    jsonData = jsonData['data']
    total_number =  jsonData['total_number'] #评论总数  他说是287。我只拿到268
    cnt = jsonData['max'] #页数  max等于29 那么payload中不可以要求30.
    print("总数量为："+ str(total_number) + " 总页数："+ str(cnt))
    for i in range (0,cnt):  #请求几页
        payload = {
            'id': str(weiboID),
            'page':str(i+1), }
        jsonData = Utils_Web.GetUrlData(s,url,params = payload)
        if jsonData.get('data'):
            jsonData = jsonData['data']
        else:
            print('返回的JSON拿不到data字段，结束')
            break  
        print("开始遍历页："+ str(i+1) + " 本页数量："+ str(len(jsonData['data'])))
        # print("第一个"+ str(jsonData['data'][0]))
        for k in jsonData['data']:  #每一页
            userid =  k['user']['id']
            idList.append(userid)
    # idList = list(set(idList))
    print('获得名单长度：' + str(len(idList)))
    return idList

#B2 从一个Url(点赞)中获得IDList
def getIDList_Att(url,weiboID):
    print('访问点赞页:' + url)
    idList = []
    pageCnt = 1
    while True:
        payload = {
                'id': str(weiboID),
                'page':str(pageCnt), 
                }
        jsonData = Utils_Web.GetUrlData(s,url,params = payload)
        if jsonData.get('data'):
            jsonData = jsonData['data']
        else:
            print('返回的JSON拿不到data字段，结束')
            break  
        if jsonData['data'] == None:
            print('点赞页完成，总页数：'+ str(pageCnt-1))
            break
        page_number =  len(jsonData['data']) #本页点赞总数
        print("点赞页：%s。 本页数量：%s"%(pageCnt,page_number))

        for k in jsonData['data']:  #每一页  这里的结构，被改掉了。 目前返回一个html. <a href="/u/2369434535">
            userid =  k['user']['id']
            idList.append(userid)
        pageCnt += 1
    print('获得点赞名单长度：' + str(len(idList)))
    # idList = list(set(idList))
    return idList
   
#A2 根据用户ID，取得用户信息（ 通过PC端弹出小的卡片   
def get_userInfo(userID):
    print("尝试获取用户信息",userID)
    url = 'http://weibo.com/aj/v6/user/newcard' 
    payload = {
        'ajwvr': '6', 
        'id': str(userID),
        'type':'1', 
        'callback':'STK_1493021223253208'
        }
    cookies1 = Utils_Web.GetCookieFromChrome('.weibo.com') 
    dataStr = Utils_Web.GetUrlData(s,url,encoding = 'unicode_escape',params = payload,headers = headers_weibo,cookies = cookies1) #需要换header 换cookies
    index1 = dataStr.find('<div')
    if(index1 == -1):
        print("怀疑该微博用户ID为空号")
        return   
    index2 = dataStr.rfind('/div>')
    dataStr1 = dataStr[index1:index2+5]  #sub
    dataStr1 = dataStr1.replace('\\','') 
    contentTree = etree.HTML(dataStr1)    #Html文本清洗完成
    info = {}   #数据
    info['userID'] =  userID
    nick = contentTree.xpath('//a[contains(@suda-uatrack,"chick_nick")]')   #----昵称
    info['nick'] =  nick[0].get('title')  
    gender = contentTree.xpath('//em[contains(@class,"male")]')    #----性别
    if len(gender) == 0:
        info['gender'] = ""
    else:
        info['gender'] =  gender[0].get('title')
    area = contentTree.xpath('//a[contains(@suda-uatrack,"chick_area")]')   #----地址
    if len(area) == 0:
        info['area'] = ""
    else:
        info['area'] =  area[0].text
    school = contentTree.xpath('//a[contains(@suda-uatrack,"chick_school")]')   #----地址
    if len(school) == 0:
        info['school'] = ""
    else:
        info['school'] =  school[0].text
    print(info)
    return info



#---------判断一个用户是不是目标
def F_UserID(userID):
    infoDic = get_userInfo(userID)
    # if infoDic.get('gender') != "女": #后面一定是正确性别
    #     print("非目标性别,PASS")
    #     return False      
    strLoc = infoDic.get('area')
    if strLoc != None and strLoc.find('深圳') != -1:
        print("------------目标通过------------")
        return True

    strSchool = infoDic.get('school')
    if strSchool != None and strSchool.find('深圳') != -1:
        print("------------目标通过------------")
        return True
    # print("性别通过，地址不通过,PASS")
    return False




#-----------------将微博url转成微博数字ID
def key62_to_key10(str_62,DICT):
    value = 0
    for s in str_62:
        value = value * 62 + DICT[s]
    return value

def murl_to_mid(murl):
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    DICT = {}
    for index in range(len(ALPHABET)):
        DICT[ALPHABET[index]] = index
    length = len(murl)
    mid = ''
    group = int(length / 4)# four characters per group
    last_count = length % 4# head group character counts
    for loop in range(group):
        value = key62_to_key10(murl[length - (loop + 1) * 4: length - loop * 4],DICT)
        mid = str(value).zfill(7) + mid
    if last_count:
        value = key62_to_key10(murl[: length - group * 4],DICT)
        mid = str(value) + mid
    return mid
#----------------------------------主启动


def main(weiboID = 'Hp0vQjVbx' , midCnt = 0):
    tarlist = []  #保存最后的结果
    # if (not ToJsonData_Q(questionID)):  #先判断是否存在已经
    #     return
    IDlist = get_commetList(weiboID) #回答者列表
    tarlist = Utils_Web.F_List(IDlist,F_UserID,curCnt = midCnt)
    print("---1 问题晒选结果",tarlist)
    # ToJsonData_Q(questionID,mode = "W")  
    # tarlist = ToJsonData_U(tarlist)
    # print("-------------------- 最后结果",tarlist)
    

#头部信息


headers_weibo = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
        'Host': 'weibo.com',
    }
headers_mweibo = {
        "User-Agent": 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko)',
        'Host': 'm.weibo.cn',
    }

cookDomain = '.weibo.cn' #移动端的cook用的cn结尾   所以用这个工具，先得进一下网页得到cookies
s = Utils_Web.GetSession(headers_mweibo,cookDomain) #这里有两个……header



#------------------------------

if __name__ == '__main__':
    testStr= 'main'  #入口
    if testStr == 'get_userInfo':
        userID = '2853972281'
        info = get_userInfo(userID)
        print(info)
    if testStr == 'get_comment':  
        lista = get_commetList('Gr6XlunCl')
    if testStr == 'main':
        weiboID = 'HtKrsowvR'
        midCnt = 130
        main(weiboID,midCnt)








