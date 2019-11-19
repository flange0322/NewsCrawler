# -*- coding: utf-8 -*
from gtts import gTTS
import os

def fileFolderInit(TypePath):
    folderPath = 'C:\\Users\\User\\Desktop\\newsVoice'
    if not os.path.exists(folderPath):
        os.mkdir(folderPath)
        
        for i in TypePath.keys():
            os.mkdir(folderPath + '\\' + TypePath[i])
        voiceGenerate('沒有此類型之新聞，請重新查詢，謝謝','CategoryErrorResponse','C:\\Users\\User\\Desktop\\newsVoice\\')
    
def sentenceMerge(NewsContent):
    result = ''
    for i in range(len(NewsContent)):
        result = result + NewsContent[i]
        if i != len(NewsContent) - 1:
            result = result + '。'
    return result
    
def voiceGenerate(sentence,fileName,filePath):
    if not os.path.exists(filePath):
        os.mkdir(filePath)
        
    print('filePath: ' + filePath)
    print('fileName: ' + fileName)
    
    try:
        newsTTS = gTTS(sentence, lang = 'zh-tw') 
        newsTTS.save("%s.mp3" % os.path.join(filePath,fileName))
    except:
        print('Have a Path Error. Make Sure the fileName.')

    print('Generate Succeeded.')
    print()