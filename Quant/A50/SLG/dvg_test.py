import Quant.A50.data.csv as csv
import Quant.A50.SLG.dvg as dvg

def test():
    df1d = csv.GetPDdata() # data prepare
    dvg.IsExtmAndTurn(df1d)


test()