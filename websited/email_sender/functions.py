#!/usr/bin/env python

"""functions.py: functions for getting results out of yelp"""
"""last commit: 08012019 02:08 am"""

import datetime
import json
import csv
import requests
from django.db import connection
from threading import Thread
from yelpscraper.models import Search, Result, ApiData, Status
import logging
# from requests_html import HTMLSession
import time
import re
import configparser
import random

logger = logging.getLogger(__name__)


def convert_field(field):
   try:
      return field.replace('"', '')
   except:
      return ''


def getSheetData(fields):
   try:
      name = functions.convert_field(fields[0])
   except:
      name = ''
   
   try:
      yurl = functions.convert_field(fields[2])
   except:
      yurl = ''
   
   try:
      address = functions.convert_field(fields[4]),
   except:
      address = ''
   
   try:
      surl = functions.convert_field(fields[3])
   except:
      surl = ''
   
   try:
      city = functions.convert_field(fields[5])
   except:
      city = ''
   
   try:
      state = functions.convert_field(fields[6])
   except:
      state = ''
   try:
      phone = "+1" + functions.convert_field(
         fields[2].replace('(', "").replace(')', "").replace(' ', "").replace('-', '').replace('"', ''))
   except:
      phone = ''
   
   return {'name': name,
           'yurl': name,
           'address': address,
           'surl': surl,
           'city': city,
           'state': state,
           'phone': phone,
           }


def start_new_thread(function):
   def decorator(*args, **kwargs):
      t = Thread(target=function, args=args, kwargs=kwargs)
      t.daemon = True
      t.start()
   
   return decorator


@start_new_thread
def scrape2(term, location):
   import django
   django.setup()
   
   status = Status.objects.get(pk=1)
   status.yelp_scraper = True
   status.url_scraper = False
   status.email_scraper = False
   status.save()
   now = datetime.datetime.now()
   
   def cat(cats):
      catz = ''
      for item in cats:
         catz = catz + '|' + item['title']
      return catz
   
   def dateGen(now):
      return str(now.year) + str(now.day) + str(now.month) + '_' + str(now.hour) + str(now.minute)
   
   def uidGen(now):
      return str(now.hour) + str(now.minute) + str(now.second) + str(now.year) + str(now.day) + str(now.month)  # #str()
   
   config = configparser.ConfigParser()
   config.read('./yelpscraper/config.ini')
   
   MY_API_KEY = config['yelp']['api_key']
   offsets = [x for x in range(0, 1000, 50)]
   headers = {'Authorization': 'Bearer %s' % MY_API_KEY}
   
   uid = uidGen(now)
   searchDB = Search(term=term, location=location, date=now, uid=uid, )
   searchDB.save()
   for x in offsets:
      url = 'https://api.yelp.com/v3/businesses/search'
      params = {'term': term, 'location': location, 'offset': x}
      
      with open('log.txt', 'a') as f:
         f.write('url ' + str(x) + '\n')
      
      req = requests.get(url, headers=headers, params=params)
      
      parsed = json.loads(req.text)
      
      with open('log.txt', 'a') as f:
         f.write('started \n')
      try:
         for item in parsed['businesses']:
            hurl = 'www.' + ''.join(item['name'].split()) + '.com'
            hurl = hurl.replace('-', '').replace('&', 'and').replace("'", '').lower()
            req2 = requests.get('https://api.yelp.com/v3/businesses/' + item['id'], headers=headers, params=params)
            parsed2 = json.loads(req2.text)
            yelp_url = item['url'].split('?')
            
            if (Result.objects.filter(yurl=yelp_url[0]).count() != 0) or (
               Result.objects.filter(phone=item['phone']).count() != 0):
               pass
            else:
               resultDB = Result(
                  uid=uid,
                  name=item['name'],
                  yurl=yelp_url[0],
                  review_count=item['review_count'],
                  address=item["location"]["address1"],
                  city=item['location']['city'],
                  state=item['location']['state'],
                  categories=cat(item['categories']),
                  phone=item['phone'],
                  surl=hurl,
                  rating=item['rating'],
                  is_claimed=str(parsed2['is_claimed']),
                  term=term
               )
               try:
                  resultDB.save()
               except:
                  pass
      except:
         pass
   
   status = Status.objects.get(pk=1)
   status.yelp_scraper = False
   status.url_scraper = False
   status.email_scraper = False
   status.save()


@start_new_thread
def mailscrape(uid):
   import django
   django.setup()
   
   def get_mail(result):
      mails = []
      
      # with HTMLSession() as session:
      #   response = session.get('https://duckduckgo.com/html?q={}%20contact%20@'.format(result.surl))
      #   divs = response.html.find('.result__snippet')
      #   for div in divs:
      #     mo = re.search('(\w+[.|\w])*@(\w+[.])*\w+', div.text)
      #     if mo:
      #       print('trying')
      #       if '.com' or '.net' in mo.group() and mo.group() not in mails:
      #         print('succesful')
      #         mails.append(str(mo.group()))
      
      mail = ' ; '.join(mails)
      
      return mail
   
   status = Status.objects.get(pk=1)
   status.yelp_scraper = False
   status.url_scraper = False
   status.email_scraper = True
   status.save()
   
   results = Result.objects.filter(uid=uid)
   for result in results:
      try:
         result.mail = get_mail(result)
         result.save()
         time.sleep(1)
      except Exception as e:
         pass
   
   status = Status.objects.get(pk=1)
   status.email_scraper = False
   status.save()


@start_new_thread
def urlscrape(uid):
   import django
   django.setup()
   status = Status.objects.get(pk=1)
   status.yelp_scraper = False
   status.url_scraper = True
   status.email_scraper = False
   status.save()
   user_agent_list = [
      # Chrome
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
      'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
      # Firefox
      'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
      'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
      'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
      'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
      'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
      'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
      'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
      'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
   ]
   
   with HTMLSession() as session:
      results = Result.objects.filter(uid=uid)
      for result in results:
         try:
            user_agent = random.choice(user_agent_list)
            headers = {'User-Agent': user_agent}
            r = session.get(result.yurl, headers=headers)
            time.sleep(20)
            url = r.html.find('.biz-website.js-biz-website.js-add-url-tagging a', first=True)
            result.surl = url.text
            result.save()
         except Exception as e:
            print(e)
   
   status = Status.objects.get(pk=1)
   status.url_scraper = False
   status.save()

# todo: Master DB for uploading to the sheets
# todo: DB for storing last item uploaded to the shets.

# https://www.yelp.com/biz/boutique-bites-chicago?adjust_creative=K9jLxBTH0ipsFvWsdAEA3g&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=K9jLxBTH0ipsFvWsdAEA3g








