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









