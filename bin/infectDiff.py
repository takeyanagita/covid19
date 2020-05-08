#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date
import re
import os
import sys

ddir = os.environ['KOUROUDATA']
dname = 'kourouKanjaDay.dat'
city_namedb = 'shichoson.db'
cnvTab = str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})
gappiTab = str.maketrans({'#':'','月':' ','日':' '},)
dorigin = date(2020,1,1).toordinal()

# 使用法: infectDiff.py [都道府県名]
# 都道府県名を省略すると全国を指定したことになる.

argvs = sys.argv
pref = ''
if len(argvs) == 1 :
    pref = '全国'
elif len(argvs) == 2 :
    pref = argvs[1]
else :
    quit()

class mydate:
    def __init__(self):
        self.sday = ''
        self.year = 0
        self.month = 0
        self.day = 0
        self.totaldays = 0

    def setDate(self, sday='', y=0, m=0, d=0, totaldays=-1):
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

shichoson_tab = {}

def make_shichosontable():
    fp = open(ddir+'/'+city_namedb,'r')
    for line in fp:
        line = line.rstrip('\n')
        d = line.split(' ')
        shichoson_tab[d[0]] = d[1]
    fp.close()

def reformline(line):
    nline = (line.translate(cnvTab)).rstrip('\n') # 全角->半角，行末改行除去
    nline = re.sub('\([^\(]*\)',' ', nline)
    return nline

def infectionnumber(line):
    ll = re.sub('[^0-9]+',' ',line)
    d = ll.split(' ')
    if len(d) < 3:
        return 0
    s = 0
    for i in range(len(d)-2):
        s += int(d[i+1])
    return s

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

def is_todohuken(pref, line) :
    hd = re.sub(':.*','',line)
    if not hd in shichoson_tab :
        return False
    else :
        return shichoson_tab[hd] == pref

make_shichosontable()

krFP = open(ddir+'/'+dname,'r')

infection_per_day = -1
acc_on = False

yesterday = mydate()
today = mydate()

for line in krFP:
    nline = reformline(line)
    if is_newday(nline) :
        if infection_per_day >= 0 :
            if not is_nextday(today, yesterday) and yesterday.totaldays > 0 :
                # 感染者0のレコードを挿入
                for i in range(today.totaldays - yesterday.totaldays - 1):
                    yesterday.setDate(totaldays=yesterday.totaldays+i+1)
                    print(yesterday.sday," ",yesterday.totaldays," ",0)
            print(today.sday," ",today.totaldays," ",infection_per_day)
            infection_per_day = -1
            yesterday.setDate(totaldays=today.totaldays)
        date_set(nline, today)
        acc_on = True
    elif is_deathline(nline) :
        acc_on = False
    elif acc_on and not is_emptyline(nline) :
        if pref == '全国' :
            if infection_per_day < 0:
                infection_per_day = 0
            # accumulate infection number
            if not re.search('^[%※患感]',nline) :
                infection_per_day += infectionnumber(nline)
        elif is_todohuken(pref,nline) :
            if infection_per_day < 0:
                infection_per_day = 0
            infection_per_day += infectionnumber(nline)
if infection_per_day >= 0 :
    if not is_nextday(today, yesterday) and yesterday.totaldays > 0 :
        # 感染者0のレコードを挿入
        for i in range(today.totaldays - yesterday.totaldays - 1):
            yesterday.setDate(totaldays=yesterday.totaldays+i+1)
            print(yesterday.sday," ",yesterday.totaldays," ",0)
    print(today.sday," ",today.totaldays," ",infection_per_day)
krFP.close()
