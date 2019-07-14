#　obj represent macd Block
class Block:
    def __init__(self): # given a invaild block
        self.ILe = -1 #base info
        self.IRi = -1
        self.F_hl = 0

        self.TyB = False  # Dvg.TyB in the Block
        self.RepUn = DvgUnit()  # the DvgUnit of this Block
    
    def Init(self,ile,iri,f_hl,df):
        self.ILe = ile
        self.IRi = iri
        self.F_hl = f_hl
        self.DF = df.loc[ile:iri]
        # print(newDF)

    # Known [ILe,IRr] Anal and filled Values
    def Anal(self):
        df = self.DF
        if self.F_hl == 0:
            return
        # print(df)
        # self.Print()
        idxP = df.close.idxmin() # self.F_hl = -1
        idxM = df.macd.idxmin()
        if self.F_hl == 1:
            idxP = df.close.idxmax()
            idxM = df.macd.idxmax()
        self.RepUn.Init(df, idxP) #总是由极值代表
        if idxP == idxM:
            # print("Block Desc:Single extm")
            return
            
        # Try TyB  价格极值总是在右边
        # print("try check TyB:%s %s"%(DFTime(df,idxM), DFTime(df,idxP)))
        dvgSet = DvgSet()
        dvgSet.InitPoint2(df, idxM, idxP,self.F_hl)
        if dvgSet.IsDvg():
            self.TyB = True
            self.TyB_Set = dvgSet
        return

    def Len(self):
        return self.IRi - self.ILe

    def Print(self):
        df = self.DF
        print("Block [%s,%s]"%(DFTime(df,self.ILe), DFTime(df,self.IRi)))
    

# 判断背离
class DvgSet:
    def __init__(self):
        self.LU = DvgUnit()
        self.RU = DvgUnit()
        self.F_hl = 0

    #two point
    def InitPoint2(self, df, idxL, idxR,f_hl):
        self.LU.Init(df, idxL)
        self.RU.Init(df, idxR)
        self.F_hl = f_hl

    def InitBlock2(self,lu,ru,f_hl):
        self.LU = lu
        self.RU = ru
        self.F_hl = f_hl

    def IsDvg(self):
        f_hl = self.F_hl
        if f_hl == 1: # red
            if self.RU.Pv >= self.LU.Pv and self.RU.Mv <= self.LU.Mv:
                return True
        if f_hl == -1:
            if self.RU.Pv <= self.LU.Pv and self.RU.Mv >= self.LU.Mv:
                return True
        return False

    def Print(self):
        print("DvgSet:[%s %s]"%(self.LU.Time, self.RU.Time))

class DvgUnit:
    def __init__(self):
        self.Idx = -1
        self.Pv = 0.0
        self.Mv = 0.0
        self.Time = ""

    def Init(self, df , idx):
        self.Idx = idx
        self.Pv = df.loc[idx, 'close']
        self.Mv = df.loc[idx, 'macd']
        self.Time = df.loc[idx, 'time']




# ----------------- struct -----------------
class ExtmCheckRst:
    def __init__(self):
        self.F_hl = 0
        self.Idx = -1

    def __init__(self, checkRst, idx):
        self.F_hl = checkRst
        self.Idx = idx


class SearchBlockL10Args:
    def __init__(self,idxNow,f_hl,minlen):
        self.IdxNow = idxNow # from where
        self.F_hl = f_hl # search for red or green
        self.MinLen = minlen # min broker Len

# ----------------- Func -----------------
def DFTime(df,idx):
    return df.loc[idx, 'time']
