
import pandas as pd
from . import calc


class Book:
    def __init__(self, FutuBook):
        self.SID = FutuBook["code"]
        self.AskL = FutuBook["Ask"]
        self.BidL = FutuBook["Bid"]
        self.CoreP = calc.GetPriceNow(self.AskL,self.BidL)

    def ToDF(self):
        df = pd.DataFrame()
        for i in range(5, 0,-1):
            s = ListToStr(self.BidL[i-1])
            df['Bid'+str(i)] = [s]
        df['core'] = [self.CoreP]
        for i in range(0, 5):
            s = ListToStr(self.AskL[i])
            df['Ask'+str(i+1)] = [s]
        return df


def ListToStr(ins):
    for i in range(0, len(ins)):
        ins[i] = str(ins[i])
    out = ','.join(ins)
    return out


def HandleFutuBookList():
    pass
