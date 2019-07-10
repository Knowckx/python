

IsLog = true


def Print(msg):
    if !IsLog:
        return
    print(msg)


def SetIsLog(bo):
    IsLog = bo
