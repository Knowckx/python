#　obj represent macd Block 
class Block:
    def __init__(self):
        self.ILe = 0
        self.IRi = 0

    def __init__(self,left,right):
        self.ILe = left
        self.IRi = right

    def Anal(self, df):
        idxp = df.close.idxmin()
        idxm = df.macd.idxmin()
        if idxp == idxm:
            # self.dvgUt = DvgUnit(df, idxp)
            self.IRep = idxm
            msg = "Block Desc:Single"
            print(msg)
            return
        # Try TyB
        idxL, idxR = idxm, idxp
        if idxL > idxR:
            idxL, idxR = idxR, idxL
        dvgSet = DvgSet(df, idxL, idxR)
        self.TypeB = devSet.IsDvg()
        self.IRep = idxm
        return

    def Len(self):
        return self.IRi - self.ILe

# dvg 对比单位
class DvgUnit:
    def __init__(self):
        self.Idx = 0
        self.Pv = 0.0
        self.Mv = 0.0

    def __init__(self, df, idx):
        self.Idx = idx
        self.Pv = df.loc[idx, 'close']
        self.Mv = df.loc[idx, 'macd']


class DvgSet:
    def __init__(self):
        self.LU = DvgUnit()
        self.RU = DvgUnit()

    def __init__(self, df, idxL, idxR):
        self.LU = DvgUnit(df, idxL)
        self.RU = DvgUnit(df, idxR)

    def IsDvg(self):
        if RU.Pv <= LU.Pv and Ru.Mv >= LU.Pv:
            return True
        return False