


import os,sqlite3

#给定站点，找出相应的Cookies
def GetCookieFromChrome(host='.zhihu.com',typeID = 1):
    #C:\Users\Eniru\AppData\Local\Google\Chrome\User Data\Default\Cookies
    cookiepath=os.environ['LOCALAPPDATA']+r"\Google\Chrome\User Data\Default\Cookies"
    
    with sqlite3.connect(cookiepath) as conn:
        cu=conn.cursor()     
        if (typeID == 1) :
            sql="select host_key,name,encrypted_value from cookies where host_key='%s'" % host  #只拿到这几项
            cookies={name:CryptUnprotectData(encrypted_value)[1].decode() for host_key,name,encrypted_value in cu.execute(sql).fetchall()}
        elif (typeID == 2) :
            sql="select * from cookies where host_key='%s'" % host 
            a  = cu.execute(sql).fetchall()
            cookies={name:CryptUnprotectData(encrypted_value)[1].decode() for host_key,name,encrypted_value in cu.execute(sql).fetchall()}            
            pass
    return cookies