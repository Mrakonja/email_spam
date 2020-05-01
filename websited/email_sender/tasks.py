from __future__ import absolute_import, unicode_literals
from celery import shared_task
import imaplib
import email as e_mail
from .models import SendingDomains, SpamDomains
import os
import selenium
from selenium import webdriver

cwdir = os.path.dirname(os.path.abspath(__file__))
webdriver_location = os.path.join(cwdir, r'geckodriver\geckodriver')

from __future__ import absolute_import, unicode_literals
from celery import shared_task
import imaplib
import email as e_mail
from .models import SendingDomains, SpamDomains
import os
import selenium
from selenium import webdriver

cwdir = os.path.dirname(os.path.abspath(__file__))
webdriver_location = os.path.join(cwdir, r'geckodriver\geckodriver')


def scan(i): #done
    email = i.Email
    password = i.Password
    print('maulchecker started')
    email_type = email.split('@')[-1]

    if email_type == 'gmail.com':
        imapa = 'imap.gmail.com'
        spam = '[Gmail]/Spam'
        inbox = 'INBOX'
    else:
        imapa = 'imap.yahoo.com'
        spam = 'Spam'

    comn = imaplib.IMAP4_SSL(imapa, 993)
    comn.login(email, password)
    comn.select(spam)

    typ, data = comn.search(None, 'ALL')
    all_data = data[0].split()
    sending_list = SendingDomains.objects.all()
    spam_list = SpamDomains.objects.all()
    for data in all_data:
        t, em = comn.fetch(data, '(RFC822)')
        raw = e_mail.message_from_bytes(em[0][1])
        for i in sending_list:
            if i.Domain in raw['From']:
                print('true')
        spamm_count = 0
        for i in spam_list:
            if i.Domain in raw['From']:
                spamm_count += 1

    comn.select(inbox)
    typ, data = comn.search(None, 'ALL')
    all_data = data[0].split()
    for data in all_data:
        t, em = comn.fetch(data, '(RFC822)')
        raw = e_mail.message_from_bytes(em[0][1])
        inbox_count = 0
        for i in sending_list:
            if i.Domain in raw['From']:
                inbox_count += 1
        for i in spam_list:
            if i.Domain in raw['From']:
                index_count += 1 #done


def login_gmail(i):
    driver.get('http://www.gmail.com')
    mail_url = 'https://mail.google.com/mail/u/0/#inbox'
    mail = i.Email
    password = i.Password
    sec_aw = i.Secret
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

    time.sleep(10)
    driver.get(mail_url)
    time.sleep(5)


def remove_security(i):
    securituy_link = 'https://myaccount.google.com/security'
    driver.get(securituy_link)
    less_secure = driver.find_element_by_xpath("//a[@href='lesssecureapps']")
    less_secure.click()
    time.sleep(5)
    checkbox = driver.find_element_by_xpath("//div[@role='checkbox']")
    checkbox.click()
    time.sleep(2)

def get_mailboxes():
    more = driver.find_element(By.TAG_NAME, 'div')
    more.find_element(By.CLASS_NAME, 'n6')
    time.sleep(5)
    mb_arr = []
    for i in driver.find_elements_by_class_name('aim'):
        mb_arr.append(i.find_element_by_tag_name('a').get_attribute('href'))
    return mb_arr


def get_senders():
    senderz = []
    for i in driver.find_elements(By.CLASS_NAME, 'bA4'):
        senderz.append(i.find_element(By.TAG_NAME, 'span').get_attribute('email'))
    return senderz



####### >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Tasks <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ########

@shared_task
def mail_cheker(array):
    if len(array):
        for i in array:
            scan(i)


@shared_task
def mail_cheker_selenium(array):
    if len(array):
        for i in array:
            with  webdriver.Firefox(executable_path=webdriver_location) as driver:
                login_gmail(i, driver)
                get_mailboxes()
                get_senders()

@shared_task
def single_security(i):
    with  webdriver.Firefox(executable_path=webdriver_location) as driver:
        login_gmail(i, driver)
        remove_securitu(i)











