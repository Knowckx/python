

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

if __name__ == '__main__':
    path = "../WebCrawler/Data/Zhihu_GZ.txt"
    
    Wfile(str(LAA),path)
    # TryFunc(TestA,3,123)
    # oo = Test(1)
    
    






