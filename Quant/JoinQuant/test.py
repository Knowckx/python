import jqdata

if __name__ == '__main__':
    import jqsdk
    params = {
        'token':'4a82a9f86897677b7dedf73a268d924c',
        'algorithmId':1,
        'baseCapital':1000000,
        'frequency':'day',
        'startTime':'2017-06-01',
        'endTime':'2017-08-01',
        'name':"Test1",
    }
    jqsdk.run(params)