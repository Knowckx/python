
import Quant.A50.data.csv as csv
import Quant.A50.SLG.dvg as dvg


class BackTest:
    def __init__(self, sheetname):
        excelFile = 'A50'
        # 所使用的验证数据集
        self.verifyDF = csv.GetPDExcel(excelFile, sheetname)
        self.Idx = 0 # 目前验证已经到的位置

    # 给定原始数据集，开始验证 | 倒序 直到dvg日期对不上
    def StartWith(self, df,grade):
        self.srcDF = df
        dvg.Init(grade)
        self.StartLoop()


    def StartLoop(self):
        df = self.srcDF
        idx = len(df)  
        gap = 200 # 数据集是idx倒退200bar

        ch = self.GetNextVerify()
        while True:
            idx -=1
            dftest = df.loc[idx-gap:idx] # 右包括 | 总长1000，第1个数就是999
            if len(dftest) < gap:
                break
            rst = dvg.Start(dftest) # 开始
            # 开始检查结果
            if rst.F_hl == 0 or rst.Patch != "":
                continue
            Re = FixRedirect(rst,df,idx) # 在回测模式中，一些点位需要重定向一下
            rst.Print()
            if rst.IsSame(ch):
                print("success at Result:{} Need:{}".format(rst.Time,ch.Time))
                if Re == 0:
                    ch = self.GetNextVerify()
                else:
                    print("ReCount is {} Excel Stay +1.".format(Re))
                print("\n")
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
            return dvg.JudgeRst()
        verf = dvg.JudgeRst()
        verf.F_hl = df["f_hl"].iat[self.Idx]
        verf.Time = df["time"].iat[self.Idx]
        if df["Fix"].iat[self.Idx] == 1:
            verf.Patch = "Fixed"
        self.Idx += 1
        return verf


# 对chan类型的结果进行时间重定向 
def FixRedirect(rst,df,idx):
    Re = 0 # 实际重定向的次数
    if rst.Type == dvg.StrChannelSign:
        newIdx = idx
        while newIdx >0:
            newIdx -= 1
            leRst = dvg.IsPriceOutBoll(df,newIdx)
            if leRst == rst.F_hl:
                rst.Time = df.time.at[newIdx] #定位到最佳时间   
                Re += 1
                continue
            break
    return Re
        

