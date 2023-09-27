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

class WebpageMonitor:
    def __init__(self, url, interval, send_email, send_pass, recv_email, sentence):
        self.url = url
        self.previous_soup = None
        self.interval: int = interval
        self.s_email = send_email
        self.s_pass = send_pass 
        self.r_email = recv_email
        self.sentence = sentence

    def get_page_soup(self):
        try:
            response = requests.get(self.url, timeout=10)
            if 'charset' in response.headers.get('content-type'):
                response.encoding = response.headers.get('content-type').split('charset=')[-1]
            else:
                from chardet import detect
                response.encoding = detect(response.content)['encoding']
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching the webpage: {e}")
            return None

    def highlight_changes(self, curr_soup):
        # title = curr_soup.title.string if curr_soup.title else "No Title"
        # curr_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # email_subject = f"{title} - {curr_time}"
        # self.send_email(email_subject, str(curr_soup), self.r_email) ///debug
        if not self.previous_soup:
            return curr_soup.prettify()
        changed_par = set()
        for prev_elem, curr_elem in zip(self.previous_soup.find_all('tr'), curr_soup.find_all('tr')):
            if prev_elem.text != curr_elem.text:
            # curr_elem['style'] = "background-color: red; font-weight: bold;"
                changed_par.add(str(curr_elem))
        if not changed_par:
            return curr_soup.prettify()
        content = "\n".join(changed_par)
        title = curr_soup.title.string if curr_soup.title else "No Title"
        curr_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        email_subject = f"{title} - {curr_time}"
        self.send_email(email_subject, f'<!DOCTYPE html>\n<html lang="ja">\n<body>\n<table>\n{content}</table>\n\n{self.sentence}\n\n</body></html>', self.r_email)
        with open(f'archive/{title}-{curr_time}.html', 'w', encoding='utf-8') as file:
            file.write(f'<!DOCTYPE html>\n<html lang="ja">\n<body>\n<table>\n{content}\n</table>\n</body>\n</html>')
        # self.local_html_to_image(f'archive/{title}-{curr_time}.html', f'archive/{title}-{curr_time}.png')
        return curr_soup.prettify()

    def run(self):
        while True:
            try:
                print("Do it")
                curr_soup = self.get_page_soup()
                self.highlight_changes(curr_soup)
                self.previous_soup = curr_soup
                time.sleep(self.interval)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                print(traceback.format_exc()) 
                time.sleep(20) 

    def local_html_to_image(self, output_filename, output_image_path):  
        try:
            html_url = 'file://' + os.path.abspath(output_filename)
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            browser = webdriver.Chrome(service=Service('./bin/chromedriver.exe'), options=options)
            browser.get(html_url)
            browser.save_screenshot(output_image_path)
            browser.quit()
        except Exception as e:
            print(f"Error converting HTML to image: {e}")

    def send_email(self, subject, content, recipient_email):
        try:
            smtp_server = 'smtp.mail.yahoo.co.jp'
            smtp_port = 465
            smtp_user = self.s_email
            smtp_pass = self.s_pass

            msg = EmailMessage()
            msg.set_content(content, subtype='html')
            msg['Subject'] = subject
            msg['From'] = smtp_user
            msg['To'] = recipient_email

            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
        except smtplib.SMTPException as e:
            print(f"Error sending email: {e}")

load_dotenv("./settings.env")
# print(os.environ)
url = os.getenv("URL")
send_email = os.getenv("SEND_EMAIL")
send_pass = os.getenv("SEND_PASS")
recv_email = os.getenv("RECIEVE_EMAIL")
interval = int(os.getenv("INTERVAL"))
url = os.getenv("URL")
sentence = os.getenv("SENTENCE").replace("\\n", "\n")
monitor = WebpageMonitor(url, interval, send_email, send_pass, recv_email, sentence)
monitor.run()