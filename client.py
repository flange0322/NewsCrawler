# -*- coding: utf-8 -*-
import os,socket

def client(idNumber,category):
    ipPort = ('127.0.0.1',1194)
    
    sk = socket.socket()
    
    sk.connect(ipPort)
    
    baseDir = os.path.dirname(os.path.abspath(__file__))
    
    while True:        
        sk.sendall(bytes(idNumber + '|' + category,'utf-8'))
        
        message = sk.recv(1024)
        if str(message,'utf-8') == 'byebye':
            print(str(message,'utf-8'))
            sk.close()
            break
        else:
            path = os.path.join(baseDir,'news.mp3')
            
            file_size = int(str(message,'utf-8'))
            
            has_sent = 0
            
            with open(path,'wb') as fp:
                while has_sent != file_size:
                    data = sk.recv(1024)
                    
                    fp.write(data)
                    
                    has_sent += len(data)
                    
                    print("[下載進度]:%s%.02f%%" % 
                             ('>' * int((has_sent / file_size) * 50),
                             float(has_sent / file_size) * 100), end = '\n')
            print("下載成功")
            sk.close()
            break
        
client(idNumber = 'RespeakerTester001',category = 'health')