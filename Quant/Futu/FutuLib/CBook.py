
import pandas as pd
from Alchemy.bookut import bookdiff,mean


class Book:
    def __init__(self, FutuBook):
        self.SID = FutuBook["code"]
        self.AskL = FutuBook["Ask"]
        self.BidL = FutuBook["Bid"]
        self.Mean = mean.GetPredictP(self.AskL[:5],self.BidL[:5])

    def ToDF(self):
        df = pd.DataFrame()
        for i in range(5, 0,-1):
            s = self.BidL[i-1]
            df['Bid'+str(i)] = [s]
        df['core'] = self.Mean
        for i in range(0, 5):
            s = self.AskL[i]
            df['Ask'+str(i+1)] = [s]
        return df

    def GetDiff(self,AskL1,BidL1):
        if len(AskL1) == 0:
            return None
        rstDiff = bookdiff.Start(AskL1,BidL1,self.AskL[:5],self.BidL[:5])
        return rstDiff

def ListToStr(ins):
    for i in range(0, len(ins)):
        ins[i] = str(ins[i])
    out = ','.join(ins)
    return out


def HandleFutuBookList():
    pass
