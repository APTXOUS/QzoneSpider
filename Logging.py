import time



def logout(type,message):
    localtime = time.asctime(time.localtime(time.time()))
    print("[%s] %s : %s"%(type,str(localtime),message))