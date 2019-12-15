# -*- coding: utf-8 -*-
import os,socket,threading
import NewsInterface as NI
from apscheduler.schedulers.background import BackgroundScheduler

def NewsServer():         
    while True:
        message = conn.recv(1024)
        
        idNumber, category = str(message,'utf-8').split('|')
        
        if NI.NewsIdentify(idNumber):
            path = NI.NewsGetFunction(idNumber,category)
            
            file_size = os.stat(path).st_size
            
            conn.sendall(bytes(str(file_size),'utf-8'))
            
            has_sent = 0
        
            with open(path,'rb') as fp:
                while has_sent != file_size:
                    data = fp.read(1024)
                    
                    conn.sendall(data)
                    
                    has_sent += len(data)
                    
                    print("[傳送進度]:%s%.02f%%" % 
                          ('>' * int((has_sent / file_size) * 50),
                          float(has_sent / file_size) * 100), end = '\n')
            print("傳送成功")
            conn.close()
            break
        else:
            conn.sendall(bytes('byebye','utf-8'))
            conn.close()
            break

def crawlerExecutor():
    NI.NewsAddFunction()
    
    sched = BackgroundScheduler()
    sched.add_job(NI.NewsAddFunction,'interval', hours = 1)
    sched.start()

threadForCrawlerExecutor = threading.Thread(target = crawlerExecutor)
threadForCrawlerExecutor.setDaemon(True)
threadForCrawlerExecutor.start()

ipPort = ('192.168.0.4',1194)
    
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sk.bind(ipPort)

sk.listen(5)

baseDir = os.path.dirname(os.path.abspath(__file__))

print("waiting...")

while True:
    conn,addr = sk.accept()
    print("{0},{1} Hello!".format(addr[0],addr[1]))
    
    thread = threading.Thread(target = NewsServer)
    thread.setDaemon(True)
    thread.start()