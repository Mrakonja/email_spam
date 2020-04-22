I would like to develop a program in Ubot Studio (so the source code can later be updated) that does the following:
- imports a list of proxy IPs to connect [✔]
- import a list of browsers/machines [✔]
- imports a list of email addresses and passwords (GMail, Yahoo!) [✔]
- imports a list of sending domains [✔]
- imports a list of spam domains [✔]
- imports a list of responses [✔]
- selects an IP address from the pool [✔]
- selects a browser/machine randomly from the list [✔]
- logs into the email account (via the proxy using the browser/machine profile) [✔]
- scans the spam folder for a sending domain(s) - if found, mark message(s) as "Not Spam" [✔]
- next scan the inbox for the sending domain(s) - if found, open the message and wait for 5-15 seconds, click on a random link 20-50% of the time, reply to the message with a random reply 40-75% of the time [✔]
- next scan the inbox for the spam domain(s) - if found, open the message and click "Mark as Spam" [✔]
- close browser [✔]
- write the results to a MySql Database (IP, email, messages opened, clicked, moved, marked as spam, etc.) [✔]

The bot should be multi-threaded (user selects number of threads to run) and should run on a scheduler.