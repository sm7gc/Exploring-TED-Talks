#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 10:28:01 2019

@author: sanjanamendu
"""

import re
import time
import json
import pandas as pd
from tqdm import tqdm
from urllib.error import HTTPError
from urllib import request
from bs4 import BeautifulSoup
from langdetect import detect

def url_request(url):
    try:
        req = request.Request(url)
        req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)')
        resp = request.urlopen(req)
        return resp.read().decode("utf-8")
    except HTTPError as e:
        if e.code == 429:
            print(e)
        return
    
def val_check(current, col):
    val = ""
    try:
        if col == "id":
            val = int(current["current_talk"])
        elif col == "comments":
            val = current['comments']['count']
        elif col == "title": 
            val = current['name']
        elif col == "headline": 
            val = current['talks'][0]['player_talks'][0]["title"]
        elif col == "duration": 
            val = int(current['talks'][0]['player_talks'][0]["duration"])
        elif col == "event":
            val = current['event']
        elif col == "languages": 
            val = len(current['talks'][0]['player_talks'][0]['languages'])
        elif col == "main_speaker": 
            val = current['talks'][0]['player_talks'][0]['speaker']
        elif col == "num_speaker": 
            val = len(current['speakers'])
        elif col == "year_filmed": 
            val = int(current['talks'][0]['player_talks'][0]['targeting']['year'])
        elif col == "published_date": 
            val = current['talks'][0]['player_talks'][0]['published']
        elif col == "ratings": 
            val = current['talks'][0]['ratings']
        elif col == "related_talks": 
            val = current['talks'][0]['related_talks']
        elif col == "speaker_occupation": 
            val = current['talks'][0]['speakers'][0]['description']
        elif col == "tags": 
            val = ",".join(current['talks'][0]['tags'])
        elif col == "description": 
            val = current['description']
        elif col == "url": 
            val = current['url']
        elif col == "views": 
            val = current['viewed_count']
    except IndexError:
        val = None
    except TypeError:
        val = None
    return val

def gather_metadata(item):
    
    href = item.find('h4',{'class':'h9 m5'}).find('a')['href']
    resp_str = url_request('http://www.ted.com' + href)
    if resp_str == None: return
    soup = BeautifulSoup(resp_str,"html.parser")
    
    json_text = soup.find('div',{'class':'main talks-main'}) \
        .find('div',{'itemtype':'http://schema.org/VideoObject'}) \
        .findNext('script').contents[0]
        
    current = json.loads(json_text.split('"__INITIAL_DATA__":')[1].split("})")[0])
    
    if detect(current['talks'][0]['player_talks'][0]["title"]) != 'en': return

    transcript_url = 'http://www.ted.com' + href + '/transcript?language=en#'
    resp_str = url_request(transcript_url)
    if resp_str == None: return
    transcript_soup = BeautifulSoup(resp_str,"html.parser")
    transcript_elem = transcript_soup.findAll('div', {'class':'Grid__cell flx-s:1 p-r:4'})
    transcript = " ".join([re.compile(r'[\n\r\t]').sub("",t.find('p').contents[0]) for t in transcript_elem])
            
    return {
            "id": val_check(current,"id"),
            "comments": val_check(current,"comments"),
            "title": val_check(current,"title"),
            "headline": val_check(current,"headline"),
            "duration": val_check(current,"id"),
            "event": val_check(current,"event"),
            "languages": val_check(current,"id"),
            "main_speaker": val_check(current,"main_speaker"),
            "num_speaker": val_check(current,"num_speaker"),
            "year_filmed": val_check(current,"year_filmed"),
            "published_date": val_check(current,"published_date"),
            "ratings": val_check(current,"ratings"),
            "related_talks": val_check(current,"related_talks"),
            "speaker_occupation": val_check(current,"speaker_occupation"),
            "tags": val_check(current,"tags"),
            "description": val_check(current,"description"),
            "url": val_check(current,"url"),
            "views": val_check(current,"views"),
            "transcript": transcript,
            "transcript_url": transcript_url
     }


npages = 101
data = []

for page_num in range(1, npages+1):
    print("Page %s" % page_num)
    time.sleep(10)
    resp_str = url_request('http://www.ted.com/talks?page=%s' % page_num)
    if resp_str == None: continue
    root = BeautifulSoup(resp_str,features="lxml")
    items = root.body.find('div', attrs={'id': 'browse-results'}).findAll('div', {'class' : 'col'})
    for item in tqdm(items):
        d = gather_metadata(item)
        if d != None: data.append(d)

df = pd.DataFrame(data)
df.to_csv("final_project/ted-talks/ted-talks-scraped.csv")
