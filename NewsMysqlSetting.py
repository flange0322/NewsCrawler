# -*- coding: utf-8 -*-
import pymysql
from datetime import datetime

class NewsSQL:
    def __init__(self,connect):
        self.conn = connect
        self.cur = self.conn.cursor()
        self.query_UseDataBase = "use NewsAndUserDB"
        
    def initTable(self):
        try:
            query_CreateDataBase = 'create database NewsAndUserDB'
            query_UserContentTable = 'create table UserInfo(UserId char(20) not null primary key) '
            query_NewsContentTable = 'create table NewsInfo(NewsId char(20) not null primary key,NewsCategory char(4) not null,NewsTitle char(100) not null,DateAndTime DATETIME not null,filePath char(100) not null)'
            query_SearchRecordTable = 'create table SearchRecord(TaskId char(30) not null primary key,UserId char(20) not null,NewsCategory char(4) not null,DateAndTime DATETIME not null,foreign key(UserId) references UserInfo(UserId) on delete cascade)'
            
            self.cur.execute(query_CreateDataBase)
            self.cur.execute(self.query_UseDataBase)
            self.cur.execute(query_UserContentTable)
            self.cur.execute(query_NewsContentTable)
            self.cur.execute(query_SearchRecordTable)
        except:
            print("DB exists.")
        
    def insertToUserInfo(self):
        try:
            query_insertUserInfo = "insert into UserInfo values('RespeakerTester001')"
            self.cur.execute(query_insertUserInfo)
        except:
            print("UserData Input Succeeded.")
        
    def insertToNewsInfo(self,NewsId,category,title,date,filePath):
        self.cur.execute(self.query_UseDataBase)
        self.cur.execute("insert into NewsInfo values(%s,%s,%s,%s,%s)",(NewsId,category,title,date,filePath))
    
    def newsIsRepeat(self,title):
        self.cur.execute(self.query_UseDataBase)
        self.cur.execute("select NewsTitle from NewsInfo where NewsTitle = %s",(title))
        if(len(self.cur.fetchall()) == 0):
            return False
        else:
            return True
    
    def searchCounts(self,tableName):
        self.cur.execute(self.query_UseDataBase)
        query_searchCounts = "select * from %s" % (tableName)
        self.cur.execute(query_searchCounts)
        dataLen = len(self.cur.fetchall())
        return dataLen
    
    def idNumberIsExist(self,idNumber):
        self.cur.execute(self.query_UseDataBase)
        self.cur.execute("select * from UserInfo where UserId = %s",(idNumber))
        if(len(self.cur.fetchall()) == 0):
            return False
        else:
            return True
    
    def getNewsPath(self,category):
        self.cur.execute(self.query_UseDataBase)
        
        date = str(datetime.now().year) + '-' + str(datetime.now().month) + '-' + str(datetime.now().day)
        self.cur.execute("select filepath,Newstitle from NewsInfo where NewsCategory = %s and DateAndTime >= %s",(category,date))
        return self.cur.fetchall()
    
    def insertToSearchRecord(self,TaskId,UserId,NewsCategory,date):
        self.cur.execute(self.query_UseDataBase)
        self.cur.execute("insert into searchrecord values(%s,%s,%s,%s)",(TaskId,UserId,NewsCategory,date))
        
    def allClose(self):
        self.cur.close()
        self.conn.commit()
        self.conn.close()
        print("DB close.")
        
def DBConfigSetting():
    connection = pymysql.connect(
            user = "root",
            password = "respeaker74561195",
            port = 1195,
            host = "127.0.0.1",
            db = "MYSQL",
            charset = "utf8",
            cursorclass = pymysql.cursors.DictCursor)
    
    newsSQL = NewsSQL(connect = connection)
    newsSQL.initTable()
    newsSQL.insertToUserInfo()
    return newsSQL