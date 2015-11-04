__author__ = 'runwei_zhang'
import unirest
import xml.etree.ElementTree as ET
import threading
from threading import Thread, Lock
from datetime import datetime
import time
import csv
import os.path

mutex = Lock()
timeset = set()
curday = ''

def callback_function(response):
    global curday
    global timeset
    root = ET.fromstring(response.raw_body)
    timestr = root.attrib['{http://www.yahooapis.com/v1/base.rng}created']
    dt = datetime.strptime(timestr,"%Y-%m-%dT%H:%M:%SZ")
    epoche = time.mktime(dt.timetuple())
    list = []
    for i in xrange(0,len(root[0])):
        list.append(root[0][i][0].text)
    if epoche not in timeset:
        print epoche,list
        mutex.acquire()
        if dt.date() != curday:
            curday = dt.date()
            timeset.clear()
        with open('%s.txt'%curday, 'a') as the_file:
            the_file.write('%s'%epoche)
            for item in list:
                the_file.write(",%s" % item)
            the_file.write("\n")
        timeset.add(epoche)
        mutex.release()


def sendrequest():
    url = 'http://query.yahooapis.com/v1/public/yql?q=select%20Rate%20from%20yahoo.finance.xchange%20where%20pair%20in%20("USDEUR",%20"USDJPY",%20"USDGBP",%20"USDCHF",%20"USDRUB",%20"USDBRL",%20"USDCNY",%20"USDINR",%20"USDSGD")&env=store://datatables.org/alltableswithkeys'
    thread = unirest.post(url, callback=callback_function)

def schedulerFun():
    sendrequest()
    threading.Timer(0.5, schedulerFun).start()

def readtimeset():
    global curday
    global timeset
    dt = datetime.now()
    curday = dt.date()
    file_path = '%s.txt'%curday
    if os.path.exists(file_path):
        with open(file_path, 'r') as the_file:
            csvreader = csv.reader(the_file)
            for line in csvreader:
                timeset.add(float(line[0]))

if __name__ == '__main__':
    readtimeset()
    schedulerFun()