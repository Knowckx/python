
class FakeOut:
    def __init__(self,path):

        with open(path, 'w', encoding='utf-8') as f:  
            f.write(tarString)

    print()
        self.str=''
        self.n=0
    def write(self,s):
        self.str+="Out:[%s] %s\n"%(self.n,s)
        self.n+=1
    def show(self): #显示函数，非必须
        print self.str
    def clear(self): #清空函数，非必须
        self.str=''
        self.n=0
f=FakeOut()
import sys
old=sys.stdout
sys.stdout=f
print('Hello weird.')
print('Hello weird too.')
sys.stdout=old
f.show()
