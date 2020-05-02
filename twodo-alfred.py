#!/usr/bin/local/python3
import sys
import json
import re
from datetime import datetime
import subprocess
import time
import urllib.parse
from logg import *
# all parameters should've been url-encoded but seems working fine without it

def check_date_format(t :str) -> bool:
    regex = re.compile('^(0?[1-9]|[12]\d|3[01])(\/(0?[1-9]|1[0-2])(\/(\d{2})?\d{2})?)?$')
    if re.search(regex, t):
        return True
    else:
        return False

def parse_date(tp :str) -> tuple:
    if check_date_format(tp):
        #return tp
        ts = list(map(int, tp.split('/')))
        if len(ts) > 2: # more than 2 elements
            if ts[2] > 2000:
                d = datetime(ts[2], ts[1], ts[0])
            else:
                d = datetime(2000+ ts[2], ts[1], ts[0])
        elif len(ts) == 2:
            cur_year = datetime.now().year
            d = datetime(cur_year, ts[1], ts[0])
        else:
            d = datetime.now()
            cur_day = d.day
            cur_year = d.year
            if ts[0] < cur_day:
                cur_month = d.month + 1
            else:
                cur_month = d.month
            d = datetime(cur_year, cur_month, ts[0])
        return d

def cal_date(tp :str) -> int:
    tar_date = parse_date(tp)
    dn = datetime.now()
    cur_date = datetime(dn.year, dn.month, dn.day)
    return (tar_date - cur_date).days

def check_time_format(t):
    regex = re.compile('^[0-1]?[0-9](:[0-5]?[0-9])?(pm)?$')
    if re.search(regex, t):
        return True
    else:
        return False

def cal_time(t :str):
    if check_time_format(t):
        if t.endswith('pm'):
            return t.replace('pm', ' pm')
        else:
            return t

def check_weekday_format(t: str):
    weekdays_sub = ['mon','tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    weekdays_sup = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    t = t.lower()
    if t in weekdays_sub or t in weekdays_sup or t == 'today' or t == 'tomorrow':
        return True
    else:
        return False

def cal_weekday(t :str) -> int:
    dt = datetime.now()
    current_weekday = dt.weekday()
    if type(t) == str:
        t = t.lower()
        weekdays_sub = ['mon','tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        weekdays_sup = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if t == 'today':
            return 0
        elif t == 'tomorrow':
            return 1
        elif t in weekdays_sub:
            target_weekday = weekdays_sub.index(t)
        elif t in weekdays_sup:
            target_weekday = weekdays_sup.index(t)
        else:
            target_weekday = dt.weekday()

        if target_weekday < current_weekday:
            n = target_weekday - current_weekday + 7
        else:
            n = target_weekday - current_weekday
    elif type(t) == int:
        if t < dt.weekday():
            n = t - current_weekday + 7 # day in index num
        else:
            n = t - current_weekday
    else:
        raise ValueError
    return n

def parse_query(q):
    d = dict()
    d['args'] = list()
    d['time'] = ''
    d['priority'] = ''
    d['forlist'] = ''
    d['task'] = ''
    d['locations'] = ''
    d['due'] = ''
    d['dueTime'] = ''
    d['tags'] = list()
    d['action'] = ''
    d['start'] = None
    d['action'] = ''

    # split
    q_split = q.split(' ')
    logger.debug(q_split)
    # web detection
    if '-web' in q_split:
        try:
            currentTabUrl = str(subprocess.check_output(['osascript', 'browser.scpt']))[2:-3]
            url = "url:" + currentTabUrl
            # if currentTabUrl == "browser not in front":
            if currentTabUrl == 'You need a supported browser as your frontmost app':
                url = ""
        except:
            url = ""
        d['action'] = url
        q_split[q_split.index('-web')] = ''
    args = ['-proj', '-check']
    for arg in args:
        if arg in q_split:
            try:
                d['args'].append(arg)
            except:
                d['args'] = list()
                d['args'].append(arg)
            q_split.remove(arg)
    # params = ['*', '**', '***', '@', '#']
    for q_i in range(len(q_split)):
        if re.search('^\*{1,3}$', q_split[q_i]):
            logger.debug('importance detected')
            d['priority'] = str(len(re.findall('\*', q_split[q_i])))
            q_split[q_i] = ''
        elif re.search('^@.*', q_split[q_i]):
            logger.debug('list selection detected')
            d['forlist'] = q_split[q_i].replace('@', '')
            q_split[q_i] = ''
        elif re.search('^\#.*', q_split[q_i]):
            logger.debug('hashtag detected')
            try:
                d['tags'].append(q_split[q_i].replace('#',''))
            except KeyError:
                d['tags'] = list()
                d['tags'].append(q_split[q_i].replace('#',''))
            q_split[q_i] = ''
    
    pre = ['on', 'at', 'by', 'from', 'near']
    for q_i in range(len(q_split)):
        rem = 0
        if q_split[q_i] in pre:
            if q_split[q_i] == 'near':
                d['locations'] = q_split[q_i + 1]
                q_split[q_i] = ''
                q_split[q_i + 1] = ''
                rem = 1
            elif q_split[q_i] == 'from':
                start = q_split[q_i + 1]
                if check_date_format(start):
                    d['start'] = cal_date(start)
                    rem = 1
                elif check_weekday_format(start):
                    d['start'] = cal_weekday(start)
                    rem = 1
                elif check_time_format(start):
                    d['start'] = cal_time(start)
                    rem = 1
            else:
                if check_date_format(q_split[q_i + 1]) or check_weekday_format(q_split[q_i + 1]) or check_time_format(q_split[q_i + 1]):
                    tar = q_split[q_i + 1]
                    if check_date_format(tar):
                        d['due'] = cal_date(tar)
                        rem = 1
                    elif check_weekday_format(tar):
                        d['due'] = cal_weekday(tar)
                        rem = 1
                    elif check_time_format(tar):
                        d['dueTime'] = cal_time(tar)
                        rem = 1
            if rem:
                q_split[q_i] = ''
                q_split[q_i + 1] = ''
    
    if 'today' in q_split:
        d['due'] = 0
        q_split[q_split.index('today')] = ''
    elif 'tomorrow' in q_split:
        d['due'] = 1
        q_split[q_split.index('tomorrow')] = ''
    
    if d['dueTime'] is not '' and d['due'] is '':
        d['due'] = 0

    t = ' '.join(q_split).strip()
    t = re.sub(' +', ' ', t)
    return t, d


def main():
    query = sys.argv[1]
    # time.sleep(0.5)

    e, d = parse_query(query)
    l = d['forlist']
    p = d['locations']
    da = d['due']
    t = d['dueTime']
    ta = ','.join(d['tags'])
    url = d['action']
    pr = d['priority']
    start = d['start']
    baseurl = "twodo://x-callback-url/add?task=" + e + \
        "&forlist=" + l + \
        "&locations=" + p + \
        "&due=" + str(da) + \
        "&dueTime=" + str(t) + \
        "&tags=" + ta + \
        "&action=" + url + \
        "&priority=" + str(pr)
        # "&start=" + str(start)

    if start is not None:
        baseurl += "&start=" + str(start)
    
    if '-proj' in d['args']:
        print(baseurl+'&type=1')
    elif '-check' in d['args']:
        print(baseurl+'&type=2')
    else:
        print(baseurl+'&type=0')

if __name__ == '__main__':
    main()
