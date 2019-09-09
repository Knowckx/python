
import Quant.A50.data.csv as csv
import Quant.A50.SLG.dvg as dvg


class BackTest:
    def __init__(self, sheetname):
        excelFile = 'A50'
        # 所使用的验证数据集
        self.verifyDF = csv.GetPDExcel(excelFile, sheetname)
        self.Idx = 0

    # 给定原始数据集，开始验证 | 倒序 直到dvg日期对不上
    def StartWith(self, df,grade):
        self.srcDF = df
        dvg.Init(grade)
        self.StartLoop()


    def StartLoop(self):
        df = self.srcDF
        idx = len(df)  # 数据集是idx倒退200bar
        gap = 200

        ch = self.GetNextVerify()
        while True:
            dftest = self.srcDF[idx-gap:idx]
            if len(dftest) < gap:
                break
            rst = dvg.Start(dftest) # 开始
            # print(dftest.time.iat[-1])
            
            if rst.F_hl == 0:
                idx -=1
                continue
            rst.Print()
            if rst.IsSame(ch):
                print("success at Result:{} Need:{}\n".format(rst.Time,ch.Time))
                idx -=1
                ch = self.GetNextVerify()
                if ch == None:
                    print("finished!!")
                continue
            else:
                print("stop at tar:{} need:{}".format(rst.Time,ch.Time))
                break


    # excel里的下一个验证点
    def GetNextVerify(self):
        df = self.verifyDF
        if self.Idx >= len(df):
            return dvg.DvgRst()
        verf = dvg.DvgRst()
        verf.F_hl = df["type"].iat[self.Idx]
        verf.Time = df["time"].iat[self.Idx]
        if df["Fix"].iat[self.Idx] == 1:
            verf.Patch = "Fixed"
        self.Idx += 1
        return verf
