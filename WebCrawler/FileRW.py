import os


#bug用 打印出来
def Wfile(path,tarString):
    with open(path, 'w', encoding='utf-8') as f:  
        f.write(tarString)


def Rfile(path):
    with open(path, 'r', encoding='utf-8') as f:  
        return f.read()


#最后还是没用装饰器。
def TryFunc(func , *args ,**kw ):
    max_try = 3  #重试三次
    errorCnt = 1
    while(True):
        try:
            re = func(*args ,**kw)
            break
        except Exception as e:
            print(e,errorCnt)
            errorCnt += 1
            if (errorCnt > max_try):
                raise (e)
                return False
    return re


def TestA(a):
    print("text123" + str(a))




LAA = ['da-hao-nu-hai-gi', 'MissLifeBeauty', 'wu-jin-hong-94', 'Rachelfang', 'shi-yu-12-6', 'xu-li-71-29']

if __name__ == '__main__':
    path = "../WebCrawler/Data/Zhihu_GZ.txt"
    
    Wfile(str(LAA),path)
    # TryFunc(TestA,3,123)
    # oo = Test(1)
    
    






