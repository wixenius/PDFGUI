# -*- coding: iso-8859-1 -*-

import smtplib

# For guessing MIME type
import mimetypes

# Import the email modules we'll need
import email
import email.mime.application
import email.mime.multipart
import email.mime.text

from passwords import GMAIL
from helpFunc import listToCommaSeperatedString

def sendEmail(fileName, toAddrs, subject, body):

    msg = email.mime.multipart.MIMEMultipart()

    msg['Subject'] = subject
    msg['From'] = GMAIL['ADRESS']
    if isinstance(toAddrs, list):
        msg['To'] = listToCommaSeperatedString(toAddrs)
    else:
        msg['To'] = toAddrs

    # The main body is just another attachment
    body = email.mime.text.MIMEText(body)
    msg.attach(body)

    # PDF attachment
    fp=open(fileName,'rb')
    att = email.mime.application.MIMEApplication(fp.read(),_subtype="pdf")
    fp.close()
    att.add_header('Content-Disposition','attachment',filename=fileName)
    msg.attach(att)

    # Credentials (if needed)
    username = GMAIL['ADRESS']


    # send via Gmail server
    # NOTE: my ISP, Centurylink, seems to be automatically rewriting
    # port 25 packets to be port 587 and it is trashing port 587 packets.
    # So, I use the default port 25, but I authenticate.
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login(username,GMAIL['PASSWORD'])
    s.sendmail(msg['From'], toAddrs, msg.as_string())
    s.quit()