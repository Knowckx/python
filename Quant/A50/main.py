import Quant.A50.data.csv as csv
import Quant.A50.SLG.dvg as dvg

def test():
    df = csv.GetPDdata() # data prepare
    df = AssignDF(df,"2017-07-25")
    # print(df[-3:])

    for i in range(0,300):
        # print(df[-3:])
        tar = df.index[-1]
        df.drop([tar],inplace = True)
        
        idxNext = dvg.Start(df)
        if idxNext != -1:
            df = df.loc[0:idxNext]
            print("New DF -- last ",df.loc[df.index[-1], 'time'])

def AssignDF(df,date):
    while True:
        # print(df[-1:])
        tar = df.index[-1]
        newT = df.loc[tar,"time"]
        if newT != date:
            df.drop([tar],inplace = True)
            continue
        break
    return df

test()