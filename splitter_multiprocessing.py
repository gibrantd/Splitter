from multiprocessing import Pool
from time import sleep
import os,fnmatch
import datetime
import sys
import pika
import subprocess
from subprocess import PIPE, Popen



#test

def f(file): 
    arraySplit = []           
    filePath =  "/Users/interware/Documents/IW/PROSA/Match-Interredes/Lab/tef/" + file    
    #credentials = pika.PlainCredentials('guest', 'guest')
    #parameters = pika.ConnectionParameters('localhost',
                                     #  15672,
                                     #  '/',
                                     #  credentials)

    connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.environ.get('HOSTNAME'), port=5672,
                credentials=pika.PlainCredentials(username='prosa', password='prosa')          
            )
        )
    channel = connection.channel()
    channel.queue_declare(queue="PROSA-CHUNK")

    cnt = 0       
    init = datetime.datetime.now()
    log = open(fileLog, "a")
    log.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%s")+" INFO - Splitter: Iniciando: "+file+"\n")     
    print(filePath)     
    log.close()
    os.system("cd /Users/interware/Documents/IW/PROSA/Match-Interredes/Lab/init/")   
    os.system("split -l "+str(num)+" "+filePath+" "+filePath.replace(".txt","-chunk"))

    os.system("mv "+filePath+" "+filePath+".procesado")
    os.system("mv "+filePath.replace(".txt","-chunk")+"* /Users/interware/Documents/IW/PROSA/Match-Interredes/Lab/init/")
    p=subprocess.Popen("ls -ltr /Users/interware/Documents/IW/PROSA/Match-Interredes/Lab/init/"+filePath.replace("/Users/interware/Documents/IW/PROSA/Match-Interredes/Lab/tef/","").replace(".txt","-")+"* |  awk -F\"init/\" '{print $2}' ",stdout=subprocess.PIPE,shell=True)
    (output,err) = p.communicate()
    arraySplit= str(output).replace("b'","").replace("'","").split("\\n") 
  
    
    for m in arraySplit:
        if len(m)>1:
            print(m)
            channel.basic_publish(exchange='', routing_key='PROSA-CHUNK', body=m)                 
    connection.close()          

    end = datetime.datetime.now()    
    log = open(fileLog, "a")
    log.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%s")+" INFO - Splitter: Terminando: "+file+" tomó "+str(end - init )+" \n") 
    log.close()
    


if __name__ == '__main__':       
    #for arg in sys.argv[1:]:
        #num=arg
    num=os.environ.get('SPLIT')    
    fileLog =  "/Users/interware/Documents/IW/PROSA/Match-Interredes/Lab/logs/process.log"    
    log = open(fileLog, "a")
    log.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%s")+" INFO - Iniciando Splitter \n")
    log.close() 
    while True:
    # start 4 worker processes
        inputDir = "/Users/interware/Documents/IW/PROSA/Match-Interredes/Lab/tef"           
        with Pool(processes=int(os.environ.get('POOL'))) as pool:            
            # print "[0, 1, 4,..., 81]"
            pool.map(f, fnmatch.filter(os.listdir(inputDir), '*.txt'))
           
        

       
