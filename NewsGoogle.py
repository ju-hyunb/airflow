import os
import sys
import time
import pandas as pd
import re
import datetime
import hashlib
import pickle
import shutil
import pytz

from Driver import *




def converttimezone(times):

    utc_time = datetime.datetime.strptime(times, '%Y-%m-%dT%H:%M:%SZ')
    korea_timezone = pytz.timezone('Asia/Seoul')
    korea_time = utc_time.astimezone(korea_timezone)

    formatted_time = korea_time.strftime('%Y-%m-%d %H:%M:%S')

    return formatted_time



def Crawling(driver, section):

    newslist = Findelementsbyxpath(driver, "//article")
    
    results=[]
    for idx, news in enumerate(newslist):
        res = {}

        writer = Findelementsbyxpath(driver, "//div[@class='vr1PYe']")[idx].text
        title = Findelementsbyxpath(driver, "//h4")[idx].text
        writedatetime = Findelementsbyxpath(driver, "//time")[idx].get_attribute('datetime')
        writedatetime = converttimezone(writedatetime)
        url = Findelementsbyxpath(driver, '//a[@class="WwrzSb"]')[idx].get_attribute('href')

        res['sitename'] = '구글뉴스'
        res['url'] = url
        res['title'] = title
        res['writer'] = writer
        res['writedate'] = writedatetime
        res['writedatetime'] = writedatetime
        if '[단독]' in title:
            res['press_pick'] = 1
        else:
            res['press_pick'] = 0
        res['section'] = section
        res['crawled_ts'] = datetime.datetime.now()

        results.append(pd.DataFrame(res, index=[0]))



    return results
        



DF = pd.DataFrame() 

sections = ['대한민국']
baseurl = 'https://news.google.com/home?hl=ko&gl=KR&ceid=KR:ko'


driver = StartDriver(baseurl)
RESULT = []
for section in sections:
    res = Findelementbyxpath(driver, f'//*[@aria-label="{section}"]')
    
    if res is not None:
        section_url = Getattribute(res, 'href')

        if section_url is not None:
            driver_ = StartDriver(section_url)
            Pagescrolldown(driver_)
            results = Crawling(driver_, section)
            RESULT.append(pd.concat(results))


    driver_.close()
driver.quit()




df=pd.concat(RESULT).reset_index(drop=True)
result_df = df[['sitename', 'url', 'title', 'writer', 'writedate', 'writedatetime', 'press_pick', 'crawled_ts', 'section']]
