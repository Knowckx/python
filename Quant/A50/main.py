import Quant.A50.data.csv as csv
import Quant.A50.SLG.dvg as dvg


def test():
    df = csv.GetPDdata()  # data prepare
    # df = AssignDF(df,"2018-05-14")
    # print(df[-3:])
    fix = 17
    for i in range(0, 300):
        print(i)
        # tar = df.index[-1]
        # df.drop([tar],inplace = True)
        dftest = df[:i-301 + fix]
        dvg.Start(dftest)

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
