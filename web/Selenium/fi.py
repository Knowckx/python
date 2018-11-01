import requests
import GetCookies
import math
from lxml import etree




def get_answer(questionID):

    #地址： https://www.zhihu.com/question/46165914?sort=created
    url = 'http://www.zhihu.com/question/' + str(questionID) + '?sort=created' 
    data = s.get(url, headers = headers ,cookies = cookies)
    contentTree = etree.HTML(data.content)
    answerNum = contentTree.find('.//*[@id="zh-question-answer-num"]')
    answerNum = int(answerNum.attrib['data-num'])
    print('问题一共的回答数：' + str(answerNum) )
    PageMaxReply = 20  #目前一页最大是20个
    PageNum = math.ceil(answerNum / PageMaxReply)
    print('计算后页数：' + str(PageNum) )   #先拿到一共的页数
    #----------------------------开始一页一页
    Ltars = [] 
    i = 1
    for Cnt in range(1,PageNum+1):
        # print('开始检索页数',Cnt)
        #https://www.zhihu.com/question/52511089?sort=created&page=2  按时间排序 页数
        url = 'http://www.zhihu.com/question/' + str(questionID) + '?sort=created&page='+ str(Cnt)
        data = s.get(url, headers = headers ,cookies = cookies)
        contentTree = etree.HTML(data.content)
        replyDivs = contentTree.xpath('//*[@id="zh-question-answer-wrap"]')  #回答内容的根节点[DIV]
        #返回的是一个list 愿意是："zh-question-answer-wrap"这样的节点有多少个。
        #print(len(replyDivs[0]))
        for repDiv in replyDivs[0]:
            authorLink = repDiv.find('.//*[@class="author-link"]')  #每个一个回答的DIV里找IDlink
            #print(i,'个回答：')
            i = i + 1
            if (authorLink == None): #<class 'NoneType'>
                print('匿名回答')
            else:
                attr = authorLink.attrib
                peoID =  attr['href']# /people/Freelancer17
                print(peoID)
                Ltars.append(peoID)
    print('获得的目标数：'  + str(len(Ltars)))
    return Ltars

    #---------------------------------------------------------





#头部信息
headers = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',
        "Referer": "http://www.zhihu.com/",
        'Host': 'www.zhihu.com',
    }
data = {
    'form_email':'ID',
    'form_password':'mm'
}
cookies = GetCookies.getcookiefromchrome('.zhihu.com')
global s
s = requests.session()

__name__ = 'get_userInfo'

if __name__ == 'get_userInfo':
    userID = 'marcovaldong'
    info = get_userInfo(userID)
    print ('输出数据' + userID)
    for i in range(len(info)):
        print info[i]
if __name__ == 'get_answer':
    get_answer(46165914)





#-------------------分析页面
def beifen():
    contentTree = etree.HTML(data.content)
    answerNum = contentTree.find('.//*[@id="zh-question-answer-num"]')
    answerNum = int(answerNum.attrib['data-num'])
    print('问题一共的回答数：' + str(answerNum) )
    PageMaxReply = 20  #目前一页最大是20个
    PageNum = math.ceil(answerNum / PageMaxReply)
    print('计算后页数：' + str(PageNum) )   #先拿到一共的页数
    #----------------------------开始一页一页
    Ltars = [] 
    i = 1
    for Cnt in range(1,PageNum+1):
        # print('开始检索页数',Cnt)
        #https://www.zhihu.com/question/52511089?sort=created&page=2  按时间排序 页数
        url = 'http://www.zhihu.com/question/' + str(questionID) + '?sort=created&page='+ str(Cnt)
        data = s.get(url, headers = headers ,cookies = cookies)
        contentTree = etree.HTML(data.content)
        replyDivs = contentTree.xpath('//*[@id="zh-question-answer-wrap"]')  #回答内容的根节点[DIV]
        #返回的是一个list 愿意是："zh-question-answer-wrap"这样的节点有多少个。
        #print(len(replyDivs[0]))
        for repDiv in replyDivs[0]:
            authorLink = repDiv.find('.//*[@class="author-link"]')  #每个一个回答的DIV里找IDlink
            #print(i,'个回答：')
            i = i + 1
            if (authorLink == None): #<class 'NoneType'>
                print('匿名回答')
            else:
                attr = authorLink.attrib
                peoID =  attr['href']# /people/Freelancer17
                print(peoID)
                Ltars.append(peoID)
    print('获得的目标数：'  + str(len(Ltars)))
    return Ltars








