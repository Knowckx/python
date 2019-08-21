
import Quant.A50.data.csv as csv
import Quant.A50.SLG.dvg as dvg


class BackTest:
    def __init__(self, sheetname):
        excelFile = 'A50'
        # 所使用的验证数据集
        self.verifyDF = csv.GetPDExcel(excelFile, sheetname)
        self.Idx = 0

    # 给定原始数据集，开始验证 | 倒序 直到dvg日期对不上
    def StartWith(self, df):
        self.srcDF = df
        self.StartLoop()




    def GetNextVerify(self):
        df = self.verifyDF
        if self.Idx >= len(df):
            return None
        verf = dvg.DvgRst()
        verf.F_hl = df["type"].iat[self.Idx]
        verf.Time = df["time"].iat[self.Idx]
        self.Idx += 1
        return verf

    def StartLoop(self):
        df = self.srcDF
        idx = len(df)
        gap = 200

        ch = self.GetNextVerify()
        while True:
            dftest = self.srcDF[idx-gap:idx]
            if len(dftest) < gap:
                break
            rst = dvg.Start(dftest,"1d")
            if rst.F_hl == 0:
                idx -=1
                continue
            if ch.IsSame(rst):
                print("success at tar:{} need:{}".format(rst.Time,ch.Time))
                idx -=1
                ch = self.GetNextVerify()
                if ch == None:
                    print("finished!!")
                    return
                continue
            else:
                print("stop at tar:{} need:{}".format(rst.Time,ch.Time))
                break

