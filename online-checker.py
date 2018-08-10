#!/usr/bin/python
# -*- coding:utf8 -*-
import threading
import sys
import re

is_py2 = (sys.version_info[0] == 2)
if is_py2:
    import Queue
    import urllib2
    workQueue = Queue.Queue()
else:
    import queue
    import urllib.request
    workQueue = queue.Queue()

output_file_200=open('checked_200.txt','a+')
output_file_302=open('checked_302.txt','a+')
error_file=open('error.txt','a+')

queueLock = threading.Lock()
thread_num = 50
threads = []


class MyThread (threading.Thread):
    def __init__(self, Queue,id):
        threading.Thread.__init__(self)
        self.q = Queue

    def run(self):
        while not workQueue.empty():
            check_online(self.q.get())



def check_online(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
        if is_py2:
            request = urllib2.Request(url=url, headers=headers)
            html = urllib2.urlopen(request)
        else:
            request = urllib.request.Request(url=url, headers=headers)
            html= urllib.request.urlopen(request)
        status_code=html.code
        if status_code == 200:
            queueLock.acquire()
            output_file_200.write(url+'\n')
            output_file_200.flush()
            print_color("[+] %s 200 ok" % url,'blue')
            queueLock.release()
        elif status_code == 302:
            queueLock.acquire()
            output_file_302.write(url+'\n')
            output_file_200.flush()
            print_color("[+] %s 302 ok" % url,'gray')
            queueLock.release()
    except Exception as e:
        error_file.write('%s    %s\n'%(url,str(e)))
        error_file.flush()
        print(str(e))

def print_color(data,color="white"):
    if color == 'green': print('\033[1;32m%s\033[1;m' % data)
    elif color == 'blue' : print('\033[1;34m%s\033[1;m' % data)
    elif color=='gray' : print('\033[1;30m%s\033[1;m' % data)
    elif color=='red' : print('\033[1;31m%s\033[1;m' % data)
    elif color=='yellow' : print('\033[1;33m%s\033[1;m' % data)
    elif color=='magenta' : print('\033[1;35m%s\033[1;m' % data)
    elif color=='cyan' : print('\033[1;36m%s\033[1;m' % data)
    elif color=='white' : print('\033[1;37m%s\033[1;m' % data)
    elif color=='crimson' : print('\033[1;38m%s\033[1;m' % data)
    else : print(data)

logo='''
   ___       _ _                ___ _               _             
  /___\_ __ | (_)_ __   ___    / __\ |__   ___  ___| | _____ _ __ 
 //  // '_ \| | | '_ \ / _ \  / /  | '_ \ / _ \/ __| |/ / _ \ '__|
/ \_//| | | | | | | | |  __/ / /___| | | |  __/ (__|   <  __/ |   
\___/ |_| |_|_|_|_| |_|\___| \____/|_| |_|\___|\___|_|\_\___|_|   
                                                                  
An adaptive URL online checker for python2 and python3
'''
def main():
    print_color(logo,'green')
    if len(sys.argv)!=2:
        print_color("Usage: python online-checker.py filename",'blue')
        exit()

    f=open(sys.argv[1],'r')
    for i in f.readlines():
        workQueue.put(i.strip())
    for i in range(thread_num):
        thread = MyThread(workQueue, i)
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
