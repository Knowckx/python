
import datetime

SToday = -1

# def SGetToday():
#     global SToday
#     if SToday == -1:
#         SToday = datetime.date.today().strftime('%Y-%m-%d')
#     return SToday



def SGetTodayMD():
    global SToday
    if SToday == -1:
        SToday = datetime.date.today().strftime('%m-%d')
    return SToday

