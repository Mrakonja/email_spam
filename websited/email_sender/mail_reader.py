import imaplib
import email as e_mail

def mail_cheker(email, password):
    email_type = email.split('@')[-1]

    if email_type == 'gmail.com':
             imapa = 'imap.gmail.com'
             spam  = '[Gmail]/Spam'
    else:
            imapa = 'imap.yahoo.com'
            spam = 'Spam'

    comn = imaplib.IMAP4_SSL(imapa, 993)
    comn.login(email, password)
    comn.select(spam)

    typ, data = comn.search(None, 'ALL')
    all_data = data[0].split()

    for data in all_data:
        t, em = comn.fetch(data, '(RFC822)')
        raw = e_mail.message_from_bytes(em[0][1])
        print(raw['From'])


mail_cheker('evelyncunni56@gmail.com', 'hkghuugp')
