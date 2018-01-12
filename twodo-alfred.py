#!/usr/bin/env python
import sys
import json
import re
from datetime import datetime
import subprocess
#import parse
#all parameters should've been url-encoded but seems work fine without it

query = sys.argv[1]

def addtask(txt):
	pre_dat = re.split(' ',txt)
	spl = re.split('( on | in | at |today|tomorrow|\s@|\s\u0023)',txt)

	#event
	e = spl[0]

	# determine duedate
	if 'today' in pre_dat:
		d = str(0)
	elif 'tomorrow' in pre_dat:
		d = str(1)
	elif ' on ' in spl: # on / 'jan' 1 / 1'/'1 / 29 // year should be decided automatically
		dat = re.split(' ',spl[spl.index(' on ')+1].lower())
		#print(dat)
		cur_day = datetime.now().weekday()
		cur_dat = datetime.now().day
		cur_mon = datetime.now().month
		cur_yr = datetime.now().year
		f_m = ['','january','february','march','april','may','june','july','august','september','october','november','december']
		s_m = ['','jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
		f_w = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
		s_w = ['mon','tue','wed','thu','fri','sat','sun']
		a_m = f_m + s_m
		a_w = f_w + s_w
		year_not_in = 1
		weekday_in = 0
		month_not_in = 1
		tdate=""
		### what if jan 1 is before than current date
		for date in dat:
			try:
				year = re.search('\d\d\d\d',date).group()
				year = int(year)
				year_not_in = 0
			except:
				year = cur_yr

			if date in a_m:
				month_not_in = 0
				if date in f_m:
					month = f_m.index(date)
				else:
					month = s_m.index(date)
			elif date in a_w:
				weekday_in = 1
				if date in f_w:
					tdatewd = f_w.index(date)
				else:
					tdatewd = s_w.index(date)
			elif year_not_in:
				dat2 = re.split('/', date)
				if len(dat2) is 1:
					tdate = date
				else:
					month = dat2[0]
					tdate = dat2[1]
				month_not_in = 0

		if year_not_in:
			year = cur_yr
			if month < cur_mon:
				year += 1

		if month_not_in:
			month = cur_mon
			if tdate < cur_dat:
				month += 1
				if month > 12:
					year += 1
					month -= 12

		if weekday_in:
			d = tdatewd
			if tdatewd < cur_day:
				d = str(int(d) - cur_day + 7)
		else:
			d = str(year)+"-"+str(month)+"-"+tdate
	else:
		d = ""

	# at makes dueTime, default is 6
	if ' at ' in spl:
		t = spl[spl.index(' at ')+1]
		t_s = re.split(' ',t)
		if len(t_s)>1:
			if 'pm' in t_s:
				t_s.remove('pm')
				colon = re.split(':',t_s[0])
				n_t = int(colon[0])+12
				try:
					t = str(n_t)+":"+colon[1]
				except:
					t = str(n_t)+":00"
		if ":" not in t:
			t = t + ":00"
		if d == "":
			d = str(0)
	else:
		t = ""

	# in makes location
	if ' in ' in spl:
		p = spl[spl.index(' in ')+1]
	else:
		p = ""

	# \@ makes list
	if ' @' in spl:
		l = spl[spl.index(' @')+1]
	else:
		l = ""

	# \# makes tag
	if ' \u0023' in spl:
		ta = spl[spl.index(' \u0023')+1]
	else:
		ta = ""

	#if on webpage, automatically add webpage to url
	try:
		currentTabUrl = str(subprocess.check_output(['osascript','browser.scpt']))[2:-3]
		url = "url:"+currentTabUrl
		if currentTabUrl == "You need a supported browser as your frontmost app":
			url = ""
	except:
		pass

	# priority
	if '***' in pre_dat:
		pr = 3
	elif '**' in pre_dat:
		pr = 2
	elif '*' in pre_dat:
		pr = 1
	else:
		pr = 0
	pr = str(pr)

	baseurl = "twodo://x-callback-url/add?task=" +e+ "&forlist=" +l+ "&locations=" +p+ "&due=" +d+ "&dueTime=" +t+"&tags=" +ta+"&action="+url+"&priority="+pr

	result = {"items": [
	    {
	        "title": "task",
	        "subtitle": "Create new task with given data",
	        "arg": baseurl,
			"icon": {
				"path":"icons/Normal.png"
			}
	    },
	    {
	        "title": "project",
	        "subtitle": "Create new project with given data",
	        "arg": baseurl + "&type=1",
			"icon": {
				"path":"icons/Project.png"
			}
	    },
	    {
	        "title": "checklist",
	        "subtitle": "Create new checklist with given data",
	        "arg": baseurl + "&type=2",
			"icon": {
				"path":"icons/Checklists.png"
			}
	    }
	]}

	finalResult = json.dumps(result)

	print(finalResult)

addtask(query)
