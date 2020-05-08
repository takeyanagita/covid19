#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import re

def sum7(buf, dat):
    sum = 0
    buf.append(dat)
    if(len(buf)>7) :
        buf.pop(0)
    for d in buf:
        sum += d
    return sum

parser = argparse.ArgumentParser()
parser.add_argument('filename', nargs='?')
args = parser.parse_args()

fp = ''

if args.filename is None:
    fp = sys.stdin
else:
    fp = open(filename, 'r')

sum = []

for line in fp:
    line = line.rstrip('\n')
    line = re.sub(' +',' ', line)
    d = line.split(' ')
    s7 = sum7(sum, int(d[2]))
    print(d[0], d[1], s7)
              

    
