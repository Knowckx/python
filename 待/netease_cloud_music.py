import requests
import GetCookies
import math
from lxml import etree

headers1 = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',
        "Referer": "http://music.163.com/song?id=212233",
        'Host': 'music.163.com',
        'Origin':'http://music.163.com'
    }
def Wfile(tarString):
    path = r"D:\Develop\Python\Web_Zhihu\Wfile.html"
    with open(path, 'w', encoding='utf-8') as f:  
        f.write(tarString)
# def get_userInfo(userID):



    # user_url = 'https://www.zhihu.com/people/' + userID
    # response = s.get(user_url, headers=header_info ,cookies = cookies)
    # # print response



    # soup = BeautifulSoup(response.content, 'lxml')
    # name = soup.find_all('span', {'class': 'name'})[1].string
    # # print 'name: %s' % name
    # ID = userID
    # # print 'ID: %s' % ID
    # location = soup.find('span', {'class': 'location item'})
    # if location == None:
    #     location = 'None'
    # else:
    #     location = location.string
    # # print 'location: %s' % location
    # business = soup.find('span', {'class': 'business item'})
    # if business == None:
    #     business = 'None'
    # else:
    #     business = business.string
    # # print 'business: %s' % business
    # gender = soup.find('input', {'checked': 'checked'})
    # if gender == None:
    #     gender = 'None'
    # else:
    #     gender = gender['class'][0]
    # # print 'gender: %s' % gender
    # employment = soup.find('span', {'class': 'employment item'})
    # if employment == None:
    #     employment = 'None'
    # else:
    #     employment = employment.string
    # # print 'employment: %s' % employment
    # position = soup.find('span', {'class': 'position item'})
    # if position == None:
    #     position = 'None'
    # else:
    #     position = position.string
    # # print 'position: %s' % position
    # education = soup.find('span', {'class': 'education item'})
    # if education == None:
    #     education = 'None'
    # else:
    #     education = education.string
    # # print 'education: %s' % education
    # major = soup.find('span', {'class': 'education-extra item'})
    # if major == None:
    #     major = 'None'
    # else:
    #     major = major.string
    # # print 'major: %s' % major
    # agree = int(soup.find('span', {'class': 'zm-profile-header-user-agree'}).strong.string)
    # # print 'agree: %d' % agree
    # thanks = int(soup.find('span', {'class': 'zm-profile-header-user-thanks'}).strong.string)
    # # print 'thanks: %d' % thanks
    # infolist = soup.find_all('a', {'class': 'item'})
    # asks = int(infolist[1].span.string)
    # # print 'asks: %d' % asks
    # answers = int(infolist[2].span.string)
    # # print 'answers: %d' % answers
    # posts = int(infolist[3].span.string)
    # # print 'posts: %d' % posts
    # collections = int(infolist[4].span.string)
    # # print 'collections: %d' % collections
    # logs = int(infolist[5].span.string)
    # # print 'logs: %d' % logs
    # followees = int(infolist[len(infolist)-2].strong.string)
    # # print 'followees: %d' % followees
    # followers = int(infolist[len(infolist)-1].strong.string)
    # # print 'followers: %d' % followers
    # scantime = int(soup.find_all('span', {'class': 'zg-gray-normal'})[len(soup.find_all('span', {'class': 'zg-gray-normal'}))-1].strong.string)
    # # print 'scantime: %d' % scantime
    # info = (name, ID, location, business, gender, employment, position,
    #         education, major, agree, thanks, asks, answers, posts,
    #         collections, logs, followees, followers, scantime)
    # return info






def get_userListbyMusicID(musicID):

    url = 'http://music.163.com/#/song?id=' + str(594758) 
    data = s.get(url, headers = headers ,cookies = cookies)
    url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_212233/'
    data = s.post(url, params = payload ,headers = headers1)
    print(data.text)
    return

    contentTree = etree.HTML(data.content)
    tarDIV = contentTree.find('.//span[@class="j-flag"]')
    str1 = tarDIV.text
    str1 = b'\xa0'
    str1 = str1.decode('utf-8')
    # str1 = etree.tostring(tarDIV.encoding=None)

    print(str1)
    # tarDIV = contentTree.findtext('.//span[@class="j-flag"]/span')

    return
    answerNum = int(answerNum.attrib['data-num'])
    print('问题一共的回答数：' + str(answerNum) )
    PageMaxReply = 20  #目前一页最大是20个
    PageNum = math.ceil(answerNum / PageMaxReply)
    print('计算后页数：' + str(PageNum) )   #先拿到一共的页数


    #---------------------------------------------------------





#头部信息
headers = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',
        "Referer": "http://music.163.com/",
        'Host': 'music.163.com',
    }

data = {
    'form_email':'ID',
    'form_password':'mm'
}
cookies = GetCookies.getcookiefromchrome('music.163.com')
csrf = cookies['__csrf']
payload = {'csrf_token': csrf}
global s
s = requests.session()

__name__ = 'get_userListbyMusicID'

if __name__ == 'get_userInfo':
    userID = '52236857' #网易云音乐的用户ID是一串数字
    info = get_userList(userID)



if __name__ == 'get_userListbyMusicID':
    musicID = '594758' #窓辺から(KYOSUKE No. 1)   ID 594758
    userIDList = get_userListbyMusicID(musicID)
    print ('输出数据' + musicID)
    # for i in range(len(userIDList)):
    #     print(userIDList[i])

# 专辑也是有评论的。那么……歌唱家也是。  http://music.163.com/#/album?id=56225













