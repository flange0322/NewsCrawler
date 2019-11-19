# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

class News_Type:
    def add(self,dt,cg,tle,hl):
        self.date = dt
        self.category = cg
        self.title = tle
        self.html = hl
    
    def getCategory(self):
        return self.category
    
    def getTitle(self):
        return self.title
    
    def getHtml(self):
        return self.html
    
    def getDate(self):
        return self.date
    
class News_Crawler:
    def __init__(self,html):
        self.html = html
        
    def getNewsData(self):
        req = requests.get(self.html).text
        soup = BeautifulSoup(req, 'html.parser')

        date = soup.find_all('span', class_ = 'date')
        tag = soup.find_all('em', class_ = 'tag')
        htag = soup.find_all('h3')
        
        tmp = []
        illegalSign = ['?','/','\'',':','*','<','>','|','"']
        for count in range(10):
            nt = News_Type()
            
            title = htag[count + 3].a.text
            for i in range(len(illegalSign)):
                title.replace(illegalSign[i],'_')

            nt.add(date[count].text,
                   tag[count].text,
                   title.replace(u'\u3000',u'_'),
                   'https://www.ettoday.net' + htag[count + 3].a['href'])
            tmp.append(nt) 
        return tmp
    
    def getNewsContent(self,url):
        req = requests.get(url).text
        soup = BeautifulSoup(req, 'html.parser')
        
        story = soup.find_all('div',class_ = 'story')[0].find_all('p',class_ = '')
       
        story_str = []
        for i in range(len(story)):
            story_str.append(str(story[i]))
        
        result = []
        for i in range(len(story)):
            content = "".join("".join(story_str[i].split()).split('►')) #去除不需要的字元
            if content[3] != '<' or content[len(content) - 2] == 'p' and content[len(content) - 5] != '>': 
                if content.find('＼') != -1 or content.find('／') != -1 or content.find('http') != -1:  
                    continue
                while content.find('<') != -1:
                    pos_start = content.find('<')
                    pos_end = content.find('>')
                    content = content.replace(content[pos_start:pos_end + 1],"")
                result.append(content)
        
        return result

if __name__ == '__main__':
    test = News_Crawler('https://sports.ettoday.net/news/1572327')
    tmp = test.getNewsContent('https://sports.ettoday.net/news/1572327')
    print(tmp)