#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
from bs4 import BeautifulSoup
import time
import datetime
import smtplib
import difflib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import cgi

def colorcode(text, n_text):
    seqm = difflib.SequenceMatcher(None, text, n_text)
    output= []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            pass
        elif opcode == 'insert':
            output.append('<span style="color:#FF0000">' + cgi.escape(seqm.b[b0:b1]) + "</span>")
        elif opcode == 'delete':
            output.append('<span style="color:#0000CD">' + cgi.escape(seqm.a[a0:a1]) + "</span>")
        elif opcode == 'replace':
            output.append('<span style="color:#00FF00">' + cgi.escape(seqm.b[b0:b1]) + "</span>")
        else:
            raise RuntimeError, "unexpected opcode"
    return ''.join(output)

url = "https://www.google.com" #replace with the site you want to monitor
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
print("started monitoring at "+datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
sys.stdout.flush()
olddate = datetime.datetime.now().strftime("%B %D, %Y")
response = requests.get(url, headers=headers, verify=False)
lastsoup = BeautifulSoup(response.text, "lxml")

while True:
    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, "lxml")
    
    if soup == lastsoup:
        time.sleep(20)
	date = datetime.datetime.now().strftime("%B %D, %Y")
	if date != olddate:
		print("No change as of "+date)
		sys.stdout.flush()
		olddate = date
        continue 
        
    else:
	print('the site was updated at '+datetime.datetime.now().strftime("%I:%M%p on %b %d, %Y"))
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'the site was updated'
        msg['From'] = 'your e-mail'
        msg['To']  = 'receiver e-mail'
        text = 'Please check: your site\n\n'
        html = """\
        <html>
            <head></head>
            <body>Please check <a href="""+url+""">"""+url+"""</a>.
	    <br><br>Here is an attempt at showing what changed:<br>
            """+colorcode(str(lastsoup), str(soup))+"""\
            </body>
        </html>
        """
        msg.attach(MIMEText(html, 'html'))
        server = smtplib.SMTP('your smtp server', port)#input your info here
        server.starttls()
        server.login("your email", "your password")#input your info here

        server.sendmail("from-address", ['to-address 1', 'to-address 2'], msg.as_string())#input your info here
        server.quit()
        lastsoup = soup 
        continue
