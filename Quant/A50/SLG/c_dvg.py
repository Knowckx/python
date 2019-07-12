#　obj represent macd Block
class Block:
    def __init__(self):
        self.ILe = -1
        self.IRi = -1
        self.TypeB = DvgSet()  # Dvg.TypeB in the Block
        self.RepUn = DvgUnit()  # the DvgUnit of this Block

    # def __init__(self,left,right):
    #     self.ILe = left
    #     self.IRi = right

    # Known [ILe,IRr] Anal and filled Values
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


class DvgSet:
    def __init__(self):
        self.LU = DvgUnit()
        self.RU = DvgUnit()

    def __init__(self, unLe, unRi):
        self.LU = unLe
        self.RU = unRi

    def __init__(self, df, idxL, idxR):
        self.LU = DvgUnit(df, idxL)
        self.RU = DvgUnit(df, idxR)

    def IsDvg(self):
        if RU.Pv <= LU.Pv and Ru.Mv >= LU.Pv:
            return True
        return False

# dvg 对比单位


class DvgUnit:
    def __init__(self):
        self.Idx = -1
        self.Pv = 0.0
        self.Mv = 0.0

    def __init__(self, df, idx):
        self.Idx = idx
        self.Pv = df.loc[idx, 'close']
        self.Mv = df.loc[idx, 'macd']


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

