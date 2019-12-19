import requests
import json
import time
import sqlite3
import QzoneLogin
import Logging
import sys

checklist=[] #添加要关注的QQ号

referer='https://user.qzone.qq.com/'
targeturl='https://user.qzone.qq.com/'


def getListofvisitors(cookies,qzonetoken,g_tk):

    cookie = cookies
    get_url = targeturl+'&g_tk='+str(g_tk)+'&qzonetoken='+qzonetoken+'&g_tk='+str(g_tk)

    headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'referer': referer,
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
    
    
    }
    # 每次都要加带有cookie的headers
    b = requests.get(get_url,headers=headers,cookies=cookies) 


    # 使用json解析Callback
    jsonstring=b.text
    jsonstring=jsonstring[jsonstring.find("(")+1:]
    jsonstring=jsonstring[:len(jsonstring)-2]
    jsonstring=jsonstring.replace("\'","\"")

    fo = open("test.txt", "w")
    fo.write(jsonstring)
    # 关闭打开的文件

    fo.close()


    user_dict = json.loads(jsonstring)

    visitors=list()

    for visitor in user_dict["data"]["module_3"]["data"]["items"]:
        if visitor["uin"] in checklist:
            timeStamp = visitor['time']
            timeArray = time.localtime(timeStamp)
            # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            # output=otherStyleTime+" :"+visitor["name"]+"("+str(visitor["uin"])+")访问了您的空间"
            visitors.append({"time":str(visitor['time']),"name":visitor["name"],"uin":str(visitor["uin"])})

    return visitors

def checkHistory(sqlcursor,dict):
    SQL="select * from VisitHistory where TIME="+dict["time"]+" AND UIN= \""+dict["uin"]+"\""
    sqlcursor.execute(SQL)
    values = sqlcursor.fetchall()
    return len(values)

def insertHistory(sqlcursor,dict):
    SQL="INSERT INTO VisitHistory (TIME, UIN, NAME) VALUES (\""+dict["time"]+"\",\""+dict["uin"]+"\",\""+dict["name"]+"\")"
    sqlcursor.execute(SQL)
    return sqlcursor.rowcount

def insertHistory(sqlcursor,dict):
    SQL="INSERT INTO VisitHistory (TIME, UIN, NAME) VALUES (\""+dict["time"]+"\",\""+dict["uin"]+"\",\""+dict["name"]+"\")"
    sqlcursor.execute(SQL)
    return sqlcursor.rowcount

def showHistory(sqlcursor):
    sqlcursor.execute('select * from VisitHistory' )

    values = sqlcursor.fetchall()

    print(values)


def spiderstart(sqldb,qq,pwd):

    cookies,qzonetoken,g_tk=QzoneLogin.loginQzone(qq,pwd)
    sqlcursor = sqldb.cursor()

    while 1:
        try:
            while 1: # 暂且使用阻塞方式，以后改为定时
                dicts=getListofvisitors(cookies,qzonetoken,g_tk)
                for dict in dicts:
                    newtime=dict["time"]
                    if checkHistory(sqlcursor,dict)==0:
                        insertHistory(sqlcursor,dict)
                        sqldb.commit()
                        Logging.logout("WARNING",dict["name"]+"("+dict["uin"]+")访问了您的空间")
                    else:
                        Logging.logout("NOMARL"," : Nothing happened")
                time.sleep(60)
        except:
            cookies,qzonetoken,g_tk=QzoneLogin.loginQzone(qq,pwd)
            Logging.logout("ERROR"," : Server Down! Get new cookies!")





def sqliteinit():
    conn = sqlite3.connect('QzoneVisitors.db')
    cursor = conn.cursor()
    cursor.execute('create table IF NOT EXISTS VisitHistory (ID INTEGER PRIMARY KEY autoincrement    NOT NULL, TIME INT,UIN varchar(20),NAME varchar(50)) ')
    cursor.close()
    conn.commit()
    return conn





if __name__ == "__main__":
    # 改用命令行输入QQ号和密码
    spiderstart(sqliteinit(),sys.argv[1],sys.argv[2])
