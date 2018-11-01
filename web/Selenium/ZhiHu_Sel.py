from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common import action_chains
from selenium.webdriver.support.wait import WebDriverWait
import GetCookies
import os
import math
import time

#-----------------------根据ID提取用户信息，返回info这个字典
def get_userInfo(userID):
    user_url = 'https://www.zhihu.com/people/' + userID
    driver.get(user_url)
    info = {}
    try:
        expandButton = driver.find_element_by_class_name("ProfileHeader-expandButton")
        expandButton.click()
    except Exception as E:
        print('目标没有详细信息')
        return info
    tarDiv = driver.find_element_by_xpath("//div[@class='ProfileHeader-contentBody']")
    try:
        LocSpan = tarDiv.find_element_by_xpath("//div[@class='ProfileHeader-detailItem']/span[text()='居住地']") #居住地的span
    except Exception as e:
        print("目标没有居住地信息")
    else:
        LocSpan = LocSpan.find_element_by_xpath("following-sibling::div/span[contains(text(),'现居')]")
        strLoc = str(LocSpan.text)[2:]  #现居西雅图（Seattle）
        info['loc'] =  strLoc
    try:
        weiboSpan = tarDiv.find_element_by_xpath("//div[@class='ProfileHeader-detailItem']/span[text()='社交帐号']") #社交帐号的span
    except Exception as e:
        print("目标没有微博信息")
    else:
        weiboHref = weiboSpan.find_element_by_xpath("following-sibling::div/a[contains(@href,'weibo')]")
        weiboHref = weiboHref.get_attribute('href')
        info['weibo'] =  weiboHref
    return info


def GetUserLoc_Weibo(url):
    driver.set_page_load_timeout(1.5)  #指定加载时间
    try:
        driver.get(url)
    except Exception as e:  #加载了一会
        pass
    strXpath = "//ul[@class='ul_detail']"  #找不到
    eleLoc = driver.find_element_by_xpath(strXpath)
    eleLoc = eleLoc.find_element_by_class_name('ficon_cd_place')  #地址的图标位置   
    eleLoc = eleLoc.find_element_by_xpath("following::span")
    strLoc = str(eleLoc.text)
    print('微博地址：',strLoc)
    return strLoc


def ConnectDomin():
    driver_path = 'E:\Python\chromedriver\chromedriver'
    options = webdriver.ChromeOptions();  #新建配置
    options.add_argument("start-maximized")  #最大化
    options.add_argument("disable-notifications")  #
    preferences = {}
    preferences["profile.managed_default_content_settings.images"] = 2
    options.add_experimental_option('prefs',preferences)
    driver = webdriver.Chrome(driver_path,chrome_options=options)
    return driver
def SetCookies_zhihu():
    driver.get('https://www.zhihu.com/question/20298527') #一个404页面
    # driver.delete_all_cookies()
    cookies = GetCookies.getcookiefromchrome()
    for k,v in cookies.items():
        driver.add_cookie({'name':k, 'value':v})
def SetCookies_weibo():
    driver.get('http://weibo.com/signup/signup.php') #一个普通页面
    # driver.delete_all_cookies()
    cookies = GetCookies.getcookiefromchrome(host='.weibo.com')
    for k,v in cookies.items():
        driver.add_cookie({'name':k, 'value':v})
#-----------------------根据ID提取回答用户的列表
def get_answer(questionID):
    url = 'http://www.zhihu.com/question/' + str(questionID) + '?sort=created' 
    driver.get(url)
    answerNumEle = driver.find_element_by_id('zh-question-answer-num')
    answerNum = answerNumEle.get_attribute('data-num')
    answerNum = int(answerNum)
    PageMaxReply = 20  #目前一页最大是20个
    PageNum = math.ceil(answerNum / PageMaxReply)
    print('目标页,回答数：' + str(answerNum))
    print('页数：' + str(PageNum))   #先拿到一共的页数
    #----------------------------
    LtarUser = [] 
    i = 1
    for Cnt in range(1,PageNum+1):
        i = i + 1
        url = 'http://www.zhihu.com/question/' + str(questionID) + '?sort=created&page='+ str(Cnt)
        driver.get(url)
        replyDivs = driver.find_element_by_id("zh-question-answer-wrap")  #回答内容的根节点[DIV]
        elesLink = replyDivs.find_elements(by = By.CLASS_NAME,value= "author-link")
        for ele in elesLink:
            # driver.execute_script("arguments[0].scrollIntoView(false);", ele)
            if(userGender(ele)):
                peoID = ele.get_attribute('href') 
                peoID = peoID.rsplit('people/')[1]
                LtarUser.append(peoID)
    print('获得的目标数：'  + str(len(LtarUser)))
    return LtarUser
#---------------------------------------------------------
#-----------------------性别为女，或者没填的，都会返回ture
def userGender(ele):
    peoID = ele.text   #记录一下用户名
    print(ele.text)
    action_chains.ActionChains(driver).move_to_element(ele).perform()  #只有这样才能拿到最新的action
    EC = WebDriverWait(driver,3,0.3) #频率填0.2会出错。因为上面操作有改动driver的内容，而driver在第一个0.2时还没有正确刷新

    cnt = 3
    while(cnt>0):
        try:
            #有效弹出卡
            EC.until(lambda x: x.find_element_by_xpath("//div[@id = 'zh-hovercard']//span[@class ='name']").text == peoID)
            break
        except Exception as e:
            print("WebDriverWait出错",cnt)
            cnt = cnt -1
            if (cnt <= 0):
                return
            continue
    
    tarDiv = driver.find_element_by_xpath("//div[@id = 'zh-hovercard']//div[@class ='upper']")
    try:  #有的没填性别
        GenderIcon = tarDiv.find_element_by_class_name('icon')
    except Exception  as e:
        print('没有性别图标')
        return True
    strGender = GenderIcon.get_attribute('class') #拿到字串，icon icon-profile-male
    action_chains.ActionChains(driver).move_by_offset(50, 50).perform() #移开
    if (strGender.endswith("female")):
        print('女')
        return True
    elif(strGender.endswith("male")): #男
        print('男')
    else:
        print('性别辨认出错')
    return False

#---------用户信息的字典  是否有你要的内容
def HandelUserDic(info):
    if(info.get('loc')):  #含有loc字段
        strLoc = info['loc']
        if(CheckStr(strLoc)):
            return True
    if(info.get('weibo')):  #含有weibo字段
        weiboUrl = info['weibo']
        strLoc = GetUserLoc_Weibo(weiboUrl)
        if(CheckStr(strLoc)):
            return True
    return False


#---------一串字符，是否有你感兴趣的
def CheckStr(str0):
    if(str(str0).count('广州') or str(str0).count('广东')):
        return True
    else:
        return False
 


__name__ = 'main'
global driver
driver = ConnectDomin() 
    
if __name__ == 'get_userInfo':
    userID = 'Knowckx'
    info = get_userInfo(userID)
    # input()
if __name__ == 'get_answer':
    get_answer(46165914)
if __name__ == 'GetUserLoc_Weibo':
    url = 'http://weibo.com/ryuetsuya'
    SetCookies_weibo()
    GetUserLoc_Weibo(url)
    
if __name__ == 'main':
    userInfo = {}
    SetCookies_zhihu()
    SetCookies_weibo()
    LtarUser = get_answer(29527455)
    for userID in LtarUser:
        info = get_userInfo(userID)
        if(HandelUserDic(info)):
            print('发现目标：',userID)
            userInfo[str(userID)] = info
    print(userInfo)







    













