
import pandas as pd
from Alchemy.bookut import bookdiff,mean
from  Alchemy.core.c_book import *


class Book:
    def __init__(self, FutuBook):
        self.SID = FutuBook["code"]
        self.AskL = FutuBook["Ask"]
        self.BidL = FutuBook["Bid"]
        self.Mean = mean.GetPredictP([self.BidL[:5],self.AskL[:5]])
        self.Book1 = CBook([FutuBook["Bid"][:],FutuBook["Ask"][:]],0)

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
        return self.Book1.DifL
        # if len(AskL1) == 0:
        #     return ""
        # rstDiff = bookdiff.Start(AskL1,BidL1,self.AskL[:5],self.BidL[:5])
        # DiffL = bookdiff.ScreenRst(rstDiff[:])
        # if len(DiffL) ==0:
        #     DiffL = ""
        # return DiffL

def ListToStr(ins):
    for i in range(0, len(ins)):
        ins[i] = str(ins[i])
    out = ','.join(ins)
    return out


def HandleFutuBookList():
    pass
