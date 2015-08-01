# -*- coding: iso-8859-1 -*-

import smtplib

# For guessing MIME type
import mimetypes

# Import the email modules we'll need
import email
import email.mime.application
import email.mime.multipart
import email.mime.text

from passwords import GMAIL_PASSWORD, GMAIL_ADRESS
from helpFunc import listToCommaSeperatedString

def sendEmail(fileName, toAddrs):

    msg = email.mime.multipart.MIMEMultipart()

    msg['Subject'] = 'Parkeringstillstånd'
    msg['From'] = GMAIL_ADRESS
    msg['To'] = listToCommaSeperatedString(toAddrs)

    # The main body is just another attachment
    body = email.mime.text.MIMEText('Här kommer dina parkeringstillstånd!')
    msg.attach(body)

    # PDF attachment
    fp=open(fileName,'rb')
    att = email.mime.application.MIMEApplication(fp.read(),_subtype="pdf")
    fp.close()
    att.add_header('Content-Disposition','attachment',filename=fileName)
    msg.attach(att)

    # Credentials (if needed)
    username = GMAIL_ADRESS


    # send via Gmail server
    # NOTE: my ISP, Centurylink, seems to be automatically rewriting
    # port 25 packets to be port 587 and it is trashing port 587 packets.
    # So, I use the default port 25, but I authenticate.
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login(username,GMAIL_PASSWORD)
    print(msg['To'])
    s.sendmail(msg['From'], toAddrs, msg.as_string())
    s.quit()