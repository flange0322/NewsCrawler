# -*- coding: utf-8 -*-
from datetime import datetime
import NewsCrawler
import NewsMysqlSetting as NMS
import NewsVoiceGenerate as NVG
import NewsTypeInfo as NTI
from time import sleep
import random

def NewsAddFunction():
    SQLconnectionObj_Add = NMS.DBConfigSetting()
    
    NVG.fileFolderInit(NTI.NewsFilePath_dict)
    
    TodayY = datetime.now().year
    TodayM = datetime.now().month
    TodayD = datetime.now().day
    
    news_Url = 'https://www.ettoday.net/news/news-list-' + str(TodayY) + '-' + str(TodayM) + '-' + str(TodayD) + '-'
    
    for i in NTI.NewType_dict.keys():
        htmls = news_Url + NTI.NewType_dict[i] + '.htm'
        news = NewsCrawler.News_Crawler(html = htmls)
        List = news.getNewsData()
        print(i + ' Start')
        
        nowPosNews = 0
        allNewsSize = len(List)
        for j in range(len(List)):
            if(SQLconnectionObj_Add.newsIsRepeat(List[j].getTitle())):
                allNewsSize = allNewsSize - 1
                continue;       
            nowPosNews = nowPosNews + 1
            
            print(str(nowPosNews) + '/' + str(allNewsSize))
            
            SQLconnectionObj_Add.insertToNewsInfo(
                    NewsId = IdMaker(str(SQLconnectionObj_Add.searchCounts('NewsInfo') + 1),"NewsData"),
                    category = List[j].getCategory(),
                    title = List[j].getTitle(),
                    date = List[j].getDate() + ':00',
                    filePath = NewsFilePathMaker(List[j].getCategory()))
            
            sentence = NVG.sentenceMerge(news.getNewsContent(List[j].getHtml()))
            
            NVG.voiceGenerate(sentence,List[j].getTitle(),NewsFilePathMaker(List[j].getCategory()))
            sleep(5)
            
        print(i + ' end')        
    SQLconnectionObj_Add.allClose()

def NewsIdentify(idNumber):
    SQLconnectionObj_Identify = NMS.DBConfigSetting()
    if SQLconnectionObj_Identify.idNumberIsExist(idNumber):
        SQLconnectionObj_Identify.allClose()
        return True
    else:
        SQLconnectionObj_Identify.allClose()
        return False
    
def NewsGetFunction(idNumber,category):
    SQLconnectionObj_Get = NMS.DBConfigSetting()
    
    chineseCategory = None
    isPass = False
    for i in NTI.NewsFilePath_dict.keys():
        if NTI.NewsFilePath_dict[i] == category:
            chineseCategory = i
            isPass = True
            break
    
    if isPass:
        newsPathDict = SQLconnectionObj_Get.getNewsPath(chineseCategory)
        tmp = newsPathDict[random.randint(0,len(newsPathDict)-1)]
        
        SQLconnectionObj_Get.insertToSearchRecord(
                TaskId = IdMaker(str(SQLconnectionObj_Get.searchCounts('SearchRecord') + 1),"RecordData"),
                UserId = idNumber,
                NewsCategory = chineseCategory,
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        SQLconnectionObj_Get.allClose()
        return tmp['filepath'] + '\\' + tmp['Newstitle'] + '.mp3'
    else:
        SQLconnectionObj_Get.allClose()
        return 'C:\\Users\\User\\Desktop\\newsVoice\\CategoryErrorResponse.mp3'
               
def IdMaker(count,header):
    while len(count) < 8:
        count = '0' + count
    return header + count

def NewsFilePathMaker(category):
     filePathMaker = NTI.NewsFilePath_dict
     path = 'C:\\Users\\User\\Desktop\\newsVoice\\' + filePathMaker[category] + '\\' + str(datetime.now().year) + '-' + str(datetime.now().month) + '-' + str(datetime.now().day)
     return path