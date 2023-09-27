import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv
import traceback

recv_email = os.getenv("RECIEVE_EMAIL")

smtp_server = 'smtp.mail.yahoo.co.jp'
smtp_port = 465
smtp_user = os.getenv("SEND_EMAIL")
smtp_pass = os.getenv("SEND_PASS")

msg = EmailMessage()
msg.set_content("テストメール", subtype='html')
msg['Subject'] = "テストメール"
msg['From'] = smtp_user
msg['To'] = os.getenv("RECIEVE_EMAIL")

with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
    server.login(smtp_user, smtp_pass)
    server.send_message(msg)