from multiprocessing import context
import smtplib
import ssl
from email.message import EmailMessage
from urllib import request
import requests
from bs4 import BeautifulSoup
from decouple import config

res = requests.get('https://news.ycombinator.com/')

soup = BeautifulSoup(res.text, 'html.parser')

links = soup.select('.titlelink')

email_password = config('email_password')


def send_email(subject, body):
    email_sender = config('email_sender')
    email_receiver = config('email_receiver')
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)


    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
    

def custom_link(links):
    cl = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None)
        try:
            page_request = requests.get(href)
            page_data = BeautifulSoup(page_request.text, 'html.parser')
            list_of_paragraph = page_data.find_all('p')
            New_links = ''
            #print(list_of_paragraph)
            for i, item in enumerate(list_of_paragraph):
                New_links = New_links + list_of_paragraph[i].getText()
                #print(New_links)
            cl.append({'title': title, 'paragraph': New_links})
        except:
            pass
    for data in cl:
        send_email(data['title'], data['paragraph'])
custom_link(links)




