from __future__ import absolute_import, unicode_literals
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from celery import shared_task
import imaplib
import email as e_mail
import os
from .models import SendingDomains, SpamDomains

@shared_task
def mail_cheker(email, password):
    print('maulchecker started')
    email_type = email.split('@')[-1]

    if email_type == 'gmail.com':
             imapa = 'imap.gmail.com'
             spam  = '[Gmail]/Spam'
             inbox = 'INBOX'
    else:
            imapa = 'imap.yahoo.com'
            spam = 'Spam'

    comn = imaplib.IMAP4_SSL(imapa, 993)
    comn.login(email, password)
    print(comn.list())
    comn.select(spam)

    typ, data = comn.search(None, 'ALL')
    all_data = data[0].split()
    sending_list = SendingDomains.objects.all()
    spam_list = SpamDomains.objects.all()
    for data in all_data:
        t, em = comn.fetch(data, '(RFC822)')
        raw = e_mail.message_from_bytes(em[0][1])
        print(raw['from'])
        for i in sending_list:
            if i.Domain in  raw['From']:
                print('true')

        for i in  spam_list:
            if i.Domain in  raw['From']:
                print('true')

    comn.select(inbox)
    typ, data = comn.search(None, 'ALL')
    all_data = data[0].split()
    for data in all_data:
        t, em = comn.fetch(data, '(RFC822)')
        raw = e_mail.message_from_bytes(em[0][1])
        print(raw['from'])
        for i in sending_list:
            if i.Domain in  raw['From']:
                print('true')

        for i in  spam_list:
            if i.Domain in  raw['From']:
                print('true')


#Selenium

webdriver_location = r'geckodriver-v0.26.0-win64\geckodriver'

@shared_task
def sec_remove(m, p, sk):
    cwdir = os.path.dirname(os.path.abspath(__file__))
    webdriver_location = os.path.join(cwdir, r'geckodriver\geckodriver' )
    with  webdriver.Firefox(executable_path=webdriver_location) as driver:
        driver.get('http://www.gmail.com')
        mail = m
        password = p
        sec_aw = sk
        securituy_link = 'https://myaccount.google.com/security'
        mail_url = 'https://mail.google.com/mail/u/0/#inbox'

        mail_input = driver.find_element_by_xpath("//input[@type='email']")
        mail_input.send_keys(mail)
        button = driver.find_element_by_xpath('//div[@role="button"]')
        button.click()
        time.sleep(10)
        mail_input = driver.find_element_by_xpath("//input[@type='password']")
        mail_input.send_keys(password)
        time.sleep(10)
        button = driver.find_element_by_xpath('//div[@id="passwordNext"]')
        button.click()
        if driver.current_url != mail_url:
            time.sleep(10)
            security_button = driver.find_element_by_xpath('//li[@class="JDAKTe cd29Sd zpCp3 SmR8"]')
            security_button.click()
            time.sleep(10)
            sec_answer_input = driver.find_element_by_xpath("//input[@id='secret-question-response']")
            sec_answer_input.send_keys(sec_aw)

            button = driver.find_element_by_xpath("//div[@role='button']")
            button.click()
            time.sleep(10)
            button2 = driver.find_element_by_xpath("//div[@role='button']")
            button2.click()

        driver.get(mail_url)
        time.sleep(5)
        driver.get(securituy_link)
        less_secure = driver.find_element_by_xpath("//a[@href='lesssecureapps']")
        less_secure.click()
        time.sleep(5)
        checkbox = driver.find_element_by_xpath("//div[@role='checkbox']")
        checkbox.click()
        time.sleep(2)