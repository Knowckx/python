import os
import codecs
from lxml import etree
import json



def Rfile():
    path = r"C:\Users\Eniru\Desktop\1111.txt"
    path = r"C:\Users\Administrator\Desktop\1111.txt"
    
    with open(path, 'r', encoding='utf-8') as f:  
        return f.read()
dataStr =''



dataStr = ""


tranDICTS = {11:'值1',"22":'值2'}
print(tranDICTS)
tmp = [11,22,33]
print("输出一下对应的字典值")
print(tranDICTS[str(tmp[1])])


# print(tmp[2])




