
# TIBA_Base   Technical index - Bid / Ask

class TIBA:
    def __init__(self,cnt):
        self.LineA = TIBA_Base(cnt)
        self.LineB = TIBA_Base(cnt*5)
        self.LineC = TIBA_Base(cnt*5*5)
    
    def Add(self,dd):
        if dd == None: # 3.过滤diff为0的盘面
            return
        self.LineA.Add(dd)
        self.LineB.Add(dd)
        self.LineC.Add(dd)

    def Print(self):
        print("A:%f B:%f C:%f"%(self.LineA.V(),self.LineB.V(),self.LineC.V()))



class TIBA_Base:
    def __init__(self,CntLimit):
        self.CntLimit = CntLimit 
        self.HisLL = [] 
        self.VV = [0,0] 

    def Add(self,dd):
        self.HisLL.append(dd)
        self.VV[0] = self.VV[0]+dd[0]
        self.VV[1] = self.VV[1]+dd[1]      
        if len(self.HisLL) > self.CntLimit:
            tailv = self.HisLL[0]
            self.VV[0] = self.VV[0] - tailv[0]
            self.VV[1] = self.VV[1] - tailv[1]              
            self.HisLL.pop(0)
        # print(self.VV)
        # print(self.HisLL)
    
    def V(self):
        if self.VV[1] == 0:
            return 0
        return round(self.VV[0]/self.VV[1],2)
        

# def TestSign2():
#     a1 = [1,1]
#     a2 = [2,2]
#     a3 = [0,3]
#     a4 = [0,4]
#     a5 = [0,5]
#     testsign = TIBA_Base(3)
#     testsign.Add(a1)
#     testsign.Add(a2)
#     testsign.Add(a3)
#     testsign.Add(a4)
#     testsign.Add(a5)

# TestSign2()
