
from . import FutuUtil


def GetPriceNow(bookN):
    AskL = bookN['Ask']
    BidL = bookN['Bid']
    P0 = GetBan(AskL[0], BidL[0])
    P1 = GetBan(AskL[1], BidL[1])
    P2 = GetBan(AskL[2], BidL[2])
    if P1 == -1:
        P1 = P0
    if P2 == -1:
        P2 = P0
    rst = 0.7*P0 + 0.2*P1 + 0.1*P2
    rst = round(rst, 5)
    return rst


def GetBan(B0, S0):
    tvo = B0[1]+S0[1]
    if tvo == 0:
        return -1
    p = (S0[1]/tvo*B0[0])+(B0[1]/tvo*S0[0])
    return p
