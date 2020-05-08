#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date
import re
import os

ddir = os.environ['KOUROUDATA']
dname = 'kourouKanjaDay.dat'
cnvTab = str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})
gappiTab = str.maketrans({'#':'','月':' ','日':' '},)
dorigin = date(2020,1,1).toordinal()

class mydate:
    def __init__(self):
        self.sday = ''
        self.year = 0
        self.month = 0
        self.day = 0
        self.totaldays = 0

    def setDate(self, sday='', y=0, m=0, d=0, totaldays=-1):
        #print("%%% ", sday," - ", totaldays)
        if sday == '' :
            tmp = date.fromordinal(totaldays+dorigin)
            self.year = tmp.year
            self.month = tmp.month
            self.day = tmp.day
            self.sday = str(self.year)+'/'+str(self.month)+'/'+str(self.day)
            self.totaldays = totaldays
        else :
            self.sday = sday
            self.year = y
            self.month = m
            self.day = d
            self.totaldays = date(y,m,d).toordinal()-dorigin
# end of mydate

def reformline(line):
    nline = (line.translate(cnvTab)).rstrip('\n') # 全角->半角，行末改行除去
    nline = re.sub('\([^\(]*\)',' ', nline)
    return nline

def deathnumber(line):
    ll = re.sub('[^0-9]+','',line)
    ll = re.sub('[例名].*',' ',ll)
    #print("ll ",today.sday," ",ll)
    d = ll.split(' ')
    if d[0] == '' :
        return 0
    return int(d[0])

def sum7(buf, dat):
    sum = 0
    buf.append(dat)
    if(len(buf)>7) :
        buf.pop(0)
    for d in buf:
        sum += d
    return sum

def date_set(nline, mdate):
    d = (nline.translate(gappiTab)).split(' ')
    sd = '2020/'+d[0]+'/'+d[1]
    mdate.setDate(sd,2020,int(d[0]),int(d[1]))

def is_nextday(d1, d2):
    if (d1.totaldays - d2.totaldays) == 1 :
        return True
    else:
        return False

def is_deathline(line):
    if re.search('^死亡',nline) :
        return True
    return False

def is_newday(line):
    if re.search('^#',nline) :  # is new day?
        return True
    return False

def is_emptyline(line):
    l = re.sub('[ \t　]+','',line)
    if len(l) > 0 :
        return False
    return True

krFP = open(ddir+'/'+dname,'r')

yesterday = mydate()
today = mydate()
death_per_day = -1

for line in krFP:
    nline = reformline(line)
    if is_newday(nline) :
        if death_per_day >= 0 :
            if not is_nextday(today, yesterday) and yesterday.totaldays > 0 :
                # 死亡者0のレコードを挿入
                for i in range(today.totaldays - yesterday.totaldays - 1):
                    yesterday.setDate(totaldays=yesterday.totaldays+i+1)
                    print(yesterday.sday," ",yesterday.totaldays," ",0)
            print(today.sday," ",today.totaldays," ",death_per_day)
            death_per_day = -1
            yesterday.setDate(totaldays=today.totaldays)
        date_set(nline, today)
    elif is_deathline(nline) :
        death_per_day = 0
    elif death_per_day >= 0 and not is_emptyline(nline) :
        # accumulate death number
        death_per_day += deathnumber(nline)
if death_per_day >= 0 :
    if not is_nextday(today, yesterday) and yesterday.totaldays > 0 :
        # 死亡者0のレコードを挿入
        for i in range(today.totaldays - yesterday.totaldays - 1):
            yesterday.setDate(totaldays=yesterday.totaldays+i+1)
            print(yesterday.sday," ",yesterday.totaldays," ",0)
    print(today.sday," ",today.totaldays," ",death_per_day)
