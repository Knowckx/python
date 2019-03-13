import os

#给定路径和文件名 保存成文本文件
def Wfile(path,tarString):
    with open(path, 'w', encoding='utf-8') as f:  
        f.write(tarString)


#A=append
def Afile(path,tarString):
    with open(path, 'a', encoding='utf-8') as f:  
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
    





