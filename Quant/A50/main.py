import Quant.A50.data.csv as csv
import Quant.A50.SLG.dvg as dvg
import sys


def test():
    tarFile = '601318_5m'
    df = csv.GetPDdata(tarFile)  # data prepare

    # print(df[-1:])  # test DF

    # TestInOneDay(df,"2019-05-24")

    # fix = 17
    for i in range(0, 600):
        # tar = df.index[-1]
        # df.drop([tar],inplace = True)
        dftest = df[:i-601]
        dvg.Start(dftest)

def TestInOneDay(df, date):
    df = AssignDF(df,date)
    print(df[-1:])
    dvg.Start(df)
    sys.exit(0)



def AssignDF(df, date):
    while True:
        # print(df[-1:])
        tar = df.index[-1]
        newT = df.loc[tar, "time"]
        if newT != date:
            df.drop([tar], inplace=True)
            continue
        break
    return df


test()
