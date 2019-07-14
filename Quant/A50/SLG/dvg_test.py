


import pandas as pd

import Quant.A50.SLG.dvg  as  dvg
import Quant.A50.data.csv as csv


# 入口
def Test_IsExtmAndTurn():
    df = csv.GetPDdata() # data prepare
    # plist = df.close

    for i in range(0,100):
        # print(df[-3:])
        tar = df.index[-1]
        df.drop([tar],inplace = True)
        
        plist = df.close
        rst = dvg.IsExtmAndTurn(plist)
        if rst !=0 :
            ti = df.loc[tar-1, 'time']
            print("%s,%d"%(ti,rst))