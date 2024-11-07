import smtplib
import os
from email.mime.text import MIMEText
from email.header import Header


def send_ya_mail(*msg_text: str):
    login = 'texipoverka@yandex.ru'
    password = 'ihvcnydoaqxcsetu'

    msg = MIMEText(str(msg_text), 'plain', 'utf-8')
    msg['Subject'] = Header('Заявка', 'utf-8')
    msg['From'] = login
    msg['To'] = ', '.join('texipoverka@yandex.ru')

    s = smtplib.SMTP('smtp.yandex.ru', 587, timeout=10)

    try:
        s.starttls()
        s.login(login, password)
        s.sendmail(msg['From'], 'texipoverka@yandex.ru', msg.as_string())
    except Exception as ex:
        print(ex)
    finally:
        s.quit()




def main():
    send_ya_mail(recipients_emails=['cruspe23091990@yandex.ru'], msg_text='привет')
