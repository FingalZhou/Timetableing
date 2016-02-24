## this program is used to extract the Individual timetable
## from the UNNC website.

## date = tables[5].find_all('b')[1].contents[0]
## course = trs[3].find_all('font')[0].contents[0]
## time = trs[0].find_all('font')[0].contents[0]
## code = trs[2].find_all('font')[0].contents[0]
## wday = trs[1].find_all('font')[0].contents[0]
## room = trs[4].find_all('font')[0].contents[0]

import time
import datetime
import urllib
from bs4 import *
import re

# each part of the whole url
urlp1 = 'http://timetablingunnc.nottingham.ac.uk:8005/reporting/Individual;student;id;'
urlp2 = '?days='
urlp3 = '&weeks='
urlp4 = '&periods='
urlp5 = '&template=SWSCUST+student+Individual&height=100&week=100'

# ask for the student ID
s_id = raw_input('Enter your student ID number: ')
try:
    if int(s_id) > 6530000 or int(s_id) < 6500000:
        print "The student id is invalid, please check again."
        exit()
except:
    print "The student id is invalid, please check again."
    exit()

for week in range(36):
    print "Week", week+1

    for day in range(5):
        # initial the variable
        course = None
        ccode = None
        stime = None
        etime = None
        wday = None
        room = None

        for period in range(20):
            # open the url and parse to extract timetable
            content = urllib.urlopen(urlp1+s_id+urlp2+str(day+3)+urlp3+str(week+1)+urlp4+str(period+1)+urlp5).read()
            soup = BeautifulSoup(content, 'html.parser')
            tables = soup.find_all('table')
            trs = tables[6].find_all('tr')

            # combine the same lecture into one
            try:
                # if the first class today
                if ccode == None:
                    wday = trs[1].find_all('font')[0].contents[0]
                    ccode = trs[2].find_all('font')[0].contents[0]
                    course = trs[3].find_all('font')[0].contents[0]
                    stime = trs[0].find_all('font')[0].contents[0]
                    try:
                        # in case thers's no room
                        room = trs[4].find_all('font')[0].contents[0]
                    except:
                        room = None
                # if the lecture code is same, combine into one line
                elif ccode == trs[2].find_all('font')[0].contents[0]:
                    etime = trs[0].find_all('font')[0].contents[0]
                # if different lecture code, print the old one and set new variable
                else:
                    print wday, course, stime, etime, room
                    etime = None
                    wday = trs[1].find_all('font')[0].contents[0]
                    ccode = trs[2].find_all('font')[0].contents[0]
                    course = trs[3].find_all('font')[0].contents[0]
                    stime = trs[0].find_all('font')[0].contents[0]
                    room = trs[4].find_all('font')[0].contents[0]
            except:
                continue

        # print the lec info if it's the last lecture today
        print wday, course, stime, etime, room
