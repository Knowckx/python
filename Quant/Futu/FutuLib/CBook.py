
import pandas as pd
from Alchemy.bookut import bookdiff,mean
from  Alchemy.core.c_book import *
from Alchemy.core import corefunc
from Alchemy.core import c_TI_BA




class Book:
    def __init__(self, FutuBook):
        self.SID = FutuBook["code"]
        self.AskL = FutuBook["Ask"][:5]
        self.BidL = FutuBook["Bid"][:5]
        self.Mean = mean.GetPredictP([self.BidL,self.AskL])
        # self.Book1 = CBook([FutuBook["Bid"][:],FutuBook["Ask"][:]],0)
        self.SignBA = c_TI_BA.TIBA(20)



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

    def GetDiff(self):
        bookL = []
        bookL.append(self.BidL)
        bookL.append(self.AskL)
        DifL = corefunc.difToSignal(bookL[:]) 
        self.SignBA.Add(DifL)
        self.SignBA.Print()
        return 

    def Static(self):



def ListToStr(ins):
    for i in range(0, len(ins)):
        ins[i] = str(ins[i])
    out = ','.join(ins)
    return out


def HandleFutuBookList():
    pass
